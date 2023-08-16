import argparse
import glob
import os

from mechbay import PKDArchive


def main():
    parser = argparse.ArgumentParser(description="Unpack & Pack PKD archives")
    parser.add_argument("pkd", type=str, help="PKD archive name")
    parser.add_argument(
        "--path", type=str, help="Root directory to search from", default="."
    )
    args = parser.parse_args()
    search_path = os.path.join(args.path, "**", args.pkd)
    print(search_path)
    paths = glob.glob(search_path, recursive=True)

    for pkd_filename in paths:
        path, filename = os.path.split(pkd_filename)
        print(filename)
        archive = PKDArchive().read_file(pkd_filename)

        for filename, raw_bytes in archive.items():
            output_path = os.path.join(path, filename)

            with open(output_path, "wb") as f:
                print("*", filename)
                f.write(raw_bytes)


if __name__ == "__main__":
    main()
