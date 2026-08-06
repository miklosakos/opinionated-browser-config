import argparse, json

def main():
    parser = argparse.ArgumentParser(description="genpol.py - a helper script to generate opinionated browser configs")
    parser.add_argument("-os", "--system", required=True, type=str, help="set os to mac/linux")
    parser.add_argument("-p", "--browser", required=True, type=str, help="set browser to chrome/firefox")
    parser.add_argument("-hp", "--homepage", type=str, help="set homepage url")
    parser.add_argument("-b", "--bookmarks", type=str, help="use /path/to/bookmarks_file to import managed bookmarks")
    parser.add_argument("-u", "--ublock", action="store_true", help="Deploy uBlock")
    args = parser.parse_args()

if __name__ == "__main__":
    main()