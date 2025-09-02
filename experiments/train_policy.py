# Training loop for RL agent
# train_policy.py

import os
import time
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.callbacks import EvalCallback
from env.geonav_env import GeoNavEnv, register_env  # You will create this later
register_env()
from datetime import datetime


def train(
    env_id="GeoNavEnv",
    total_timesteps=100_000,
    log_dir="logs/",
    save_path="models/ppo_geonav",
    eval_freq=10_000,
    n_eval_episodes=5,
):
    # Create log dir
    os.makedirs(log_dir, exist_ok=True)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    # Register or instantiate the environment
    # You will later need to register GeoNavEnv if not using make_vec_env
    env = make_vec_env("GeoNavEnv-v0", n_envs=1)

    # Set up evaluation callback
    eval_callback = EvalCallback(
        env,
        best_model_save_path=save_path,
        log_path=log_dir,
        eval_freq=eval_freq,
        n_eval_episodes=n_eval_episodes,
        deterministic=True,
        render=False,
    )

    # Initialize PPO model
    model = PPO("MlpPolicy", env, verbose=1)

    # Train the model
    start_time = time.time()
    print(f"🚀 Training started at {datetime.now().isoformat()}")
    model.learn(total_timesteps=total_timesteps, callback=eval_callback)
    duration = time.time() - start_time
    print(f"✅ Training complete in {duration:.2f} seconds")

    # Save final model
    model.save(save_path + "_final")
    print(f"💾 Final model saved to {save_path}_final")


if __name__ == "__main__":
    train()



