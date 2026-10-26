# NBA Player Efficiency Rating (PER): from leaky fit to honest forecast

This project began in 2023 as a group project with **Carli Kelley, Chad Readey and Garner Hasler**. That work predicted a player's PER from their season stats and is kept unchanged in [`NBA_Python_Code_Report.ipynb`](NBA_Python_Code_Report.ipynb). Carli Kelley's original repository is [here](https://github.com/carli-kelley/nba-player-efficiency); I host this copy with permission.

The 2026 refresh (`train.py`, `nba_per/`) is my own work. It has two parts:

1. It shows why the original headline accuracy was mostly **leakage**.
2. It replaces that setup with a real forecasting task, **next-season PER**, tested with a rolling-origin backtest against a strong baseline.

## 1. The original result was formula recovery, not prediction

The 2023 notebook reported a test MAE of **0.35** (stacking ensemble), against a PER standard deviation of about 4.7. Rerunning it shows why the number is so low:

- **The target is a function of the features.** PER is computed from the same season's box score, plus team and league pace adjustments. The model was given that box score, plus composites built from it (BPM, Win Shares, VORP). The task is to reconstruct a formula.
- **Out-of-time testing doesn't hurt it.** Training on earlier seasons and testing on later ones gives almost the same error as the random split: untuned gradient boosting gets MAE 0.39 (test 2013–17) and 0.36 (test 2022–26). The setup itself is the problem, not just the split.
- **The composite features carry the signal.** Removing BPM, Win Shares and VORP raises the out-of-time MAE to 0.60 on the old data and 1.34 on the new data.
- **Near-duplicate rows cross the split.** A traded player has a combined-season row plus one row per team. 3,537 of the 14,585 modelled rows come from such player-seasons, and a random 80/20 split puts near-copies on both sides.
- **The sample was narrower than described.** After `dropna()`, the model used 14,585 rows from 1980–2017, not "~24,700 rows since 1950". Players with no 3-point attempts (mostly low-minute players) were silently dropped.

Reproduction check: the notebook's exact cleaning and split, with untuned gradient boosting, gives MAE 0.403. The notebook's XGBoost gave 0.4065.

## 2. The refreshed task: forecast next season's PER

The model predicts a player's PER in season *t+1* using only what is known at the end of season *t*:

- PER and minutes for seasons *t*, *t−1* and *t−2*
- age and years of experience
- season-*t* rate stats, composites and per-36 box score

**Baseline.** A Marcel-style forecast: a minutes-weighted average of the last three seasons' PER (weights 5/4/3), regressed toward the league mean. Its regression strength is tuned like any other model, so it is a strong baseline, not a straw man.

**Evaluation protocol.**
- **Test windows:** four 5-season windows covering 2007–2026.
- **Tuning:** in each window, hyperparameters are chosen by **time-ordered (rolling-origin) cross-validation**. That means three 2-season folds just before the window, each fit only on seasons before itself.
- **Competition:** the baseline, ridge regression and gradient boosting compete on the same CV score, and the winner is the window's *selected* model. The chosen setting is then refit on all earlier seasons and scored **once** on the test window.
- **Uncertainty:** 95% intervals come from a player-cluster bootstrap, so a player who appears several times is resampled as one unit.
- **Seeds:** gradient boosting is refit with 5 seeds, and its test MAE varies by at most 0.039 across seeds in any window.

**Results** (players with at least 500 minutes in the target season; data through 2025-26). Δ is the selected model's MAE minus the baseline's MAE; negative means the selected model is better.

| Test window | Player-seasons | Baseline MAE | Selected model | Selected MAE | Δ (95% CI) |
|---|---|---|---|---|---|
| 2007–11 | 1,450 | 2.024 | gradient boosting | 1.829 | −0.195 (−0.253 to −0.139) |
| 2012–16 | 1,531 | 2.087 | gradient boosting | 1.880 | −0.207 (−0.271 to −0.150) |
| 2017–21 | 1,560 | 2.075 | gradient boosting | 1.944 | −0.131 (−0.187 to −0.073) |
| 2022–26 | 1,643 | 1.911 | gradient boosting | 1.977 | **+0.067** (+0.001 to +0.133) |
| **All four** | **6,184** | **2.022** | | **1.910** | **−0.112 (−0.143 to −0.080)** |

How to read this:
- **The gain is real but modest.** Over 20 test seasons, the selected model beats a tuned weighted-average baseline by about 0.11 PER of MAE, roughly 5–6%.
- **It doesn't hold in the newest window.** In 2022–26 the selected model is slightly *worse* than the baseline. Ridge regression does beat the baseline there (−0.085), but CV didn't pick it, and choosing it after seeing the test result would be selecting on the test set.
- **Last season's PER alone is clearly worse.** It has an overall MAE of 2.249.
- **The older dataset agrees.** On the 2023 data (test windows 2003–2017), the selected model beats the baseline in all three windows: Δ −0.149 overall (95% CI −0.180 to −0.116).

Full per-window output, chosen hyperparameters and seed spreads are in [`results/bbref.md`](results/bbref.md) and [`results/legacy.md`](results/legacy.md). Every tried setting is in `results/*_sweep.json`.

## Limitations

- **Selection bias.** A next-season row exists only if the player returned and logged at least 500 minutes. The forecast is conditional on that, so it says nothing about players who left the league or were injured.
- **Box-score-only signal.** PER is a box-score metric. Neither this project nor PER captures defence or team context well.
- **Small searches.** The hyperparameter grids are small, with 3 CV folds per window. The 2022–26 folds include the shortened 2019-20 and 2020-21 seasons; that may have hurt model selection there, but I haven't tested it.
- **Final-season data.** The 2025-26 rows come from a dataset snapshot taken the day after the regular season ended.

## Data and terms

| Dataset | Use | Version | Kaggle licence label |
|---|---|---|---|
| [`sumitrodatta/nba-aba-baa-stats`](https://www.kaggle.com/datasets/sumitrodatta/nba-aba-baa-stats) | Main data, 1947 to 2025-26 | v56, updated 2026-04-13 | CC0 |
| [`drgilermo/nba-players-stats`](https://www.kaggle.com/datasets/drgilermo/nba-players-stats) | 2023 notebook, `Seasons_Stats.csv` (1950–2017) | v2 | Unknown |

- **Raw data is not committed.** `nba_per/data.py` downloads each dataset at its pinned version and checks its SHA-256 checksum.
- **Upstream source.** Both datasets come from [Basketball-Reference](https://www.basketball-reference.com/), which this project credits. Their [terms of use](https://www.sports-reference.com/termsofuse.html) restrict scraping and some downstream uses. A Kaggle licence label is set by the uploader and doesn't override those terms. This project does no scraping and redistributes no data.

## Reproduce

```bash
uv venv --python 3.12 && uv pip install numpy pandas scikit-learn
.venv/bin/python train.py --source bbref    # data through 2025-26 (about 6 min on a laptop)
.venv/bin/python train.py --source legacy   # 2023 dataset, plus the notebook replication
```

`modal_app.py` runs the same script on [Modal](https://modal.com) for larger sweeps; the current experiments don't need it.

| Path | Contents |
|---|---|
| `nba_per/data.py` | Pinned download, checksum check, one row per player-season (traded players collapsed) |
| `nba_per/experiments.py` | Notebook replication, leakage checks, next-season backtest |
| `train.py` | Runs everything and writes `results/` |
| `docs/REFRESH_PLAN.md` | Working notes and the full findings |
| `NBA_Python_Code_Report.ipynb` | The original 2023 analysis (Kelley, Readey, Hasler) |
