#!/usr/bin/env python3

import click
import os
import subprocess
import zipfile
import shutil


@click.group()
def main():
    """CLI tooling for game-utils module"""
    pass


@main.command()
@click.argument("mode")
@click.option("--game", "-g", default=None)
@click.option("--path", "-p", default=None)
def package(mode: str, game: str | None, path: str | None):
    modes = {
        "batocera": _package_for_batocera,
    }

    fn = modes.get(mode)

    if fn is None:
        print(f"no packaging available for {mode}")
    else:
        fn(game, path)


def _package_for_batocera(game: str | None, path: str | None):
    UTILS_URL = "https://gitlab.com/madmadam/games/game_utils/-/archive/master/game_utils-master.zip"
    MODULE_OUTPUT_FILE = "game_utils.zip"

    path = path or os.getcwd()
    output_file_path = os.path.join(path, MODULE_OUTPUT_FILE)
    game_file = _get_game_file(entry_point=game, path=path)

    if game_file is None:
        print(f"unable to package {game}")
        return

    print(f"packaging game {game_file} for batocera pygame port")
    # download the game_utils package
    subprocess.run(
        ["wget", UTILS_URL, "-qO", output_file_path],
        check=True,
    )

    # extract the download, and copy the module package here
    with zipfile.ZipFile(output_file_path, "r") as zip_file:
        zip_file.extractall(path)
    shutil.move(
        src=os.path.join(path, "game_utils-master", "src", "game_utils"), dst=path
    )

    # create a .pygame copy of the main file
    game_name = game_file.rstrip(".py")
    shutil.copy(
        src=os.path.join(path, game_file), dst=os.path.join(path, f"{game_name}.pygame")
    )

    # delete job files
    os.remove(output_file_path)
    shutil.rmtree(os.path.join(path, "game_utils-master"))


def _get_game_file(path: str, entry_point: str | None) -> str | None:
    games = [f for f in os.listdir(path) if f.endswith(".py")]
    if len(games) == 0:
        print(f"no games found in {path}")
        return None
    else:
        game_dir = os.path.dirname(games[0])

        for g in games:
            if (
                entry_point is not None and g == f"{entry_point}.py"
            ) or g == f"{game_dir}.py":
                return g
    return None


if __name__ == "__main__":
    main()
