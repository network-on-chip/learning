#!/usr/bin/env python3
"""
===============================================================================
Channel Dependency Graph (CDG) & Routing Deadlock Freedom Verification Engine
Network-on-Chip (NoC) and Advanced Interconnects: Textbook Companion
Chapter 5: Deadlock Theory, Turn Models & Adaptive Routing

Grounded in:
- W. J. Dally and C. L. Seitz, "Deadlock-Free Message Routing in Multiprocessor
  Interconnection Networks," IEEE Trans. Computers, 1987.
- J. Duato, "A New Theory of Deadlock-Free Adaptive Routing in Wormhole
  Networks," IEEE TPDS, 1993.
- C. J. Glass and L. M. Ni, "The Turn Model for Adaptive Routing," JACM, 1994.
- G.-M. Chiu, "The Odd-Even Turn Model for Adaptive Routing," IEEE TPDS, 2000.
===============================================================================
"""

from collections import defaultdict
from typing import Dict, List, Set, Tuple


class ChannelDependencyGraph:
    """
    Channel Dependency Graph (CDG) D = (C, E_CDG).
    Vertices in C are physical/virtual channels: 'C(x1,y1->x2,y2)[VC]'.
    Directed edges in E_CDG represent valid flit transitions from an ingress
    channel to an egress channel at a router.
    """

    def __init__(self, name: str):
        self.name = name
        self.channels: Set[str] = set()
        self.adj: Dict[str, Set[str]] = defaultdict(set)

    def add_channel(self, ch: str):
        self.channels.add(ch)

    def add_dependency(self, ch_in: str, ch_out: str):
        """Add directed dependency: ch_out is requested after acquiring ch_in."""
        self.channels.add(ch_in)
        self.channels.add(ch_out)
        self.adj[ch_in].add(ch_out)

    def find_cycles(self) -> List[List[str]]:
        """
        Detect simple cycles in the CDG using DFS recursion stack tracking.
        """
        cycles = []
        visited = set()
        rec_stack = []
        stack_set = set()

        def dfs(u: str):
            visited.add(u)
            rec_stack.append(u)
            stack_set.add(u)

            for v in sorted(list(self.adj[u])):
                if v not in visited:
                    dfs(v)
                elif v in stack_set:
                    idx = rec_stack.index(v)
                    cycles.append(rec_stack[idx:] + [v])

            rec_stack.pop()
            stack_set.remove(u)

        for ch in sorted(list(self.channels)):
            if ch not in visited:
                dfs(ch)

        return cycles

    def verify_duato_escape(self, escape_channels: Set[str]) -> Tuple[bool, str]:
        """
        Verify Duato's Theorem (1993):
        An adaptive routing algorithm is deadlock-free iff there exists an escape
        subnetwork C1 that is strictly acyclic and reachable from any channel.
        """
        subgraph = ChannelDependencyGraph(f"{self.name} [Escape Subnetwork]")
        for ch in escape_channels:
            subgraph.add_channel(ch)
            for nbr in self.adj[ch]:
                if nbr in escape_channels:
                    subgraph.add_dependency(ch, nbr)

        escape_cycles = subgraph.find_cycles()
        if escape_cycles:
            return (
                False,
                f"FAILED: Escape subnetwork contains {len(escape_cycles)} cycle(s).",
            )

        for ch in self.channels:
            if ch not in escape_channels:
                q = [ch]
                seen = {ch}
                can_reach_escape = False
                while q:
                    curr = q.pop(0)
                    if curr in escape_channels:
                        can_reach_escape = True
                        break
                    for nxt in self.adj[curr]:
                        if nxt not in seen:
                            seen.add(nxt)
                            q.append(nxt)
                if not can_reach_escape:
                    return (
                        False,
                        f"FAILED: Channel {ch} cannot reach the escape subnetwork.",
                    )

        return (
            True,
            "PASSED: Connected escape subnetwork is strictly acyclic (Duato's Theorem holds).",
        )


# =============================================================================
# Turn Model & CDG Generators
# =============================================================================

OPPOSITE = {"E": "W", "W": "E", "N": "S", "S": "N"}
DELTA = {"E": (1, 0), "W": (-1, 0), "N": (0, 1), "S": (0, -1)}


def is_turn_allowed(in_dir: str, out_dir: str, policy: str) -> bool:
    """
    Check if a transition from in_dir to out_dir is permissible under the policy.
    In minimal routing, packets never make 180-degree U-turns (out_dir != OPPOSITE[in_dir]).
    """
    if out_dir == OPPOSITE[in_dir]:
        return False  # No 180-degree U-turns

    if policy == "xy":
        # Dimension-Order Routing: X first, then Y.
        # Prohibited turns: N->E, N->W, S->E, S->W (no Y->X turns)
        if in_dir in ["N", "S"] and out_dir in ["E", "W"]:
            return False
        return True

    elif policy == "fully_adaptive":
        # All 90-degree and straight turns allowed
        return True

    elif policy == "west_first":
        # Prohibit turns to the West: N->W and S->W
        if out_dir == "W" and in_dir in ["N", "S"]:
            return False
        return True

    elif policy == "north_last":
        # Prohibit turns from the North: N->E and N->W
        if in_dir == "N" and out_dir in ["E", "W"]:
            return False
        return True

    elif policy == "negative_first":
        # Negative directions (W, S) must be traversed before positive (E, N).
        # Prohibited turns: E->S, E->W, N->S, N->W
        if in_dir in ["E", "N"] and out_dir in ["W", "S"]:
            return False
        return True

    return True


