
# Makefile for GeoNavRL project

.PHONY: help install train rollout test format clean

# ---- General ----
help:
	@echo "🧭 GeoNavRL Makefile commands:"
	@echo "  make install     - Install Python dependencies"
	@echo "  make train       - Train PPO policy"
	@echo "  make rollout     - Run trained policy and plot trajectory"
	@echo "  make test        - Run unit tests"
	@echo "  make format      - Auto-format code with black"
	@echo "  make clean       - Remove model and log files"

# ---- Setup ----
install:
	pip install -r requirements.txt

# ---- Training ----
train:
	PYTHONPATH=. python experiments/train_policy.py

# ---- Rollout and Visualization ----
rollout:
	PYTHONPATH=. python experiments/rollout_policy.py --model models/ppo_geonav_final.zip --save outputs/trajectory.png

# ---- Testing ----
test:
	PYTHONPATH=. pytest tests/

# ---- Code Formatting ----
format:
	black env/ experiments/ visualizations/ tests/

# ---- Cleanup (including Jupyter notebooks) ----
clean:
	rm -rf __pycache__ */__pycache__ .pytest_cache logs/ models/ outputs/ *.zip
	rm -rf *.ipynb_checkpoints */*.ipynb_checkpoints

# ---- Additionally delete all subfolders with name "cache" and what is inside ----
clean_cache:
	find . -type d -name "cache" -exec rm -rf {} +