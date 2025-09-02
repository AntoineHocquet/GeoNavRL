# geonav_env.py

# geonav_env.py

import numpy as np
import gymnasium as gym
from gymnasium import spaces
from env.dynamics import apply_dynamics
from env.map_parser import load_map
from env.map_parser import load_osm_area

_, blocked_basic = load_map("data/berlin_sample.geojson", grid_size=10)
_, blocked_hussitenstrasse = load_osm_area("Hussitenstrasse 68, Berlin, Germany", grid_size=20)

class GeoNavEnv(gym.Env):
    """
    Minimal grid-world mockup for last-mile delivery simulation.
    The agent starts at the top-left corner of a grid and must navigate to the bottom-right corner.
    Actions: 0=up, 1=down, 2=left, 3=right
    Reward: +1 for reaching the goal, -0.01 per step to encourage efficiency.
    Observation: (x, y) coordinates of the agent.
    Grid cells can be blocked to simulate obstacles (grid cells that cannot be entered)
    Ex.: blocked_cells = {(1,1), (2,2), (3,3)}
    """

    metadata = {"render.modes": ["human"]}

    def __init__(self, grid_size=5, default_blocked=blocked_hussitenstrasse):
        super().__init__()
        self.grid_size = grid_size
        self.action_space = spaces.Discrete(4)  # 0: up, 1: down, 2: left, 3: right
        self.observation_space = spaces.Box(
            low=0, high=grid_size - 1, shape=(2,), dtype=np.int32
        )
        self.blocked_cells = default_blocked

        self.start = np.array([0, 0])
        self.goal = np.array([grid_size - 1, grid_size - 1])
        self.state = self.start.copy()

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.state = self.start.copy()
        return self.state.copy(), {}

    def step(self, action):
        prev_state = self.state.copy()
        self.state = apply_dynamics(
            state=prev_state,
            action=action,
            grid_size=self.grid_size,
            noise_prob=0.1, # to adjust later
            blocked_cells=self.blocked_cells
        )

        done = np.array_equal(self.state, self.goal)
        reward = 1.0 if done else -0.01  # light shaping

        return self.state.copy(), reward, done, False, {}

    def render(self):
        grid = np.full((self.grid_size, self.grid_size), '.', dtype=str)
        x, y = self.state
        gx, gy = self.goal

        for bx, by in self.blocked_cells:
            grid[by, bx] = '#'

        grid[gy, gx] = 'G'
        grid[y, x] = 'A'
        print("\n".join(" ".join(row) for row in grid))
        print()


# Optional for gym registration
def register_env():
    gym.envs.registration.register(
        id="GeoNavEnv-v0",
        entry_point="env.geonav_env:GeoNavEnv",
    )


# To test the  code locally
if __name__ == "__main__":
    # Simple test run
    env = GeoNavEnv()

    print(f"Observation space: {env.observation_space}")
    print(f"Action space: {env.action_space}")
    walkable, blocked = load_map("data/berlin_sample.geojson", grid_size=10)
    print("Walkable cells:", walkable)
    print("Blocked cells:", blocked)

    obs, _ = env.reset()

    for _ in range(10):
        action = env.action_space.sample()
        obs, reward, done, _, _ = env.step(action)
        print(f"Action: {action}, Obs: {obs}, Reward: {reward}, Done: {done}")
        env.render()
        if done:
            break
