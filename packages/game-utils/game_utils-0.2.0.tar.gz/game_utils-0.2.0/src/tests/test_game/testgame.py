import game_utils
import game_utils.game


if __name__ == "__main__":
    GAME = game_utils.game.Game(game_utils.game.Game.ScreenSettings(no_screen=True))
    count = 0

    def handler(event):
        if count == 5:
            GAME.running = False
        count += 1

    GAME.run(handler)

    print("goodbye")
