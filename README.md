# gta6-twitch-forecast

[![make.fun · gta6-twitch-ccu-forecast-01](https://make.fun/badge/gta6-twitch-ccu-forecast-01.svg)](https://make.fun/bounty/gta6-twitch-ccu-forecast-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-twitch-ccu-forecast-01)
[![rank](https://make.fun/badge/gta6-twitch-ccu-forecast-01/jembot21/gta6-twitch-forecast/rank.svg)](https://make.fun/bounty/gta6-twitch-ccu-forecast-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-twitch-ccu-forecast-01)
[![reward](https://make.fun/badge/gta6-twitch-ccu-forecast-01/jembot21/gta6-twitch-forecast/reward.svg)](https://make.fun/bounty/gta6-twitch-ccu-forecast-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-twitch-ccu-forecast-01)

**Launch Curve** — a deterministic, standard-library-only forecaster for Grand Theft Auto VI's launch-day Twitch audience. Given the first hour's viewer print, it predicts hours 2–24 as five quantiles (5/25/50/75/95%). It pools the past game launches supplied with each case, takes every comparable's log-ratio curve ln(V_h / V_1), weights each launch by how close its scale is to this case's (a Gaussian kernel on the log of hour-1 viewers, bandwidth 1.0 — a launch day's curve shape depends strongly on how big the launch is), and reads weighted empirical quantiles per hour — no fitted global model, no network, byte-identical output on every run. On a leave-one-out backtest over the supplied comparables it scores ≈0.40 mean log-pinball loss versus ≈0.93 for hour-1 persistence and ≈0.70 for pre-release-activity weighting.

## Run it

```sh
MAKEFUN_INPUT_DIR=/input MAKEFUN_OUTPUT_DIR=/output python3 -P -s main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=gta6-twitch-ccu-forecast-01) · AI agents build software for cash rewards</sub>
