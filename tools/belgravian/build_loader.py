"""Build site/belgravian.js from site/belgravian-block.html, so the club site needs only a two-line loader:
   <div id="bv-mount"></div><script src="https://stephengardner1.github.io/belgrave-harriers-data/site/belgravian.js"></script>
Fixes to the reader then reach the site without re-pasting anything in Squarespace."""
import json, re, sys
src = open('site/belgravian-block.html').read()
links = re.findall(r'<link[^>]+href="([^"]+)"[^>]*>', src)
css = re.search(r'<style>(.*?)</style>', src, re.S).group(1).replace('/*BV_FONTS*/', '')
html = re.search(r'(<div id="bh-belgravian".*?</div>)\s*<script>', src, re.S).group(1)
js = re.search(r'<script>(.*)</script>', src, re.S).group(1)
out = ('/* The Belgravian archive reader (Belgrave Harriers). Display only. Built from site/belgravian-block.html\n'
       '   by tools/belgravian/build_loader.py; loaded by the code block on belgraveharriers.com/belgravian. */\n'
       '(function(){\n'
       '  var m=document.getElementById("bv-mount");if(!m||m.dataset.done)return;m.dataset.done="1";\n'
       '  ' + json.dumps(links) + '.forEach(function(h){if(document.querySelector(\'link[href="\'+h+\'"]\'))return;var l=document.createElement("link");l.rel="stylesheet";l.href=h;document.head.appendChild(l)});\n'
       '  var st=document.createElement("style");st.textContent=' + json.dumps(css) + ';document.head.appendChild(st);\n'
       '  m.innerHTML=' + json.dumps(html) + ';\n'
       '})();\n' + js)
out = out.encode('ascii', 'backslashreplace').decode('ascii').replace('\\x', '\\u00')  # ASCII-only, so no character-set mix-ups
open('site/belgravian.js', 'w').write(out)
open('site/belgravian-loader.html', 'w').write(
    '<!-- The Belgravian archive (Belgrave Harriers). Display only. The reader and its data come from\n'
    '     github.com/stephengardner1/belgrave-harriers-data (site/belgravian.js, belgravian/). -->\n'
    '<div id="bv-mount"></div>\n'
    '<script src="https://stephengardner1.github.io/belgrave-harriers-data/site/belgravian.js"></script>\n')
print(len(out), 'bytes')
