# Visualizations using folium/matplotlib
# visualize_routes.py

import matplotlib.pyplot as plt
import numpy as np


def plot_trajectory(trajectory, grid_size=5, goal=(4, 4), obstacles=None, save_path=None, show=True):
    """
    Plot the agent's trajectory on a 2D grid.

    Parameters
    ----------
    trajectory : list of (x, y)
        List of (x, y) positions visited by the agent.
    grid_size : int
        Size of the square grid.
    goal : tuple
        Coordinates of the goal location.
    save_path : str or None
        If set, saves the plot to this file.
    show : bool
        If True, displays the plot interactively.
    """
    fig, ax = plt.subplots(figsize=(6, 6))

    # Background grid
    for x in range(grid_size + 1):
        ax.axhline(x, color="lightgray", linewidth=1)
        ax.axvline(x, color="lightgray", linewidth=1)

    # Plot obstacles
    if obstacles:
        obs_x, obs_y = zip(*obstacles)
        ax.scatter(np.array(obs_x) + 0.5, np.array(obs_y)+ 0.5, color='black', s=100, marker='X', label='Obstacle')

    # Plot trajectory
    x_vals, y_vals = zip(*trajectory)
    ax.plot(np.array(x_vals) + 0.5, np.array(y_vals) + 0.5, marker='o', color='blue', label="Trajectory")
    ax.scatter([goal[0] + 0.5], [goal[1] + 0.5], color='green', s=100, marker='*', label='Goal')

    # Mark start
    ax.scatter([x_vals[0] + 0.5], [y_vals[0] + 0.5], color='red', s=100, marker='s', label='Start')

    # Formatting
    ax.set_xlim(0, grid_size)
    ax.set_ylim(0, grid_size)
    ax.set_xticks(np.arange(0, grid_size + 1))
    ax.set_yticks(np.arange(0, grid_size + 1))
    ax.set_aspect('equal')
    ax.invert_yaxis()
    ax.legend()
    ax.set_title("Agent Trajectory")

    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
        print(f"🖼️ Plot saved to {save_path}")

    if show:
        plt.show()

    plt.close()


if __name__ == "__main__":
    # Example usage (hardcoded dummy trajectory)
    sample_trajectory = [(0, 0), (1, 0), (2, 0), (2, 1), (3, 1), (4, 1), (4, 2), (4, 3), (4, 4)]
    plot_trajectory(sample_trajectory, grid_size=5)


