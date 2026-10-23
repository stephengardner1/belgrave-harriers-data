#!/usr/bin/env python3
"""
Belgrave Harriers archive harvester
-----------------------------------
Collects old pages from belgraveharriers.com and belgraveharriers.co.uk
as saved by the Internet Archive's Wayback Machine, so the lost news
stories (roughly 2000-2017) can be restored to the current site.

What it does, in plain English:
  1. Asks the Wayback Machine for a list of every page it ever saved
     from the two club domains, between FIRST_YEAR and LAST_YEAR.
  2. Keeps the most recent good copy of each page.
  3. Downloads those pages slowly and politely (one every few seconds),
     into a folder called "belgrave-archive" next to this script.
  4. Zips the folder up at the end, ready to attach to Claude.

If it stops for any reason, just run it again: it skips anything
already downloaded and carries on where it left off.

Only uses tools built into Python, so nothing needs installing.
"""

import csv
import hashlib
import http.client
import json
import os
import re
import shutil
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

# ---------------------------------------------------------------
# Settings you can change
# ---------------------------------------------------------------
DOMAINS = ["belgraveharriers.com", "belgraveharriers.co.uk"]
FIRST_YEAR = 1999
LAST_YEAR = 2018          # roughly when the Squarespace site took over
SECONDS_BETWEEN_PAGES = 4 # be gentle with the Internet Archive

# Pages that are never stories (WordPress plumbing, feeds, logins etc.)
SKIP_PATTERNS = [
    r"/feed/?", r"/wp-login", r"/wp-admin", r"/wp-json", r"xmlrpc",
    r"/wp-content/", r"/wp-includes/", r"[?&]replytocom=", r"[?&]s=",
    r"/trackback/?$", r"/comment-page-", r"[?&]share=",
    r"\.(css|js|jpg|jpeg|gif|png|pdf|ico|xml|txt|zip|doc|docx|xls)$",
]
# ---------------------------------------------------------------

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "belgrave-archive")
PAGES = os.path.join(OUT, "pages")
INDEX_CSV = os.path.join(OUT, "archive_index.csv")
FAILED_TXT = os.path.join(OUT, "failed.txt")
CDX = "https://web.archive.org/cdx/search/cdx"
HEADERS = {"User-Agent": "BelgraveHarriersArchiveRestore/1.0 (club history recovery)"}


def fetch(url, tries=6):
    """Download a URL, waiting and retrying if the archive is busy.
    If a big page gets cut off partway, ask for just the missing part
    and stitch the pieces together, rather than starting again."""
    wait = 30
    got = b""
    for attempt in range(1, tries + 1):
        try:
            headers = dict(HEADERS)
            if got:
                headers["Range"] = f"bytes={len(got)}-"
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=90) as r:
                if got and r.status != 206:
                    got = b""  # archive ignored the request for the missing part
                return got + r.read()
        except http.client.IncompleteRead as e:
            if got and not e.partial:
                pass
            got += e.partial
            print(f"   big page cut off at {len(got):,} bytes - fetching the rest...")
            time.sleep(5)
            continue
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return got or None
            if e.code == 416 and got:
                return got  # nothing more to fetch
            reason = f"HTTP {e.code}"
        except urllib.error.URLError as e:
            if isinstance(getattr(e, "reason", None), ssl.SSLError):
                print("\nYour Mac's Python is missing its security certificates.")
                print("Fix: open Finder > Applications > Python 3.x and double-click")
                print("'Install Certificates.command', then run this script again.\n")
                sys.exit(1)
            reason = str(e.reason)
        except Exception as e:  # timeouts, dropped connections
            reason = str(e)
        if attempt < tries:
            print(f"   archive busy ({reason}) - waiting {wait}s and trying again...")
            time.sleep(wait)
            wait = min(wait * 2, 600)
    if got:
        print("   couldn't get the whole page - keeping the part we have")
        return got + b"\n<!-- PARTIAL: download incomplete -->\n"
    return None


def skip(url):
    return any(re.search(p, url, re.IGNORECASE) for p in SKIP_PATTERNS)


