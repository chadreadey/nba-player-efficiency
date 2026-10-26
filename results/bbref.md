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
| next_season | ridge (tuned) | test 2007-2011; CV folds 2001-2002, 2003-2004, 2005-2006 | 6422 | 1450 | 1.842 | 1.748–1.948 | 0.651 | 4.19 |
| next_season | hist gradient boosting (tuned) | test 2007-2011; CV folds 2001-2002, 2003-2004, 2005-2006 | 6422 | 1450 | 1.829 | 1.750–1.913 | 0.691 | 4.19 |
| next_season | selected by CV (hist gradient boosting) | test 2007-2011; CV folds 2001-2002, 2003-2004, 2005-2006 | 6422 | 1450 | 1.829 | 1.750–1.913 | 0.691 | 4.19 |
| next_season | baseline: last-season PER | test 2012-2016; CV folds 2006-2007, 2008-2009, 2010-2011 | 7872 | 1531 | 2.356 | 2.244–2.478 | 0.449 | 4.21 |
| next_season | Marcel-style weighted PER (tuned) | test 2012-2016; CV folds 2006-2007, 2008-2009, 2010-2011 | 7872 | 1531 | 2.087 | 1.999–2.168 | 0.605 | 4.21 |
| next_season | ridge (tuned) | test 2012-2016; CV folds 2006-2007, 2008-2009, 2010-2011 | 7872 | 1531 | 1.901 | 1.820–1.979 | 0.665 | 4.21 |
| next_season | hist gradient boosting (tuned) | test 2012-2016; CV folds 2006-2007, 2008-2009, 2010-2011 | 7872 | 1531 | 1.880 | 1.802–1.957 | 0.670 | 4.21 |
| next_season | selected by CV (hist gradient boosting) | test 2012-2016; CV folds 2006-2007, 2008-2009, 2010-2011 | 7872 | 1531 | 1.880 | 1.802–1.957 | 0.670 | 4.21 |
| next_season | baseline: last-season PER | test 2017-2021; CV folds 2011-2012, 2013-2014, 2015-2016 | 9403 | 1560 | 2.259 | 2.154–2.362 | 0.578 | 4.63 |
| next_season | Marcel-style weighted PER (tuned) | test 2017-2021; CV folds 2011-2012, 2013-2014, 2015-2016 | 9403 | 1560 | 2.075 | 1.986–2.169 | 0.672 | 4.63 |
| next_season | ridge (tuned) | test 2017-2021; CV folds 2011-2012, 2013-2014, 2015-2016 | 9403 | 1560 | 2.012 | 1.923–2.103 | 0.686 | 4.63 |
| next_season | hist gradient boosting (tuned) | test 2017-2021; CV folds 2011-2012, 2013-2014, 2015-2016 | 9403 | 1560 | 1.944 | 1.865–2.028 | 0.716 | 4.63 |
| next_season | selected by CV (hist gradient boosting) | test 2017-2021; CV folds 2011-2012, 2013-2014, 2015-2016 | 9403 | 1560 | 1.944 | 1.865–2.028 | 0.716 | 4.63 |
| next_season | baseline: last-season PER | test 2022-2026; CV folds 2016-2017, 2018-2019, 2020-2021 | 10963 | 1643 | 2.078 | 1.980–2.178 | 0.583 | 4.38 |
| next_season | Marcel-style weighted PER (tuned) | test 2022-2026; CV folds 2016-2017, 2018-2019, 2020-2021 | 10963 | 1643 | 1.911 | 1.839–1.985 | 0.698 | 4.38 |
| next_season | ridge (tuned) | test 2022-2026; CV folds 2016-2017, 2018-2019, 2020-2021 | 10963 | 1643 | 1.826 | 1.746–1.905 | 0.710 | 4.38 |
| next_season | hist gradient boosting (tuned) | test 2022-2026; CV folds 2016-2017, 2018-2019, 2020-2021 | 10963 | 1643 | 1.977 | 1.898–2.055 | 0.667 | 4.38 |
| next_season | selected by CV (hist gradient boosting) | test 2022-2026; CV folds 2016-2017, 2018-2019, 2020-2021 | 10963 | 1643 | 1.977 | 1.898–2.055 | 0.667 | 4.38 |
| next_season_pooled | baseline: last-season PER | all test windows (2007-2011, 2012-2016, 2017-2021, 2022-2026) | 0 | 6184 | 2.249 | 2.193–2.307 | 0.487 | 4.36 |
| next_season_pooled | Marcel-style weighted PER (tuned) | all test windows (2007-2011, 2012-2016, 2017-2021, 2022-2026) | 0 | 6184 | 2.022 | 1.980–2.067 | 0.652 | 4.36 |
| next_season_pooled | ridge (tuned) | all test windows (2007-2011, 2012-2016, 2017-2021, 2022-2026) | 0 | 6184 | 1.895 | 1.852–1.935 | 0.681 | 4.36 |
| next_season_pooled | hist gradient boosting (tuned) | all test windows (2007-2011, 2012-2016, 2017-2021, 2022-2026) | 0 | 6184 | 1.910 | 1.870–1.948 | 0.687 | 4.36 |
| next_season_pooled | selected by CV | all test windows (2007-2011, 2012-2016, 2017-2021, 2022-2026) | 0 | 6184 | 1.910 | 1.870–1.948 | 0.687 | 4.36 |

