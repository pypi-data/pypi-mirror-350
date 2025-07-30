from game_utils.game import Game
from pygame.event import Event
import pygame.key
from pygame.locals import K_ESCAPE, QUIT, USEREVENT
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

TESTEVENT = USEREVENT


class TestGame(Game):
    def __init__(self):
        super().__init__(
            Game.ScreenSettings(width=600, height=400, bg_color="cyan", no_screen=True)
        )

        self.state = 0.0

    def _update(self):
        self.state += 1
        if self.state == 1:
            pygame.event.post(Event(TESTEVENT))
        if self.state == 3:
            self.running = False


def _event_handler(event: Event):
    if event.type == TESTEVENT:
        logger.warning("test event activated")
        pygame.event.post(Event(pygame.QUIT))


def test_run():
    tg = TestGame()

    assert tg.screen_settings.width == 600
    assert tg.screen_settings.bg_color is not None
    assert tg.state == 0

    tg.run()

    assert tg.state == 3


def test_run_with_handler():
    tg = TestGame()
    tg.run(_event_handler)

    assert tg.state == 2