def build_mesh_cdg(k: int, routing_policy: str) -> ChannelDependencyGraph:
    """Build the Channel Dependency Graph for a k x k Mesh."""
    cdg = ChannelDependencyGraph(f"{routing_policy.upper()} on {k}x{k} Mesh")

    def ch_name(x: int, y: int, direction: str, vc: int = 0) -> str:
        dx, dy = DELTA[direction]
        return f"C({x},{y}->{x+dx},{y+dy})[VC{vc}]"

    # Add all physical channels
    for y in range(k):
        for x in range(k):
            for d, (dx, dy) in DELTA.items():
                nx, ny = x + dx, y + dy
                if 0 <= nx < k and 0 <= ny < k:
                    cdg.add_channel(ch_name(x, y, d, 0))

    # Add dependencies between ingress channels and egress channels at each router (x, y)
    for y in range(k):
        for x in range(k):
            for in_d, (idx, idy) in DELTA.items():
                px, py = x - idx, y - idy
                if 0 <= px < k and 0 <= py < k:
                    in_ch = ch_name(px, py, in_d, 0)
                    for out_d, (odx, ody) in DELTA.items():
                        nx, ny = x + odx, y + ody
                        if 0 <= nx < k and 0 <= ny < k:
                            out_ch = ch_name(x, y, out_d, 0)
                            if is_turn_allowed(in_d, out_d, routing_policy):
                                cdg.add_dependency(in_ch, out_ch)

    return cdg


# =============================================================================
# Main Verification Suite
# =============================================================================


def main():
    print("=" * 80)
    print("  Chapter 5: Channel Dependency Graph (CDG) Deadlock Verification")
    print("  NoC Research Consortium (Dally-Seitz & Duato Formulations)")
    print("=" * 80)

    mesh_k = 3
    policies = ["xy", "fully_adaptive", "west_first", "north_last", "negative_first"]

    for pol in policies:
        cdg = build_mesh_cdg(mesh_k, pol)
        cycles = cdg.find_cycles()
        status = (
            "DEADLOCK-FREE (Acyclic CDG)"
            if len(cycles) == 0
            else f"DEADLOCK-PRONE ({len(cycles)} cycle(s))"
        )
        print(f"\n[*] Routing Policy: {pol.upper()} on {mesh_k}x{mesh_k} Mesh")
        print(f"    Total Physical Channels: {len(cdg.channels)}")
        print(f"    Channel Transitions:     {sum(len(v) for v in cdg.adj.values())}")
        print(f"    Cycle Count in CDG:      {len(cycles)}")
        print(f"    Verification Result:     {status}")

        if cycles:
            print("    Sample Dependency Cycle:")
            sample = cycles[0]
            print(f"      {' -> '.join(sample[:4])} ... -> {sample[0]}")

    print("\n" + "=" * 80)
    print("  Duato's Escape Subnetwork Theorem Evaluation")
    print("=" * 80)

    # Build 2-VC network: VC0 = XY Escape Subnetwork, VC1 = Adaptive Subnetwork
    duato_cdg = ChannelDependencyGraph("Duato Adaptive + XY Escape (3x3 Mesh)")
    escape_channels = set()
    k = 3

    def ch_name(x: int, y: int, direction: str, vc: int) -> str:
        dx, dy = DELTA[direction]
        return f"C({x},{y}->{x+dx},{y+dy})[VC{vc}]"

    for y in range(k):
        for x in range(k):
            for d, (dx, dy) in DELTA.items():
                nx, ny = x + dx, y + dy
                if 0 <= nx < k and 0 <= ny < k:
                    vc0 = ch_name(x, y, d, 0)
                    vc1 = ch_name(x, y, d, 1)
                    duato_cdg.add_channel(vc0)
                    duato_cdg.add_channel(vc1)
                    escape_channels.add(vc0)

    for y in range(k):
        for x in range(k):
            for in_d, (idx, idy) in DELTA.items():
                px, py = x - idx, y - idy
                if 0 <= px < k and 0 <= py < k:
                    in_vc0 = ch_name(px, py, in_d, 0)
                    in_vc1 = ch_name(px, py, in_d, 1)

                    for out_d, (odx, ody) in DELTA.items():
                        nx, ny = x + odx, y + ody
                        if 0 <= nx < k and 0 <= ny < k:
                            out_vc0 = ch_name(x, y, out_d, 0)
                            out_vc1 = ch_name(x, y, out_d, 1)

                            # VC0 -> VC0: Strict XY routing only
                            if is_turn_allowed(in_d, out_d, "xy"):
                                duato_cdg.add_dependency(in_vc0, out_vc0)

                            # VC1 -> VC1: Fully adaptive routing
                            if is_turn_allowed(in_d, out_d, "fully_adaptive"):
                                duato_cdg.add_dependency(in_vc1, out_vc1)

                            # VC1 -> VC0: Packets can escape from adaptive to escape VC!
                            if is_turn_allowed(in_d, out_d, "xy"):
                                duato_cdg.add_dependency(in_vc1, out_vc0)

    is_safe, msg = duato_cdg.verify_duato_escape(escape_channels)
    all_cycles = duato_cdg.find_cycles()
    print(f"[*] Total Network Channels (VC0 + VC1): {len(duato_cdg.channels)}")
    print(f"[*] Escape Subnetwork Channels (VC0):     {len(escape_channels)}")
    print(
        f"[*] Total Cycles in Combined CDG:       {len(all_cycles)} (Adaptive cycles permitted)"
    )
    print(f"[*] Duato Escape Theorem Check:          {msg}")
    print("=" * 80)


if __name__ == "__main__":
    main()
