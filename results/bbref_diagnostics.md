# Diagnostics: next-season PER backtest (bbref)

## Noise ceiling

Year-to-year PER change variance vs harmonic minutes (age-demeaned, 20 quantile bins, WLS):

| min MP per season | robust variance | pairs | k | Var(true change) | noise SD at 1,000 MP |
|---|---|---|---|---|---|
| 100 | no | 14288 | 2330.5 | 2.943 | 1.527 |
| 100 | yes | 14288 | 2088.8 | 2.956 | 1.445 |
| 250 | no | 13007 | 2431.1 | 2.713 | 1.559 |
| 250 | yes | 13007 | 2007.0 | 3.023 | 1.417 |
| 500 | no | 11276 | 2522.2 | 2.57 | 1.588 |
| 500 | yes | 11276 | 2457.4 | 2.346 | 1.568 |

Main fit: min MP 250, plain variance (k = 2431.1).

- Oracle noise floor (knows true next-season talent exactly): MAE **1.054** (range across fits 0.958–1.074)
- Static-talent oracle (knows current true talent + average aging, nothing else): MAE 1.696
- Selected model: MAE **1.88**; Marcel: 2.022
- Measurement noise is 32% of the selected model's MSE (1.848 of 5.781)

Normal approximation throughout; PER errors are heavier-tailed, so MAE floors are rough.

## Error breakdown

Δ = selected-model MAE minus Marcel MAE (negative = better), player-cluster 95% CI. 'earlier' / 'latest' split Δ into windows before 2022-2026 and 2022-2026.
Groups use target-season information (minutes, team), so they diagnose errors; they are not forecast-time features.

### minutes in target season

| group | n | noise floor | Marcel | ridge | GBM | selected | Δ (95% CI) | Δ earlier | Δ latest |
|---|---|---|---|---|---|---|---|---|---|
| 500-999 | 1397 | 1.449 | 2.494 | 2.327 | 2.248 | 2.248 | -0.246 (-0.308 to -0.189) | -0.239 (n=982) | -0.264 (n=415) |
| 1000-1499 | 1409 | 1.117 | 1.966 | 1.942 | 1.867 | 1.867 | -0.099 (-0.154 to -0.042) | -0.133 (n=1013) | -0.012 (n=396) |
| 1500-1999 | 1452 | 0.943 | 1.792 | 1.735 | 1.706 | 1.706 | -0.086 (-0.138 to -0.036) | -0.067 (n=1056) | -0.137 (n=396) |
| 2000+ | 1926 | 0.806 | 1.896 | 1.809 | 1.753 | 1.753 | -0.143 (-0.197 to -0.097) | -0.142 (n=1490) | -0.148 (n=436) |

### age in target season

| group | n | noise floor | Marcel | ridge | GBM | selected | Δ (95% CI) | Δ earlier | Δ latest |
|---|---|---|---|---|---|---|---|---|---|
| <=21 | 397 | 1.053 | 2.263 | 2.234 | 2.020 | 2.020 | -0.242 (-0.364 to -0.133) | -0.252 (n=267) | -0.222 (n=130) |
| 22-24 | 1525 | 1.058 | 2.064 | 2.003 | 1.897 | 1.897 | -0.167 (-0.224 to -0.112) | -0.162 (n=1074) | -0.178 (n=451) |
| 25-28 | 2218 | 1.040 | 1.898 | 1.945 | 1.900 | 1.900 | +0.003 (-0.031 to +0.036) | +0.013 (n=1658) | -0.027 (n=560) |
| 29-32 | 1414 | 1.059 | 2.033 | 1.885 | 1.867 | 1.867 | -0.166 (-0.232 to -0.098) | -0.175 (n=1077) | -0.138 (n=337) |
| 33+ | 630 | 1.085 | 2.185 | 1.701 | 1.704 | 1.704 | -0.482 (-0.599 to -0.369) | -0.520 (n=465) | -0.375 (n=165) |

### prior NBA seasons

| group | n | noise floor | Marcel | ridge | GBM | selected | Δ (95% CI) | Δ earlier | Δ latest |
|---|---|---|---|---|---|---|---|---|---|
| 1 (second-year player) | 788 | 1.123 | 2.087 | 2.130 | 1.982 | 1.982 | -0.105 (-0.175 to -0.027) | -0.075 (n=580) | -0.190 (n=208) |
| 2-3 | 1486 | 1.071 | 2.023 | 1.963 | 1.862 | 1.862 | -0.161 (-0.219 to -0.105) | -0.150 (n=1076) | -0.188 (n=410) |
| 4+ | 3910 | 1.034 | 2.009 | 1.892 | 1.866 | 1.866 | -0.144 (-0.177 to -0.109) | -0.155 (n=2885) | -0.113 (n=1025) |

### team change (t to t+1)

| group | n | noise floor | Marcel | ridge | GBM | selected | Δ (95% CI) | Δ earlier | Δ latest |
|---|---|---|---|---|---|---|---|---|---|
| changed team in offseason | 1134 | 1.101 | 2.161 | 2.056 | 2.020 | 2.020 | -0.141 (-0.208 to -0.074) | -0.139 (n=912) | -0.153 (n=222) |
| same team | 3704 | 1.009 | 1.974 | 1.911 | 1.843 | 1.843 | -0.131 (-0.164 to -0.096) | -0.124 (n=2683) | -0.148 (n=1021) |
| traded mid-season (t or t+1) | 1346 | 1.138 | 2.039 | 1.918 | 1.862 | 1.862 | -0.177 (-0.231 to -0.127) | -0.203 (n=946) | -0.118 (n=400) |

### minutes change (MP t+1 / MP t)

| group | n | noise floor | Marcel | ridge | GBM | selected | Δ (95% CI) | Δ earlier | Δ latest |
|---|---|---|---|---|---|---|---|---|---|
| fell (<0.67x) | 945 | 1.329 | 2.507 | 2.307 | 2.196 | 2.196 | -0.312 (-0.385 to -0.240) | -0.323 (n=715) | -0.276 (n=230) |
| stable | 3901 | 0.979 | 1.883 | 1.788 | 1.747 | 1.747 | -0.136 (-0.170 to -0.102) | -0.133 (n=2878) | -0.147 (n=1023) |
| rose (>1.5x) | 1338 | 1.080 | 2.087 | 2.120 | 2.044 | 2.044 | -0.043 (-0.115 to +0.023) | -0.041 (n=948) | -0.047 (n=390) |

### test window

| group | n | noise floor | Marcel | ridge | GBM | selected | Δ (95% CI) | Δ earlier | Δ latest |
|---|---|---|---|---|---|---|---|---|---|
| 2007-2011 | 1450 | 1.008 | 2.024 | 1.915 | 1.874 | 1.874 | -0.150 (-0.207 to -0.097) | – | – |
| 2012-2016 | 1531 | 1.053 | 2.087 | 1.972 | 1.923 | 1.923 | -0.164 (-0.222 to -0.112) | – | – |
| 2017-2021 | 1560 | 1.072 | 2.075 | 2.050 | 1.959 | 1.959 | -0.116 (-0.178 to -0.056) | – | – |
| 2022-2026 | 1643 | 1.079 | 1.911 | 1.825 | 1.769 | 1.769 | -0.141 (-0.199 to -0.090) | – | – |
