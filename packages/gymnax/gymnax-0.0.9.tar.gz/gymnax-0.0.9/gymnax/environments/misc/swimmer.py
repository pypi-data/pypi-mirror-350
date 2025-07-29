"""JAX implementation of Swimmer environment."""

from typing import Any

import jax
import jax.numpy as jnp
from flax import struct

from gymnax.environments import environment, spaces


@struct.dataclass
class EnvState(environment.EnvState):
    urchin_xys: jax.Array
    xy: jax.Array
    xy_vel: jax.Array
    goal_xy: jax.Array
    time: float


@struct.dataclass
class EnvParams(environment.EnvParams):
    dt: float = 0.05
    max_steps_in_episode: int = 500  # Steps in an episode (constant goal)


class Swimmer(environment.Environment[EnvState, EnvParams]):
    """JAX implementation of Swimmer environment.


    Adapted from: https://github.com/unifyai/gym/blob/master/ivy_gym/swimmer.py
    """

    def __init__(self, num_urchins: int = 5):
        super().__init__()
        self.num_urchins = num_urchins

    @property
    def default_params(self) -> EnvParams:
        # Default environment parameters
        return EnvParams()

    def step_env(
        self,
        key: jax.Array,
        state: EnvState,
        action: int | float | jax.Array,
        params: EnvParams,
    ) -> tuple[jax.Array, EnvState, jax.Array, jax.Array, dict[Any, Any]]:
        """Sample bernoulli reward, increase counter, construct input."""
        xy_vel = state.xy_vel + params.dt * action
        xy = state.xy + params.dt * xy_vel

        state = EnvState(
            urchin_xys=state.urchin_xys,
            xy=xy,
            xy_vel=xy_vel,
            goal_xy=state.goal_xy,
            time=state.time + 1,
        )

        rew = jnp.exp(-0.5 * jnp.sum((state.xy - state.goal_xy) ** 2))
        # Urchins proximity.
        reward = rew * jnp.prod(
            1 - jnp.exp(-30 * jnp.sum((state.xy - state.urchin_xys) ** 2, axis=-1)),
            axis=-1,
        )

        done = self.is_terminal(state, params)
        return (
            jax.lax.stop_gradient(self.get_obs(state, params)),
            jax.lax.stop_gradient(state),
            reward,
            done,
            {"discount": self.discount(state, params)},
        )

    def reset_env(
        self, key: jax.Array, params: EnvParams
    ) -> tuple[jax.Array, EnvState]:
        """Reset environment state by sampling initial position."""
        # Sample reward function + construct state as concat with timestamp
        key_urchin, key_xy, key_goal = jax.random.split(key, 3)

        urchin_xys = jax.random.uniform(
            key_urchin, minval=-1, maxval=1, shape=(self.num_urchins, 2)
        )
        xy = jax.random.uniform(key_xy, minval=-1, maxval=1, shape=(2,))
        xy_vel = jnp.zeros((2,))
        goal_xy = jax.random.uniform(key_goal, minval=-1, maxval=1, shape=(2,))

        state = EnvState(
            urchin_xys=urchin_xys,
            xy=xy,
            xy_vel=xy_vel,
            goal_xy=goal_xy,
            time=0,
        )
        return self.get_obs(state, params), state

    def get_obs(self, state: EnvState, params: EnvParams, key=None) -> jax.Array:
        """Concatenate reward, one-hot action and time stamp."""
        ob = (
            jnp.reshape(state.urchin_xys, (-1, 2)),
            jnp.reshape(state.xy, (-1, 2)),
            jnp.reshape(state.xy_vel, (-1, 2)),
            jnp.reshape(state.goal_xy, (-1, 2)),
        )
        ob = jnp.concatenate(ob, axis=0)
        return jnp.reshape(ob, (-1,))

    def is_terminal(self, state: EnvState, params: EnvParams) -> jax.Array:
        """Check whether state is terminal."""
        # Check number of steps in episode termination condition
        done = state.time >= params.max_steps_in_episode
        return jnp.array(done)

    @property
    def name(self) -> str:
        """Environment name."""
        return "Swimmer-misc"

    @property
    def num_actions(self) -> int:
        """Number of actions possible in environment."""
        return 2

    def action_space(self, params: EnvParams | None = None) -> spaces.Box:
        """Action space of the environment."""
        # if params is None:
        #   params = self.default_params
        low = jnp.array(2 * [-1], dtype=jnp.float32)
        high = jnp.array(2 * [1], dtype=jnp.float32)
        return spaces.Box(low, high, (2,), jnp.float32)

    def observation_space(self, params: EnvParams) -> spaces.Box:
        """Observation space of the environment."""
        low = jnp.array(
            (6 + self.num_urchins * 2) * [-jnp.finfo(jnp.float32).max],
            dtype=jnp.float32,
        )
        high = jnp.array(
            (6 + self.num_urchins * 2) * [jnp.finfo(jnp.float32).max],
            dtype=jnp.float32,
        )
        return spaces.Box(low, high, (6 + self.num_urchins * 2,), jnp.float32)

    def state_space(self, params: EnvParams) -> spaces.Dict:
        """State space of the environment."""
        return spaces.Dict(
            {
                "urchin_xys": spaces.Box(
                    -jnp.finfo(jnp.float32).max,
                    jnp.finfo(jnp.float32).max,
                    (self.num_urchins,),
                    jnp.float32,
                ),
                "xy": spaces.Box(
                    -jnp.finfo(jnp.float32).max,
                    jnp.finfo(jnp.float32).max,
                    (2,),
                    jnp.float32,
                ),
                "xy_vel": spaces.Box(
                    -jnp.finfo(jnp.float32).max,
                    jnp.finfo(jnp.float32).max,
                    (2,),
                    jnp.float32,
                ),
                "goal_xy": spaces.Box(
                    -1,
                    1,
                    (2,),
                    jnp.float32,
                ),
                "time": spaces.Discrete(params.max_steps_in_episode),
            }
        )
