from pygame import Vector2
from game_utils.controller import *
from game_utils.controller import VectorAction

VALUES = [0.1, 2.2, 4.7]
DIRECTIONS = [
    Vector2(0.1, 2.2),
    Vector2(2.2, 4.7),
    Vector2(0.1, 4.7),
]


class TestActions(Enum):
    ACTION_A = 0
    ACTION_B = 1
    ACTION_C = 2
    ACTION_Z = -1


class TestController(Controller):
    def __init__(self, *args: VectorAction, speed: int = 1, **kwargs: VectorAction):
        super().__init__(*args, speed=speed, **kwargs)
        self.action_: TestActions | None = None

    def direction(self) -> Vector2:
        if not self.action_:
            self.action_ = TestActions.ACTION_Z

        return DIRECTIONS[self.action_.value]

    def action(self, key: str) -> float:
        assert self._actions.get(key)
        return VALUES[self._actions[key]["input_id"]]


def test_controller():
    c = TestController(
        {
            "input_id": TestActions.ACTION_A.value,
            "action_type": "hat",
            "action_name": TestActions.ACTION_A.name,
        },
        {
            "input_id": TestActions.ACTION_B.value,
            "action_type": "axis",
            "action_name": TestActions.ACTION_B.name,
        },
        {
            "input_id": TestActions.ACTION_C.value,
            "action_type": "button",
            "action_name": TestActions.ACTION_C.name,
        },
    )

    assert c.action(TestActions.ACTION_A.name) == VALUES[TestActions.ACTION_A.value]
    assert c.action(TestActions.ACTION_C.name) == VALUES[TestActions.ACTION_Z.value]

    assert c.direction() == DIRECTIONS[-1]
    c.action_ = TestActions.ACTION_B
    assert c.direction() == DIRECTIONS[1]
