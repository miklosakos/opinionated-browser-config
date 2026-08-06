import argparse, json, sys, plistlib
from genpol import firefox
from genpol import chrome
from genpol import chrome_mac
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="genpol.py - a helper script to generate opinionated browser configs")
    parser.add_argument("-os", "--system", required=True, type=str, help="set os to mac/linux")
    parser.add_argument("-p", "--browser", required=True, type=str, help="set browser to chrome/firefox")
    parser.add_argument("-hp", "--homepage", type=str, help="set homepage url")
    parser.add_argument("-b", "--bookmarks", type=str, help="use /path/to/bookmarks_file to import managed bookmarks")
    parser.add_argument("-u", "--ublock", action="store_true", help="Deploy uBlock")
    parser.add_argument("-s", "--search", type=str, help="Search engine URL")
    args = parser.parse_args()
    searchname, searchurl = None, None
    if args.search:
        if "," in args.search:
            searchname, searchurl = args.search.split(",", 1)
        else:
            print("Error: --search must be: 'Name,URL'")
            return
    
    if args.browser == "firefox":
        data = firefox.generate_policy(
            homepage = args.homepage,
            search = searchname,
            searchurl = searchurl+"{searchTerms}",
            bookmarks_file = args.bookmarks,
            ublock = args.ublock
        )
        filename = "firefox_policies.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    else:
        if args.system in ("macos", "osx", "mac"):
            plist_bytes = chrome_mac.generate_policy(
                homepage = args.homepage,
                search = searchname,
                searchurl = searchurl+"{searchTerms}",
                bookmarks_file=args.bookmarks,
                ublock=args.ublock
            )
            filename = "com.google.Chrome.plist"
            with open(filename, "wb") as f:
                f.write(plist_bytes)
            
        else:
            data = chrome.generate_policy(
                homepage = args.homepage,
                search = searchname,
                searchurl = searchurl+"{searchTerms}",
                bookmarks_file=args.bookmarks,
                ublock = args.ublock
            )
            filename = "chrome_policies.json"
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

if __name__ == "__main__":
    main()