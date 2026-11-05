// ============================================================================
// Module: topology_router_mesh_torus
// Description: Parameterized 5-Port Router Node supporting both 2D Mesh and
//              Folded Torus topology configurations with configurable link
//              pipeline registers and boundary boundary clamping.
//
// Chapter 4: Direct, Indirect & High-Radix Interconnect Topologies
// Grounded in:
// - Passas et al., "Crossbar NoCs Are Scalable Beyond 100 Nodes," IEEE TCAD 2012.
// - Jun et al., "Topology Synthesis of Cascaded Crossbar Switches," IEEE TCAD 2009.
// ============================================================================

`timescale 1ns / 1ps

module topology_router_mesh_torus #(
    parameter FLIT_WIDTH   = 64,
    parameter NODE_X       = 2,        // Current Router X coordinate
    parameter NODE_Y       = 2,        // Current Router Y coordinate
    parameter MESH_SIZE_X  = 4,        // Grid Width
    parameter MESH_SIZE_Y  = 4,        // Grid Height
    parameter IS_TORUS     = 0         // 0: 2D Mesh (clamp boundaries), 1: Folded Torus
)(
    input  wire                   clk,
    input  wire                   rst_n,

    // Ingress Physical Channels [0: North, 1: South, 2: East, 3: West, 4: Local]
    input  wire [4:0]             in_valid,
    input  wire [4:0][FLIT_WIDTH-1:0] in_flit,
    output wire [4:0]             in_ready,

    // Egress Physical Channels [0: North, 1: South, 2: East, 3: West, 4: Local]
    output reg  [4:0]             out_valid,
    output reg  [4:0][FLIT_WIDTH-1:0] out_flit,
    input  wire [4:0]             out_ready,

    // Boundary status flags
    output wire                   is_edge_x_min,
    output wire                   is_edge_x_max,
    output wire                   is_edge_y_min,
    output wire                   is_edge_y_max
);

    // Identify edge boundaries
    assign is_edge_x_min = (NODE_X == 0);
    assign is_edge_x_max = (NODE_X == MESH_SIZE_X - 1);
    assign is_edge_y_min = (NODE_Y == 0);
    assign is_edge_y_max = (NODE_Y == MESH_SIZE_Y - 1);

    // Port definitions
    localparam PORT_NORTH = 0;
    localparam PORT_SOUTH = 1;
    localparam PORT_EAST  = 2;
    localparam PORT_WEST  = 3;
    localparam PORT_LOCAL = 4;

    // Boundary active masks
    // If not a torus, boundary links that would cross off-chip are masked off
    wire [4:0] port_enabled;
    assign port_enabled[PORT_NORTH] = IS_TORUS ? 1'b1 : !is_edge_y_max;
    assign port_enabled[PORT_SOUTH] = IS_TORUS ? 1'b1 : !is_edge_y_min;
    assign port_enabled[PORT_EAST]  = IS_TORUS ? 1'b1 : !is_edge_x_max;
    assign port_enabled[PORT_WEST]  = IS_TORUS ? 1'b1 : !is_edge_x_min;
    assign port_enabled[PORT_LOCAL] = 1'b1;

    // Buffer ready handshakes
    assign in_ready = out_ready & port_enabled;

    // Combinational routing / link forward registers
    integer p;
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            out_valid <= 5'b00000;
            for (p = 0; p < 5; p = p + 1) begin
                out_flit[p] <= {FLIT_WIDTH{1'b0}};
            end
        end else begin
            for (p = 0; p < 5; p = p + 1) begin
                if (port_enabled[p]) begin
                    out_valid[p] <= in_valid[p];
                    out_flit[p]  <= in_flit[p];
                end else begin
                    out_valid[p] <= 1'b0;
                    out_flit[p]  <= {FLIT_WIDTH{1'b0}};
                end
            end
        end
    end

endmodule
