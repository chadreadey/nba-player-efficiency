# NBA PER refresh: findings and plan (2026-10-24)

Status: the local scripts run; nothing is pushed and no Modal resources have been created.
Every number below comes from `results/legacy.md` and `results/bbref.md`, which `train.py` produced.

## 1. What the 2023 notebook actually measured

The notebook predicts a player's PER from that **same season's** stats, using an 80/20 random row split.
Its best test MAE is 0.3496 (stacking ensemble). These are the problems with that design.

| Issue | Evidence |
|---|---|
| **The target is a formula of the inputs.** PER is computed from the same season's box score plus team and league pace adjustments. The features are that box score, plus composites built from it (BPM, OBPM, WS, WS/48, VORP). The model is reconstructing Hollinger's formula, not predicting anything. | Same features with an out-of-time split, untuned gradient boosting: MAE 0.390 (legacy data, test 2013–17) and 0.357 (new data, test 2022–26). Out-of-time is no worse than the notebook's random split, so the accuracy is formula recovery rather than split luck. |
| **Composite features leak.** BPM and WS are near-substitutes for PER. | Dropping BPM, WS and VORP raises the out-of-time MAE from 0.390 to 0.599 (legacy) and from 0.357 to 1.337 (new data). |
| **Duplicate rows across the split.** Traded players have a `TOT` row and one row per team, and the `TOT` row is the sum of the team rows. A random split puts these near-duplicates on both sides. | 3,537 of the 14,585 modelled rows come from traded player-seasons. |
| **The sample is smaller and biased.** The write-up says about 24,700 rows from 1950. After `dropna()` the model actually used 14,585 rows from **1980–2017**. Players with no 3-point attempts (3P% null) are silently dropped, and they are mostly low-minute players. | 3,511 rows from 1980 onward have a null 3P%. Their median minutes are 208, against 985 overall. |
| **No minutes floor.** PER on tiny samples is noise (range −23 to 40). | 805 of the modelled rows have fewer than 100 minutes. |
| Minor | The model selection and the "most important features" claims both rest on this leaky setup. Random-split tuning CV was also run on the same rows. |

Replication check: untuned HistGradientBoosting with the notebook's exact cleaning and split gives MAE 0.403. The notebook's XGBoost gave 0.4065, so the pipeline reproduces.

## 2. Data sources

