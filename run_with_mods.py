import argparse
from mechbay.modmerge import mod_merge


def main():
    parser = argparse.ArgumentParser(description="Run with mods")
    parser.add_argument("game", type=str, help="Game directory with executable")
    parser.add_argument("mods", type=str, help="Mods directory")
    args = parser.parse_args()
    mod_merge(args.game, args.mods)


if __name__ == "__main__":
    main()
