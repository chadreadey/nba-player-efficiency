# Notes on the 2023 notebook's setup

Background for why this repository forecasts *next-season* PER. These checks were run on the 2023 group notebook ([`NBA_Python_Code_Report.ipynb`](../NBA_Python_Code_Report.ipynb)) with `train.py --source legacy`.

The 2023 notebook reported a test MAE of **0.35** (stacking ensemble), against a PER standard deviation of about 4.7. Rerunning it shows why the number is so low:

- **The target is a function of the features.** PER is computed from the same season's box score, plus team and league pace adjustments. The model was given that box score, plus composites built from it (BPM, Win Shares, VORP). The task is to reconstruct a formula.
- **Out-of-time testing doesn't hurt it.** Training on earlier seasons and testing on later ones gives almost the same error as the random split: untuned gradient boosting gets MAE 0.39 (test 2013–17) and 0.36 (test 2022–26). The setup itself is the problem, not just the split.
- **The composite features carry the signal.** Removing BPM, Win Shares and VORP raises the out-of-time MAE to 0.60 on the old data and 1.34 on the new data.
- **Near-duplicate rows cross the split.** A traded player has a combined-season row plus one row per team. 3,537 of the 14,585 modelled rows come from such player-seasons, and a random 80/20 split puts near-copies on both sides.
- **The sample was narrower than described.** After `dropna()`, the model used 14,585 rows from 1980–2017, not "~24,700 rows since 1950". Players with no 3-point attempts (mostly low-minute players) were silently dropped.

Reproduction check: the notebook's exact cleaning and split, with untuned gradient boosting, gives MAE 0.403. The notebook's XGBoost gave 0.4065.
