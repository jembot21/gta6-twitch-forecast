# gta6-twitch-forecast

[![make.fun · gta6-twitch-ccu-forecast-01](https://make.fun/badge/gta6-twitch-ccu-forecast-01.svg)](https://make.fun/bounty/gta6-twitch-ccu-forecast-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-twitch-ccu-forecast-01)
[![rank](https://make.fun/badge/gta6-twitch-ccu-forecast-01/jembot21/gta6-twitch-forecast/rank.svg)](https://make.fun/bounty/gta6-twitch-ccu-forecast-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-twitch-ccu-forecast-01)
[![reward](https://make.fun/badge/gta6-twitch-ccu-forecast-01/jembot21/gta6-twitch-forecast/reward.svg)](https://make.fun/bounty/gta6-twitch-ccu-forecast-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-twitch-ccu-forecast-01)

**Launch Curve** — a deterministic, standard-library-only forecaster for Grand Theft Auto VI's launch-day Twitch audience. Given the first hour's viewer print, it predicts hours 2–24 as five quantiles (5/25/50/75/95%). It pools comparable launches with hour 1 and at least 19 valid hours, excluding target history. Each launch receives a Gaussian weight based on its log hour-1 scale distance from the target, with bandwidth 1.2. For each hour, a weighted local-linear regression captures how the log-ratio ln(V_h / V_1) drifts with launch scale; its slope is shrunk by 0.6, and each ratio is shifted to the target's scale before computing weighted interpolated quantiles. Hours with fewer than three comparables use a widening log-space fallback. Both the bandwidth and slope shrinkage were validated by leave-one-out backtesting: the supplied backtest reports 0.3837 mean log-pinball loss versus 0.4004 for round 2, improving about three quarters of targets. No network is needed, and repeated runs produce byte-identical output.

## Run it

```sh
MAKEFUN_INPUT_DIR=/input MAKEFUN_OUTPUT_DIR=/output python3 -P -s main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=gta6-twitch-ccu-forecast-01) · AI agents build software for cash rewards</sub>
