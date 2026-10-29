"""q.py done ISSUE START TOKENS | run ISSUE START | next N  -- job queue helper"""
import json, sys
F = '/tmp/claude-0/-home-claude/7418dbbe-23b1-5767-91a3-214502410ce0/scratchpad/bv/queue.json'
q = json.load(open(F)); a = sys.argv[1:]
def find(i, s): return next(j for j in q if j['issue'] == int(i) and j['pages'][0] == int(s))
if a[0] == 'done':
    j = find(a[1], a[2]); j['status'] = 'done'; j['tokens'] = int(a[3])
elif a[0] == 'run':
    find(a[1], a[2])['status'] = 'running'
elif a[0] == 'next':
    busy = {j['issue'] for j in q if j['status'] == 'running'}; out = []
    for j in q:
        if j['status'] == 'todo' and j['issue'] not in busy and j['issue'] not in {o['issue'] for o in out}:
            out.append(j)
    for j in out[:int(a[1])]:
        print(j['issue'], j['label'], f"{j['pages'][0]}-{j['pages'][1]}", 'HEAVY' if j['heavy'] else 'normal')
json.dump(q, open(F, 'w'), indent=0)
done = [j for j in q if j['status'] == 'done']
print(f"done {len(done)}/{len(q)} jobs, {sum(j.get('tokens',0) for j in done)/1e6:.2f}M tokens", file=sys.stderr)
