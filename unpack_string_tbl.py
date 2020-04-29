import argparse
import glob
import os

from mechbay import StringTBL


def main():
    parser = argparse.ArgumentParser(description="Unpack all string TBL files")
    parser.add_argument("tbl", type=str, help="Files to unpack")
    parser.add_argument(
        "--path", type=str, help="Root directory to search from", default="."
    )
    args = parser.parse_args()

    search_path = os.path.join(args.path, "**", args.tbl)
    print(search_path)

    paths = glob.glob(search_path, recursive=True)

    for string_filename in paths:
        print(string_filename)
        try:
            StringTBL().dump(string_filename)
        except AssertionError:
            continue


if __name__ == "__main__":
    main()
