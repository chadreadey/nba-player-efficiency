# Results: source=legacy, test seasons >= 2013

| experiment | model | split | n_train | n_test | MAE | MAE 95% CI (player bootstrap) | R² | target SD |
|---|---|---|---|---|---|---|---|---|
| replicate | train mean | random 80/20 (notebook) | 11668 | 2917 | 3.630 | – | -0.001 | 4.80 |
| replicate | hist gradient boosting | random 80/20 (notebook) | 11668 | 2917 | 0.403 | – | 0.984 | 4.80 |
| box_score_only | linear regression | train <2013, test >=2013 | 10879 | 1996 | 1.320 | 1.285–1.354 | 0.888 | 4.44 |
| box_score_only | hist gradient boosting | train <2013, test >=2013 | 10879 | 1996 | 0.870 | 0.838–0.904 | 0.939 | 4.44 |
| same_season_oot | train mean | train <2013, test >=2013 | 10879 | 1996 | 3.448 | 3.244–3.659 | -0.002 | 4.44 |
| same_season_oot | hist gradient boosting (notebook features) | train <2013, test >=2013 | 10879 | 1996 | 0.390 | 0.368–0.412 | 0.985 | 4.44 |
| same_season_oot | hist gradient boosting (without BPM/WS/VORP) | train <2013, test >=2013 | 10879 | 1996 | 0.599 | 0.572–0.625 | 0.968 | 4.44 |
| next_season | baseline: last-season PER | test 2003-2007; CV folds 1997-1998, 1999-2000, 2001-2002 | 5272 | 1439 | 2.334 | 2.182–2.520 | 0.079 | 4.19 |
| next_season | Marcel-style weighted PER (tuned) | test 2003-2007; CV folds 1997-1998, 1999-2000, 2001-2002 | 5272 | 1439 | 2.066 | 1.981–2.154 | 0.612 | 4.19 |
| next_season | ridge (tuned) | test 2003-2007; CV folds 1997-1998, 1999-2000, 2001-2002 | 5272 | 1439 | 1.963 | 1.870–2.067 | 0.592 | 4.19 |
| next_season | hist gradient boosting (tuned) | test 2003-2007; CV folds 1997-1998, 1999-2000, 2001-2002 | 5272 | 1439 | 1.912 | 1.835–1.995 | 0.669 | 4.19 |
| next_season | selected by CV (hist gradient boosting) | test 2003-2007; CV folds 1997-1998, 1999-2000, 2001-2002 | 5272 | 1439 | 1.912 | 1.835–1.995 | 0.669 | 4.19 |
| next_season | baseline: last-season PER | test 2008-2012; CV folds 2002-2003, 2004-2005, 2006-2007 | 6711 | 1452 | 2.284 | 2.180–2.397 | 0.478 | 4.21 |
| next_season | Marcel-style weighted PER (tuned) | test 2008-2012; CV folds 2002-2003, 2004-2005, 2006-2007 | 6711 | 1452 | 2.044 | 1.953–2.134 | 0.615 | 4.21 |
| next_season | ridge (tuned) | test 2008-2012; CV folds 2002-2003, 2004-2005, 2006-2007 | 6711 | 1452 | 1.934 | 1.843–2.016 | 0.638 | 4.21 |
| next_season | hist gradient boosting (tuned) | test 2008-2012; CV folds 2002-2003, 2004-2005, 2006-2007 | 6711 | 1452 | 1.878 | 1.791–1.961 | 0.674 | 4.21 |
| next_season | selected by CV (hist gradient boosting) | test 2008-2012; CV folds 2002-2003, 2004-2005, 2006-2007 | 6711 | 1452 | 1.878 | 1.791–1.961 | 0.674 | 4.21 |
| next_season | baseline: last-season PER | test 2013-2017; CV folds 2007-2008, 2009-2010, 2011-2012 | 8163 | 1550 | 2.311 | 2.203–2.427 | 0.491 | 4.26 |
| next_season | Marcel-style weighted PER (tuned) | test 2013-2017; CV folds 2007-2008, 2009-2010, 2011-2012 | 8163 | 1550 | 2.054 | 1.967–2.146 | 0.624 | 4.26 |
| next_season | ridge (tuned) | test 2013-2017; CV folds 2007-2008, 2009-2010, 2011-2012 | 8163 | 1550 | 1.981 | 1.891–2.071 | 0.631 | 4.26 |
| next_season | hist gradient boosting (tuned) | test 2013-2017; CV folds 2007-2008, 2009-2010, 2011-2012 | 8163 | 1550 | 1.924 | 1.847–2.007 | 0.669 | 4.26 |
| next_season | selected by CV (hist gradient boosting) | test 2013-2017; CV folds 2007-2008, 2009-2010, 2011-2012 | 8163 | 1550 | 1.924 | 1.847–2.007 | 0.669 | 4.26 |
| next_season_pooled | baseline: last-season PER | all test windows (2003-2007, 2008-2012, 2013-2017) | 0 | 4441 | 2.310 | 2.239–2.393 | 0.356 | 4.22 |
| next_season_pooled | Marcel-style weighted PER (tuned) | all test windows (2003-2007, 2008-2012, 2013-2017) | 0 | 4441 | 2.054 | 2.006–2.102 | 0.618 | 4.22 |
| next_season_pooled | ridge (tuned) | all test windows (2003-2007, 2008-2012, 2013-2017) | 0 | 4441 | 1.960 | 1.904–2.012 | 0.622 | 4.22 |
| next_season_pooled | hist gradient boosting (tuned) | all test windows (2003-2007, 2008-2012, 2013-2017) | 0 | 4441 | 1.905 | 1.859–1.955 | 0.671 | 4.22 |
| next_season_pooled | selected by CV | all test windows (2003-2007, 2008-2012, 2013-2017) | 0 | 4441 | 1.905 | 1.859–1.955 | 0.671 | 4.22 |

