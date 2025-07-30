from numpy.random import normal
from pygame import Vector2, Vector3


class PhysicsBody:
    """Applies physics to a GameSprite"""

    ZERO_VECTOR = Vector2(0, 0)
    GRAVITY = 9.8

    def __init__(
        self,
        mass: float = 1.0,
        position: Vector2 = ZERO_VECTOR.copy(),
        velocity: Vector2 = ZERO_VECTOR.copy(),
        friction: float = 0.0,
        elasticity: float = 0.0,
        slip: float = 1.0,
    ):
        """Creates new instance of PhysicsBody object

        Args:
            mass (float, optional): The mass of the body. Defaults to 1.0.
            position (Vector2, optional): The current positional vector of the body. Defaults to (0,0).
            friction (float, optional): Static friction force. Defaults to 0.0.
            elasticity (float, optional): Elasticity is used in caluclating loss of energy. 0 elasticity will have no effect. Defaults to 0.0.
            slip (float, optional): Used in calculating change in static to kinetic friction. Defaults to 1.0.
        """
        self.mass = mass
        self.velociy = velocity.copy()
        self.position = position.copy()
        self.static_friction = friction
        self.kinetic_friction = 0
        self.elasticity = 1 - elasticity
        if self.static_friction > 0:
            self.kinetic_friction = self.static_friction * normal(loc=slip)

    def force(self, acceleration: Vector2, dtime: float) -> Vector2:
        """Applies an acceleration vector to this body's current velocity with the given change in time.
        If friction was given, friction is calculated into the new velocity

        Args:
            acceleration (Vector2): The acceleration to apply
            dtime (float): The change in time

        Returns:
            Vector2: The new velocity at this moment in time
        """
        new_velocity = acceleration * dtime
        force = acceleration * self.mass

        if force.magnitude() > self.friction_force().magnitude():
            self.velociy += new_velocity
        else:
            self.velociy -= self.velociy * self.friction_force().magnitude() * dtime
        self.move(dtime)

        return self.velociy.copy()

    def move(self, dtime: float) -> Vector2:
        """Returns the position at this moment in time.\n
        Applies velocity over dtime"""
        self.position += self.velociy * dtime

        return self.position.copy()

    def on_collide(self, other):
        """New velocity is given by V`= (V(m-s) + U2s)/(m+s)
        for initial magnitudes Vm(self) and Us(other).  Calculates loss of
        energy from this body's elasticity

        Args:
            other (object): The object with which this body has collided
        """
        assert isinstance(other, PhysicsBody)

        self.velociy *= self.mass - other.mass
        self.velociy += other.velociy * 2 * other.mass
        self.velociy /= self.mass + other.mass

        # energy loss, if any
        self.velociy *= self.elasticity

    def momentum(self) -> Vector2:
        """This body's current momentum

        Returns:
            Vector2: Vm of this body
        """
        return self.velociy * self.mass

    def normal_force(self) -> Vector3:
        """The normal force of this body

        Returns:
            Vector3: (0, 0, mg)
        """
        return Vector3(0, 0, self.mass * self.GRAVITY)

    def friction_force(self) -> Vector3:
        """fs * N if not in motion, else fk * N

        Returns:
            Vector3: (0, 0, fN)
        """
        return (
            self.static_friction * self.normal_force()
            if self.velociy == self.ZERO_VECTOR
            else self.kinetic_friction * self.normal_force()
        )

    def __str__(self) -> str:
        return str(self.position)