def page_key(url):
    """Treat www/non-www, http/https and trailing slashes as the same page."""
    p = urllib.parse.urlsplit(url)
    host = (p.hostname or "").lower()
    if host.startswith("www."):
        host = host[4:]
    path = p.path.rstrip("/") or "/"
    return host + path + (("?" + p.query) if p.query else "")


def list_captures():
    """Step 1: ask the Wayback Machine what it holds."""
    found = {}
    for domain in DOMAINS:
        print(f"Asking the Wayback Machine what it saved from {domain} ...")
        resume = None
        while True:
            params = [
                ("url", domain), ("matchType", "domain"), ("output", "json"),
                ("fl", "timestamp,original"),
                ("filter", "statuscode:200"), ("filter", "mimetype:text/html"),
                ("from", str(FIRST_YEAR)), ("to", str(LAST_YEAR)),
                ("collapse", "digest"), ("limit", "20000"),
                ("showResumeKey", "true"),
            ]
            if resume:
                params.append(("resumeKey", resume))
            data = fetch(CDX + "?" + urllib.parse.urlencode(params))
            if not data:
                print(f"   Couldn't get the list for {domain} this time.")
                break
            rows = json.loads(data.decode("utf-8") or "[]")
            resume = None
            for i, row in enumerate(rows):
                if i == 0 and row and row[0] == "timestamp":
                    continue  # header row
                if row == []:
                    # the next row (if any) holds the key for the next batch
                    if i + 1 < len(rows) and rows[i + 1]:
                        resume = rows[i + 1][0]
                    break
                ts, original = row[0], row[1]
                if skip(original):
                    continue
                k = page_key(original)
                entry = found.setdefault(k, {"first": ts, "latest": ts,
                                             "url": original, "copies": 0})
                entry["copies"] += 1
                if ts < entry["first"]:
                    entry["first"] = ts
                if ts >= entry["latest"]:
                    entry["latest"], entry["url"] = ts, original
            print(f"   ...{len(found)} different pages so far")
            if not resume:
                break
            time.sleep(SECONDS_BETWEEN_PAGES)
    return found


def filename_for(key):
    safe = re.sub(r"[^A-Za-z0-9]+", "_", key).strip("_")[:120]
    short = hashlib.md5(key.encode()).hexdigest()[:8]
    return f"{safe}__{short}.html"


def main():
    os.makedirs(PAGES, exist_ok=True)
    found = list_captures()
    if not found:
        print("Nothing found. Check your internet connection and try again.")
        return

    # Save the master list (useful even before any downloads finish)
    with open(INDEX_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["page", "original_url", "first_saved", "last_saved",
                    "times_saved", "file"])
        for k in sorted(found):
            e = found[k]
            w.writerow([k, e["url"], e["first"], e["latest"], e["copies"],
                        filename_for(k)])

    todo = [k for k in sorted(found)
            if not os.path.exists(os.path.join(PAGES, filename_for(k)))]
    hours = len(todo) * (SECONDS_BETWEEN_PAGES + 1.5) / 3600
    print()
    print(f"Found {len(found)} pages. {len(found) - len(todo)} already downloaded.")
    print(f"{len(todo)} to go - roughly {hours:.1f} hours. Leave it running.")
    input("Press Enter to start (or close this window to stop)... ")

    failed = []
    for n, k in enumerate(todo, 1):
        e = found[k]
        # 'id_' asks for the original page without the Wayback toolbar added
        url = f"https://web.archive.org/web/{e['latest']}id_/{e['url']}"
        data = fetch(url)
        if data:
            with open(os.path.join(PAGES, filename_for(k)), "wb") as f:
                f.write(data)
            print(f"[{n}/{len(todo)}] saved  {k}")
        else:
            failed.append(k)
            print(f"[{n}/{len(todo)}] FAILED {k}")
        time.sleep(SECONDS_BETWEEN_PAGES)

    if failed:
        with open(FAILED_TXT, "w", encoding="utf-8") as f:
            f.write("\n".join(failed))
        print(f"\n{len(failed)} pages failed - run the script again to retry them.")

    zip_path = shutil.make_archive(os.path.join(HERE, "belgrave-archive"), "zip", OUT)
    print("\nAll done.")
    print(f"Attach this file to Claude: {zip_path}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped. Run the script again any time to carry on.")
