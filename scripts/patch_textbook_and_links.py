import os

# 1. Update textbook/index.md
p = 'share/learning/docs/textbook/index.md'
with open(p, 'r', encoding='utf-8') as f:
    c = f.read()

old_table = """| **Ch 1: Interconnect Crisis & Wire Physics** | [Track 1: Fundamentals](../track1-fundamentals/index.md) | [Wire Wizard: Interconnect Physics](../interactive/wire.md) | `bus_arbiter_contention.v` |
| **Ch 2: Switching, Flow Control & Buffers** | [Track 1: Fundamentals](../track1-fundamentals/index.md) | [Credit Commander: Flow Control](../interactive/credits.md) | `credit_counter.v` |
| **Ch 3: Router Microarchitecture & Arbitration** | [Track 2: Router Microarchitecture](../track2-router-architecture/index.md) | [Arbiter Arena: Crossbar Clash](../interactive/arbiter.md) | `matrix_arbiter_4x4.v` |
| **Ch 4: Direct, Indirect & High-Radix Topologies** | [Track 3: Topologies & Metrics](../track3-topologies/index.md) | [Topology Titans: Graph Architect](../interactive/topology.md) | `topology_graph_metrics.v` |
| **Ch 5: Deadlock Theory & Turn Models** | [Track 4: Routing & Deadlock](../track4-routing-deadlock/index.md) | [Deadlock Buster & Packet Master](../interactive/game.md) | `escape_vc_router.v` |
| **Ch 6: Low Power & Dark Silicon** | [Track 5: Thermal & Congestion](../track5-congestion-thermal/index.md) | [Volt Vortex & Deflection Duel](../interactive/power.md) | `power_gating_router_fsm.v` |
| **Ch 7: Thermal Modeling & Fault Tolerance** | [Track 5: Thermal & Congestion](../track5-congestion-thermal/index.md) | [Hotspot Hero & Fault Defender](../interactive/hotspot.md) | `fault_tolerant_router_bypass.v` |
| **Ch 8: 3D-NoC & TSVs** | [Track 6: Chiplets & 3D NoC](../track6-chiplets-and-3d/index.md) | [TSV Titan: 3D-NoC Architect](../interactive/tsv3d.md) | `tsv_arbiter_3d.v` |
| **Ch 9: Multi-Chiplets & UCIe** | [Track 6: Chiplets & 3D NoC](../track6-chiplets-and-3d/index.md) | [Chiplet Tycoon: Advanced Packaging](../interactive/chiplet.md) | `chiplet_bridge_protocol.v` |
| **Ch 10: Optical & Wireless NoC** | [Track 6: Chiplets & 3D NoC](../track6-chiplets-and-3d/index.md) | [Photon Pilot & Wireless Wave](../interactive/optical.md) | `photonic_mrr_switch.v` |
| **Ch 11: Hardware Security & Trust** | [Track 8: Hardware Security](../interactive/security.md) | [Silicon Sentinel Arcade Game](../interactive/security.md) | `wma_thermal_detector.sv` |
| **Ch 12: AI, LLM & Neuromorphic NoC** | [Track 9: AI Interconnects](../interactive/transformer.md) | [Transformer Titan & Neuromorphic Nexus](../interactive/transformer.md) | `in_network_reduction_router.sv` |"""

new_table = """| **Ch 1: Interconnect Crisis & Wire Physics** | [Track 1: Interconnect Crisis](../track1-interconnect-crisis/index.md) | [Wire Wizard: Interconnect Physics](../interactive/wire.md) | `bus_arbiter_contention.v` |
| **Ch 2: Switching, Flow Control & Buffers** | [Track 2: Switching & Flow Control](../track2-switching-flow-control/index.md) | [Credit Commander: Flow Control](../interactive/credits.md) | `credit_counter.v` |
| **Ch 3: Router Microarchitecture & Arbitration** | [Track 3: Router Microarchitecture](../track3-router-microarchitecture/index.md) | [Arbiter Arena: Crossbar Clash](../interactive/arbiter.md) | `matrix_arbiter_4x4.v` |
| **Ch 4: Direct, Indirect & High-Radix Topologies** | [Track 4: Topologies & Metrics](../track4-topologies-and-metrics/index.md) | [Topology Titans: Graph Architect](../interactive/topology.md) | `topology_graph_metrics.v` |
| **Ch 5: Deadlock Theory & Turn Models** | [Track 5: Deadlock Theory & Routing](../track5-routing-deadlock/index.md) | [Deadlock Buster & Packet Master](../interactive/game.md) | `escape_vc_router.v` |
| **Ch 6: Low Power & Dark Silicon** | [Track 6: Low Power & Dark Silicon](../track6-low-power-dark-silicon/index.md) | [Volt Vortex & Deflection Duel](../interactive/power.md) | `power_gating_router_fsm.v` |
| **Ch 7: Thermal Modeling & Fault Tolerance** | [Track 7: Thermal & Fault Tolerance](../track7-thermal-fault-tolerance/index.md) | [Hotspot Hero & Fault Defender](../interactive/hotspot.md) | `fault_tolerant_router_bypass.v` |
| **Ch 8: 3D-NoC & TSVs** | [Track 8: 3D-NoC & TSVs](../track8-3d-noc-tsvs/index.md) | [TSV Titan: 3D-NoC Architect](../interactive/tsv3d.md) | `tsv_arbiter_3d.v` |
| **Ch 9: Multi-Chiplets & UCIe** | [Track 9: Multi-Chiplets & UCIe](../track9-chiplets-ucie/index.md) | [Chiplet Tycoon: Advanced Packaging](../interactive/chiplet.md) | `chiplet_bridge_protocol.v` |
| **Ch 10: Optical & Wireless NoC** | [Track 10: Optical & Wireless NoC](../track10-optical-wireless/index.md) | [Photon Pilot & Wireless Wave](../interactive/optical.md) | `photonic_mrr_switch.v` |
| **Ch 11: Hardware Security & Trust** | [Track 11: Hardware Security](../track11-security/index.md) | [Silicon Sentinel Arcade Game](../interactive/security.md) | `wma_thermal_detector.sv` |
| **Ch 12: AI, LLM & Neuromorphic NoC** | [Track 12: AI & LLM Interconnects](../track12-ai-llm-snn/index.md) | [Transformer Titan & Neuromorphic Nexus](../interactive/transformer.md) | `in_network_reduction_router.sv` |
| **Synthesis: Capstone Systems** | [Track 13: Capstone System Synthesis](../track13-capstone/index.md) | [Web EDA Unix Terminal Workbench](../interactive/terminal.md) | `secure_moe_router_top.sv` |"""

