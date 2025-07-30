import multiprocessing as mp
import pytest
import numpy as np
from myrtle.tests.fixtures import setup_mq_server  # noqa: F401
from myrtle.worlds import pendulum


@pytest.fixture
def initialize_world():
    world = pendulum.Pendulum(
        q_action=mp.Queue(),
        q_reward=mp.Queue(),
        q_sensor=mp.Queue(),
    )
    yield world


def test_initialization(initialize_world):
    world = initialize_world

    assert world.n_sensors == 2
    assert world.n_actions == 13
    assert world.n_rewards == 1


def test_reset(initialize_world):
    world = initialize_world

    assert world.velocity == 0
    assert world.position == 0


def test_sense(
    initialize_world,
    setup_mq_server,  # noqa: F811
):
    world = initialize_world
    world.initialize_mq()
    world.sense()

    assert world.rewards[0] < 0.001


def test_step_world(
    initialize_world,
    setup_mq_server,  # noqa: F811
):
    world = initialize_world
    world.initialize_mq()
    world.actions = np.zeros(world.n_actions)
    world.actions[-1] = 1
    world.i_world_step = 0
    world.step_world()

    assert world.velocity > 0.8
    assert world.position > 0.005 and world.position < 0.05