Next-season MAE minus Marcel baseline MAE (paired, player bootstrap; negative = better):

- test 2003-2007, baseline: last-season PER: +0.269 (95% CI +0.131 to +0.449)
- test 2003-2007, Marcel-style weighted PER (tuned): +0.000 (95% CI +0.000 to +0.000)
- test 2003-2007, ridge (tuned): -0.102 (95% CI -0.174 to -0.018)
- test 2003-2007, hist gradient boosting (tuned): -0.154 (95% CI -0.205 to -0.099)
- test 2003-2007, selected by CV (hist gradient boosting): -0.154 (95% CI -0.205 to -0.099)
- test 2008-2012, baseline: last-season PER: +0.240 (95% CI +0.153 to +0.334)
- test 2008-2012, Marcel-style weighted PER (tuned): +0.000 (95% CI +0.000 to +0.000)
- test 2008-2012, ridge (tuned): -0.110 (95% CI -0.172 to -0.049)
- test 2008-2012, hist gradient boosting (tuned): -0.165 (95% CI -0.223 to -0.109)
- test 2008-2012, selected by CV (hist gradient boosting): -0.165 (95% CI -0.223 to -0.109)
- test 2013-2017, baseline: last-season PER: +0.257 (95% CI +0.171 to +0.347)
- test 2013-2017, Marcel-style weighted PER (tuned): +0.000 (95% CI +0.000 to +0.000)
- test 2013-2017, ridge (tuned): -0.073 (95% CI -0.140 to -0.007)
- test 2013-2017, hist gradient boosting (tuned): -0.130 (95% CI -0.189 to -0.073)
- test 2013-2017, selected by CV (hist gradient boosting): -0.130 (95% CI -0.189 to -0.073)
- all test windows (2003-2007, 2008-2012, 2013-2017), baseline: last-season PER: +0.255 (95% CI +0.189 to +0.324)
- all test windows (2003-2007, 2008-2012, 2013-2017), Marcel-style weighted PER (tuned): +0.000 (95% CI +0.000 to +0.000)
- all test windows (2003-2007, 2008-2012, 2013-2017), ridge (tuned): -0.095 (95% CI -0.137 to -0.054)
- all test windows (2003-2007, 2008-2012, 2013-2017), hist gradient boosting (tuned): -0.149 (95% CI -0.180 to -0.116)
- all test windows (2003-2007, 2008-2012, 2013-2017), selected by CV: -0.149 (95% CI -0.180 to -0.116)

Chosen on the validation window (MAE there), then refit and scored once on test:

- test 2003-2007, Marcel-style weighted PER (tuned): {'ballast_mp': 2000} (CV MAE 1.971)
- test 2003-2007, ridge (tuned): {'alpha': 10.0} (CV MAE 1.919)
- test 2003-2007, hist gradient boosting (tuned): {'learning_rate': 0.03, 'max_leaf_nodes': 31, 'min_samples_leaf': 20, 'max_iter': 150} (CV MAE 1.880)
- test 2003-2007, selected by CV (hist gradient boosting): {'learning_rate': 0.03, 'max_leaf_nodes': 31, 'min_samples_leaf': 20, 'max_iter': 150} (CV MAE 1.880)
- test 2008-2012, Marcel-style weighted PER (tuned): {'ballast_mp': 2000} (CV MAE 2.067)
- test 2008-2012, ridge (tuned): {'alpha': 10.0} (CV MAE 1.946)
- test 2008-2012, hist gradient boosting (tuned): {'learning_rate': 0.03, 'max_leaf_nodes': 7, 'min_samples_leaf': 100, 'max_iter': 500} (CV MAE 1.890)
- test 2008-2012, selected by CV (hist gradient boosting): {'learning_rate': 0.03, 'max_leaf_nodes': 7, 'min_samples_leaf': 100, 'max_iter': 500} (CV MAE 1.890)
- test 2013-2017, Marcel-style weighted PER (tuned): {'ballast_mp': 2000} (CV MAE 2.057)
- test 2013-2017, ridge (tuned): {'alpha': 100.0} (CV MAE 1.947)
- test 2013-2017, hist gradient boosting (tuned): {'learning_rate': 0.1, 'max_leaf_nodes': 7, 'min_samples_leaf': 100, 'max_iter': 150} (CV MAE 1.887)
- test 2013-2017, selected by CV (hist gradient boosting): {'learning_rate': 0.1, 'max_leaf_nodes': 7, 'min_samples_leaf': 100, 'max_iter': 150} (CV MAE 1.887)

Gradient boosting across seeds [0, 1, 2, 3, 4] (table rows use the first seed):

- test 2003-2007: MAE 1.910–1.920 (sd 0.004); minus Marcel -0.156 to -0.146
- test 2008-2012: MAE 1.878–1.886 (sd 0.003); minus Marcel -0.165 to -0.158
- test 2013-2017: MAE 1.914–1.927 (sd 0.004); minus Marcel -0.140 to -0.127

Notes:
- sample: 1980-2017 after dropna
- rows_from_traded_player_seasons: 3537
- features: per-36 box-score counts + season
- eval_filter: player logged >= 500 MP in target season

data: kaggle drgilermo/nba-players-stats v2 (sha256 04876c15d43b…); seed=1, python 3.12.15, scikit-learn 1.9.1
