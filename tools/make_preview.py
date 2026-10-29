"""Wrap the site code block as a standalone page: belgravian/index.html on GitHub Pages."""
import sys
block = open(sys.argv[1]).read()
fonts = """@font-face{font-family:"Castoro Belgrave";src:url(../fonts/CastoroBelgrave-Semibold.woff2) format("woff2");font-weight:600;font-display:swap}
@font-face{font-family:"Castoro Belgrave";src:url(../fonts/CastoroBelgrave-Bold.woff2) format("woff2");font-weight:700;font-display:swap}
@font-face{font-family:"Castoro Belgrave Titling";src:url(../fonts/CastoroBelgraveTitlingLight-Regular.woff2) format("woff2");font-weight:300;font-display:swap}
body{margin:0;background:#fff}#bh-belgravian{padding:24px max(16px,env(safe-area-inset-right,0px)) 24px max(16px,env(safe-area-inset-left,0px))}"""
block = block.replace('/*BV_FONTS*/', fonts)
page = ('<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
        '<title>The Belgravian archive · Belgrave Harriers</title><meta name="robots" content="noindex"><script>window.BV_BASE="./";</script></head><body>'
        + block + '</body></html>')
open(sys.argv[2], 'w').write(page)
