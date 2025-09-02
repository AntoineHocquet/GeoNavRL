# rollout_policy.py

import argparse
from stable_baselines3 import PPO
from env.geonav_env import GeoNavEnv
from visualizations.visualize_routes import plot_trajectory


def rollout(model_path=None, num_steps=100, render=False, save_plot=None):
    env = GeoNavEnv()
    obs, _ = env.reset()
    trajectory = [tuple(obs)]

    if model_path:
        model = PPO.load(model_path)
        print(f"✅ Loaded model from {model_path}")
    else:
        model = None
        print("⚠️ No model loaded — using random actions.")

    for _ in range(num_steps):
        if model:
            action, _ = model.predict(obs, deterministic=True)
        else:
            action = env.action_space.sample()

        obs, reward, done, _, _ = env.step(action)
        trajectory.append(tuple(obs))

        if render:
            env.render()

        if done:
            print("🏁 Goal reached!")
            break

    # Visualize
    plot_trajectory(
        trajectory,
        grid_size = env.grid_size,
        goal=env.goal,
        obstacles=env.blocked_cells,
        save_path=save_plot
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Roll out a policy and visualize trajectory.")
    parser.add_argument("--model", type=str, default=None, help="Path to PPO model (.zip)")
    parser.add_argument("--steps", type=int, default=100, help="Max steps to roll out")
    parser.add_argument("--render", action="store_true", help="Render env to terminal")
    parser.add_argument("--save", type=str, default=None, help="Path to save the trajectory plot")

    args = parser.parse_args()
    rollout(model_path=args.model, num_steps=args.steps, render=args.render, save_plot=args.save)
