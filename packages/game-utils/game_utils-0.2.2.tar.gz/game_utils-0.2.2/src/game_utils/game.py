from abc import abstractmethod
from collections.abc import Callable
import pygame
import logging
from .sprites import GameSprite

logger = logging.getLogger(__name__)

ColorType = str | tuple[int, int, int] | pygame.Color


class Game:
    """Game class defines high-level game logic. This class includes a run method, which controls the game loop.
    User is required to implement abstract methods _update(), which is invoked within run()
    """

    class ScreenSettings:
        """defines information needed to udpate the screen"""

        def __init__(
            self,
            *,
            width: float = 0.0,
            height: float = 0.0,
            frames_per_second: int = 60,
            bg_color: ColorType | None = None,
            bg_image: pygame.Surface | None = None,
            no_screen: bool = False,
        ):
            self.bg_image = bg_image
            self.bg_color = bg_color
            self.frames_per_second = frames_per_second
            self.width = width
            self.height = height
            self.no_screen = no_screen

            if not self.no_screen:
                self.activate_screen()

        def activate_screen(self):
            self.no_screen = False
            if self.width == 0.0 and self.height == 0.0:
                self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                self.width = self.screen.get_width()
                self.height = self.screen.get_height()
            else:
                self.screen = pygame.display.set_mode((self.width, self.height))

        def resize_screen(self, width: float = 0.0, height: float = 0.0):
            """resizes to fullscreen by default"""
            self.width = width
            self.height = height
            self.activate_screen()

    def __init__(self, screen_settings: ScreenSettings):
        """Invokes pygame.init()

        Args:
            screen_settings (ScreenSettings): Any screen settings
        """
        pygame.init()
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.running = False
        self.screen_settings = screen_settings

    def run(self, *event_handlers: Callable[[pygame.event.Event], None]):
        """Runs and maintains the game loop and clock. Updates the screen and invokes any handlers
        Invokes pygame.quit() when pygame.QUIT event is reached
        """
        logger.debug("starting game...")
        self.running = True
        while self.running:
            self.dt = self._get_delta_time()
            self._update()
            if not self.screen_settings.no_screen:
                self._update_screen()
                pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                for handler in event_handlers:
                    handler(event)
        pygame.quit()

    def _get_delta_time(self) -> float:
        return self.clock.tick(self.screen_settings.frames_per_second) / 1000

    def _update_screen(self):
        pass

    @abstractmethod
    def _update(self):
        raise NotImplementedError()


class SpriteGame(Game):

    def __init__(
        self,
        screen_settings: Game.ScreenSettings,
        player_sprite: GameSprite | None = None,
        *other_sprites: GameSprite,
    ):
        """Create new instance of SpriteGame object.  Invokes pygame.init().  Must
        implement _update_sprites()

        Args:
            settings (Settings): Information needed to update the screen
            player_sprite (GameSprite): The sprite to be used for the player
            *other_sprites (GameSprite): Any other sprites needed for the game
        """
        super().__init__(screen_settings=screen_settings)
        self.player_sprite = player_sprite
        self.other_sprites = other_sprites
        self.other_sprites_group = pygame.sprite.Group()
        for sprite in other_sprites:
            self.other_sprites_group.add(sprite)

    @abstractmethod
    def _update_sprites(self):
        """Defines behavior for all GameSprite objects over time

        Args:
            dt (float): change in time
        """
        raise NotImplementedError
