# Forecasting next-season NBA Player Efficiency Rating (PER)

This project forecasts each NBA player's PER for next season, using only what is known at the end of the current season. It is tested over 20 seasons (2007–2026) against a tuned baseline.

Across 6,184 player-seasons, the selected model has a mean absolute error (MAE) of **1.88 PER**, against **2.02** for the baseline. It beats the baseline in all four 5-season test windows.

It started as a 2023 group project with Carli Kelley and Garner Hasler ([original repository](https://github.com/carli-kelley/nba-player-efficiency); notebook kept unchanged in [`NBA_Python_Code_Report.ipynb`](NBA_Python_Code_Report.ipynb), hosted with permission). The forecast (`train.py`, `diagnostics.py`, `nba_per/`) is my own work.

## 1. The task

The model predicts a player's PER in season *t+1* using only what is known at the end of season *t*:

- PER and minutes for seasons *t*, *t−1* and *t−2*
- age and prior NBA seasons
- season-*t* rate stats, composites and per-36 box score

The target is next season rather than the current one because PER is computed from the same season's box score: predicting it from that box score mostly reconstructs the formula. [`docs/2023_notebook_notes.md`](docs/2023_notebook_notes.md) has the checks behind this.

## 2. Evaluation

**Baseline.** A Marcel-style forecast: a minutes-weighted average of the last three seasons' PER (weights 5/4/3), regressed toward the league mean. Its regression strength is tuned the same way as the models' settings.

**Protocol.**
- **Test windows:** four 5-season windows covering 2007–2026.
- **Tuning:** in each window, hyperparameters are chosen by **time-ordered (rolling-origin) cross-validation**. That means three 2-season folds just before the window, each fit only on seasons before itself.
- **Competition:** the baseline, ridge regression and gradient boosting compete on the same CV score, and the winner is the window's *selected* model. The chosen setting is then refit on all earlier seasons and scored **once** on the test window.
- **Uncertainty:** 95% intervals come from a player-cluster bootstrap, so a player who appears several times is resampled as one unit.
- **Seeds:** gradient boosting is refit with 5 seeds, and its test MAE varies by at most 0.011 across seeds in any window.

## 3. Results

Players with at least 500 minutes in the target season; data through 2025-26. Δ is the selected model's MAE minus the baseline's MAE; negative means the selected model is better.

| Test window | Player-seasons | Baseline MAE | Selected model | Selected MAE | Δ (95% CI) |
|---|---|---|---|---|---|
| 2007–11 | 1,450 | 2.024 | gradient boosting | 1.874 | −0.150 (−0.207 to −0.097) |
| 2012–16 | 1,531 | 2.087 | gradient boosting | 1.923 | −0.164 (−0.222 to −0.112) |
| 2017–21 | 1,560 | 2.075 | gradient boosting | 1.959 | −0.116 (−0.178 to −0.056) |
| 2022–26 | 1,643 | 1.911 | gradient boosting | 1.769 | −0.141 (−0.199 to −0.090) |
| **All four** | **6,184** | **2.022** | | **1.880** | **−0.143 (−0.170 to −0.116)** |

How to read this:
- **The gain is consistent.** CV picks gradient boosting in every window, and it beats a tuned weighted-average baseline in all four, by about 0.14 PER of MAE (roughly 7%).
- **Ridge regression gains less.** Its overall Δ is −0.083 (95% CI −0.117 to −0.049).
- **Last season's PER alone is clearly worse.** It has an overall MAE of 2.249.
- **The older dataset agrees.** On the 2023 data (test windows 2003–2017), the selected model beats the baseline in all three windows: Δ −0.149 overall (95% CI −0.180 to −0.116).

## 4. How good could it get? Noise ceiling and error breakdown

A player's PER over one season includes luck that shrinks with minutes played. I estimate its size from how year-to-year PER changes grow as minutes fall, over about 13,000 consecutive-season pairs.

- **Noise size:** about 1.4–1.6 PER at 1,000 minutes, and about 1.1 at 2,000.
- **Best possible MAE:** a forecaster that knew every player's true next-season talent would still score about **1.05** on this test set (0.96–1.07 across model variants).
- **Room to improve:** measurement noise is only about 32% of the selected model's squared error. Most of the remaining error is real change in talent and role that the model doesn't anticipate.
- **Knowing current talent isn't enough:** a forecaster that knew each player's true *current* talent plus average aging would score about 1.70. That beats this model (1.88), so better estimates of current talent are still worth having.

Where the model gains over the baseline (all four windows pooled; Δ with 95% CI):

| Group | n | Baseline MAE | Selected MAE | Δ |
|---|---|---|---|---|
| Age 33+ in target season | 630 | 2.185 | 1.704 | −0.482 (−0.599 to −0.369) |
| Minutes fell below 0.67× | 945 | 2.507 | 2.196 | −0.312 (−0.385 to −0.240) |
| Age 21 or younger | 397 | 2.263 | 2.020 | −0.242 (−0.364 to −0.133) |
| Age 25–28 | 2,218 | 1.898 | 1.900 | +0.003 (−0.031 to +0.036) |
| Minutes rose above 1.5× | 1,338 | 2.087 | 2.044 | −0.043 (−0.115 to +0.023) |

The model mostly adds **aging** (very old and very young players) and some ability to anticipate declines. It adds nothing for players in their prime, or for players who are about to earn a much bigger role. Those groups are the most likely place to find further gains.

The minutes and team groupings use target-season information. They diagnose where errors come from; they aren't features available when the forecast is made.

Full per-window output, chosen hyperparameters and seed spreads are in [`results/bbref.md`](results/bbref.md) and [`results/legacy.md`](results/legacy.md). The noise model and full breakdown are in [`results/bbref_diagnostics.md`](results/bbref_diagnostics.md). Every tried setting is in `results/*_sweep.json`.

## Limitations

- **Selection bias.** A next-season row exists only if the player returned and logged at least 500 minutes. The forecast is conditional on that, so it says nothing about players who left the league or were injured.
- **Rough noise estimate.** The noise model assumes noise variance proportional to 1/minutes and uses a normal approximation. If low-minute players also change more in true talent, noise is overstated and the floor is somewhat optimistic.
- **Box-score-only signal.** PER is a box-score metric. Neither this project nor PER captures defence or team context well.
- **Small searches.** The hyperparameter grids are small, with 3 CV folds per window.
- **Final-season data.** The 2025-26 rows come from a dataset snapshot taken the day after the regular season ended.

## Data and terms

| Dataset | Use | Version | Kaggle licence label |
|---|---|---|---|
| [`sumitrodatta/nba-aba-baa-stats`](https://www.kaggle.com/datasets/sumitrodatta/nba-aba-baa-stats) | Main data, 1947 to 2025-26 | v56, updated 2026-04-13 | CC0 |
| [`drgilermo/nba-players-stats`](https://www.kaggle.com/datasets/drgilermo/nba-players-stats) | 2023 notebook, `Seasons_Stats.csv` (1950–2017) | v2 | Unknown |

- **Raw data is not committed.** `nba_per/data.py` downloads each dataset at its pinned version and checks its SHA-256 checksum. Per-player predictions are written to the gitignored `data/derived/`; only aggregate results are committed.
- **Upstream source.** Both datasets come from [Basketball-Reference](https://www.basketball-reference.com/), which this project credits. Their [terms of use](https://www.sports-reference.com/termsofuse.html) restrict scraping and some downstream uses. A Kaggle licence label is set by the uploader and doesn't override those terms. This project does no scraping and redistributes no data.

## Reproduce

```bash
uv venv --python 3.12 && uv pip install numpy pandas scikit-learn
.venv/bin/python train.py --source bbref      # data through 2025-26 (about 7 min on a laptop)
.venv/bin/python diagnostics.py --source bbref  # noise ceiling + error breakdown (needs the run above)
.venv/bin/python train.py --source legacy     # the 2023 dataset (1950–2017)
```

`modal_app.py` runs the same script on [Modal](https://modal.com) for larger sweeps; the current experiments don't need it.

| Path | Contents |
|---|---|
| `nba_per/data.py` | Pinned download, checksum check, one row per player-season (traded players collapsed) |
| `nba_per/experiments.py` | Next-season backtest, plus the checks on the 2023 setup |
| `train.py` | Runs everything and writes `results/` |
| `diagnostics.py` | Noise-ceiling estimate and error breakdown |
| `docs/REFRESH_PLAN.md` | Working notes |
| `docs/2023_notebook_notes.md` | Checks on the 2023 notebook's same-season setup |
| `NBA_Python_Code_Report.ipynb` | The original 2023 analysis (Kelley, Readey, Hasler) |

## Changes

- **2026-10-26:** fixed a leak in the "prior NBA seasons" feature. On the newer dataset it was computed in file order, and the file lists the newest seasons first, so it counted a player's future seasons. Sorting by season before counting fixed it. An earlier version of this README reported a smaller gain that reversed in 2022–26; all numbers above are after the fix. The 2023 dataset, stored oldest-first, was unaffected.
