import argparse
import glob
import os

from mechbay import PKDArchive


def main():
    parser = argparse.ArgumentParser(description="Unpack all PKD files")
    parser.add_argument(
        "pkd", type=str, help="Files to unpack"
    )
    parser.add_argument(
        "--path", type=str, help="Root directory to search from", default="."
    )
    args = parser.parse_args()
    search_path = os.path.join(args.path, "**", args.pkd)
    print(search_path)
    paths = glob.glob(search_path, recursive=True)
    for pkd_filename in paths:
        print(pkd_filename)
        path, _, filename = pkd_filename.rpartition("/")
        records = PKDArchive().read_file(pkd_filename)
        for record in records:
            output_path = os.path.join(path, record["filename"])
            with open(output_path, "wb") as f:
                f.write(record["bytes"])


if __name__ == "__main__":
    main()
