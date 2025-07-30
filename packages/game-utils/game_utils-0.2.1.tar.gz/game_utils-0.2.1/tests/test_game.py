from src.game_utils.game import Game
import pygame.event
from pygame.locals import K_ESCAPE, QUIT, USEREVENT
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

TESTEVENT = USEREVENT


class MockGame(Game):
    def __init__(self):
        super().__init__(
            Game.ScreenSettings(width=600, height=400, bg_color="cyan", no_screen=True)
        )

        self.state = 0.0

    def _update(self):
        self.state += 1
        if self.state == 1:
            pygame.event.post(pygame.event.Event(TESTEVENT))
        if self.state == 3:
            self.running = False


def _event_handler(event: pygame.event.Event):
    if event.type == TESTEVENT:
        logger.warning("test event activated")
        pygame.event.post(pygame.event.Event(pygame.QUIT))


def test_run():
    tg = MockGame()

    assert tg.screen_settings.width == 600
    assert tg.screen_settings.bg_color is not None
    assert tg.state == 0

    tg.run()

    assert tg.state == 3


def test_run_with_handler():
    tg = MockGame()
    tg.run(_event_handler)

    assert tg.state == 2
