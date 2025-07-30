import subprocess


def test_batocera_package():
    subprocess.run(
        [
            "python",
            "-m",
            "game_utils.tooling",
            "package",
            "batocera",
            "testgame",
            "test_game",
        ]
    )
