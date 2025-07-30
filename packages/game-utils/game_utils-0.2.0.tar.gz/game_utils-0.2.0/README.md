# Game Utils

>0.2.0

## `game-utils` is a pygame engine.  The engine includes modules to facilitate boilerplate game operations. 

### Requirements

**Dependences:**
- pygame
- numpy

### Example usage

```python
from game_utils.game import Game
import pygame

class MyAwesomeGame(Game):
    def __init__(self, player_speed: int, screen_settings: Game.ScreenSettings):
        super().__init__(screen_settings)

        # Where, and how big, to draw the player.
        # I like to scale things by the screen size.
        self.player_radius = self.screen_settings.height / 4
        self.player_rect = pygame.Rect(
            self.screen_settings.height / 2 - self.player_radius,
            self.screen_settings.width / 2 - self.player_radius,
            self.player_radius * 2,
            self.player_radisu * 2,
        )
        self.player_speed = player_speed

    def _update_screen(self):
        self.screen_settings.screen.fill(
            self.screen_settings.bg_color or "dodgerblue2"
        )

        pygame.draw.circle(
            self.screen_settings.screen,
            "lightseagreen",
            self.player_rect.center,
            self.player_radius
        )

    def _update(self):
        # any other game logic...
        # This came from a tutorial I found on custom events...
        pressed_keys = pygame.key.get_pressed()
        up, down, left, right = map(
            lambda key: key * self.player_speed,
            [pressed_keys[key] for key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]] 
        )

        self.player_rect.move_ip((-left + right, -up + down))

if __name__ == "__main__":
    # these could also come from a config file
    game = MyAwesomeGame(
        player_speed=10,
        screen_settings=Game.ScreenSettings(
            bg_color="coral2",
            width=600,
            height=400
        )
    )

    print("Starting game...")
    game.run()
    print("Thanks for playing!")
```

### Tooling

These are tools for various packaging strategies for your game

```bash
python -m game_utils.tooling package batocera
```

---

## See Also...

<p><b>My ongoing game projects</b></p>

- Madmadam Games [gitlab](https://gitlab.com/madmadam/games)
