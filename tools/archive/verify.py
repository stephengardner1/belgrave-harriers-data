import sys, re, glob, json, xml.etree.ElementTree as ET, collections
sys.path.insert(0, "/home/claude/tools")
from extract import index, load
from bs4 import BeautifulSoup
ix = index()
P = {p["slug"]: p for p in json.load(open("/home/claude/out/all_posts.json"))}
nows = lambda s: re.sub(r"\s+", "", s)
norm = lambda s: re.sub(r"\s+", " ", s).strip()
cache = {}
def orig(page):
    if page not in cache:
        s = BeautifulSoup(load(ix[page]), "html.parser")
        cache[page] = (nows(s.get_text("")), {nows(i.get("alt", "")) for i in s.find_all("img")}, " " + norm(s.get_text("")) + " " + norm(s.get_text(" ")) + " ")
    return cache[page]
problems = collections.Counter(); examples = []
total_items = total_paras = 0; slugs = set(); titles_empty = 0
for f in sorted(glob.glob("/home/claude/out/import/*.xml")):
    root = ET.parse(f).getroot()   # fails loudly if any file isn't valid XML
    for it in root.iter("item"):
        total_items += 1
        slug = it.find("{http://wordpress.org/export/1.2/}post_name").text
        assert slug not in slugs, slug; slugs.add(slug)
        title = it.find("title").text or ""
        if not title.strip(): titles_empty += 1
        p = P[slug]; text, alts, spaced = orig(p["page"])
        body = it.find("{http://purl.org/rss/1.0/modules/content/}encoded").text
        assert body.rstrip().endswith("as originally written.</em></p>"), slug
        for para in re.findall(r"<p>(.*?)</p>", body, re.S)[:-1]:
            total_paras += 1
            s = BeautifulSoup(para, "html.parser")
            if s.find("img"):
                c = nows(s.get_text(""))
                if c and c not in alts: problems["caption not in original"] += 1; examples.append((slug, c[:80]))
                continue
            t = nows(s.get_text(""))
            if t and t not in text:
                problems["paragraph not found verbatim"] += 1; examples.append((slug, t[:100]))
            # every word must exist as a word on the old page (catches words wrongly joined or split)
            spaced_post = BeautifulSoup(re.sub(r"(<br\s*/?>|</t[dh]>|</li>|</?p>|</?div>)", r" \1", para), "html.parser").get_text("")
            for w in norm(spaced_post).split(" "):
                if w and w not in spaced:
                    problems["word not on the old page"] += 1; examples.append((slug, w)); break
        for img in re.findall(r'<img src="([^"]+)"', body):
            if not img.startswith("https://stephengardner1.github.io/belgrave-harriers-data/archive/photos/"):
                problems["photo not on GitHub"] += 1
print(f"files OK | posts {total_items} | unique addresses {len(slugs)} | paragraphs checked {total_paras} | empty titles {titles_empty}")
print("problems:", dict(problems) or "none")
for e in examples[:15]: print("  ", e)
