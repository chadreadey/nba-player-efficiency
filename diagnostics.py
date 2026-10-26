"""Noise ceiling and error breakdown for the next-season PER backtest.

Run after train.py (which writes data/derived/<source>_next_season_predictions.csv):

    .venv/bin/python diagnostics.py --source bbref

Writes aggregate tables only (no player rows) to results/<source>_diagnostics.{md,json}.

Noise model: observed PER = true PER + noise with variance k / MP. For consecutive
seasons, Var(PER_t+1 - PER_t) = Var(true change) + k * (1/MP_t + 1/MP_t+1), so k is
the slope of the year-to-year change variance against harmonic minutes.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from nba_per import data
from nba_per import experiments as ex

ROOT = Path(__file__).resolve().parent
SQRT_2_PI = np.sqrt(2 / np.pi)  # E|X| = sqrt(2/pi) * sd for normal X

MODELS = {
    "marcel": "pred_Marcel-style weighted PER (tuned)",
    "ridge": "pred_ridge (tuned)",
    "hgb": "pred_hist gradient boosting (tuned)",
    "selected": "pred_selected by CV",
}


# ------------------------------------------------------------------ noise model
def season_pairs(source, min_mp):
    df = data.load(source)
    df = df[(df.season >= 1981) & df.per.notna() & (df.mp >= min_mp)]
    nxt = df[["player_key", "season", "per", "mp"]].assign(season=df.season - 1)
    p = df[["player_key", "season", "age", "per", "mp"]].merge(
        nxt, on=["player_key", "season"], suffixes=("", "_next"))
    p["d"] = p.per_next - p.per
    p["d"] -= p.groupby("age").d.transform("mean")  # remove the average aging step
    p["x"] = 1 / p.mp + 1 / p.mp_next
    return p


def fit_noise(pairs, n_bins=20, robust=False):
    """WLS of binned change variance on harmonic minutes. Returns (k, var_true_change, bins)."""
    pairs = pairs.assign(bin=pd.qcut(pairs.x, n_bins, duplicates="drop"))
    if robust:
        var = lambda d: (1.4826 * np.median(np.abs(d - np.median(d)))) ** 2
    else:
        var = lambda d: float(np.var(d, ddof=1))
    b = pairs.groupby("bin", observed=True).agg(x=("x", "mean"), v=("d", var), n=("d", "size"))
    A = np.c_[np.ones(len(b)), b.x]
    w = np.sqrt(b.n.values)
    a, k = np.linalg.lstsq(A * w[:, None], b.v.values * w, rcond=None)[0]
    return float(k), float(a), b


# ------------------------------------------------------------- error breakdown
def groups(p: pd.DataFrame) -> dict[str, pd.Series]:
    traded = p.team.str.fullmatch(r"\dTM|TOT") | p.team_next.str.fullmatch(r"\dTM|TOT")
    ratio = p.mp_next / p.mp
    return {
        "minutes in target season": pd.cut(p.mp_next, [500, 1000, 1500, 2000, 1e9], right=False,
                                           labels=["500-999", "1000-1499", "1500-1999", "2000+"]),
        "age in target season": pd.cut(p.age + 1, [0, 22, 25, 29, 33, 99], right=False,
                                       labels=["<=21", "22-24", "25-28", "29-32", "33+"]),
        "prior NBA seasons": pd.cut(p.exp + 1, [1, 2, 4, 99], right=False,
                                    labels=["1 (second-year player)", "2-3", "4+"]),
        "team change (t to t+1)": pd.Series(
            np.where(traded, "traded mid-season (t or t+1)",
                     np.where(p.team != p.team_next, "changed team in offseason", "same team")),
            index=p.index),
        "minutes change (MP t+1 / MP t)": pd.cut(ratio, [0, 0.67, 1.5, np.inf], right=False,
                                                 labels=["fell (<0.67x)", "stable", "rose (>1.5x)"]),
        "test window": p.window,
    }


def summarize(p, mask, k):
    s = p[mask]
    y, g = s.per_next.values, s.player_key.values
    out = {"n": int(len(s))}
    out["noise_floor_mae"] = round(float(np.mean(SQRT_2_PI * np.sqrt(k / s.mp_next))), 3)
    for m, col in MODELS.items():
        out[f"mae_{m}"] = round(float(np.mean(np.abs(y - s[col]))), 3)
    if len(s) >= 30:
        out["delta_selected_vs_marcel"] = ex.paired_delta_ci(y, s[MODELS["selected"]], s[MODELS["marcel"]], g)
    return out


def main(source):
    # Noise model, with sensitivity to the minutes floor and to outliers.
    fits = []
    for min_mp in (100, 250, 500):
        pairs = season_pairs(source, min_mp)
        for robust in (False, True):
            k, a, _ = fit_noise(pairs, robust=robust)
            fits.append({"min_mp": min_mp, "robust": robust, "pairs": len(pairs),
                         "k": round(k, 1), "var_true_change": round(a, 3),
                         "noise_sd_at_1000mp": round(float(np.sqrt(max(k, 0) / 1000)), 3)})
    main_fit = next(f for f in fits if f["min_mp"] == 250 and not f["robust"])
    k = main_fit["k"]

    p = pd.read_csv(ROOT / "data" / "derived" / f"{source}_next_season_predictions.csv")
    resid = p.per_next - p[MODELS["selected"]]
    noise_var = k / p.mp_next
    overall = summarize(p, pd.Series(True, index=p.index), k)
    headroom = {
        "selected_mse": round(float(np.mean(resid ** 2)), 3),
        "mean_noise_var": round(float(np.mean(noise_var)), 3),
        "noise_share_of_mse": round(float(np.mean(noise_var) / np.mean(resid ** 2)), 3),
        # perfect knowledge of current true talent + average aging, nothing about change
        "static_talent_oracle_mae": round(float(np.mean(
            SQRT_2_PI * np.sqrt(main_fit["var_true_change"] + noise_var))), 3),
    }
    floors = [round(float(np.mean(SQRT_2_PI * np.sqrt(max(f["k"], 0) / p.mp_next))), 3) for f in fits]

    breakdown = {}
    late = p.window == p.window.max()
    for name, grp in groups(p).items():
        rows = []
        for level in grp.dropna().unique().tolist():
            m = grp == level
            r = {"group": str(level), **summarize(p, m, k)}
            if name != "test window":
                for tag, sub in (("earlier", m & ~late), ("latest", m & late)):
                    if sub.sum() >= 30:
                        s = p[sub]
                        r[f"delta_{tag}"] = ex.paired_delta_ci(
                            s.per_next, s[MODELS["selected"]], s[MODELS["marcel"]], s.player_key)[0]
                        r[f"n_{tag}"] = int(sub.sum())
            rows.append(r)
        order = [str(c) for c in grp.cat.categories] if hasattr(grp, "cat") else sorted(r["group"] for r in rows)
        breakdown[name] = sorted(rows, key=lambda r: order.index(r["group"]))

    res = {"source": source, "noise_fits": fits, "main_fit": main_fit,
           "noise_floor_range": [min(floors), max(floors)], "overall": overall,
           "headroom": headroom, "latest_window": str(p.window.max()), "breakdown": breakdown}
    out = ROOT / "results"
    (out / f"{source}_diagnostics.json").write_text(json.dumps(res, indent=2))
    (out / f"{source}_diagnostics.md").write_text(to_markdown(res))
    return res


def to_markdown(res):
    f, o, h = res["main_fit"], res["overall"], res["headroom"]
    L = [f"# Diagnostics: next-season PER backtest ({res['source']})", "",
         "## Noise ceiling", "",
         "Year-to-year PER change variance vs harmonic minutes (age-demeaned, 20 quantile bins, WLS):", "",
         "| min MP per season | robust variance | pairs | k | Var(true change) | noise SD at 1,000 MP |",
         "|---|---|---|---|---|---|"]
    L += [f"| {x['min_mp']} | {'yes' if x['robust'] else 'no'} | {x['pairs']} | {x['k']} | "
          f"{x['var_true_change']} | {x['noise_sd_at_1000mp']} |" for x in res["noise_fits"]]
    L += ["", f"Main fit: min MP 250, plain variance (k = {f['k']}).", "",
          f"- Oracle noise floor (knows true next-season talent exactly): MAE **{o['noise_floor_mae']}** "
          f"(range across fits {res['noise_floor_range'][0]}–{res['noise_floor_range'][1]})",
          f"- Static-talent oracle (knows current true talent + average aging, nothing else): "
          f"MAE {h['static_talent_oracle_mae']}",
          f"- Selected model: MAE **{o['mae_selected']}**; Marcel: {o['mae_marcel']}",
          f"- Measurement noise is {h['noise_share_of_mse']:.0%} of the selected model's MSE "
          f"({h['mean_noise_var']} of {h['selected_mse']})", "",
          "Normal approximation throughout; PER errors are heavier-tailed, so MAE floors are rough.", "",
          "## Error breakdown", "",
          f"Δ = selected-model MAE minus Marcel MAE (negative = better), player-cluster 95% CI. "
          f"'earlier' / 'latest' split Δ into windows before {res['latest_window']} and {res['latest_window']}.",
          "Groups use target-season information (minutes, team), so they diagnose errors; they are "
          "not forecast-time features.", ""]
    for name, rows in res["breakdown"].items():
        L += [f"### {name}", "",
              "| group | n | noise floor | Marcel | ridge | GBM | selected | Δ (95% CI) | Δ earlier | Δ latest |",
              "|---|---|---|---|---|---|---|---|---|---|"]
        for r in rows:
            d = r.get("delta_selected_vs_marcel")
            ds = f"{d[0]:+.3f} ({d[1]:+.3f} to {d[2]:+.3f})" if d else "–"
            de = f"{r['delta_earlier']:+.3f} (n={r['n_earlier']})" if "delta_earlier" in r else "–"
            dl = f"{r['delta_latest']:+.3f} (n={r['n_latest']})" if "delta_latest" in r else "–"
            L.append(f"| {r['group']} | {r['n']} | {r['noise_floor_mae']:.3f} | {r['mae_marcel']:.3f} | "
                     f"{r['mae_ridge']:.3f} | {r['mae_hgb']:.3f} | {r['mae_selected']:.3f} | {ds} | {de} | {dl} |")
        L.append("")
    return "\n".join(L)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", choices=["legacy", "bbref"], default="bbref")
    print(to_markdown(main(ap.parse_args().source)))