Next-season MAE minus Marcel baseline MAE (paired, player bootstrap; negative = better):

- test 2007-2011, baseline: last-season PER: +0.297 (95% CI +0.177 to +0.447)
- test 2007-2011, Marcel-style weighted PER (tuned): +0.000 (95% CI +0.000 to +0.000)
- test 2007-2011, ridge (tuned): -0.183 (95% CI -0.261 to -0.091)
- test 2007-2011, hist gradient boosting (tuned): -0.195 (95% CI -0.253 to -0.139)
- test 2007-2011, selected by CV (hist gradient boosting): -0.195 (95% CI -0.253 to -0.139)
- test 2012-2016, baseline: last-season PER: +0.269 (95% CI +0.181 to +0.364)
- test 2012-2016, Marcel-style weighted PER (tuned): +0.000 (95% CI +0.000 to +0.000)
- test 2012-2016, ridge (tuned): -0.186 (95% CI -0.256 to -0.126)
- test 2012-2016, hist gradient boosting (tuned): -0.207 (95% CI -0.271 to -0.150)
- test 2012-2016, selected by CV (hist gradient boosting): -0.207 (95% CI -0.271 to -0.150)
- test 2017-2021, baseline: last-season PER: +0.184 (95% CI +0.099 to +0.269)
- test 2017-2021, Marcel-style weighted PER (tuned): +0.000 (95% CI +0.000 to +0.000)
- test 2017-2021, ridge (tuned): -0.063 (95% CI -0.126 to +0.004)
- test 2017-2021, hist gradient boosting (tuned): -0.131 (95% CI -0.187 to -0.073)
- test 2017-2021, selected by CV (hist gradient boosting): -0.131 (95% CI -0.187 to -0.073)
- test 2022-2026, baseline: last-season PER: +0.167 (95% CI +0.077 to +0.247)
- test 2022-2026, Marcel-style weighted PER (tuned): +0.000 (95% CI +0.000 to +0.000)
- test 2022-2026, ridge (tuned): -0.085 (95% CI -0.139 to -0.031)
- test 2022-2026, hist gradient boosting (tuned): +0.067 (95% CI +0.001 to +0.133)
- test 2022-2026, selected by CV (hist gradient boosting): +0.067 (95% CI +0.001 to +0.133)
- all test windows (2007-2011, 2012-2016, 2017-2021, 2022-2026), baseline: last-season PER: +0.227 (95% CI +0.183 to +0.280)
- all test windows (2007-2011, 2012-2016, 2017-2021, 2022-2026), Marcel-style weighted PER (tuned): +0.000 (95% CI +0.000 to +0.000)
- all test windows (2007-2011, 2012-2016, 2017-2021, 2022-2026), ridge (tuned): -0.127 (95% CI -0.159 to -0.091)
- all test windows (2007-2011, 2012-2016, 2017-2021, 2022-2026), hist gradient boosting (tuned): -0.112 (95% CI -0.143 to -0.080)
- all test windows (2007-2011, 2012-2016, 2017-2021, 2022-2026), selected by CV: -0.112 (95% CI -0.143 to -0.080)

