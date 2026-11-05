#!/usr/bin/env python3
"""
Optical Network-on-Chip (ONoC) & Wavelength-Routed ONoC (WRONoC)
Optical Link Budget, Insertion Loss & Laser Power Simulation Model.

Grounded in:
1. W.-Y. Kao, T.-J. Lin, and Y.-W. Chang, "Provably Good Physically Aware
   WRONoC Design for Customized and Fault-Tolerant Topologies With Parallel
   Switching Elements and Sequence-Based Models", IEEE TCAD 2026.
2. Y. Ye et al., "System-Level Modeling and Analysis of Thermal Effects
   in Optical Networks-on-Chip", IEEE TVLSI 2013.
3. M. Shahmoradi et al., "Channel-Aware Behavioral Power Modeling of CMOS
   OOK Transceivers for Wireless Network-on-Chip Systems", IEEE TCAS-I 2026.
"""

from __future__ import annotations
import math
from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class OpticalPhysicalParams:
    """Physical optical parameters in silicon nanophotonics."""
    waveguide_prop_loss_db_per_cm: float = 0.25   # dB/cm propagation loss
    waveguide_bend_loss_db: float = 0.005          # dB per 90-degree bend
    waveguide_crossing_loss_db: float = 0.12       # dB per waveguide crossing
    mrr_through_loss_db: float = 0.015             # dB off-resonance through loss
    mrr_drop_loss_db: float = 0.50                 # dB on-resonance drop loss
    modulator_insertion_loss_db: float = 1.20      # dB electro-optic Mach-Zehnder or MRR modulator
    photodetector_responsivity_a_w: float = 0.85   # A/W Ge-on-Si photodiode
    photodetector_sensitivity_dbm: float = -20.0   # dBm receiver sensitivity for BER = 1e-12
    laser_wall_plug_efficiency: float = 0.20       # Wall-plug efficiency of DFB laser (20%)
    thermo_optic_coefficient: float = 1.86e-4      # dn/dT of silicon (K^-1)
    mrr_thermal_sensitivity_nm_c: float = 0.10     # dlambda/dT = ~0.10 nm/°C
    microheater_efficiency_mw_nm: float = 18.0     # Thermal tuning power per nm redshift (mW/nm)


class ONoCLinkBudgetModel:
    """Evaluates optical insertion losses, laser power budgets, and thermal tuning costs."""

    def __init__(self, params: OpticalPhysicalParams | None = None):
        self.p = params or OpticalPhysicalParams()

    def calculate_path_loss(
        self,
        waveguide_length_cm: float,
        num_bends: int,
        num_crossings: int,
        num_mrr_through: int,
        num_mrr_drops: int
    ) -> float:
        """
        Calculates end-to-end optical insertion loss along a lightpath (in dB).
        """
        l_prop = waveguide_length_cm * self.p.waveguide_prop_loss_db_per_cm
        l_bend = num_bends * self.p.waveguide_bend_loss_db
        l_cross = num_crossings * self.p.waveguide_crossing_loss_db
        l_thru = num_mrr_through * self.p.mrr_through_loss_db
        l_drop = num_mrr_drops * self.p.mrr_drop_loss_db
        l_mod = self.p.modulator_insertion_loss_db

        total_loss_db = l_prop + l_bend + l_cross + l_thru + l_drop + l_mod
        return total_loss_db

    def calculate_laser_power_mw(self, max_insertion_loss_db: float) -> Tuple[float, float]:
        """
        Calculates required optical laser output power and electrical wall-plug power (mW).
        P_laser_out(dBm) = P_rx_sens(dBm) + L_max(dB) + Margin(3dB)
        """
        optical_margin_db = 3.0
        p_laser_dbm = self.p.photodetector_sensitivity_dbm + max_insertion_loss_db + optical_margin_db
        p_laser_optical_mw = 10.0 ** (p_laser_dbm / 10.0)
        p_laser_wall_plug_mw = p_laser_optical_mw / self.p.laser_wall_plug_efficiency
        return p_laser_optical_mw, p_laser_wall_plug_mw

    def calculate_thermal_tuning_power(self, temperature_delta_c: float, num_mrrs: int) -> float:
        """
        Calculates total microheater tuning power required to stabilize resonant wavelengths.
        Shift Delta_lambda = (dlambda/dT) * Delta_T.
        P_tune = N_mrr * Delta_lambda * microheater_efficiency_mw_nm.
        """
        delta_lambda_nm = abs(temperature_delta_c) * self.p.mrr_thermal_sensitivity_nm_c
        p_tune_total_mw = num_mrrs * delta_lambda_nm * self.p.microheater_efficiency_mw_nm
        return p_tune_total_mw


