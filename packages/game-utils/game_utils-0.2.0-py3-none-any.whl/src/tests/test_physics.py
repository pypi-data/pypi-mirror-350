import math
from game_utils.physics import *
from pygame import Vector2


def test_physics_body():
    pb = PhysicsBody()

    assert pb is not None
    assert pb.elasticity == 1.0
    assert pb.mass == 1.0
    assert pb.static_friction == 0.0
    assert pb.kinetic_friction == 0.0

    pb2 = PhysicsBody(
        mass=2.0,
        friction=0.009,
        elasticity=0.02,
        slip=1.1,
    )

    assert pb2 is not None
    assert math.fabs(pb2.kinetic_friction) > 0


def test_forces():
    pb = PhysicsBody(mass=2.0)

    v = pb.force(Vector2(0.1, -0.1), 0.1)
    assert v is not None
    assert v == Vector2(0.01, -0.01)

    v2 = pb.move(0.08)

    assert v2 is not None
    assert (v2 - v).magnitude() != 0


def test_collisions():
    v_i1 = Vector2(-1, 0)
    d_i1 = Vector2(1, 0)

    pb = PhysicsBody(
        mass=2.0,
        position=d_i1,
        velocity=v_i1,
    )

    v_i2 = Vector2(1, 0)
    d_i2 = Vector2(-1, 0)

    pb2 = PhysicsBody(
        mass=3.0,
        position=d_i2,
        velocity=v_i2,
    )

    t1 = 0.1

    d1_t1 = pb.move(t1)
    d2_t1 = pb2.move(t1)

    assert d1_t1 is not d_i1
    assert d2_t1 is not d_i2

    pb.on_collide(pb2)
    pb2.on_collide(pb)

    t2 = 0.2

    d1_t2 = pb.move(t2)
    d2_t2 = pb2.move(t2)

    assert d1_t2 is not d1_t1
    assert d2_t2 is not d2_t1
