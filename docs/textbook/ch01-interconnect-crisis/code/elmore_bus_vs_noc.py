#!/usr/bin/env python3
"""
Elmore Delay & Scaling Comparison: Shared Multi-Drop Bus vs. Crossbar vs. 2D Mesh NoC.
Accompanying Code for Chapter 1: The Multi-Core Communication Crisis & Interconnect Physics.
Author: NoC-Lab Community
"""

import math
import sys
from typing import Dict, List, Tuple


def calculate_copper_resistivity(
    w_nm: float,
    bulk_rho: float = 1.68e-8,
    mean_free_path_nm: float = 39.0,
    specularity_p: float = 0.2,
    reflectivity_r: float = 0.3,
    barrier_thickness_nm: float = 1.5,
) -> float:
    """
    Computes effective copper resistivity under Mayadas-Shatzkes and Fuchs-Sondheimer models.
    Takes into account thin barrier liners (Ta/TaN or Co/Ru) that reduce conducting Cu cross-section.
    """
    w_eff = max(w_nm - 2 * barrier_thickness_nm, 0.5)
    # Fuchs-Sondheimer surface scattering
    k = w_eff / mean_free_path_nm
    c_fs = 1.0 + (3.0 / (8.0 * k)) * (1.0 - specularity_p)

    # Mayadas-Shatzkes grain boundary scattering
    alpha = (mean_free_path_nm / w_eff) * (reflectivity_r / (1.0 - reflectivity_r))
    f_alpha = 1.0 - 1.5 * alpha + 3.0 * (alpha**2) - 3.0 * (alpha**3) * math.log(1.0 + 1.0 / alpha)
    c_ms = 1.0 / max(f_alpha, 0.01)

    rho_eff = bulk_rho * c_fs * c_ms
    # Geometric penalty from non-conducting barrier liner
    area_total = w_nm * w_nm
    area_cu = w_eff * w_eff
    rho_total = rho_eff * (area_total / area_cu)
    return rho_total


def evaluate_interconnect_scaling(core_counts: List[int]) -> List[Dict[str, float]]:
    """
    Evaluates physical interconnect metrics across core counts (N = 2 to 256):
    - Bus Propagation Delay (Elmore Model)
    - Full Crossbar Area Complexity
    - 2D Mesh NoC Zero-Load Latency & Aggregate Bandwidth
    """
    results = []

    # Process parameters (typical 16nm / 7nm baseline)
    r_driver = 500.0        # Driver resistance (Ohms)
    r_wire_per_mm = 800.0   # Wire resistance (Ohms/mm)
    c_wire_per_mm = 0.18e-12# Wire capacitance (F/mm)
    c_tap = 8e-15           # Master/slave tap capacitance (F)
    f_local_clk = 2.0e9     # Core clock (2.0 GHz)
    die_edge_mm = 12.0      # Die size: 12 mm x 12 mm
    bus_width_bits = 128    # 128-bit bus

    for N in core_counts:
        # 1. Shared Bus Scaling
        # Long bus spans across die edge
        wire_length_mm = die_edge_mm
        r_wire = r_wire_per_mm * wire_length_mm
        c_wire = c_wire_per_mm * wire_length_mm
        c_taps_total = N * c_tap

        # Elmore delay: tau_bus ~ 0.38 * R_wire * C_wire + R_driver * (C_wire + C_taps) + 0.5 * R_wire * C_taps
        tau_bus = (0.38 * r_wire * c_wire) + (r_driver * (c_wire + c_taps_total)) + (0.5 * r_wire * c_taps_total)
        f_max_bus_ghz = (1.0 / (2.0 * tau_bus)) / 1e9

        # Aggregate Bus Bandwidth (serialized medium: only 1 transaction at a time)
        bw_bus_gbps = (bus_width_bits * min(f_max_bus_ghz * 1e9, f_local_clk)) / 8e9

        # 2. Monolithic Crossbar Scaling
        crosspoints = N * N
        crossbar_wiring_tracks = N * bus_width_bits

        # 3. 2D Mesh NoC Scaling (sqrt(N) x sqrt(N))
        grid_dim = int(math.ceil(math.sqrt(N)))
        tile_pitch_mm = die_edge_mm / grid_dim
        # Short point-to-point link
        r_link = r_wire_per_mm * tile_pitch_mm
        c_link = c_wire_per_mm * tile_pitch_mm
        tau_link = (0.38 * r_link * c_link) + (r_driver * (c_link + 2 * c_tap))
        f_max_link_ghz = (1.0 / (2.0 * tau_link)) / 1e9

        # Average hop count in 2D mesh: (2/3) * sqrt(N)
        avg_hops = (2.0 / 3.0) * grid_dim
        # 2-cycle router pipeline + 1-cycle link
        zero_load_latency_cycles = avg_hops * (2 + 1)
        zero_load_latency_ns = (zero_load_latency_cycles / 2.0) # at 2 GHz

        # Bisection bandwidth = grid_dim * 2 * link_width * frequency
        bisection_bw_gbps = (grid_dim * 2 * bus_width_bits * 2.0e9) / 8e9

        results.append({
            "cores": N,
            "bus_delay_ps": tau_bus * 1e12,
            "bus_fmax_mhz": f_max_bus_ghz * 1000.0,
            "bus_agg_bw_gbps": bw_bus_gbps,
            "crossbar_crosspoints": crosspoints,
            "noc_link_fmax_ghz": f_max_link_ghz,
            "noc_zero_load_ns": zero_load_latency_ns,
            "noc_bisection_bw_gbps": bisection_bw_gbps,
        })

    return results


def main():
    cores = [2, 4, 8, 16, 32, 64, 128, 256]
    data = evaluate_interconnect_scaling(cores)

    print("=" * 95)
    print(" INTERCONNECT SCALING STUDY: SHARED BUS vs. CROSSBAR vs. 2D MESH NoC")
    print("=" * 95)
    print(f"{'Cores':<6} | {'Bus Delay (ps)':<14} | {'Bus Fmax':<12} | {'Bus BW (GB/s)':<14} | {'XBar Switches':<14} | {'NoC Bisection BW':<18}")
    print("-" * 95)
    for r in data:
        print(f"{r['cores']:<6} | {r['bus_delay_ps']:<14.1f} | {r['bus_fmax_mhz']:<10.1f} MHz | {r['bus_agg_bw_gbps']:<14.2f} | {r['crossbar_crosspoints']:<14} | {r['noc_bisection_bw_gbps']:<14.1f} GB/s")
    print("=" * 95)

    print("\n[Mayadas-Shatzkes Sub-14nm Copper Resistivity Surge]")
    widths = [65.0, 45.0, 32.0, 22.0, 14.0, 7.0, 5.0, 3.0]
    for w in widths:
        rho = calculate_copper_resistivity(w)
        rho_ratio = rho / 1.68e-8
        print(f"  Wire Width: {w:4.1f} nm -> Effective Resistivity: {rho*1e8:5.2f} uOhm-cm ({rho_ratio:4.2f}x of bulk Cu)")


if __name__ == "__main__":
    main()
