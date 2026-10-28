#!/bin/sh
# page.sh PDF PAGE OUTPREFIX [DPI]  -> renders one page to OUTPREFIX.png (default 110 dpi)
pdftoppm -r ${4:-110} -f $2 -l $2 -png -singlefile "$1" "$3"
