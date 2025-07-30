from abc import abstractmethod
from typing import Any
from collections.abc import Callable
from pygame import Rect, Surface, Vector2
from pygame.sprite import Sprite

from .controller import Controller
from .physics import PhysicsBody


class GameSprite(Sprite):
    def __init__(
        self,
        image: Surface,
        position: Vector2,
        boundaries: Rect | None = None,
        id: int = 0,
    ):
        """Implement a Game Sprite object. Subclass must implement GameSprite.update

        Args:
            image (Surface): The image for the sprite
            position (Vector2): Where to put the sprite
            boundaries (Rect | None, optional): Optional boundary vectors for this sprite (xmax, xmin, ymax, ymin). Defaults to None.
        """
        super().__init__()
        self.image = image
        _, _, *dimensions = image.get_rect()
        self.rect = Rect(position.x, position.y, *dimensions)
        self.position = position
        self.boundaries = boundaries
        self.id = id

    @abstractmethod
    def update(self, *args: Any, **kwargs: Any):
        pass

    def _update_pos(
        self,
        position: Vector2 | None = None,
        xbounds: Callable[[], None] | None = None,
        ybounds: Callable[[], None] | None = None,
    ):
        """Updates position of this sprite. Maintains any given boundaries. Invokes callbacks given when boundaries are reached

        Args:
            position (Vector2 | None, optional): _description_. Defaults to None.
            xbounds (Callable[[], None] | None, optional): _description_. Defaults to None.
            ybounds (Callable[[], None] | None, optional): _description_. Defaults to None.
        """
        if position is not None:
            self.position = position

        x, y, w, h = self.rect

        if self.boundaries is not None:
            bx_max, bx_min, by_max, by_min = self.boundaries

            if self.position.y > by_max - h / 2:
                if ybounds is not None:
                    ybounds()

                self.position.y = by_max - h / 2

            elif self.position.y < by_min + h / 2:
                if ybounds is not None:
                    ybounds()

                self.position.y = by_min + h / 2

            if self.position.x > bx_max - w / 2:
                if xbounds is not None:
                    xbounds()

                self.position.x = bx_max - w / 2

            elif self.position.x < bx_min + w / 2:
                if xbounds is not None:
                    xbounds()

                self.position.x = bx_min + w / 2

        x = self.position.x - w / 2
        y = self.position.y - h / 2

        self.rect = Rect(x, y, w, h)

    def __str__(self) -> str:
        return str(tuple(self.rect))


class PhysicsSprite(GameSprite):
    """GameSprite that uses a PhysicsBody reference to apply physics"""

    def __init__(
        self,
        image: Surface,
        position: Vector2,
        physics_body: PhysicsBody,
        boundaries: Rect | None = None,
        id: int = 0,
    ):
        super().__init__(image, position, boundaries, id)
        self.physics_body = physics_body
        self.physics_body.position = self.position


class PlayerSprite(PhysicsSprite):
    """GameSprite with PhysicsBody and Controller input"""

    def __init__(
        self,
        image: Surface,
        position: Vector2,
        controller: Controller,
        physics_body: PhysicsBody,
        boundaries: Rect | None = None,
        id: int = 0,
    ):
        super().__init__(image, position, physics_body, boundaries, id)
        self.controller = controller