Chosen on the validation window (MAE there), then refit and scored once on test:

- test 2007-2011, Marcel-style weighted PER (tuned): {'ballast_mp': 1500} (CV MAE 2.040)
- test 2007-2011, ridge (tuned): {'alpha': 31.622777} (CV MAE 1.860)
- test 2007-2011, hist gradient boosting (tuned): {'learning_rate': 0.03, 'max_leaf_nodes': 15, 'min_samples_leaf': 20, 'max_iter': 150} (CV MAE 1.825)
- test 2007-2011, selected by CV (hist gradient boosting): {'learning_rate': 0.03, 'max_leaf_nodes': 15, 'min_samples_leaf': 20, 'max_iter': 150} (CV MAE 1.825)
- test 2012-2016, Marcel-style weighted PER (tuned): {'ballast_mp': 2000} (CV MAE 2.051)
- test 2012-2016, ridge (tuned): {'alpha': 31.622777} (CV MAE 1.880)
- test 2012-2016, hist gradient boosting (tuned): {'learning_rate': 0.03, 'max_leaf_nodes': 7, 'min_samples_leaf': 100, 'max_iter': 500} (CV MAE 1.826)
- test 2012-2016, selected by CV (hist gradient boosting): {'learning_rate': 0.03, 'max_leaf_nodes': 7, 'min_samples_leaf': 100, 'max_iter': 500} (CV MAE 1.826)
- test 2017-2021, Marcel-style weighted PER (tuned): {'ballast_mp': 2000} (CV MAE 2.063)
- test 2017-2021, ridge (tuned): {'alpha': 0.0001} (CV MAE 1.869)
- test 2017-2021, hist gradient boosting (tuned): {'learning_rate': 0.03, 'max_leaf_nodes': 15, 'min_samples_leaf': 100, 'max_iter': 500} (CV MAE 1.842)
- test 2017-2021, selected by CV (hist gradient boosting): {'learning_rate': 0.03, 'max_leaf_nodes': 15, 'min_samples_leaf': 100, 'max_iter': 500} (CV MAE 1.842)
- test 2022-2026, Marcel-style weighted PER (tuned): {'ballast_mp': 2000} (CV MAE 2.081)
- test 2022-2026, ridge (tuned): {'alpha': 0.0001} (CV MAE 1.983)
- test 2022-2026, hist gradient boosting (tuned): {'learning_rate': 0.03, 'max_leaf_nodes': 15, 'min_samples_leaf': 100, 'max_iter': 500} (CV MAE 1.918)
- test 2022-2026, selected by CV (hist gradient boosting): {'learning_rate': 0.03, 'max_leaf_nodes': 15, 'min_samples_leaf': 100, 'max_iter': 500} (CV MAE 1.918)

Gradient boosting across seeds [0, 1, 2, 3, 4] (table rows use the first seed):

- test 2007-2011: MAE 1.825–1.829 (sd 0.002); minus Marcel -0.200 to -0.195
- test 2012-2016: MAE 1.876–1.881 (sd 0.002); minus Marcel -0.211 to -0.206
- test 2017-2021: MAE 1.936–1.947 (sd 0.004); minus Marcel -0.139 to -0.128
- test 2022-2026: MAE 1.960–1.999 (sd 0.012); minus Marcel +0.049 to +0.088

Notes:
- features: per-36 box-score counts + season
- eval_filter: player logged >= 500 MP in target season

data: kaggle sumitrodatta/nba-aba-baa-stats v56 (sha256 5be35c283702…); seed=1, python 3.12.15, scikit-learn 1.9.1
