"""Search suggestions for the Belgravian reader: the races and competitions printed most often.

Reads belgravian/issues/*.json (read only) and writes belgravian/suggest.json:
  {"events": [["National Cross Country Championships", 281], ...]}
Counts are items that carry the event tag. Names that differ only in capitals are counted together under
their most common printed form. People are not listed here: the reader already has people.json.
Run after the archive is rebuilt:  python3 tools/belgravian/build_suggest.py
"""
import collections, glob, json, os
ROOT = os.path.join(os.path.dirname(__file__), '..', '..', 'belgravian')
forms, totals = collections.defaultdict(collections.Counter), collections.Counter()
for f in glob.glob(os.path.join(ROOT, 'issues', 'B*.json')):
    for it in json.load(open(f, encoding='utf-8')).get('items', []):
        for e in set((x or '').strip() for x in it.get('events') or []):
            if e:
                forms[e.lower()][e] += 1
                totals[e.lower()] += 1
events = [[forms[k].most_common(1)[0][0], n] for k, n in totals.most_common() if n >= 5]
json.dump({'events': events}, open(os.path.join(ROOT, 'suggest.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print(len(events), 'events written to belgravian/suggest.json')
