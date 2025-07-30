import logging

from abc import abstractmethod
from enum import Enum
from typing import Any, Literal, TypedDict

from pygame import K_ESCAPE, Vector2
from pygame.key import get_pressed as get_pressed_keys
from pygame.joystick import Joystick, JoystickType
from pygame.joystick import get_count as get_joystick_count
from pygame.locals import K_UP, K_LEFT, K_DOWN, K_RIGHT

logger = logging.getLogger(__name__)


class VectorAction(TypedDict):
    """Mapping of controller ID to action

    Args:
        input_id (int): The unique id of the button or axis
        action_type (str): Axis or button type. Only [axis, button] allowed
        action_name (str): The name of the action. Should be unique
    """

    input_id: int
    action_type: Literal["axis", "button", "hat"]
    action_name: str


class Controller:
    """Abstract class for controller
    Must implement 'direction' method
    Optional rotation and action methods
    """

    def __init__(
        self,
        *args: VectorAction,
        speed: int = 1,
        **kwargs: VectorAction,
    ):
        """Creates new instance of Controller object.

        Args:
            speed (int, optional): Scalar multiple applied to controller output. Defaults to 1.
            *args (VectorAction): A list of action metadata for the controller
            **kwargs (VectorAction): A mapping of metadata for the controller
        """
        self.speed = speed

        self._actions: dict[str, VectorAction] = {}
        for action in args:
            id = action["action_name"]
            self._actions[id] = action
        self._actions.update(kwargs)

    @abstractmethod
    def direction(self) -> Vector2:
        """Applies direction from controller input

        Raises:
            NotImplementedError: Abstract method

        Returns:
            Vector2: The new direction vector
        """
        raise NotImplementedError()

    def rotation(self, axis: Literal["x", "y", "z"]) -> Vector2:
        """Applies rotation from controller input

        Args:
            axis (Literal[&quot;x&quot;, &quot;y&quot;, &quot;z&quot;]): The axis of rotation

        Raises:
            NotImplementedError: Abstract method

        Returns:
            Vector2: the new rotation vector
        """
        raise NotImplementedError()

    def action(self, key: str) -> float:
        """_summary_

        Args:
            key (str): The unique key(name) of the action

        Raises:
            NotImplementedError: Abstract method

        Returns:
            float: The value from the controller output for this action
        """
        raise NotImplementedError()


class ControllerHandler:
    """Helper class for getting controllers
    Implement cls._new_controller_instance(joy, speed, *args, **kwargs) method
    """

    @classmethod
    @abstractmethod
    def _new_controller_instance(
        cls,
        joystick: JoystickType,
        speed: int,
        *args: VectorAction,
        **kwargs: VectorAction,
    ) -> Controller:
        """Creates a new instance of Controller with given args

        Args:
            input (pygame.JoystickType): The pygame Joystick reference
            speed (int): Scalar multiple applied to controller output
            *args (VectorAction): A list of action metadata for the controller
            **kwargs (VectorAction): A mapping of metadata for the controller

        Raises:
            NotImplementedError: Abstract method

        Returns:
            Controller: the new instance of Controller
        """
        raise NotImplementedError

    @classmethod
    def get_controllers(
        cls,
        players: int = 1,
        speed: int = 1,
    ) -> list[Controller]:
        """Base implementation for getting all Joystick controllers for each player

        Args:
            players (int, optional): The number of players. Defaults to 1.
            speed (int, optional): Scalar multiple applied to controller output. Defaults to 1.

        Returns:
            list[Controller]: A list of controllers for each player
        """
        controllers = []
        for i in range(get_joystick_count()):
            new_controller = cls._new_controller_instance(
                joystick=Joystick(i),
                speed=speed,
            )
            controllers.append(new_controller)

        if len(controllers) < players:
            logger.warning(
                f"Not enough controllers for players! (Players: {players}, Controllers: {len(controllers)})"
            )

        return controllers


class JoystickController(Controller):
    """Joystick base class.  Implements Controller class action(key) method.
    Abstract class that requires implementation for direction() method.
    """

    def __init__(
        self,
        input: JoystickType,
        *args: VectorAction,
        speed: int = 1,
        **kwargs: VectorAction,
    ):
        """_summary_

        Args:
            input (pygame.JoystickType): The pygame Joystick reference
            speed (int, optional): Scalar multiple applied to controller output. Defaults to 1.
            *args (VectorAction): A list of action metadata for the controller
            **kwargs (VectorAction): A mapping of metadata for the controller
        """
        super().__init__(*args, speed=speed, **kwargs)
        self.input = input

    def action(self, key: str) -> float:
        vector_action = self._actions.get(key)

        if vector_action is not None:
            id = vector_action["input_id"]
            action_type = vector_action["action_type"]
            if action_type == "axis":
                axis = self.input.get_axis(id)
                return axis
            else:
                return 1.0 if self.input.get_button(id) else 0.0

        else:
            return 0.0


class KeyboardController(Controller):
    """Keyboard base class.  Implements Controller class action(key) method.
    Abstract class that requires implementation for direction() method.
    Adds get_keys() method that gets all keyboard keys pressed
    """

    def get_keys(self) -> Any:
        return get_pressed_keys()

    def action(self, key: str) -> float:
        vector_action = self._actions.get(key)

        if vector_action is not None:
            id = vector_action["input_id"]
            all_keys = self.get_keys()
            if len(all_keys) > 0 and all_keys[id] is True:
                return 1.0

        return 0.0


class DefaultKeyboardController(KeyboardController):
    class Commands(Enum):
        """Constant keyboard commands"""

        X_AXIS_POS = "x_axis_pos"
        X_AXIS_NEG = "x_axis_neg"
        Y_AXIS_POS = "y_axis_pos"
        Y_AXIS_NEG = "y_axis_neg"
        QUIT = "quit"

    """A simple Keyboard Controller implementation"""

    def direction(self) -> Vector2:
        """Applies direction from keyboard input

        Returns:
            Vector2: The new directional vector
        """
        vx = (
            self.action(self.Commands.X_AXIS_POS.value)
            - self.action(self.Commands.X_AXIS_NEG.value)
        ) * self.speed

        vy = (
            self.action(self.Commands.Y_AXIS_POS.value)
            - self.action(self.Commands.Y_AXIS_NEG.value)
        ) * self.speed

        return Vector2(vx, vy)


DEFAULT_KEYBOARD_ACTIONS: list[VectorAction] = [
    {
        "input_id": K_RIGHT,
        "action_name": DefaultKeyboardController.Commands.X_AXIS_POS.value,
        "action_type": "button",
    },
    {
        "input_id": K_LEFT,
        "action_name": DefaultKeyboardController.Commands.X_AXIS_NEG.value,
        "action_type": "button",
    },
    {
        "input_id": K_DOWN,
        "action_name": DefaultKeyboardController.Commands.Y_AXIS_POS.value,
        "action_type": "button",
    },
    {
        "input_id": K_UP,
        "action_name": DefaultKeyboardController.Commands.Y_AXIS_NEG.value,
        "action_type": "button",
    },
    {
        "input_id": K_ESCAPE,
        "action_name": DefaultKeyboardController.Commands.QUIT.value,
        "action_type": "button",
    },
]
