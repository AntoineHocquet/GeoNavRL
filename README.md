# GeoNavRL

Reinforcement Learning + Control-based Navigation under Geospatial Constraints.# GeoNavRL

**Reinforcement Learning + Control-Based Navigation under Geospatial Constraints**

## 🌍 Project Overview

**GeoNavRL** is a reinforcement learning environment for simulating last-mile delivery navigation. Inspired by real-world challenges in logistics and urban mapping, this project explores how agents can learn to make optimal routing decisions in uncertain, noisy, and geospatially constrained environments.

The goal is to prototype intelligent navigation algorithms using:
- **Geospatial data** (e.g. maps, addresses, building entry points),
- **Noisy control** (inspired by stochastic differential equations and control theory),
- **Sensor-like observations** (simulated GPS, accelerometers),
- and **reinforcement learning** (e.g. PPO, DQN).

## 🧠 Why This Project

This project is designed to demonstrate:
- Application of **mathematical control theory** in practical decision-making environments.
- Use of **reinforcement learning** in the context of urban navigation.
- Handling **uncertainty**, **sensor noise**, and **dynamic environments**, drawing on ideas from your previous research on stochastic control and McKean–Vlasov systems.


## 🏗️ Project Structure

## 🧪 Features to Implement

- [ ] Create a graph-based map from GeoJSON/OpenStreetMap
- [ ] Simulate agent walking + parking with discrete + continuous controls
- [ ] Add stochastic noise to state evolution (GPS drift, footpath blockages)
- [ ] Train agent using RL (PPO, DQN)
- [ ] Evaluate performance against classical shortest-path routing
- [ ] Add metrics: time to reach target, number of failed deliveries, etc.
- [ ] Visualize learned paths using `folium` or `matplotlib`

## 🛠️ Technologies

- `Python`, `PyTorch`, `stable-baselines3`
- `geopandas`, `shapely`, `folium`, `matplotlib`, `osmnx`
- `gymnasium`, `pytest`, `Docker`, `Makefile`

## 📈 Future Directions

- Multi-agent setting (mean-field style interaction between couriers)
- Learnable parking spot selection
- Real data from Berlin or OpenStreetMap
- Incorporate hybrid filtering + prediction models
- Use noisy time-series data from sensors (control + filtering loop)

## 🔗 Author

Antoine Hocquet  
[Personal Website](https://antoinehocquet.com) | [GitHub](https://github.com/AntoineHocquet) | [LinkedIn](https://www.linkedin.com/in/antoine-hocquet-875231a7)

---

> 🚧 This project is under active development. All contributions welcome.

