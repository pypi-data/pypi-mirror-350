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
@click.option("--mode", "-m", default="")
@click.option("--game", "-g", default=None)
@click.option("--path", "-p", default=None)
def package(mode: str, game: str | None, path: str | None):
    {
        "batocera": package_for_batocera,
    }.get(
        mode, default_package
    )(game, path)


def default_package(
    game: str | None = None, path: str | None = None, game_file: str | None = None
):
    path = path or os.getcwd()
    game_file = game_file or _get_game_file(
        path=path, entry_point=game, allow_none=False
    )
    game_path = os.path.join(path, game_file)
    print(f"game file path: {game_path}")
    game_name = game or os.path.dirname(game_path)
    zip_package = f"{game_name}.zip"
    with zipfile.ZipFile(os.path.join(path, zip_package), "w") as zip_file:
        for f in os.listdir(path):
            arcpath = os.path.relpath(path)
            zip_file.write(os.path.join(arcpath, f))


def package_for_batocera(
    game: str | None = None,
    path: str | None = None,
    allow_none: bool = True,
):
    MODULE_IMPORT = "game_utils-main"
    UTILS_URL = "https://gitlab.com/madmadam/games/game_utils/-/archive/main/game_utils-main.zip"
    MODULE_OUTPUT_FILE = "game_utils.zip"

    path = path or os.getcwd()
    zip_export_path = os.path.join(path, MODULE_OUTPUT_FILE)
    game_file = _get_game_file(entry_point=game, path=path, allow_none=allow_none)

    if game_file is None:
        print(f"unable to package game")
        return

    print(f"packaging game {game_file} for batocera pygame port")
    # download the game_utils package
    subprocess.run(
        ["wget", UTILS_URL, "-qO", zip_export_path],
        check=True,
    )

    # extract the download, and copy the module package here
    with zipfile.ZipFile(zip_export_path, "r") as zip_file:
        zip_file.extractall(path)
    shutil.move(src=os.path.join(path, MODULE_IMPORT, "src", "game_utils"), dst=path)

    # create a .pygame copy of the main file
    game_name = game_file.rstrip(".py")
    shutil.copy(
        src=os.path.join(path, game_file), dst=os.path.join(path, f"{game_name}.pygame")
    )

    # delete job files
    os.remove(zip_export_path)
    shutil.rmtree(os.path.join(path, MODULE_IMPORT))

    # package the game
    default_package(game, path, game_file)

    # remove generated files
    shutil.rmtree(os.path.join(path, "game_utils"))
    os.remove(os.path.join(path, f"{game_name}.pygame"))


def _get_game_file(
    *, path: str, entry_point: str | None, allow_none: bool = True
) -> str | None:
    games = _get_py_files(path)
    print(f"game files: {games}")

    if len(games) == 0:
        print(f"no games found in {path}")
        return None
    else:
        game_dir = os.path.dirname(games[0])

        for g in games:
            if (
                (entry_point is not None and g == f"{entry_point}.py")
                or g == f"{game_dir}.py"
                or g == "main.py"
            ):
                return g
    return None if allow_none else games[-1]


def _get_py_files(path):
    return [f for f in os.listdir(path) if f.endswith(".py")]


if __name__ == "__main__":
    main()
