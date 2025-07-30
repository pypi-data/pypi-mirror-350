import shutil
import os
import src.game_utils.toolkit as toolkit

TEST_PATH = os.path.dirname(os.path.abspath(__file__))
TEST_GAME_PATH = os.path.join(TEST_PATH, "test_game")


def test_batocera_package_path():
    def _clear():
        os.remove(os.path.join(TEST_GAME_PATH, "testgame.zip"))

    lib_path = os.path.join(TEST_GAME_PATH, "game_utils")
    if os.path.exists(lib_path):
        _clear()

    assert os.path.exists(TEST_GAME_PATH)
    assert os.path.exists(os.path.join(TEST_GAME_PATH, "testgame.py"))

    toolkit.package_for_batocera("testgame", TEST_GAME_PATH)

    assert os.path.exists(os.path.join(TEST_GAME_PATH, "testgame.zip"))

    _clear()


def test_default_package():
    def _clear():
        os.remove(os.path.join(TEST_GAME_PATH, "testgame.zip"))

    if os.path.exists(os.path.join(TEST_GAME_PATH, "testgame.zip")):
        _clear()

    toolkit.default_package("testgame", TEST_GAME_PATH)
    assert os.path.exists(os.path.join(TEST_GAME_PATH, "testgame.zip"))

    _clear()
