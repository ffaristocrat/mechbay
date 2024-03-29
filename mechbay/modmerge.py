import os
import subprocess
from glob import glob


def mod_merge(game_path: str, mod_path: str, exe: str = "togg.exe"):
    print(game_path, mod_path)

    # first get all files in mod
    mod_glob = glob(os.path.join(mod_path, "**"), recursive=True)
    mod_files = [
        f.replace(mod_path + os.sep, "") for f in mod_glob if os.path.isfile(f)
    ]

    clean_up(game_path, mod_files)

    make_directories(game_path, mod_path, mod_glob)
    make_links(game_path, mod_path, mod_files)

    # launch ggcr
    current_directory = os.getcwd()
    os.chdir(os.path.join(game_path, ".."))
    command = exe
    subprocess.run(command)
    os.chdir(current_directory)

    clean_up(game_path, mod_files)


def make_links(game_path: str, mod_path: str, mod_files: list[str]):
    for file in mod_files:
        game_file = os.path.join(game_path, file)
        mod_file = os.path.join(mod_path, file)

        # if the file is already there and exists
        if os.path.isfile(game_file) and not os.path.islink(game_file):
            # rename it
            directory, filename = os.path.split(game_file)
            renamed_file = os.path.join(directory, "__" + filename)
            print(f"Renaming {game_file} to {renamed_file}")
            os.rename(game_file, renamed_file)

        # create a symlink to the mod version
        print(f"Linking {mod_file} to {game_file}")
        os.symlink(os.path.abspath(mod_file), game_file)


def make_directories(game_path: str, mod_path: str, mod_glob: list[str]):
    directories = {os.path.split(f)[0].replace(mod_path + os.sep, "") for f in mod_glob}
    for directory in directories:
        if directory == mod_path:
            continue

        game_dir = os.path.join(game_path, directory)
        if not os.path.isdir(game_dir) and not os.path.isfile(game_dir):
            print(f"Creating {directory}")
            os.makedirs(game_dir, exist_ok=True)


def clean_up(game_path: str, mod_files: list[str]):
    # clean up all the symlinks
    for file in mod_files:
        game_file = os.path.join(game_path, file)

        if os.path.islink(game_file):
            print(f"Unlinking {game_file}")
            os.remove(game_file)

        # Find renamed versions
        directory, filename = os.path.split(game_file)
        renamed_file = os.path.join(directory, "__" + filename)

        if os.path.isfile(renamed_file) and not os.path.isfile(game_file):
            print(f"Renaming {renamed_file} back to {game_file}")
            os.rename(renamed_file, game_file)
