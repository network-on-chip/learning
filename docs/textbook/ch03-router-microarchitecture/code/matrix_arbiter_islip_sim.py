#!/usr/bin/env python3
"""
Matrix Arbiter & iSLIP Crossbar Allocation Simulator.
Accompanying Code for Chapter 3: High-Performance Router Microarchitecture & Arbitration.
Author: NoC Community
"""

import random
from typing import Dict, List, Tuple


class MatrixArbiter:
    """
    N-input Matrix Arbiter using a strict triangular priority matrix M[N][N].
    Priority rule: Client i has priority over Client j if M[i][j] == 1.
    Update rule on granting client k:
      Row k is cleared to 0: M[k][j] = 0 for all j != k (k becomes lowest priority)
      Column k is set to 1:  M[i][k] = 1 for all i != k (all other clients have priority over k)
    """

    def __init__(self, n: int):
        self.n = n
        # Initialize matrix: client i has priority over client j if i < j
        self.matrix = [[1 if i < j else 0 for j in range(n)] for i in range(n)]

    def arbitrate(self, requests: List[int]) -> int:
        """Returns the granted client index (0..n-1), or -1 if no requests."""
        grants = []
        for i in range(self.n):
            if not requests[i]:
                continue
            # Client i is granted if for all other requesting clients j, M[i][j] == 1
            has_priority = True
            for j in range(self.n):
                if i != j and requests[j] and not self.matrix[i][j]:
                    has_priority = False
                    break
            if has_priority:
                grants.append(i)

        if not grants:
            return -1

        winner = grants[0]
        # Update matrix state: Winner becomes Least Recently Used
        for j in range(self.n):
            if j != winner:
                self.matrix[winner][j] = 0
                self.matrix[j][winner] = 1
        return winner


def simulate_islip(
    num_inputs: int = 4,
    num_outputs: int = 4,
    iterations: int = 2,
    num_cycles: int = 500,
    load: float = 0.8,
) -> Dict[str, float]:
    """
    Simulates McKeown's iSLIP algorithm for an N x N crossbar switch.
    Phase 1: Request
    Phase 2: Grant (Round-robin among requests per output)
    Phase 3: Accept (Round-robin among grants per input)
    Pointers update only on iteration 1 for accepted matches.
    """
    # Round-robin pointers for outputs (grant phase) and inputs (accept phase)
    grant_ptrs = [0] * num_outputs
    accept_ptrs = [0] * num_inputs

    total_requests_generated = 0
    total_matches_made = 0

    for _ in range(num_cycles):
        # Generate random Bernoulli traffic matrix
        req_matrix = [
            [1 if random.random() < load else 0 for _ in range(num_outputs)]
            for _ in range(num_inputs)
        ]
        total_requests_generated += sum(sum(row) for row in req_matrix)

        unmatched_inputs = set(range(num_inputs))
        unmatched_outputs = set(range(num_outputs))
        matched_pairs: List[Tuple[int, int]] = []

        # iSLIP Iterations
        for iter_idx in range(iterations):
            # Step 1: Grant Phase (Each unmatched output chooses one requesting input)
            output_grants: Dict[int, int] = {}  # output -> input
            for out_port in list(unmatched_outputs):
                ptr = grant_ptrs[out_port]
                # Search cyclically starting from grant_ptrs[out_port]
                for offset in range(num_inputs):
                    in_port = (ptr + offset) % num_inputs
                    if in_port in unmatched_inputs and req_matrix[in_port][out_port]:
                        output_grants[out_port] = in_port
                        break

            # Step 2: Accept Phase (Each unmatched input chooses one granting output)
            input_accepts: Dict[int, int] = {}  # input -> output
            for in_port in list(unmatched_inputs):
                ptr = accept_ptrs[in_port]
                # Search cyclically starting from accept_ptrs[in_port]
                for offset in range(num_outputs):
                    out_port = (ptr + offset) % num_outputs
                    if out_port in output_grants and output_grants[out_port] == in_port:
                        input_accepts[in_port] = out_port
                        break

            # Step 3: Record new matches & Update pointers on iteration 1
            for in_port, out_port in input_accepts.items():
                matched_pairs.append((in_port, out_port))
                unmatched_inputs.remove(in_port)
                unmatched_outputs.remove(out_port)
                # Clear request in current matrix
                req_matrix[in_port][out_port] = 0

                if iter_idx == 0:
                    grant_ptrs[out_port] = (in_port + 1) % num_inputs
                    accept_ptrs[in_port] = (out_port + 1) % num_outputs

        total_matches_made += len(matched_pairs)

    avg_matches_per_cycle = total_matches_made / num_cycles
    crossbar_efficiency = avg_matches_per_cycle / min(num_inputs, num_outputs)

    return {
        "num_inputs": num_inputs,
        "num_outputs": num_outputs,
        "iterations": iterations,
        "load": load,
        "avg_matches_per_cycle": avg_matches_per_cycle,
        "crossbar_efficiency_pct": crossbar_efficiency * 100.0,
    }


def main():
    print("=" * 85)
    print(" MATRIX ARBITER (LRU HARDWARE DEMONSTRATION)")
    print("=" * 85)
    arb = MatrixArbiter(n=4)
    print("Initial Triangular Priority Matrix M (Row i has priority over Col j if 1):")
    for row in arb.matrix:
        print("  ", row)

    requests_sequence = [
        [1, 1, 0, 1], # Client 0, 1, 3 request -> Client 0 should win
        [1, 1, 0, 1], # Client 0, 1, 3 request -> Client 1 should win (0 was LRU)
        [1, 1, 0, 1], # Client 0, 1, 3 request -> Client 3 should win (0, 1 were LRU)
        [1, 1, 0, 1], # Client 0, 1, 3 request -> Client 0 should win again
    ]

    for cycle, req in enumerate(requests_sequence):
        winner = arb.arbitrate(req)
        print(f"Cycle {cycle+1}: Requests = {req} -> Granted Winner = Client {winner}")

    print("\n" + "=" * 85)
    print(" MCKEOWN'S iSLIP ITERATIVE MATCHING SIMULATION (4x4 CROSSBAR, 500 CYCLES)")
    print("=" * 85)
    print(f"{'Offered Load':<14} | {'Iterations':<12} | {'Avg Matches/Cycle':<20} | {'Crossbar Efficiency':<20}")
    print("-" * 85)

    loads = [0.3, 0.5, 0.7, 0.9, 1.0]
    for ld in loads:
        for iters in [1, 2, 4]:
            res = simulate_islip(num_inputs=4, num_outputs=4, iterations=iters, num_cycles=500, load=ld)
            print(f"{ld*100.0:<12.0f}% | {iters:<12} | {res['avg_matches_per_cycle']:<20.2f} | {res['crossbar_efficiency_pct']:<18.1f}%")
    print("=" * 85)


if __name__ == "__main__":
    main()
