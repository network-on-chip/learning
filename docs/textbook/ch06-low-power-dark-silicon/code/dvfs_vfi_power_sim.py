#!/usr/bin/env python3
"""
===============================================================================
DVFS, Voltage-Frequency Island (VFI) & Power-Gating Simulator
Network-on-Chip (NoC) and Advanced Interconnects: Textbook Companion
Chapter 6: Low-Power Architectures & Dark Silicon Dynamics

Grounded in:
- H. Matsutani et al., "Performance, Area, and Power Evaluations of
  Ultrafine-Grained Run-Time Power-Gating Routers for CMPs," IEEE TCAD, 2011.
- M. K. Yadav, M. R. Casu, M. Zamboni, "LAURA-NoC: Local Automatic Rate
  Adjustment in Network-on-Chips With a Simple DVFS," IEEE TCAS-II, 2013.
- M. Adelkhani et al., "LPCR: Information-Theory-Based Low-Power Code
  Reordering for Serial Links in Network-on-Chip," IEEE TCAD, 2025.
===============================================================================
"""

import math
from typing import Dict, List, Tuple


class RouterPowerModel:
    """
    CMOS Power & Thermal Feedback Model for an on-chip router tile.
    Computes dynamic power, sub-threshold leakage, gate oxide leakage,
    and power-gating wake-up overheads under dark silicon thermal constraints.
    """

    def __init__(
        self,
        node_id: int,
        c_eff_buf: float = 2.5e-12,  # Effective switching capacitance (Farads)
        c_eff_xbar: float = 4.0e-12,
        c_eff_link: float = 6.0e-12,
        r_th: float = 1.8,  # Thermal resistance (K / Watt)
        t_ambient: float = 318.15,  # 45 deg C in Kelvin
    ):
        self.node_id = node_id
        self.c_eff_total = c_eff_buf + c_eff_xbar + c_eff_link
        self.r_th = r_th
        self.t_ambient = t_ambient
        self.temperature = t_ambient

        # DVFS Operating Points (Voltage, Frequency)
        self.dvfs_levels = [
            (0.60, 0.4e9),  # Low power mode
            (0.75, 0.8e9),  # Nominal power mode
            (0.90, 1.2e9),  # High performance mode
            (1.05, 1.6e9),  # Boost turbo mode
        ]
        self.current_dvfs_idx = 1  # Default nominal

        # Power gating parameters
        self.is_power_gated = False
        self.sleep_leakage_ratio = 0.05  # 95% leakage eliminated when sleep transistor is OFF
        self.wake_energy_joules = 1.2e-11  # Charge virtual VDD rail during wakeup
        self.wake_latency_cycles = 4  # Pipeline cycles to stabilize rail

    def set_dvfs_mode(self, level_idx: int):
        self.current_dvfs_idx = max(0, min(len(self.dvfs_levels) - 1, level_idx))

    def compute_power(
        self, flit_rate_norm: float, power_gate_active: bool
    ) -> Dict[str, float]:
        """
        Compute total power dissipation:
        P_total = P_dynamic + P_leakage
        P_dynamic = alpha * C_eff * Vdd^2 * f
        P_leakage = Vdd * I_leak(T, Vdd)
        """
        vdd, freq = self.dvfs_levels[self.current_dvfs_idx]

        # 1. Dynamic Power
        # Flit rate (0.0 to 1.0) dictates the average switching activity factor alpha
        alpha = max(0.01, min(1.0, flit_rate_norm))
        p_dyn = alpha * self.c_eff_total * (vdd**2) * freq

        # 2. Leakage Power with Temperature Feedback (Arrhenius scaling)
        # Subthreshold leakage scales exponentially with absolute temperature
        t_kelvin = self.temperature
        t_ratio = t_kelvin / 300.0
        # Reference leakage current at 300K, 0.9V
        i_leak_base = 12.0e-3  # 12 mA baseline leakage per router in 45nm/28nm
        i_leak = i_leak_base * (t_ratio**2) * math.exp((t_kelvin - 300.0) / 45.0)

        p_leak = vdd * i_leak

        if power_gate_active and alpha < 0.05:
            # Power gating sleep mode cuts leakage by 95%
            p_leak *= self.sleep_leakage_ratio
            p_dyn = 0.0

        p_total = p_dyn + p_leak

        # Update temperature self-consistently: T = T_amb + R_th * P_total
        self.temperature = self.t_ambient + self.r_th * p_total

        return {
            "vdd": vdd,
            "freq_ghz": freq / 1e9,
            "p_dyn_mw": p_dyn * 1e3,
            "p_leak_mw": p_leak * 1e3,
            "p_total_mw": p_total * 1e3,
            "temp_celsius": self.temperature - 273.15,
        }

    def compute_breakeven_time(self) -> float:
        """
        Calculate the breakeven idle time (tau_breakeven):
        tau_breakeven = E_wake_overhead / P_leak_active
        If idle duration > tau_breakeven, entering power-gating saves net energy.
        """
        vdd, _ = self.dvfs_levels[self.current_dvfs_idx]
        p_leak_active = (
            vdd * 12.0e-3 * math.exp((self.temperature - 300.0) / 45.0)
        )
        return self.wake_energy_joules / p_leak_active if p_leak_active > 0 else 0.0


