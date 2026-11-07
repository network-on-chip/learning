#!/usr/bin/env python3
"""
Switching Techniques & Credit Flow Control Simulation.
Accompanying Code for Chapter 2: Switching Techniques, Flow Control & Buffer Management.
Author: NoC Community
"""

import math
from typing import Dict, List, Tuple


def calculate_zero_load_latencies(
    packet_length_flits: int,
    hop_count: int,
    router_latency_cycles: int = 2,
    link_latency_cycles: int = 1,
) -> Dict[str, float]:
    """
    Computes theoretical zero-load network latency for:
    1. Store-and-Forward (SAF): Whole packet buffered at every intermediate hop before forwarding.
    2. Virtual Cut-Through (VCT): Pipelined flit forwarding when output is free, but requires full packet buffering.
    3. Wormhole Switching: Pipelined flits spanning across multiple routers, buffer depth << packet size.
    """
    # Flit serialization latency at source
    t_serialize = packet_length_flits

    # Store-and-Forward: At every hop, router waits for entire packet to arrive before forwarding
    # T_SAF = H * (t_serialize + router_latency + link_latency)
    t_saf = hop_count * (packet_length_flits + router_latency_cycles + link_latency_cycles)

    # Virtual Cut-Through & Wormhole under zero load:
    # Head flit takes H * (router_latency + link_latency), subsequent flits arrive 1 per cycle
    # T_VCT = T_WH = (H * (router_latency + link_latency)) + (packet_length_flits - 1)
    t_vct_wh = (hop_count * (router_latency_cycles + link_latency_cycles)) + (packet_length_flits - 1)

    # Buffer memory requirement per router per Virtual Channel (in flits)
    buf_saf = packet_length_flits
    buf_vct = packet_length_flits
    buf_wh = 4  # Standard wormhole buffer depth (typically 2 to 4 flits)

    return {
        "packet_length": packet_length_flits,
        "hop_count": hop_count,
        "t_saf_cycles": t_saf,
        "t_vct_cycles": t_vct_wh,
        "t_wh_cycles": t_vct_wh,
        "speedup_vct_over_saf": t_saf / t_vct_wh,
        "buf_saf_flits": buf_saf,
        "buf_vct_flits": buf_vct,
        "buf_wh_flits": buf_wh,
        "buf_saving_wh_pct": ((buf_vct - buf_wh) / buf_vct) * 100.0,
    }


def simulate_credit_turnaround_loop(
    buffer_depth: int,
    link_flight_cycles: int = 1,
    rx_proc_cycles: int = 1,
    credit_flight_cycles: int = 1,
    tx_proc_cycles: int = 1,
    total_sim_cycles: int = 100,
) -> Tuple[float, int, int]:
    """
    Simulates credit-based flow control loop over total_sim_cycles.
    Returns: (link_utilization, flits_sent, stall_cycles)
    """
    rtt = link_flight_cycles + rx_proc_cycles + credit_flight_cycles + tx_proc_cycles

    credits_available = buffer_depth
    flits_sent = 0
    stall_cycles = 0

    # Flight queues
    forward_link_pipeline: List[Tuple[int, bool]] = []  # (arrival_cycle, has_flit)
    credit_link_pipeline: List[Tuple[int, bool]] = []   # (arrival_cycle, credit_pulse)
    rx_buffer_occupancy = 0

    for current_cycle in range(total_sim_cycles):
        # 1. Receiver consumes 1 flit per cycle if available and generates credit
        if rx_buffer_occupancy > 0:
            rx_buffer_occupancy -= 1
            # Credit generated; enters credit flight link
            credit_link_pipeline.append((current_cycle + rx_proc_cycles + credit_flight_cycles, True))

        # 2. Check arriving flits at receiver
        new_forward = []
        for arrival_cycle, has_flit in forward_link_pipeline:
            if arrival_cycle <= current_cycle:
                rx_buffer_occupancy += 1
            else:
                new_forward.append((arrival_cycle, has_flit))
        forward_link_pipeline = new_forward

        # 3. Check arriving credits at transmitter
        new_credits = []
        for arrival_cycle, credit_pulse in credit_link_pipeline:
            if arrival_cycle <= current_cycle:
                credits_available += 1
            else:
                new_credits.append((arrival_cycle, credit_pulse))
        credit_link_pipeline = new_credits

        # 4. Transmitter injects flit if credit available
        if credits_available > 0:
            credits_available -= 1
            flits_sent += 1
            forward_link_pipeline.append((current_cycle + tx_proc_cycles + link_flight_cycles, True))
        else:
            stall_cycles += 1

    link_utilization = flits_sent / total_sim_cycles
    return link_utilization, flits_sent, stall_cycles


def main():
    print("=" * 95)
    print(" SWITCHING TECHNIQUES LATENCY & BUFFER COMPARISON")
    print("=" * 95)
    print(f"{'Packet Flits':<14} | {'Hops':<6} | {'SAF Latency':<14} | {'VCT/WH Latency':<16} | {'Speedup':<10} | {'WH Buffer Saving':<18}")
    print("-" * 95)

    cases = [(4, 4), (8, 4), (16, 4), (32, 4), (16, 8), (32, 8), (64, 8)]
    for length, hops in cases:
        r = calculate_zero_load_latencies(length, hops)
        print(f"{r['packet_length']:<14} | {r['hop_count']:<6} | {r['t_saf_cycles']:<10} cyc | {r['t_wh_cycles']:<12} cyc | {r['speedup_vct_over_saf']:<8.2f}x | {r['buf_saving_wh_pct']:<16.1f}%")
    print("=" * 95)

    print("\n" + "=" * 95)
    print(" CREDIT ROUND-TRIP TIME (RTT) & MINIMUM BUFFER SIZING SIMULATION")
    print(" (RTT = 1 flight + 1 rx_proc + 1 credit_flight + 1 tx_proc = 4 cycles)")
    print("=" * 95)
    print(f"{'Buffer Depth (B)':<18} | {'RTT (Cycles)':<14} | {'Link Utilization':<18} | {'Flits Sent (100 cyc)':<22} | {'Stall Cycles':<14}")
    print("-" * 95)

    rtt_nominal = 1 + 1 + 1 + 1
    for b in range(1, 9):
        util, sent, stalls = simulate_credit_turnaround_loop(buffer_depth=b, total_sim_cycles=100)
        status = " (STALLING / UNDERFLOW)" if b < rtt_nominal else " (100% WIRE-RATE)"
        print(f"{b:<18} | {rtt_nominal:<14} | {util*100.0:<16.1f}% | {sent:<22} | {stalls:<14}{status}")
    print("=" * 95)


if __name__ == "__main__":
    main()
