# NBA PER refresh: findings and plan (started 2026-10-24, updated 2026-10-26)

Status: the refresh was pushed 2026-10-25 (commit b666f82). The `exp`-leak correction in section 3 is local and not yet pushed. No Modal resources have been created.
Every number below comes from `results/legacy.md`, `results/bbref.md` and `results/bbref_diagnostics.md`, which `train.py` and `diagnostics.py` produced.

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

**Correction (2026-10-26):**
- **The bug:** on the bbref data, the `exp` (prior seasons) feature was computed with `cumcount` in file order, and the bbref files list the newest seasons first. So `exp` counted a player's *future* seasons: a leak, and a feature whose distribution shifted in the latest window.
- **The fix:** sort by player and season before counting.
- **What changed:** ridge and gradient-boosting numbers on bbref. Everything quoted before this date for those models on bbref is superseded.
- **Unchanged:** the legacy results, which are byte-identical after the rerun, and the Marcel and last-season baselines, which don't use `exp`.

**Protocol (rolling-origin backtest):**
- Data: Kaggle `sumitrodatta/nba-aba-baa-stats` **v56**, pinned and verified against a sha256 checksum on every load.
- Four 5-season test windows: 2007–11, 2012–16, 2017–21 and 2022–26.
- For each window, settings are chosen by **rolling-origin CV**: three 2-season folds just before the window, each fit only on seasons before itself, scored by mean fold MAE.
- Marcel (ballast), ridge and gradient boosting compete on that CV score, and the winner is "selected by CV". Its setting is refit on all earlier seasons and scored once on the window.
- Sweeps:
  - Marcel ballast: 8 values
  - ridge alpha: 17 values, 1e-4 to 1e4
  - gradient boosting: 24 combinations, with 80% feature subsampling
- The chosen gradient-boosting setting is refit with 5 seeds; its test MAE varies by at most 0.011 in any window.

Results after the fix, scored on players with at least 500 MP in the target season. Δ is the MAE minus the tuned Marcel baseline's MAE: paired, with a 95% player-cluster bootstrap CI, and negative means better.

| test window | n | Marcel MAE | ridge MAE (Δ) | gradient boosting MAE (Δ) | selected by CV |
|---|---|---|---|---|---|
| 2007–11 | 1,450 | 2.024 | 1.915 (−0.109, CI −0.183 to −0.015) | 1.874 (−0.150, CI −0.207 to −0.097) | gradient boosting |
| 2012–16 | 1,531 | 2.087 | 1.972 (−0.116, CI −0.181 to −0.062) | 1.923 (−0.164, CI −0.222 to −0.112) | gradient boosting |
| 2017–21 | 1,560 | 2.075 | 2.050 (−0.025, CI −0.091 to +0.046) | 1.959 (−0.116, CI −0.178 to −0.056) | gradient boosting |
| 2022–26 | 1,643 | 1.911 | 1.825 (−0.086, CI −0.143 to −0.029) | 1.769 (−0.141, CI −0.199 to −0.090) | gradient boosting |
| **pooled** | 6,184 | 2.022 | 1.939 (−0.083, CI −0.117 to −0.049) | 1.880 (−0.143, CI −0.170 to −0.116) | **1.880 (−0.143, CI −0.170 to −0.116)** |

- **Last-season PER alone:** pooled MAE 2.249.
- **Legacy data (test windows 2003–07, 2008–12, 2013–17):** the selected model beats Marcel in all three, pooled Δ −0.149 (95% CI −0.180 to −0.116).
- **What the bug did:** before the fix, gradient boosting looked better in the early windows and lost to Marcel in 2022–26. The leaked "future seasons" signal helped where there were many future seasons to count, and broke where there weren't.