def evaluate_cse_vs_pse_topologies() -> Dict[str, Dict[str, float]]:
    """
    Compares Crossing Switching Element (CSE) vs. Parallel Switching Element (PSE)
    architectures in an 8x8 optical mesh interconnect (64 cores, 20mm x 20mm chip).
    Grounded in Kao et al. (IEEE TCAD 2026).
    """
    model = ONoCLinkBudgetModel()

    # Scenario A: 8x8 ONoC with Crossing Switching Elements (CSEs - 90 deg / 270 deg)
    # Conventional grid template suffers high crossing counts and longer waveguide routing.
    cse_wg_length_cm = 4.8  # cm
    cse_bends = 24
    cse_crossings = 62      # High crossing count due to orthogonal waveguide grid
    cse_mrr_through = 28
    cse_mrr_drop = 2
    num_mrrs_cse = 192

    # Scenario B: 8x8 ONoC with Parallel Switching Elements (PSEs - ADF Sequence-based)
    # Kao et al. TCAD 2026: parallel waveguides avoid crossings inside switching elements.
    pse_wg_length_cm = 3.9  # cm (-19% shorter routing)
    pse_bends = 18
    pse_crossings = 24      # -61% fewer crossings
    pse_mrr_through = 16
    pse_mrr_drop = 2
    num_mrrs_pse = 112      # -41.6% fewer MRRs

    # Insertion loss evaluations
    cse_loss = model.calculate_path_loss(cse_wg_length_cm, cse_bends, cse_crossings, cse_mrr_through, cse_mrr_drop)
    pse_loss = model.calculate_path_loss(pse_wg_length_cm, pse_bends, pse_crossings, pse_mrr_through, pse_mrr_drop)

    cse_laser_opt, cse_laser_elec = model.calculate_laser_power_mw(cse_loss)
    pse_laser_opt, pse_laser_elec = model.calculate_laser_power_mw(pse_loss)

    # Thermal drift tuning under 15°C across-die gradient
    temp_delta = 15.0
    cse_tune_power = model.calculate_thermal_tuning_power(temp_delta, num_mrrs_cse)
    pse_tune_power = model.calculate_thermal_tuning_power(temp_delta, num_mrrs_pse)

    results = {
        "CSE_Architecture": {
            "max_loss_db": cse_loss,
            "crossing_count": cse_crossings,
            "mrr_count": num_mrrs_cse,
            "laser_optical_mw": cse_laser_opt,
            "laser_wall_plug_mw": cse_laser_elec,
            "thermal_tuning_mw": cse_tune_power,
            "total_power_mw": cse_laser_elec + cse_tune_power
        },
        "PSE_Architecture": {
            "max_loss_db": pse_loss,
            "crossing_count": pse_crossings,
            "mrr_count": num_mrrs_pse,
            "laser_optical_mw": pse_laser_opt,
            "laser_wall_plug_mw": pse_laser_elec,
            "thermal_tuning_mw": pse_tune_power,
            "total_power_mw": pse_laser_elec + pse_tune_power
        }
    }
    return results


def print_evaluation_report(results: Dict[str, Dict[str, float]]) -> None:
    cse = results["CSE_Architecture"]
    pse = results["PSE_Architecture"]

    print("=" * 70)
    print(" Optical Network-on-Chip (ONoC) Insertion Loss & Power Budget Analysis")
    print(" Comparative Study: Crossing (CSE) vs. Parallel (PSE) Switching Elements")
    print(" Grounded in: Kao et al. (IEEE TCAD 2026) & Ye et al. (IEEE TVLSI 2013)")
    print("=" * 70)
    print(f"{'Performance Metric':<35} | {'CSE Architecture':<16} | {'PSE Architecture':<16}")
    print("-" * 70)
    print(f"{'Waveguide Crossings':<35} | {cse['crossing_count']:<16} | {pse['crossing_count']:<16}")
    print(f"{'Active MRR Count':<35} | {cse['mrr_count']:<16} | {pse['mrr_count']:<16}")
    print(f"{'Worst-Case Insertion Loss (dB)':<35} | {cse['max_loss_db']:<16.2f} | {pse['max_loss_db']:<16.2f}")
    print(f"{'Required Optical Laser Power (mW)':<35} | {cse['laser_optical_mw']:<16.2f} | {pse['laser_optical_mw']:<16.2f}")
    print(f"{'Laser Wall-Plug Electrical Power':<35} | {cse['laser_wall_plug_mw']:<16.2f} | {pse['laser_wall_plug_mw']:<16.2f}")
    print(f"{'MRR Thermal Tuning Power (mW)':<35} | {cse['thermal_tuning_mw']:<16.2f} | {pse['thermal_tuning_mw']:<16.2f}")
    print(f"{'Total Optical Subsystem Power (mW)':<35} | {cse['total_power_mw']:<16.2f} | {pse['total_power_mw']:<16.2f}")
    print("-" * 70)

    loss_reduction = cse["max_loss_db"] - pse["max_loss_db"]
    power_reduction = (cse["total_power_mw"] - pse["total_power_mw"]) / cse["total_power_mw"] * 100.0
    print(f"Summary: PSE architecture reduces optical insertion loss by {loss_reduction:.2f} dB")
    print(f"         and slashes total optical power dissipation by {power_reduction:.1f}%!")
    print("=" * 70)


if __name__ == "__main__":
    res = evaluate_cse_vs_pse_topologies()
    print_evaluation_report(res)

