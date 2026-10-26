# Results: source=bbref, test seasons >= 2022

| experiment | model | split | n_train | n_test | MAE | MAE 95% CI (player bootstrap) | R² | target SD |
|---|---|---|---|---|---|---|---|---|
| box_score_only | linear regression | train <2022, test >=2022 | 14514 | 2166 | 2.252 | 2.209–2.299 | 0.706 | 4.39 |
| box_score_only | hist gradient boosting | train <2022, test >=2022 | 14514 | 2166 | 0.741 | 0.706–0.777 | 0.952 | 4.39 |
| same_season_oot | train mean | train <2022, test >=2022 | 14514 | 2166 | 3.422 | 3.217–3.641 | -0.007 | 4.39 |
| same_season_oot | hist gradient boosting (notebook features) | train <2022, test >=2022 | 14514 | 2166 | 0.357 | 0.342–0.374 | 0.988 | 4.39 |
| same_season_oot | hist gradient boosting (without BPM/WS/VORP) | train <2022, test >=2022 | 14514 | 2166 | 1.337 | 1.296–1.379 | 0.880 | 4.39 |
| next_season | baseline: last-season PER | test 2007-2011; CV folds 2001-2002, 2003-2004, 2005-2006 | 6422 | 1450 | 2.322 | 2.186–2.488 | 0.284 | 4.19 |
| next_season | Marcel-style weighted PER (tuned) | test 2007-2011; CV folds 2001-2002, 2003-2004, 2005-2006 | 6422 | 1450 | 2.024 | 1.944–2.116 | 0.618 | 4.19 |
| next_season | ridge (tuned) | test 2007-2011; CV folds 2001-2002, 2003-2004, 2005-2006 | 6422 | 1450 | 1.915 | 1.821–2.028 | 0.619 | 4.19 |
| next_season | hist gradient boosting (tuned) | test 2007-2011; CV folds 2001-2002, 2003-2004, 2005-2006 | 6422 | 1450 | 1.874 | 1.795–1.954 | 0.675 | 4.19 |
| next_season | selected by CV (hist gradient boosting) | test 2007-2011; CV folds 2001-2002, 2003-2004, 2005-2006 | 6422 | 1450 | 1.874 | 1.795–1.954 | 0.675 | 4.19 |
| next_season | baseline: last-season PER | test 2012-2016; CV folds 2006-2007, 2008-2009, 2010-2011 | 7872 | 1531 | 2.356 | 2.244–2.478 | 0.449 | 4.21 |
| next_season | Marcel-style weighted PER (tuned) | test 2012-2016; CV folds 2006-2007, 2008-2009, 2010-2011 | 7872 | 1531 | 2.087 | 1.999–2.168 | 0.605 | 4.21 |
| next_season | ridge (tuned) | test 2012-2016; CV folds 2006-2007, 2008-2009, 2010-2011 | 7872 | 1531 | 1.972 | 1.885–2.053 | 0.642 | 4.21 |
| next_season | hist gradient boosting (tuned) | test 2012-2016; CV folds 2006-2007, 2008-2009, 2010-2011 | 7872 | 1531 | 1.923 | 1.845–1.997 | 0.659 | 4.21 |
| next_season | selected by CV (hist gradient boosting) | test 2012-2016; CV folds 2006-2007, 2008-2009, 2010-2011 | 7872 | 1531 | 1.923 | 1.845–1.997 | 0.659 | 4.21 |
| next_season | baseline: last-season PER | test 2017-2021; CV folds 2011-2012, 2013-2014, 2015-2016 | 9403 | 1560 | 2.259 | 2.154–2.362 | 0.578 | 4.63 |
| next_season | Marcel-style weighted PER (tuned) | test 2017-2021; CV folds 2011-2012, 2013-2014, 2015-2016 | 9403 | 1560 | 2.075 | 1.986–2.169 | 0.672 | 4.63 |
| next_season | ridge (tuned) | test 2017-2021; CV folds 2011-2012, 2013-2014, 2015-2016 | 9403 | 1560 | 2.050 | 1.963–2.139 | 0.672 | 4.63 |
| next_season | hist gradient boosting (tuned) | test 2017-2021; CV folds 2011-2012, 2013-2014, 2015-2016 | 9403 | 1560 | 1.959 | 1.878–2.038 | 0.710 | 4.63 |
| next_season | selected by CV (hist gradient boosting) | test 2017-2021; CV folds 2011-2012, 2013-2014, 2015-2016 | 9403 | 1560 | 1.959 | 1.878–2.038 | 0.710 | 4.63 |
| next_season | baseline: last-season PER | test 2022-2026; CV folds 2016-2017, 2018-2019, 2020-2021 | 10963 | 1643 | 2.078 | 1.980–2.178 | 0.583 | 4.38 |
| next_season | Marcel-style weighted PER (tuned) | test 2022-2026; CV folds 2016-2017, 2018-2019, 2020-2021 | 10963 | 1643 | 1.911 | 1.839–1.985 | 0.698 | 4.38 |
| next_season | ridge (tuned) | test 2022-2026; CV folds 2016-2017, 2018-2019, 2020-2021 | 10963 | 1643 | 1.825 | 1.749–1.901 | 0.710 | 4.38 |
| next_season | hist gradient boosting (tuned) | test 2022-2026; CV folds 2016-2017, 2018-2019, 2020-2021 | 10963 | 1643 | 1.769 | 1.694–1.843 | 0.730 | 4.38 |
| next_season | selected by CV (hist gradient boosting) | test 2022-2026; CV folds 2016-2017, 2018-2019, 2020-2021 | 10963 | 1643 | 1.769 | 1.694–1.843 | 0.730 | 4.38 |
| next_season_pooled | baseline: last-season PER | all test windows (2007-2011, 2012-2016, 2017-2021, 2022-2026) | 0 | 6184 | 2.249 | 2.193–2.307 | 0.487 | 4.36 |
| next_season_pooled | Marcel-style weighted PER (tuned) | all test windows (2007-2011, 2012-2016, 2017-2021, 2022-2026) | 0 | 6184 | 2.022 | 1.980–2.067 | 0.652 | 4.36 |
| next_season_pooled | ridge (tuned) | all test windows (2007-2011, 2012-2016, 2017-2021, 2022-2026) | 0 | 6184 | 1.939 | 1.897–1.980 | 0.664 | 4.36 |
| next_season_pooled | hist gradient boosting (tuned) | all test windows (2007-2011, 2012-2016, 2017-2021, 2022-2026) | 0 | 6184 | 1.880 | 1.839–1.916 | 0.696 | 4.36 |
| next_season_pooled | selected by CV | all test windows (2007-2011, 2012-2016, 2017-2021, 2022-2026) | 0 | 6184 | 1.880 | 1.839–1.916 | 0.696 | 4.36 |