if old_table in c:
    c = c.replace(old_table, new_table)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(c)
    print('Patched textbook/index.md table')
else:
    print('Warning: old_table not found in textbook/index.md')

# Chapter badges
badge_updates = [
    ('ch01-interconnect-crisis/index.md',
     'https://network-on-chip.github.io/learning/track1-fundamentals/',
     '../../track1-interconnect-crisis/'),
    ('ch02-switching-flow-control/index.md',
     'https://network-on-chip.github.io/learning/track1-fundamentals/',
     '../../track2-switching-flow-control/'),
    ('ch02-switching-flow-control/index.md',
     'Track%201%3A%20Fundamentals-blue',
     'Track%202%3A%20Switching%20%26%20Flow-blue'),
    ('ch03-router-microarchitecture/index.md',
     'https://network-on-chip.github.io/learning/track2-router-architecture/',
     '../../track3-router-microarchitecture/'),
    ('ch04-topologies-and-metrics/index.md',
     'https://network-on-chip.github.io/learning/track3-topologies/',
     '../../track4-topologies-and-metrics/'),
    ('ch05-routing-deadlock-theory/index.md',
     'https://network-on-chip.github.io/learning/track4-routing-deadlock/',
     '../../track5-routing-deadlock/'),
    ('ch06-low-power-dark-silicon/index.md',
     'https://network-on-chip.github.io/learning/track5-thermal-congestion/',
     '../../track6-low-power-dark-silicon/'),
    ('ch06-low-power-dark-silicon/index.md',
     'Track%205%3A%20Energy-blue',
     'Track%206%3A%20Dark%20Silicon-blue'),
    ('ch07-thermal-fault-tolerance/index.md',
     'https://network-on-chip.github.io/learning/track5-congestion-thermal/',
     '../../track7-thermal-fault-tolerance/'),
    ('ch07-thermal-fault-tolerance/index.md',
     'Track%205%3A%20Thermal%20%26%20Congestion-blue',
     'Track%207%3A%20Thermal%20%26%20Faults-blue'),
    ('ch08-3d-noc-tsvs/index.md',
     'https://network-on-chip.github.io/learning/track6-chiplets-and-3d/',
     '../../track8-3d-noc-tsvs/'),
    ('ch08-3d-noc-tsvs/index.md',
     'Track%206%3A%20Chiplets%20%26%203D-blue',
     'Track%208%3A%203D%20TSVs-blue'),
    ('ch09-chiplets-ucie/index.md',
     'https://network-on-chip.github.io/learning/track6-chiplets-and-3d/',
     '../../track9-chiplets-ucie/'),
    ('ch09-chiplets-ucie/index.md',
     'Track%206%3A%20Chiplets%20%26%203D-blue',
     'Track%209%3A%20UCIe%20Chiplets-blue'),
    ('ch10-optical-wireless/index.md',
     'https://network-on-chip.github.io/learning/track7-emerging-frontiers/',
     '../../track10-optical-wireless/'),
    ('ch10-optical-wireless/index.md',
     'Track%207%3A%20Emerging%20Frontiers-blue',
     'Track%2010%3A%20Optical%20%26%20Wireless-blue'),
    ('ch11-security/index.md',
     '../../interactive/security/',
     '../../track11-security/'),
    ('ch12-ai-llm-snn/index.md',
     '../../interactive/transformer/',
     '../../track12-ai-llm-snn/')
]

for ch_rel, old_s, new_s in badge_updates:
    ch_path = os.path.join('share/learning/docs/textbook', ch_rel)
    if os.path.exists(ch_path):
        with open(ch_path, 'r', encoding='utf-8') as f:
            fc = f.read()
        if old_s in fc:
            fc = fc.replace(old_s, new_s)
            with open(ch_path, 'w', encoding='utf-8') as f:
                f.write(fc)
            print(f'Updated badge in {ch_rel}')
        else:
            print(f'Badge target not in {ch_rel}: {old_s[:30]}...')
