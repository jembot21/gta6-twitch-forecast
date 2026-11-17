"""Deterministic empirical release-day forecast, using only supplied observations."""
import json
import math
import os
from datetime import datetime

LEVELS = (.05, .25, .5, .75, .95)
SIMILARITY = 'history'
SPREAD = 1.0

def timestamp(s):
    return datetime.fromisoformat(s.replace('Z', '+00:00'))

def curve(comp):
    start = timestamp(comp['day_start'])
    result = {}
    for row in comp.get('hourly', []):
        h = int((timestamp(row['from']) - start).total_seconds() // 3600) + 1
        v = row.get('viewers', 0)
        if 1 <= h <= 24 and v is not None and v > 0:
            result[h] = float(v)
    return result

def quantile(pairs, level):
    pairs = sorted(pairs)
    total = sum(w for v, w in pairs)
    # Interpolate between weighted observation centers.
    centers = []
    cumulative = 0.0
    for v, w in pairs:
        centers.append(((cumulative + w / 2) / total, v))
        cumulative += w
    if level <= centers[0][0]:
        return centers[0][1]
    for (a, x), (b, y) in zip(centers, centers[1:]):
        if level <= b:
            return x + (y-x) * (level-a) / (b-a)
    return centers[-1][1]

def features(comp, rows):
    start = timestamp(comp['day_start'])
    before = [r['viewers'] for r in comp.get('hourly', [])
              if -24 <= (timestamp(r['from'])-start).total_seconds()/3600 < 0
              and r.get('viewers') is not None]
    # Pre-release activity relative to midnight distinguishes an already live
    # category from an upcoming single-time global unlock.
    return math.log((max(before, default=rows[1]) + 100) / (rows[1]+100))

def forecast(case, variant=None, spread=None):
    variant = SIMILARITY if variant is None else variant
    spread = SPREAD if spread is None else spread
    known = next(row for row in case['known'] if row['hour'] == 1)
    p1 = max(1.0, float(known['viewers']))
    target = {'day_start': case['day_start'], 'hourly': case.get('history_hourly') or []}
    target_feature = features(target, {1:p1})
    pool = []
    for comp in case.get('comparables') or []:
        rows = curve(comp)
        if rows.get(1) and len(rows) >= 19 and 'target-history' not in str(comp.get('unlock','')).lower():
            weight = 1.0
            if variant != 'initial':
                delta = features(comp, rows) - target_feature
                weight = .05 + math.exp(-.5 * (delta / .7)**2)
            pool.append((rows, weight))
    hours = []
    for h in range(2,25):
        pairs = [(math.log(rows[h]/rows[1]), w) for rows,w in pool if h in rows]
        if len(pairs) >= 3:
            logs = [quantile(pairs, t) for t in LEVELS]
            mid = logs[2]
            logs = [mid + spread*(v-mid) for v in logs]
        else:
            logs = [z*.2*math.sqrt(h-1) for z in (-1.645,-.674,0,.674,1.645)]
        qs = [min(1e9,max(1e-6,p1*math.exp(max(-30,min(30,v))))) for v in logs]
        hours.append({'hour':h,'q':qs})
    return {'hours':hours}

def main():
    indir = os.environ.get('MAKEFUN_INPUT_DIR','/input')
    outdir = os.environ.get('MAKEFUN_OUTPUT_DIR','/output')
    os.makedirs(outdir,exist_ok=True)
    for name in sorted(os.listdir(indir)):
        if name.endswith('.in'):
            with open(os.path.join(indir,name),encoding='utf-8') as f:
                case=json.load(f)
            result=forecast(case)
            with open(os.path.join(outdir,os.path.splitext(name)[0]+'.out'),'w',encoding='utf-8') as f:
                f.write(json.dumps(result,separators=(',',':'),allow_nan=False)+'\n')

if __name__=='__main__':
    main()
