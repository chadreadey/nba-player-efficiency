"""Run all experiments and write results/<source>.json and results/<source>.md.

    uv run python train.py --source bbref --test-from 2022
    uv run python train.py --source legacy --test-from 2013
"""

from __future__ import annotations

import argparse
import json
import platform
import time
from pathlib import Path

import sklearn

from nba_per import data
from nba_per import experiments as ex

ROOT = Path(__file__).resolve().parent
DEFAULT_TEST_FROM = {"legacy": 2013, "bbref": 2022}


def run(source: str, test_from: int) -> dict:
    rows = []
    if source == "legacy":
        rows += ex.replicate()
    rows += ex.box_score_only(source, test_from)
    rows += ex.same_season_oot(source, test_from)
    ns_rows, sweeps = ex.next_season(source)
    rows += ns_rows
    return {
        "source": source,
        "dataset": data.KAGGLE_DATASETS[source],
        "test_from": test_from,
        "next_season_design": {
            "test_windows": [[t, t + ex.WINDOW - 1] for t in ex.TEST_WINDOWS[source]],
            "cv": f"{ex.VAL_FOLDS} rolling-origin folds of {ex.VAL_FOLD_LEN} seasons before each window",
            "hgb_seeds": list(ex.SEEDS),
        },
        "sweeps": sweeps,
        "seed": ex.SEED,
        "python": platform.python_version(),
        "sklearn": sklearn.__version__,
        "generated_unix": int(time.time()),
        "results": rows,
    }


def to_markdown(res: dict) -> str:
    lines = [
        f"# Results: source={res['source']}, test seasons >= {res['test_from']}",
        "",
        "| experiment | model | split | n_train | n_test | MAE | MAE 95% CI (player bootstrap) | R² | target SD |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for r in res["results"]:
        ci = "–" if "mae_ci95" not in r else f"{r['mae_ci95'][0]:.3f}–{r['mae_ci95'][1]:.3f}"
        lines.append(
            f"| {r['experiment']} | {r['model']} | {r['split']} | {r['n_train']} | {r['n_test']} "
            f"| {r['mae']:.3f} | {ci} | {r['r2']:.3f} | {r['target_sd']:.2f} |"
        )
    deltas = [r for r in res["results"] if "mae_minus_marcel_ci95" in r]
    if deltas:
        lines += ["", "Next-season MAE minus Marcel baseline MAE (paired, player bootstrap; negative = better):", ""]
        lines += [f"- {r['split'].split(';')[0]}, {r['model']}: {r['mae_minus_marcel_ci95'][0]:+.3f} "
                  f"(95% CI {r['mae_minus_marcel_ci95'][1]:+.3f} to {r['mae_minus_marcel_ci95'][2]:+.3f})"
                  for r in deltas]
    tuned = [r for r in res["results"] if "params" in r]
    if tuned:
        lines += ["", "Chosen on the validation window (MAE there), then refit and scored once on test:", ""]
        lines += [f"- {r['split'].split(';')[0]}, {r['model']}: {r['params']} (CV MAE {r['val_mae']:.3f})"
                  for r in tuned]
    seeded = [r for r in res["results"] if "seed_mae" in r]
    if seeded:
        lines += ["", f"Gradient boosting across seeds {res['next_season_design']['hgb_seeds']} "
                  "(table rows use the first seed):", ""]
        lines += [f"- {r['split'].split(';')[0]}: MAE {min(r['seed_mae']):.3f}–{max(r['seed_mae']):.3f} "
                  f"(sd {r['seed_mae_sd']:.3f}); minus Marcel {min(r['seed_delta_vs_marcel']):+.3f} to "
                  f"{max(r['seed_delta_vs_marcel']):+.3f}" for r in seeded]
    notes = {k: v for r in res["results"] for k, v in r.items()
             if k in ("sample", "rows_from_traded_player_seasons", "eval_filter", "features")}
    if notes:
        lines += ["", "Notes:"] + [f"- {k}: {v}" for k, v in notes.items()]
    ds = res["dataset"]
    lines += ["", f"data: kaggle {ds['slug']} v{ds['version']} (sha256 {ds['sha256'][:12]}…); "
              f"seed={res['seed']}, python {res['python']}, scikit-learn {res['sklearn']}"]
    return "\n".join(lines) + "\n"


def main(source: str, test_from: int | None = None, out_dir: Path = ROOT / "results") -> dict:
    res = run(source, test_from or DEFAULT_TEST_FROM[source])
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"{source}_sweep.json").write_text(json.dumps(res.pop("sweeps"), indent=2))
    (out_dir / f"{source}.json").write_text(json.dumps(res, indent=2))
    (out_dir / f"{source}.md").write_text(to_markdown(res))
    return res


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--source", choices=["legacy", "bbref"], default="bbref")
    p.add_argument("--test-from", type=int, default=None,
                   help="first season held out for testing (season 2026 = 2025-26)")
    a = p.parse_args()
    print(to_markdown(main(a.source, a.test_from)))
