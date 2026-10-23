import sys, json, datetime, re, os
sys.path.insert(0, "/home/claude/tools")
from build import wxr, slugify
P = json.load(open("/home/claude/out/all_posts.json"))
for p in P:
    p["date"] = datetime.date.fromisoformat(p["date"])
# one set of unique web addresses across the whole archive
seen = set()
for p in sorted(P, key=lambda p: (p["date"], p["title"])):
    slug = slugify(p["title"])[:70].strip("-") or "story"
    if not re.search(r"(19|20)\d\d", slug):
        slug += f"-{p['date'].year}"
    s0, n = slug, 2
    while slug in seen:
        slug, n = f"{s0}-{n}", n + 1
    seen.add(slug); p["slug"] = slug; p["fixed_slug"] = True; p["id"] = 1000 + len(seen)
PERIODS = [(2000, 2003), (2004, 2006), (2007, 2010), (2011, 2013)]
os.makedirs("/home/claude/out/import", exist_ok=True)
for a, b in PERIODS:
    group = [p for p in P if a <= p["date"].year <= b]
    path = f"/home/claude/out/import/belgrave-archive-{a}-{b}.xml"
    wxr(group, path)
    print(os.path.basename(path), len(group), "posts", f"{os.path.getsize(path)/1e6:.1f} MB")
bylines = {p["slug"]: p["writer"] for p in P if p["writer"] and p["kind"] != "round-up"}
json.dump(dict(sorted(bylines.items())), open("/home/claude/out/bylines.json", "w"), indent=1, ensure_ascii=False)
json.dump([{**p, "date": p["date"].isoformat()} for p in P], open("/home/claude/out/all_posts.json", "w"), ensure_ascii=False)
print("bylines:", len(bylines), "| total:", len(P))