Next-season MAE minus Marcel baseline MAE (paired, player bootstrap; negative = better):

- test 2007-2011, baseline: last-season PER: +0.297 (95% CI +0.177 to +0.447)
- test 2007-2011, Marcel-style weighted PER (tuned): +0.000 (95% CI +0.000 to +0.000)
- test 2007-2011, ridge (tuned): -0.109 (95% CI -0.183 to -0.015)
- test 2007-2011, hist gradient boosting (tuned): -0.150 (95% CI -0.207 to -0.097)
- test 2007-2011, selected by CV (hist gradient boosting): -0.150 (95% CI -0.207 to -0.097)
- test 2012-2016, baseline: last-season PER: +0.269 (95% CI +0.181 to +0.364)
- test 2012-2016, Marcel-style weighted PER (tuned): +0.000 (95% CI +0.000 to +0.000)
- test 2012-2016, ridge (tuned): -0.116 (95% CI -0.181 to -0.062)
- test 2012-2016, hist gradient boosting (tuned): -0.164 (95% CI -0.222 to -0.112)
- test 2012-2016, selected by CV (hist gradient boosting): -0.164 (95% CI -0.222 to -0.112)
- test 2017-2021, baseline: last-season PER: +0.184 (95% CI +0.099 to +0.269)
- test 2017-2021, Marcel-style weighted PER (tuned): +0.000 (95% CI +0.000 to +0.000)
- test 2017-2021, ridge (tuned): -0.025 (95% CI -0.091 to +0.046)
- test 2017-2021, hist gradient boosting (tuned): -0.116 (95% CI -0.178 to -0.056)
- test 2017-2021, selected by CV (hist gradient boosting): -0.116 (95% CI -0.178 to -0.056)
- test 2022-2026, baseline: last-season PER: +0.167 (95% CI +0.077 to +0.247)
- test 2022-2026, Marcel-style weighted PER (tuned): +0.000 (95% CI +0.000 to +0.000)
- test 2022-2026, ridge (tuned): -0.086 (95% CI -0.143 to -0.029)
- test 2022-2026, hist gradient boosting (tuned): -0.141 (95% CI -0.199 to -0.090)
- test 2022-2026, selected by CV (hist gradient boosting): -0.141 (95% CI -0.199 to -0.090)
- all test windows (2007-2011, 2012-2016, 2017-2021, 2022-2026), baseline: last-season PER: +0.227 (95% CI +0.183 to +0.280)
- all test windows (2007-2011, 2012-2016, 2017-2021, 2022-2026), Marcel-style weighted PER (tuned): +0.000 (95% CI +0.000 to +0.000)
- all test windows (2007-2011, 2012-2016, 2017-2021, 2022-2026), ridge (tuned): -0.083 (95% CI -0.117 to -0.049)
- all test windows (2007-2011, 2012-2016, 2017-2021, 2022-2026), hist gradient boosting (tuned): -0.143 (95% CI -0.170 to -0.116)
- all test windows (2007-2011, 2012-2016, 2017-2021, 2022-2026), selected by CV: -0.143 (95% CI -0.170 to -0.116)

