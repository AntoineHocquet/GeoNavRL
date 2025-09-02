# Dynamics + control under uncertainty
# dynamics.py

import numpy as np
import random


def apply_dynamics(state, action, grid_size, noise_prob=0.1, blocked_cells=None):
    """
    Apply dynamics to state-action pair with optional noise and obstacles.

    Parameters
    ----------
    state : np.ndarray
        Current position (x, y).
    action : int
        Chosen action: 0=up, 1=down, 2=left, 3=right
    grid_size : int
        Size of the square grid.
    noise_prob : float
        Probability of taking a random wrong move.
    blocked_cells : set of (x, y)
        Locations that are blocked (walls or obstacles)

    Returns
    -------
    new_state : np.ndarray
        Updated position after applying dynamics.
    """
    x, y = state

    # With noise, replace action with random one
    if random.random() < noise_prob:
        action = random.choice([0, 1, 2, 3])

    # Move based on action
    if action == 0 and y > 0:        # up
        y -= 1
    elif action == 1 and y < grid_size - 1:  # down
        y += 1
    elif action == 2 and x > 0:      # left
        x -= 1
    elif action == 3 and x < grid_size - 1:  # right
        x += 1

    new_state = np.array([x, y])

    # Handle obstacles
    if blocked_cells and tuple(new_state) in blocked_cells:
        return state  # no movement

    return new_state