**Noise ceiling and error breakdown (`diagnostics.py`, `results/bbref_diagnostics.md`):**
- **Noise model:** observed PER = true PER + noise with variance k/MP. It is fit from the variance of age-demeaned year-to-year PER changes against 1/MP_t + 1/MP_t+1 (20 quantile bins, WLS).
- **Stable across choices:** k = 2,007–2,522 across minutes floors (100/250/500) and plain vs robust variance. That is a noise SD of about 1.4–1.6 PER at 1,000 MP.
- **Oracle noise floor** on the test set (knows true next-season talent): MAE about **1.05** (0.96–1.07 across fits).
- **Static-talent oracle** (knows current true talent plus average aging, nothing about change): MAE about 1.70. The selected model's 1.88 is above it.
- **Noise share:** measurement noise is 32% of the selected model's MSE (1.848 of 5.781).
- **Where the model beats Marcel** (pooled Δ):
  - age 33+: −0.48
  - minutes fell below 0.67×: −0.31
  - age 21 or younger: −0.24
- **Where it doesn't:**
  - age 25–28: +0.003, CI −0.031 to +0.036
  - minutes rose above 1.5×: −0.04, CI −0.115 to +0.023

  Those groups are where to look for gains.
- **Caveat:** the minutes and team groupings use target-season information, so they're diagnostic only.

A portfolio line that holds up:

> "Next-season PER forecast, rolling-origin backtest over four 5-season windows (2007–2026, 6,184 player-seasons), with hyperparameters chosen by time-ordered CV. Gradient boosting cut MAE vs a tuned Marcel-style baseline by 0.14 (2.02 → 1.88; 95% CI 0.12–0.17) and won in every window. An estimated noise floor of about 1.05 shows most of the remaining error is real, unmodelled change in talent and role."

## 4. Limitations of the current results

- **Selection bias:** next-season rows exist only for players who returned and played at least 500 minutes. That conditions on the future, so the results don't cover players who left the league or got hurt.
- **Rough noise model.** It assumes noise variance proportional to 1/MP with normal errors. If low-minute players also change more in true talent, k is overstated and the floor is optimistic.
- **Modest search.** The sweeps are small grids. Seeds only matter for gradient boosting, and their spread is reported.
- **Same-season experiments are untuned.** They use fixed hyperparameters, which is fine because they only demonstrate leakage.
- **Snapshot timing:** the 2025-26 rows come from v56, a snapshot taken 2026-04-13, a day after the regular season ended. The minute-weighted league PER is 15.00 for every test season, which is consistent with final data.
- **Unexplained gap:** removing BPM, WS and VORP hurts much more on the new data (1.337) than on legacy (0.599). Not investigated.
- **Imperfect player key:** legacy data has no player id, so the key is name plus birth year.

## 5. Next steps (pending go-ahead)

1. ~~Pick the target and data source~~ (done: next-season PER on sumitrodatta). Still open: Chad confirms he's comfortable with Sports Reference item 11.
2. ~~Pin the dataset version, add a validation window and a tuning sweep~~ (done; it runs locally in about 1.5 minutes per source).
3. ~~Rolling-origin validation, wider ridge grid, multiple seeds~~ (done locally).
   - ~~Noise ceiling and error breakdown~~ (done; it found and fixed the `exp` leak).
   - Next modelling step, not started:
     - predict the residual on Marcel
     - shooting-luck and role-change features (offseason team change, draft position)
     - a ridge plus gradient-boosting average
     - minutes weighting
     - target groups: prime-age players and players about to earn a bigger role
4. **(Needs approval: paid)** Modal is optional: the full backtest runs locally in about 7 minutes. It would only matter for much bigger sweeps, for example more windows, feature ablations, or a minutes-forecast model to address the selection bias. Command: `modal run modal_app.py --source bbref` (CPU only: 4 vCPU, 4 GB, 30-minute timeout).
5. ~~Rewrite the README~~ (done; updated 2026-10-26 with the correction and the noise ceiling).
6. ~~Commit and push~~ (b666f82). **(Needs approval)** Commit and push the `exp` correction and the diagnostics.

## Reproduce

```bash
uv venv --python 3.12 && uv pip install numpy pandas scikit-learn
.venv/bin/python train.py --source legacy   # 2023 data, test seasons 2013-2017
.venv/bin/python train.py --source bbref    # data through 2025-26, test seasons 2022-2026
```