Chosen on the validation window (MAE there), then refit and scored once on test:

- test 2007-2011, Marcel-style weighted PER (tuned): {'ballast_mp': 1500} (CV MAE 2.040)
- test 2007-2011, ridge (tuned): {'alpha': 100.0} (CV MAE 1.921)
- test 2007-2011, hist gradient boosting (tuned): {'learning_rate': 0.03, 'max_leaf_nodes': 7, 'min_samples_leaf': 100, 'max_iter': 500} (CV MAE 1.866)
- test 2007-2011, selected by CV (hist gradient boosting): {'learning_rate': 0.03, 'max_leaf_nodes': 7, 'min_samples_leaf': 100, 'max_iter': 500} (CV MAE 1.866)
- test 2012-2016, Marcel-style weighted PER (tuned): {'ballast_mp': 2000} (CV MAE 2.051)
- test 2012-2016, ridge (tuned): {'alpha': 100.0} (CV MAE 1.953)
- test 2012-2016, hist gradient boosting (tuned): {'learning_rate': 0.03, 'max_leaf_nodes': 7, 'min_samples_leaf': 20, 'max_iter': 500} (CV MAE 1.885)
- test 2012-2016, selected by CV (hist gradient boosting): {'learning_rate': 0.03, 'max_leaf_nodes': 7, 'min_samples_leaf': 20, 'max_iter': 500} (CV MAE 1.885)
- test 2017-2021, Marcel-style weighted PER (tuned): {'ballast_mp': 2000} (CV MAE 2.063)
- test 2017-2021, ridge (tuned): {'alpha': 0.0001} (CV MAE 1.948)
- test 2017-2021, hist gradient boosting (tuned): {'learning_rate': 0.03, 'max_leaf_nodes': 15, 'min_samples_leaf': 100, 'max_iter': 500} (CV MAE 1.899)
- test 2017-2021, selected by CV (hist gradient boosting): {'learning_rate': 0.03, 'max_leaf_nodes': 15, 'min_samples_leaf': 100, 'max_iter': 500} (CV MAE 1.899)
- test 2022-2026, Marcel-style weighted PER (tuned): {'ballast_mp': 2000} (CV MAE 2.081)
- test 2022-2026, ridge (tuned): {'alpha': 316.227766} (CV MAE 2.028)
- test 2022-2026, hist gradient boosting (tuned): {'learning_rate': 0.03, 'max_leaf_nodes': 15, 'min_samples_leaf': 20, 'max_iter': 500} (CV MAE 1.944)
- test 2022-2026, selected by CV (hist gradient boosting): {'learning_rate': 0.03, 'max_leaf_nodes': 15, 'min_samples_leaf': 20, 'max_iter': 500} (CV MAE 1.944)

Gradient boosting across seeds [0, 1, 2, 3, 4] (table rows use the first seed):

- test 2007-2011: MAE 1.874–1.876 (sd 0.001); minus Marcel -0.150 to -0.148
- test 2012-2016: MAE 1.922–1.927 (sd 0.002); minus Marcel -0.165 to -0.160
- test 2017-2021: MAE 1.955–1.962 (sd 0.003); minus Marcel -0.120 to -0.113
- test 2022-2026: MAE 1.767–1.778 (sd 0.004); minus Marcel -0.143 to -0.133

Notes:
- features: per-36 box-score counts + season
- eval_filter: player logged >= 500 MP in target season

data: kaggle sumitrodatta/nba-aba-baa-stats v56 (sha256 5be35c283702…); seed=1, python 3.12.15, scikit-learn 1.9.1
