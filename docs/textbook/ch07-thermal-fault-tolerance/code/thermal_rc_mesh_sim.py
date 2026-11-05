#!/usr/bin/env python3
"""Compact Thermal RC Network & Kalman Sensor Reconstruction Simulator.

Simulates 2D on-chip mesh thermal dynamics governed by heat-electricity duality:
    C_i * (dT_i / dt) + G_v * (T_i - T_amb) + sum_{j in N(i)} G_L * (T_i - T_j) = P_i(t)
Includes:
- Dynamic power injection with traffic-dependent router switching dissipation
- Non-Gaussian sensor measurement noise (Gaussian Mixture Model with EMI spikes)
- Discrete-time Kalman filter / state estimation for proactive thermal throttling
- Thermal hotspot emergence and closed-loop throttling mitigation.

Grounded in:
- Y. Fu et al., IEEE TCAD 2017 & IEEE TCAD 2019
- E. Kakoulli et al., IEEE TCAD 2012
"""

from __future__ import annotations
import math
import random
from typing import Dict, List, Tuple


class MeshThermalRCSimulator:
    """Cycle-by-cycle / timestep-by-timestep compact thermal RC simulator."""

    def __init__(
        self,
        grid_dim: int = 4,
        ambient_temp_c: float = 45.0,
        dt_sec: float = 0.002,  # 2 ms discretization timestep
        c_th_j_per_k: float = 0.003,  # Thermal capacitance per tile (J/K) -> tau ~ 36ms
        r_v_k_per_w: float = 12.0,  # Vertical thermal resistance to heatsink (K/W)
        r_lat_k_per_w: float = 25.0,  # Lateral thermal resistance between adjacent tiles (K/W)
        base_leakage_w: float = 0.6,  # Static leakage power per tile (W)
        max_dynamic_w: float = 5.0,  # Peak dynamic switching power at full injection (W)
    ):
        self.grid_dim = grid_dim
        self.num_nodes = grid_dim * grid_dim
        self.ambient_temp = ambient_temp_c
        self.dt = dt_sec
        self.c_th = c_th_j_per_k
        self.g_v = 1.0 / r_v_k_per_w
        self.g_lat = 1.0 / r_lat_k_per_w
        self.base_leakage = base_leakage_w
        self.max_dynamic = max_dynamic_w

        # State vector: temperatures of all nodes (Celsius)
        self.temperatures = [ambient_temp_c for _ in range(self.num_nodes)]

        # Injection rate (0.0 to 1.0 flits/cycle)
        self.injection_rates = [0.12 for _ in range(self.num_nodes)]

        # Sensor placements (subset of nodes equipped with physical thermal diodes)
        self.sensor_indices = [
            0,
            grid_dim - 1,
            self.num_nodes - grid_dim,
            self.num_nodes - 1,
            5,  # Tile (1,1)
            6,  # Tile (1,2)
        ]

        # Kalman Filter state estimates: x_hat (temp above ambient)
        self.x_hat = [0.0 for _ in range(self.num_nodes)]

        # Construct continuous thermal conductance matrix A_c
        self.a_c = [[0.0] * self.num_nodes for _ in range(self.num_nodes)]
        for r in range(grid_dim):
            for c in range(grid_dim):
                i = r * grid_dim + c
                neighbors = []
                if r > 0:
                    neighbors.append((r - 1) * grid_dim + c)
                if r < grid_dim - 1:
                    neighbors.append((r + 1) * grid_dim + c)
                if c > 0:
                    neighbors.append(r * grid_dim + (c - 1))
                if c < grid_dim - 1:
                    neighbors.append(r * grid_dim + (c + 1))

                num_neighbors = len(neighbors)
                # Diagonal: - (G_v + num_neighbors * G_lat) / C_th
                self.a_c[i][i] = -(self.g_v + num_neighbors * self.g_lat) / self.c_th
                for nb in neighbors:
                    self.a_c[i][nb] = self.g_lat / self.c_th

        # Forward Euler discretization: A_d = I + A_c * dt
        self.a_d = [[0.0] * self.num_nodes for _ in range(self.num_nodes)]
        for i in range(self.num_nodes):
            for j in range(self.num_nodes):
                self.a_d[i][j] = (1.0 if i == j else 0.0) + self.a_c[i][j] * self.dt

    def step(
        self,
        throttle_threshold_c: float = 75.0,
        enable_proactive_dtm: bool = True,
    ) -> Dict[str, float]:
        """Simulate one discrete thermal timestep."""
        # 1. Compute power dissipation per tile
        powers = []
        for i in range(self.num_nodes):
            p_dyn = self.max_dynamic * self.injection_rates[i]
            temp_kelvin = self.temperatures[i] + 273.15
            leakage_factor = (temp_kelvin / 318.15) ** 2.0
            p_leak = self.base_leakage * leakage_factor
            powers.append(p_dyn + p_leak)

        # 2. Update true physical temperatures via heat conduction
        new_temps = list(self.temperatures)
        for i in range(self.num_nodes):
            dT_dt = 0.0
            for j in range(self.num_nodes):
                dT_dt += self.a_c[i][j] * (self.temperatures[j] - self.ambient_temp)
            dT_dt += powers[i] / self.c_th
            new_temps[i] = self.temperatures[i] + dT_dt * self.dt
        self.temperatures = new_temps

        # 3. Generate noisy sensor observations with Gaussian + EMI impulse noise
        measurements: Dict[int, float] = {}
        for s_idx in self.sensor_indices:
            true_t = self.temperatures[s_idx]
            # 90% typical diode noise (sigma=0.5 K), 10% high-amplitude EMI spike (sigma=5.0 K)
            if random.random() < 0.10:
                noise = random.gauss(0.0, 5.0)
            else:
                noise = random.gauss(0.0, 0.5)
            measurements[s_idx] = true_t + noise

        # 4. Kalman Filter Prediction & Update Step
        x_pred = [0.0 for _ in range(self.num_nodes)]
        for i in range(self.num_nodes):
            acc = 0.0
            for j in range(self.num_nodes):
                acc += self.a_d[i][j] * self.x_hat[j]
            acc += (self.dt / self.c_th) * powers[i]
            x_pred[i] = acc

        # Measurement residual & update for observed sensors
        for s_idx, z in measurements.items():
            z_above_amb = z - self.ambient_temp
            innovation = z_above_amb - x_pred[s_idx]
            # Huber outlier rejection: drop measurements with innovation > 6.0 K
            if abs(innovation) < 6.0:
                kalman_gain = 0.50
                for i in range(self.num_nodes):
                    if i == s_idx:
                        x_pred[i] += kalman_gain * innovation
                    elif self.a_c[i][s_idx] > 0:
                        x_pred[i] += 0.20 * kalman_gain * innovation

        self.x_hat = x_pred

        # 5. Proactive Dynamic Thermal Management (DTM) Throttling
        throttled_nodes = 0
        if enable_proactive_dtm:
            for i in range(self.num_nodes):
                est_temp = self.ambient_temp + self.x_hat[i]
                if est_temp >= throttle_threshold_c:
                    # Actively throttle overheated node to 0.05
                    self.injection_rates[i] = 0.05
                    throttled_nodes += 1
                else:
                    # Maintain nominal rate
                    self.injection_rates[i] = min(0.12, self.injection_rates[i] + 0.01)

        max_t = max(self.temperatures)
        avg_t = sum(self.temperatures) / self.num_nodes
        est_max_t = self.ambient_temp + max(self.x_hat)

        return {
            "max_temp": max_t,
            "avg_temp": avg_t,
            "est_max_temp": est_max_t,
            "throttled_nodes": float(throttled_nodes),
        }

    def render_ascii_thermal_map(self) -> str:
        """Render a 2D ASCII thermal grid map."""
        lines = []
        for r in range(self.grid_dim):
            row_str = " | ".join(
                f"{self.temperatures[r * self.grid_dim + c]:5.1f}°C"
                for c in range(self.grid_dim)
            )
            lines.append(f"  Row {r}: [ {row_str} ]")
        return "\n".join(lines)


