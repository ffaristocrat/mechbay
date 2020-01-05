import argparse

from mechbay import PKDArchive


def main():
    parser = argparse.ArgumentParser(description="Pack all PKD files")
    parser.add_argument(
        "pkd", type=str, help="PKD output",
    )
    parser.add_argument(
        "files", type=str, help="Files to pack", nargs="+",
    )

    args = parser.parse_args()

    records = []
    for filename in args.files:
        with open(filename, "rb") as file:
            record = {
                "filename": filename,
                "bytes": file.read(),
            }
            records.append(record)

    with open(args.pkd, "wb") as file:
        file.write(PKDArchive().write(records))


if __name__ == "__main__":
    main()
