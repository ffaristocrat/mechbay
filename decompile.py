import argparse
import glob
import os
import subprocess


def main():
    parser = argparse.ArgumentParser(description="Decompile all Lua scripts")
    parser.add_argument("--game", type=str, help="Game directory", default="./ggcr")
    parser.add_argument(
        "--output", type=str, help="Output location", default="./scripts"
    )
    parser.add_argument(
        "--java",
        type=str,
        help="Java runtime",
        default="java",
    )
    parser.add_argument(
        "--decompile",
        type=str,
        help="Decompiler jar",
        default="./third_party/unluac/unluac.jar",
    )

    args = parser.parse_args()
    search_path = os.path.join(args.game, "**", "*.luac")
    print(search_path)
    paths = glob.glob(search_path, recursive=True)
    print(f"Creating {args.output}")
    os.makedirs(args.output, exist_ok=True)

    for script in paths:
        new_name = (
            os.path.relpath(script, args.game)
            .replace("./", "_")
            .replace("..", "_")
            .replace("/", "_")
            .replace("\\", "_")
            .replace(".luac", ".lua")
        )
        print(f"Decompiling {new_name}")
        output_name = os.path.join(args.output, new_name)
        try:
            subprocess.run(
                args=[args.java, "-jar", args.decompile, script],
                stdout=open(output_name, "wt"),
            )
        except Exception as E:
            print(E)


if __name__ == "__main__":
    main()
