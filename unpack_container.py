import argparse
import json
import os.path as op

from mechbay.container import class_map


def main():
    parser = argparse.ArgumentParser(description="Unpack container")
    parser.add_argument("container", type=str, help="Container", choices=class_map.keys())
    parser.add_argument("--path", type=str, help="Root data directory", default=".")
    parser.add_argument("--output", type=str, help="Output directory", default=".")
    args = parser.parse_args()

    container = class_map[args.container](args.path, args.output)
    data = container.read()
    file = f"container_{container}.json"
    json.dump(data, open(op.join(args.output, file), "wt"))


if __name__ == "__main__":
    main()
