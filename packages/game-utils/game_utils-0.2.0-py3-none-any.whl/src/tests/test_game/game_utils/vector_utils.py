from numpy.random import choice, rand
from pygame import Vector2
from collections.abc import Callable


def get_random_vector(scalar_mag: int = 1, non_negative: bool = False) -> Vector2:
    def rand_sign() -> int:
        return choice([-1, 1]) if not non_negative else 1

    return Vector2(
        x=rand() * rand_sign() * scalar_mag,
        y=rand() * rand_sign() * scalar_mag,
    )


def apply(vector: Vector2, *actions: Callable[[Vector2], Vector2]) -> Vector2:
    for action in actions:
        vector = action(vector)

    return vector