Summary (links and licence labels are in the README's "Data and terms" section):

- **Recommended: Kaggle `sumitrodatta/nba-aba-baa-stats`.**
  - Covers 1947 to 2025-26 (season `2026`), with PER, BPM, WS and USG%, and has a `player_id`.
  - Kaggle lists it as CC0; last updated 2026-04-13. It downloads without credentials, and `nba_per/data.py` does that.
  - **Caveat:** the data comes from Basketball-Reference. Sports Reference's terms (section 5, items 9–11) bar scraping, competing databases and AI/ML training.
  - A CC0 label set by the uploader does not override those upstream terms. Nobody has checked the exact wording of item 11 yet; Chad should read it.
  - Plan: download by script, never commit raw data, credit Basketball-Reference.
- The current data, Kaggle `drgilermo/nba-players-stats`, has licence "Unknown" and stops at 2017. Keep it only to reproduce the old notebook.
- `nba_api` / stats.nba.com has no PER, and NBA.com's terms are personal and non-commercial only. Not recommended.
- Kaggle `bendikfltaas/nba-historical-stats-1985-2026` (MIT label) is a possible second source. I haven't inspected it.

## 3. Target: next-season PER (chosen by Chad, 2026-10-25)

**Next-season PER.** Predict PER in season t+1 using only what is known at the end of season t:

- PER and minutes for t, t-1 and t-2
- age and years of experience
- season t rates and composites, and per-36 box score

**Protocol (rolling-origin backtest):**
- Data: Kaggle `sumitrodatta/nba-aba-baa-stats` **v56**, pinned and verified against a sha256 checksum on every load.
- Four 5-season test windows: 2007–11, 2012–16, 2017–21 and 2022–26.
- For each window, settings are chosen by **rolling-origin CV**: three 2-season folds just before the window, each fit only on seasons before itself, scored by mean fold MAE.
- The chosen setting is refit on every season before the window and scored **once** on it.
- Marcel (ballast), ridge and gradient boosting all compete on the same CV score. The winner in each window is the **"selected by CV"** model, the protocol's honest pick.
- Sweeps:
  - Marcel ballast: 8 values, 250–6,000 minutes
  - ridge alpha: 17 values, 1e-4 to 1e4
  - gradient boosting: 24 combinations, with 80% feature subsampling
- The chosen gradient-boosting setting is refit with 5 seeds (0–4).
- Everything runs locally (the new-data run took about 6 minutes). Full sweeps are in `results/bbref_sweep.json`.

Scored on players with at least 500 MP in the target season. Δ is the MAE minus the tuned Marcel baseline's MAE: paired, with a 95% player-cluster bootstrap CI, and negative means better.

| test window | n | Marcel (tuned) MAE | ridge MAE (Δ) | gradient boosting MAE (Δ) | selected by CV |
|---|---|---|---|---|---|
| 2007–11 | 1,450 | 2.024 | 1.842 (−0.183, CI −0.261 to −0.091) | 1.829 (−0.195, CI −0.253 to −0.139) | gradient boosting |
| 2012–16 | 1,531 | 2.087 | 1.901 (−0.186, CI −0.256 to −0.126) | 1.880 (−0.207, CI −0.271 to −0.150) | gradient boosting |
| 2017–21 | 1,560 | 2.075 | 2.012 (−0.063, CI −0.126 to +0.004) | 1.944 (−0.131, CI −0.187 to −0.073) | gradient boosting |
| 2022–26 | 1,643 | 1.911 | 1.826 (−0.085, CI −0.139 to −0.031) | 1.977 (**+0.067**, CI +0.001 to +0.133) | gradient boosting |
| **pooled** | 6,184 | 2.022 | 1.895 (−0.127, CI −0.159 to −0.091) | 1.910 (−0.112, CI −0.143 to −0.080) | **1.910 (−0.112, CI −0.143 to −0.080)** |

For reference, last season's PER alone scores a pooled MAE of 2.249, which is worse than Marcel by 0.227.

**Seeds:** gradient-boosting test MAE varies by at most 0.039 across the 5 seeds in any window (SD 0.002–0.012). Seed noise doesn't explain any of the window results; in 2022–26 every seed is worse than Marcel (by +0.049 to +0.088).

**Legacy data (test windows 2003–07, 2008–12, 2013–17):**
- The CV-selected model (gradient boosting in every window) beats Marcel in all three.
- Pooled Δ is −0.149 (95% CI −0.180 to −0.116), over 4,441 player-seasons.

**The honest reading:**
- **Real but modest gain.** Across 20 test seasons, the protocol's pick beats a tuned weighted-average baseline by about 0.11 PER MAE, roughly 5–6%.
- **The latest window is the exception.** In 2022–26, CV still picks gradient boosting, and it is slightly *worse* than the baseline. Ridge beats the baseline there, but choosing ridge because of that would mean selecting on test data.
- **Untested guess:** the 2022–26 CV folds include the shortened 2019-20 and 2020-21 seasons, which may mislead selection.
- **Ridge alpha:** the chosen value moves between 1e-4 and 31.6 across windows. In two windows it lands at the low edge (1e-4), meaning effectively plain least squares, so extending the grid lower would change nothing.

A portfolio line that holds up:

> "Next-season PER forecast, rolling-origin backtest over four 5-season windows (2007–2026, 6,184 player-seasons), with hyperparameters chosen by time-ordered CV. The selected model (gradient boosting) cut MAE vs a tuned Marcel-style baseline by 0.11 (2.02 → 1.91; 95% CI 0.08–0.14). The gain held in 3 of 4 windows and reversed slightly in 2022–26."

## 4. Limitations of the current results

- **Selection bias:** next-season rows exist only for players who returned and played at least 500 minutes. That conditions on the future, so the results don't cover players who left the league or got hurt.
- **Modest search.** The sweeps are small grids. Seeds only matter for gradient boosting, and their spread is reported.
- **Same-season experiments are untuned.** They use fixed hyperparameters, which is fine because they only demonstrate leakage.
- **Snapshot timing:** the 2025-26 rows come from v56, a snapshot taken 2026-04-13, a day after the regular season ended. The minute-weighted league PER is 15.00 for every test season, which is consistent with final data.
- **Unexplained gap:** removing BPM, WS and VORP hurts much more on the new data (1.337) than on legacy (0.599). Not investigated.
- **Imperfect player key:** legacy data has no player id, so the key is name plus birth year.

## 5. Next steps (pending go-ahead)

1. ~~Pick the target and data source~~ (done: next-season PER on sumitrodatta). Still open: Chad confirms he's comfortable with Sports Reference item 11.
2. ~~Pin the dataset version, add a validation window and a tuning sweep~~ (done; it runs locally in about 1.5 minutes per source).
3. ~~Rolling-origin validation, wider ridge grid, multiple seeds~~ (done locally).
4. **(Needs approval: paid)** Modal is optional: the full backtest runs locally in about 6 minutes. It would only matter for much bigger sweeps, for example more windows, feature ablations, or a minutes-forecast model to address the selection bias. Command: `modal run modal_app.py --source bbref` (CPU only: 4 vCPU, 4 GB, 30-minute timeout).
5. Rewrite the README with the leakage story and the honest results table. Keep the 2023 notebook as the "original" and credit its authors.
6. **(Needs approval)** Commit and push to `chadreadey/nba-player-efficiency`.

## Reproduce

```bash
uv venv --python 3.12 && uv pip install numpy pandas scikit-learn
.venv/bin/python train.py --source legacy   # 2023 data, test seasons 2013-2017
.venv/bin/python train.py --source bbref    # data through 2025-26, test seasons 2022-2026
```