# =============================================================================
# Multi-Core Interconnect Power Sweep
# =============================================================================


def simulate_traffic_profile(
    routers: List[RouterPowerModel],
    traffic_profile: str,
    enable_power_gating: bool,
    enable_dvfs: bool,
) -> Dict[str, float]:
    """Simulate a 64-router fabric across bursty or uniform workload traces."""
    total_energy_joules = 0.0
    sim_time_sec = 1.0e-4  # 100 microseconds trace
    time_steps = 100
    dt = sim_time_sec / time_steps

    total_dyn_mw = 0.0
    total_leak_mw = 0.0

    for step in range(time_steps):
        # Determine current network load factor
        if traffic_profile == "bursty":
            # 20% active burst, 80% idle gap
            load = 0.75 if (step % 10 < 2) else 0.01
        else:
            # Steady 25% background load
            load = 0.25

        for r in routers:
            if enable_dvfs:
                # Local automatic rate adjustment (LAURA-NoC concept)
                if load > 0.6:
                    r.set_dvfs_mode(3)  # Turbo 1.05V, 1.6GHz
                elif load > 0.3:
                    r.set_dvfs_mode(2)  # High 0.90V, 1.2GHz
                elif load > 0.05:
                    r.set_dvfs_mode(1)  # Nominal 0.75V, 0.8GHz
                else:
                    r.set_dvfs_mode(0)  # Low 0.60V, 0.4GHz
            else:
                r.set_dvfs_mode(2)  # Fixed high performance baseline

            p_stats = r.compute_power(
                flit_rate_norm=load, power_gate_active=enable_power_gating
            )
            total_dyn_mw += p_stats["p_dyn_mw"]
            total_leak_mw += p_stats["p_leak_mw"]
            total_energy_joules += (p_stats["p_total_mw"] * 1e-3) * dt

    mean_dyn_w = (total_dyn_mw / (time_steps * len(routers))) * 1e-3
    mean_leak_w = (total_leak_mw / (time_steps * len(routers))) * 1e-3
    mean_temp_c = (
        sum(r.temperature - 273.15 for r in routers) / len(routers)
        if routers
        else 0.0
    )

    return {
        "profile": traffic_profile,
        "power_gating": enable_power_gating,
        "dvfs": enable_dvfs,
        "energy_micro_joules": total_energy_joules * 1e6,
        "avg_power_per_router_mw": (mean_dyn_w + mean_leak_w) * 1e3,
        "leakage_fraction_pct": (mean_leak_w / (mean_dyn_w + mean_leak_w) * 100)
        if (mean_dyn_w + mean_leak_w) > 0
        else 0.0,
        "mean_temp_celsius": mean_temp_c,
    }


def main():
    print("=" * 80)
    print("  Chapter 6: NoC Low-Power Architecture & Dark Silicon Simulator")
    print("  NoC Research Consortium (IEEE TCAD / TVLSI / TCAS-II Benchmarks)")
    print("=" * 80)

    # Instantiate an 8x8 (64-router) fabric
    num_routers = 64
    configs = [
        ("bursty", False, False, "Baseline (Fixed 0.9V/1.2GHz, No PG)"),
        ("bursty", True, False, "Ultrafine Power Gating (Matsutani et al.)"),
        ("bursty", False, True, "Distributed DVFS (LAURA-NoC)"),
        ("bursty", True, True, "Full Co-Design (DVFS + Ultrafine PG)"),
        ("uniform", False, False, "Uniform Baseline (Fixed 0.9V/1.2GHz)"),
        ("uniform", True, True, "Uniform Co-Design (DVFS + PG)"),
    ]

    header = f"{'Configuration':<42} | {'Energy (uJ)':>11} | {'Avg Pwr (mW)':>11} | {'Leak %':>7} | {'Temp (C)':>8}"
    print(header)
    print("-" * len(header))

    baseline_energy = None

    for profile, pg, dvfs, label in configs:
        routers = [RouterPowerModel(i) for i in range(num_routers)]
        res = simulate_traffic_profile(routers, profile, pg, dvfs)
        if baseline_energy is None and profile == "bursty" and not pg and not dvfs:
            baseline_energy = res["energy_micro_joules"]

        print(
            f"{label:<42} | "
            f"{res['energy_micro_joules']:>11.2f} | "
            f"{res['avg_power_per_router_mw']:>11.2f} | "
            f"{res['leakage_fraction_pct']:>6.1f}% | "
            f"{res['mean_temp_celsius']:>7.1f} C"
        )

    print("=" * 80)
    # Breakeven idle calculation
    sample_r = RouterPowerModel(0)
    breakeven_ns = sample_r.compute_breakeven_time() * 1e9
    print(
        f"[*] Power-Gating Breakeven Idle Threshold (tau_breakeven): {breakeven_ns:.2f} ns"
    )
    print(
        f"[*] At 1.2 GHz clock period (0.83 ns), sleep mode saves power if idle >= {int(math.ceil(breakeven_ns / 0.83))} cycles."
    )
    print("=" * 80)


if __name__ == "__main__":
    main()
