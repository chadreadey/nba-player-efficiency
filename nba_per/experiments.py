"""Experiments. Each returns a list of result rows (dicts) for the report.

1. ``replicate``       - the 2023 notebook's design (random 80/20, same-season features).
2. ``box_score_only``  - same-season PER from per-36 box-score counts alone, season split.
                         If this is near-perfect, same-season "prediction" is formula recovery.
3. ``same_season_oot`` - notebook feature set, de-duplicated, out-of-time season split.
4. ``next_season``     - forecast PER in season t+1 from information available after season t.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from . import data

SEED = 1
MIN_MP = 250  # minutes floor for same-season rows (PER is unstable on tiny samples)
MIN_MP_TARGET = 500  # next-season target must be a season with real minutes


def hgb() -> HistGradientBoostingRegressor:
    return HistGradientBoostingRegressor(
        max_iter=600, learning_rate=0.05, max_leaf_nodes=31,
        l2_regularization=1.0, random_state=SEED,
    )


def cluster_bootstrap_ci(y, pred, groups, n=1000, seed=SEED):
    """95% CI of MAE, resampling players (not rows) because players repeat."""
    rng = np.random.default_rng(seed)
    err = pd.Series(np.abs(np.asarray(y) - np.asarray(pred))).groupby(np.asarray(groups))
    sums, counts = err.sum().values, err.count().values
    idx = rng.integers(0, len(sums), size=(n, len(sums)))
    maes = sums[idx].sum(1) / counts[idx].sum(1)
    return float(np.percentile(maes, 2.5)), float(np.percentile(maes, 97.5))


def paired_delta_ci(y, pred, ref, groups, n=1000, seed=SEED):
    """MAE(pred) - MAE(ref) with a 95% player-cluster bootstrap CI (negative = pred better)."""
    rng = np.random.default_rng(seed)
    y = np.asarray(y)
    d = pd.Series(np.abs(y - np.asarray(pred)) - np.abs(y - np.asarray(ref))).groupby(np.asarray(groups))
    sums, counts = d.sum().values, d.count().values
    idx = rng.integers(0, len(sums), size=(n, len(sums)))
    deltas = sums[idx].sum(1) / counts[idx].sum(1)
    point = sums.sum() / counts.sum()
    return [round(float(point), 4), round(float(np.percentile(deltas, 2.5)), 4),
            round(float(np.percentile(deltas, 97.5)), 4)]


def score(experiment, model, y, pred, n_train, split, groups=None, **extra):
    row = {
        "experiment": experiment, "model": model, "split": split,
        "n_train": int(n_train), "n_test": int(len(y)),
        "mae": round(float(mean_absolute_error(y, pred)), 4),
        "r2": round(float(r2_score(y, pred)), 4),
        "target_sd": round(float(np.std(y)), 3),
    }
    if groups is not None:
        lo, hi = cluster_bootstrap_ci(y, pred, groups)
        row["mae_ci95"] = [round(lo, 4), round(hi, 4)]
    row.update(extra)
    return row


def per36(df: pd.DataFrame) -> pd.DataFrame:
    return df[data.TOTALS].div(df["mp"].replace(0, np.nan), axis=0) * 36


# ---------------------------------------------------------------- 1. replicate
def replicate() -> list[dict]:
    """Notebook cell 12: drop ids, dummies, dropna, drop G/GS/MP, random 80/20."""
    raw = data.load_legacy_raw()
    df = raw.drop(columns=["Year", "Player", "Tm", "blanl", "blank2", "Unnamed: 0"])
    df = pd.get_dummies(df).dropna()
    y, X = df["PER"], df.drop(columns=["PER", "G", "GS", "MP"])
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=SEED)

    kept = raw.loc[df.index]
    split = "random 80/20 (notebook)"
    extra = dict(
        sample=f"{kept.Year.min():.0f}-{kept.Year.max():.0f} after dropna",
        rows_from_traded_player_seasons=int(kept.duplicated(["Player", "Year"], keep=False).sum()),
    )
    return [
        score("replicate", "train mean", y_te, np.full(len(y_te), y_tr.mean()), len(y_tr), split, **extra),
        score("replicate", "hist gradient boosting", y_te, hgb().fit(X_tr, y_tr).predict(X_te),
              len(y_tr), split, **extra),
    ]


# ---------------------------------------------------------- shared helpers
def season_split(df, test_from):
    return df[df.season < test_from], df[df.season >= test_from]


def same_season_frame(source):
    df = data.load(source)
    return df[(df.season >= 1980) & (df.mp >= MIN_MP) & df.per.notna()].copy()


# ------------------------------------------------------- 2. box score only
def box_score_only(source, test_from) -> list[dict]:
    df = same_season_frame(source)
    X = per36(df).assign(season=df.season)
    keep = X.notna().all(axis=1)
    df, X = df[keep], X[keep]
    tr, te = season_split(df, test_from)
    split = f"train <{test_from}, test >={test_from}"
    rows = []
    for name, m in [("linear regression", LinearRegression()), ("hist gradient boosting", hgb())]:
        m.fit(X.loc[tr.index], tr.per)
        rows.append(score("box_score_only", name, te.per, m.predict(X.loc[te.index]), len(tr),
                          split, te.player_key, features="per-36 box-score counts + season"))
    return rows


# ------------------------------------------------- 3. same-season, out of time
def same_season_oot(source, test_from) -> list[dict]:
    df = same_season_frame(source)
    feats = data.RATES + data.COMPOSITES + data.TOTALS + ["age"]
    no_comp = [f for f in feats if f not in data.COMPOSITES]
    tr, te = season_split(df, test_from)
    split = f"train <{test_from}, test >={test_from}"
    rows = [score("same_season_oot", "train mean", te.per, np.full(len(te), tr.per.mean()),
                  len(tr), split, te.player_key)]
    for label, f in [("notebook features", feats), ("without BPM/WS/VORP", no_comp)]:
        pred = hgb().fit(tr[f], tr.per).predict(te[f])
        rows.append(score("same_season_oot", f"hist gradient boosting ({label})", te.per, pred,
                          len(tr), split, te.player_key))
    return rows


# -------------------------------------------------------- 4. next-season PER
def next_season_frame(source):
    df = data.load(source)
    df = df[df.season >= 1978].copy()  # turnovers recorded from 1977-78
    df["exp"] = df.groupby("player_key").cumcount()
    for c, v in per36(df).items():
        df[f"{c}_36"] = v
    base = ["per", "mp", "g", "gs", "bpm", "obpm", "dbpm", "ws_48", "usg_percent", "ts_percent",
            "x3p_ar", "f_tr", "ast_percent", "trb_percent", "stl_percent", "blk_percent",
            "tov_percent"] + [f"{c}_36" for c in data.TOTALS]
    cur = df[["player_key", "player", "season", "age", "exp"] + base]

    def lag(k):
        return cur[["player_key", "season", "per", "mp"]].assign(season=cur.season + k)

    X = cur.merge(lag(1), on=["player_key", "season"], how="left", suffixes=("", "_l1"))
    X = X.merge(lag(2), on=["player_key", "season"], how="left", suffixes=("", "_l2"))

    tgt = df[["player_key", "season", "per", "mp"]].rename(columns={"per": "per_next", "mp": "mp_next"})
    tgt["season"] -= 1  # align season t+1 target with season t features
    out = X.merge(tgt, on=["player_key", "season"], how="inner")
    out["target_season"] = out.season + 1
    out = out[(out.mp_next >= MIN_MP_TARGET) & (out.target_season >= 1981) & out.per_next.notna()]
    feats = [c for c in out.columns
             if c not in ("player_key", "player", "season", "per_next", "mp_next", "target_season")]
    return out.reset_index(drop=True), feats


def marcel(df, league_mean, weights=(5, 4, 3), ballast_mp=1000):
    """Minutes-weighted PER over seasons t, t-1, t-2, regressed toward the league mean."""
    num = np.full(len(df), league_mean * ballast_mp)
    den = np.full(len(df), float(ballast_mp))
    for w, (p, m) in zip(weights, [("per", "mp"), ("per_l1", "mp_l1"), ("per_l2", "mp_l2")]):
        ok = (df[p].notna() & df[m].notna()).values
        num += np.where(ok, w * df[p].fillna(0) * df[m].fillna(0), 0)
        den += np.where(ok, w * df[m].fillna(0), 0)
    return num / den


WINDOW = 5  # target seasons per backtest test window
VAL_FOLDS, VAL_FOLD_LEN = 3, 2  # rolling-origin CV: three 2-season folds just before each test window
SEEDS = (0, 1, 2, 3, 4)  # gradient-boosting refits (feature subsampling makes seeds matter)
TEST_WINDOWS = {"legacy": (2003, 2008, 2013), "bbref": (2007, 2012, 2017, 2022)}
TUNED = ("marcel", "ridge", "hist gradient boosting")

SWEEP = {
    "marcel": [{"ballast_mp": b} for b in (250, 500, 1000, 1500, 2000, 3000, 4000, 6000)],
    "ridge": [{"alpha": float(a)} for a in np.logspace(-4, 4, 17).round(6)],
    "hist gradient boosting": [
        {"learning_rate": lr, "max_leaf_nodes": leaves, "min_samples_leaf": msl, "max_iter": it}
        for lr in (0.03, 0.1) for leaves in (7, 15, 31) for msl in (20, 100) for it in (150, 500)
    ],
}


def build(name, params, seed=SEED):
    if name == "ridge":
        return make_pipeline(SimpleImputer(strategy="median", add_indicator=True),
                             StandardScaler(), Ridge(alpha=params["alpha"]))
    return HistGradientBoostingRegressor(l2_regularization=1.0, max_features=0.8,
                                         random_state=seed, **params)


def predict(name, params, fit, ev, feats, seed=SEED):
    if name == "marcel":
        return marcel(ev, fit.per_next.mean(), **params)
    return build(name, params, seed).fit(fit[feats], fit.per_next).predict(ev[feats])


def val_folds(test_from):
    start = test_from - VAL_FOLDS * VAL_FOLD_LEN
    return [(lo, lo + VAL_FOLD_LEN) for lo in range(start, test_from, VAL_FOLD_LEN)]


def tune(name, df, feats, test_from):
    """Rolling-origin CV: each fold is fit on target seasons before it; pick by mean fold MAE."""
    sweep = []
    for params in SWEEP[name]:
        maes = []
        for lo, hi in val_folds(test_from):
            fit = df[df.target_season < lo]
            ev = df[(df.target_season >= lo) & (df.target_season < hi)]
            maes.append(float(mean_absolute_error(ev.per_next, predict(name, params, fit, ev, feats))))
        sweep.append({**params, "fold_mae": [round(m, 4) for m in maes],
                      "val_mae": round(float(np.mean(maes)), 4)})
    best = min(sweep, key=lambda r: r["val_mae"])
    return {k: v for k, v in best.items() if k not in ("fold_mae", "val_mae")}, best["val_mae"], sweep


def next_season(source) -> tuple[list[dict], dict]:
    """Backtest over several test windows, tuning each by rolling-origin CV on prior seasons only."""
    df, feats = next_season_frame(source)
    filt = dict(eval_filter=f"player logged >= {MIN_MP_TARGET} MP in target season")
    rows, sweeps = [], {}
    pooled = {"y": [], "g": [], "ref": [], "preds": {}}

    for t in TEST_WINDOWS[source]:
        tr = df[df.target_season < t]
        te = df[(df.target_season >= t) & (df.target_season < t + WINDOW)]
        folds = ", ".join(f"{lo}-{hi - 1}" for lo, hi in val_folds(t))
        split = f"test {t}-{t + WINDOW - 1}; CV folds {folds}"
        g = te.player_key

        chosen = {name: tune(name, df, feats, t) for name in TUNED}
        sweeps[str(t)] = {name: c[2] for name, c in chosen.items()}
        fitted = {name: predict(name, chosen[name][0], tr, te, feats) for name in ("marcel", "ridge")}
        ref = fitted["marcel"]
        runs = [predict("hist gradient boosting", chosen["hist gradient boosting"][0], tr, te, feats, s)
                for s in SEEDS]
        fitted["hist gradient boosting"] = runs[0]
        seed_maes = [float(mean_absolute_error(te.per_next, p)) for p in runs]
        ref_mae = float(mean_absolute_error(te.per_next, ref))
        picked = min(TUNED, key=lambda n: chosen[n][1])

        # name -> (prediction, tuned model it came from or None, extra fields)
        preds = {
            "baseline: last-season PER": (te.per.fillna(tr.per_next.mean()).values, None, {}),
            "Marcel-style weighted PER (tuned)": (ref, "marcel", {}),
            "ridge (tuned)": (fitted["ridge"], "ridge", {}),
            "hist gradient boosting (tuned)": (runs[0], "hist gradient boosting", {
                "seed_mae": [round(m, 4) for m in seed_maes],
                "seed_mae_sd": round(float(np.std(seed_maes)), 4),
                "seed_delta_vs_marcel": [round(m - ref_mae, 4) for m in seed_maes],
            }),
            "selected by CV": (fitted[picked], picked, {"picked": picked}),
        }
        for name, (p, tuned, extra) in preds.items():
            if tuned:
                extra = {**extra, "params": chosen[tuned][0], "val_mae": chosen[tuned][1]}
            label = f"selected by CV ({picked})" if name == "selected by CV" else name
            rows.append(score("next_season", label, te.per_next, p, len(tr), split, g,
                              mae_minus_marcel_ci95=paired_delta_ci(te.per_next, p, ref, g),
                              **extra, **filt))
            pooled["preds"].setdefault(name, []).append(np.asarray(p))
        pooled["y"].append(te.per_next.values)
        pooled["g"].append(g.values)
        pooled["ref"].append(np.asarray(ref))

    y, g, ref = (np.concatenate(pooled[k]) for k in ("y", "g", "ref"))
    windows = ", ".join(f"{t}-{t + WINDOW - 1}" for t in TEST_WINDOWS[source])
    for name, parts in pooled["preds"].items():
        p = np.concatenate(parts)
        rows.append(score("next_season_pooled", name, y, p, 0, f"all test windows ({windows})", g,
                          mae_minus_marcel_ci95=paired_delta_ci(y, p, ref, g), **filt))
    return rows, sweeps
