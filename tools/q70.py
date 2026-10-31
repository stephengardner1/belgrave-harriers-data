"""1970s queue.  q70.py init | next N | run KIND ISSUE START | done KIND ISSUE START TOKENS | stat
Read jobs of an issue run in page order, one at a time; its check jobs start only once the issue is read and
renumbered (status 'ready' set by finalize70.py)."""
import json, sys, os, subprocess, math
B = '/tmp/claude-0/-home-claude/7418dbbe-23b1-5767-91a3-214502410ce0/scratchpad/bv'
F = f'{B}/queue70.json'
a = sys.argv[1:]
if a[0] == 'init':
    q = {'issues': {}, 'jobs': []}
    for line in open(f'{B}/list70.txt'):
        no, yr = line.split()[:2]
        pdf = f'B{no}_{yr}.pdf'
        n = int(subprocess.run(['pdfinfo', f'{B}/pdf/{pdf}'], capture_output=True, text=True).stdout.split('Pages:')[1].split()[0])
        k = math.ceil(n / 10); size = math.ceil(n / k)
        q['issues'][no] = {'pdf': pdf, 'pages': n, 'state': 'reading'}
        for kind in ('read', 'check'):
            for s in range(1, n + 1, size):
                q['jobs'].append({'kind': kind, 'issue': int(no), 'pages': [s, min(n, s + size - 1)], 'status': 'todo'})
    q['jobs'].sort(key=lambda j: j['issue'])
    json.dump(q, open(F, 'w'), indent=0); print(len(q['jobs']), 'jobs'); sys.exit()
q = json.load(open(F))
def find(k, i, s): return next(j for j in q['jobs'] if j['kind'] == k and j['issue'] == int(i) and j['pages'][0] == int(s))
if a[0] == 'run':
    find(a[1], a[2], a[3])['status'] = 'running'
elif a[0] == 'done':
    j = find(a[1], a[2], a[3]); j['status'] = 'done'; j['tokens'] = int(a[4])
elif a[0] == 'next':
    busy = {j['issue'] for j in q['jobs'] if j['status'] == 'running'}; out = []
    for j in q['jobs']:
        if j['status'] != 'todo' or j['issue'] in busy or j['issue'] in {o['issue'] for o in out}: continue
        st = q['issues'][str(j['issue'])]['state']
        if j['kind'] == 'read':
            prev = [x for x in q['jobs'] if x['kind'] == 'read' and x['issue'] == j['issue'] and x['pages'][0] < j['pages'][0]]
            if all(x['status'] == 'done' for x in prev): out.append(j)
        elif st == 'ready':
            out.append(j)
    for j in out[:int(a[1])]:
        print(j['kind'], j['issue'], q['issues'][str(j['issue'])]['pdf'], f"{j['pages'][0]}-{j['pages'][1]}")
json.dump(q, open(F, 'w'), indent=0)
done = [j for j in q['jobs'] if j['status'] == 'done']
t = sum(j.get('tokens', 0) for j in done)
print(f"done {len(done)}/{len(q['jobs'])} jobs, {t/1e6:.2f}M tokens ≈ {t/1.33e6:.1f} weekly points (calibrated: 27%→43% = 21.3M tokens, 29 Oct 10:15); cap 70%: stop starting issues at 53M", file=sys.stderr)
