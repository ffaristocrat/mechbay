import argparse
import glob
import os

from mechbay import StringTBL


def main():
    parser = argparse.ArgumentParser(description="Unpack all string TBL files")
    parser.add_argument(
        "tbl", type=str, help="Files to unpack"
    )
    parser.add_argument(
        "--path", type=str, help="Root directory to search from", default="."
    )
    args = parser.parse_args()
    search_path = os.path.join(args.path, "**", args.tbl)
    print(search_path)
    paths = glob.glob(search_path, recursive=True)
    for pkd_filename in paths:
        print(pkd_filename)
        try:
            StringTBL().dump(pkd_filename)
        except ValueError:
            continue


if __name__ == "__main__":
    main()