def run_thermal_simulation() -> Tuple[float, float, str]:
    """Execute complete thermal simulation with hotspot generation and DTM."""
    random.seed(42)
    sim = MeshThermalRCSimulator(grid_dim=4, ambient_temp_c=45.0)

    # Step 1: Reach nominal steady state (80 steps)
    for _ in range(80):
        sim.step(enable_proactive_dtm=False)

    # Step 2: Inject extreme traffic hotspot into Center Nodes 5 and 6
    sim.injection_rates[5] = 0.95
    sim.injection_rates[6] = 0.90

    # Step 3: Run unthrottled for 100 steps to permit hotspot saturation
    for _ in range(100):
        sim.step(enable_proactive_dtm=False)
    peak_unthrottled = max(sim.temperatures)
    unthrottled_map = sim.render_ascii_thermal_map()

    # Step 4: Engage proactive DTM throttling for 120 steps to quench the hotspot
    for _ in range(120):
        sim.step(throttle_threshold_c=75.0, enable_proactive_dtm=True)
    quenched_peak = max(sim.temperatures)
    quenched_map = sim.render_ascii_thermal_map()

    report = (
        f"=== Thermal RC & Kalman Estimation Simulation Results ===\n"
        f"Grid Scale: 4x4 Mesh (16 Router-Tile Nodes)\n"
        f"Ambient Temp: 45.0 °C\n"
        f"Unthrottled Hotspot Peak (Center Nodes 5,6): {peak_unthrottled:.2f} °C\n"
        f"Post-DTM Quenched Peak Temperature:         {quenched_peak:.2f} °C\n"
        f"Thermal Hotspot Mitigation Delta:            {peak_unthrottled - quenched_peak:.2f} °C\n\n"
        f"--- Unthrottled Hotspot Map (Peak Saturation) ---\n{unthrottled_map}\n\n"
        f"--- Post-Proactive Quenched Map (Post-DTM) ---\n{quenched_map}\n"
    )
    return peak_unthrottled, quenched_peak, report


if __name__ == "__main__":
    peak_unthrottled, quenched_peak, report = run_thermal_simulation()
    print(report)
    assert peak_unthrottled > 78.0, f"Hotspot should exceed 78°C, got {peak_unthrottled:.2f}"
    assert quenched_peak < peak_unthrottled, "DTM must reduce peak temperature"
    assert quenched_peak < 75.0, f"Quenched temp should drop below 75°C threshold, got {quenched_peak:.2f}"
    print("Self-test passed successfully!")
