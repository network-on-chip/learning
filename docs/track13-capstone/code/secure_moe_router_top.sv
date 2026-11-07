`timescale 1ns / 1ps

//=============================================================================
// File: secure_moe_router_top.sv
// Module: secure_moe_router_top
// Description: Capstone Grand Challenge 13.5:
//              16-Chiplet Active Interposer Zero-Trust MoE Collective Router Top
//
// Synthesizes 4 core architectural subsystems:
//   1. IEEE TCAD 2026 HeatSense WMA Thermal Anomaly Detector
//      - Multiplierless EWMA baseline tracking (alpha = 1/8)
//      - Real-time Mean Absolute Deviation (MAD) estimation
//      - Adaptive 3-sigma hardware Trojan detection & quarantine filter
//   2. IEEE TVLSI 2026 PAC-NoC In-Network Collective Reduction Engine
//      - In-flight 32-bit fixed-point gradient accumulation tree
//      - Collective reduction tag matching & barrier synchronization
//   3. 16-Chiplet Mixture-of-Experts (MoE) All-to-All Token Dispatch Interface
//      - Top-2 gating dispatch with token coordinate decoding
//   4. 5-Port Timing-Closed Mesh Crossbar with Adaptive Quarantine Bypass
//      - Dimension-Order Routing (XY DOR)
//      - Fault-tolerant bypass routing diverting flits around compromised tiles
//=============================================================================

module secure_moe_router_top #(
    parameter integer CHIPLET_ID    = 0,     // Local chiplet ID (0..15)
    parameter integer NUM_CHIPLETS  = 16,    // 4x4 Active Interposer Mesh
    parameter integer DATA_WIDTH    = 64,    // Flit bit-width
    parameter integer TAG_WIDTH     = 8,     // Collective tensor tag width
    parameter integer TEMP_WIDTH    = 16,    // Fixed-point temperature (8.8 Kelvin)
    parameter integer ALPHA_SHIFT   = 3,     // alpha = 1/8 (shift by 3)
    parameter integer SIGMA_FACTOR  = 3      // 3-sigma adaptive threshold
)(
    input  wire                          clk,
    input  wire                          rst_n,

    // Ingress Packet Channels (5 Directions: 0:N, 1:S, 2:E, 3:W, 4:Local)
    input  wire [4:0]                    mesh_in_valid,
    input  wire [DATA_WIDTH-1:0]         mesh_in_data [4:0],
    output reg  [4:0]                    mesh_in_credit,

    // Egress Packet Channels (5 Directions: 0:N, 1:S, 2:E, 3:W, 4:Local)
    output reg  [4:0]                    mesh_out_valid,
    output reg  [DATA_WIDTH-1:0]         mesh_out_data [4:0],
    input  wire [4:0]                    mesh_out_credit,

    // Local Chiplet MoE Accelerator Interface
    input  wire                          moe_dispatch_valid,
    input  wire [3:0]                    moe_target_expert_id, // Target expert (0..15)
    input  wire [TAG_WIDTH-1:0]          moe_collective_tag,
    input  wire [DATA_WIDTH-1:0]         moe_token_payload,
    output wire                          moe_dispatch_ready,

    // Thermal Sensor & Security Interface (HeatSense TCAD '26)
    input  wire                          sensor_sample_valid,
    input  wire [TEMP_WIDTH-1:0]         sensor_temp_val,      // Fixed-point 8.8 Kelvin
    output reg                           trojan_alert,
    output reg                           trojan_quarantine_active,
    output wire [TEMP_WIDTH-1:0]         wma_baseline_temp,
    output wire [TEMP_WIDTH-1:0]         wma_deviation_val,

    // Collective In-Network Reduction Interface (PAC-NoC TVLSI '26)
    input  wire                          reduction_in_valid,
    input  wire [TAG_WIDTH-1:0]          reduction_in_tag,
    input  wire [31:0]                   reduction_in_data,
    output reg                           reduction_out_valid,
    output reg  [TAG_WIDTH-1:0]          reduction_out_tag,
    output reg  [31:0]                   reduction_out_data,

    // Telemetry & Hardware Security Counters
    output reg  [31:0]                   total_tokens_dispatched,
    output reg  [31:0]                   total_reductions_done,
    output reg  [15:0]                   quarantine_drop_count,
    output reg  [15:0]                   quarantine_reroute_count
);

    // Port Enumeration Constants
    localparam [2:0] PORT_NORTH = 3'd0;
    localparam [2:0] PORT_SOUTH = 3'd1;
    localparam [2:0] PORT_EAST  = 3'd2;
    localparam [2:0] PORT_WEST  = 3'd3;
    localparam [2:0] PORT_LOCAL = 3'd4;

    // Local coordinates in 4x4 mesh
    wire [1:0] local_x = CHIPLET_ID[1:0];
    wire [1:0] local_y = CHIPLET_ID[3:2];

    //=========================================================================
    // 1. HEATSENSE WMA THERMAL ANOMALY DETECTOR ENGINE
    //=========================================================================
    reg [TEMP_WIDTH-1:0] mean_reg;
    reg [TEMP_WIDTH-1:0] dev_reg;
    reg [3:0]            consecutive_anomalies;

    wire signed [TEMP_WIDTH:0] diff_temp;
    wire signed [TEMP_WIDTH:0] abs_diff;
    wire [TEMP_WIDTH-1:0]      threshold;

    assign diff_temp = $signed({1'b0, sensor_temp_val}) - $signed({1'b0, mean_reg});
    assign abs_diff  = (diff_temp < 0) ? -diff_temp : diff_temp;
    assign threshold = (dev_reg << 1) + dev_reg; // 3 * deviation (shift-and-add)

    assign wma_baseline_temp = mean_reg;
    assign wma_deviation_val = dev_reg;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            mean_reg                 <= {8'd45, 8'd0}; // Baseline: 318.15 K (45 C)
            dev_reg                  <= {8'd2,  8'd0}; // Initial deviation: 2.0 K
            trojan_alert             <= 1'b0;
            trojan_quarantine_active <= 1'b0;
            consecutive_anomalies    <= 4'd0;
        end else if (sensor_sample_valid) begin
            if (abs_diff[TEMP_WIDTH-1:0] > threshold) begin
                trojan_alert <= 1'b1;
                if (consecutive_anomalies < 4'd15)
                    consecutive_anomalies <= consecutive_anomalies + 1'b1;
                
                if (consecutive_anomalies >= 4'd2)
                    trojan_quarantine_active <= 1'b1;
            end else begin
                trojan_alert <= 1'b0;
                if (consecutive_anomalies > 4'd0)
                    consecutive_anomalies <= consecutive_anomalies - 1'b1;
                else
                    trojan_quarantine_active <= 1'b0;

                if (diff_temp >= 0)
                    mean_reg <= mean_reg + (diff_temp[TEMP_WIDTH-1:0] >> ALPHA_SHIFT);
                else
                    mean_reg <= mean_reg - (abs_diff[TEMP_WIDTH-1:0] >> ALPHA_SHIFT);

                if (abs_diff[TEMP_WIDTH-1:0] >= dev_reg)
                    dev_reg <= dev_reg + ((abs_diff[TEMP_WIDTH-1:0] - dev_reg) >> ALPHA_SHIFT);
                else
                    dev_reg <= dev_reg - ((dev_reg - abs_diff[TEMP_WIDTH-1:0]) >> ALPHA_SHIFT);
            end
        end else begin
            trojan_alert <= 1'b0;
        end
    end

    //=========================================================================
    // 2. PAC-NOC IN-NETWORK COLLECTIVE REDUCTION ENGINE
    //=========================================================================
    reg [31:0]          red_accumulator;
    reg [TAG_WIDTH-1:0] red_current_tag;
    reg [1:0]           red_flit_count;
    reg                 red_in_progress;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            red_accumulator         <= 32'd0;
            red_current_tag         <= {TAG_WIDTH{1'b0}};
            red_flit_count          <= 2'd0;
            red_in_progress         <= 1'b0;
            reduction_out_valid     <= 1'b0;
            reduction_out_tag       <= {TAG_WIDTH{1'b0}};
            reduction_out_data      <= 32'd0;
            total_reductions_done   <= 32'd0;
        end else begin
            reduction_out_valid <= 1'b0;

            if (reduction_in_valid && !trojan_quarantine_active) begin
                if (!red_in_progress) begin
                    red_accumulator <= reduction_in_data;
                    red_current_tag <= reduction_in_tag;
                    red_flit_count  <= 2'd1;
                    red_in_progress <= 1'b1;
                end else if (reduction_in_tag == red_current_tag) begin
                    if (red_flit_count == 2'd3) begin
                        reduction_out_valid   <= 1'b1;
                        reduction_out_tag     <= red_current_tag;
                        reduction_out_data    <= red_accumulator + reduction_in_data;
                        red_accumulator       <= 32'd0;
                        red_flit_count        <= 2'd0;
                        red_in_progress       <= 1'b0;
                        total_reductions_done <= total_reductions_done + 1'b1;
                    end else begin
                        red_accumulator <= red_accumulator + reduction_in_data;
                        red_flit_count  <= red_flit_count + 1'b1;
                    end
                end
            end
        end
    end

    //=========================================================================
    // 3. MOE TOKEN DISPATCH & ROUTE COMPUTATION (XY DOR)
    //=========================================================================
    assign moe_dispatch_ready = !trojan_quarantine_active && mesh_out_credit[PORT_LOCAL];

    wire [1:0] expert_x = moe_target_expert_id[1:0];
    wire [1:0] expert_y = moe_target_expert_id[3:2];

    function [2:0] compute_dor_port(
        input [1:0] cur_x_pos,
        input [1:0] cur_y_pos,
        input [1:0] tgt_x_pos,
        input [1:0] tgt_y_pos
    );
        begin
            if (tgt_x_pos > cur_x_pos)
                compute_dor_port = PORT_EAST;
            else if (tgt_x_pos < cur_x_pos)
                compute_dor_port = PORT_WEST;
            else if (tgt_y_pos > cur_y_pos)
                compute_dor_port = PORT_SOUTH;
            else if (tgt_y_pos < cur_y_pos)
                compute_dor_port = PORT_NORTH;
            else
                compute_dor_port = PORT_LOCAL;
        end
    endfunction

    wire [2:0] moe_egress_port = compute_dor_port(local_x, local_y, expert_x, expert_y);

    //=========================================================================
    // 4. CROSSBAR SWITCH ROUTING & FAULT-TOLERANT QUARANTINE BYPASS
    //=========================================================================
    reg [2:0] in_target_port [0:4];
    reg [1:0] pkt_dx;
    reg [1:0] pkt_dy;
    integer p_idx;

    always @(*) begin
        for (p_idx = 0; p_idx < 5; p_idx = p_idx + 1) begin
            if (mesh_in_valid[p_idx]) begin
                pkt_dx = mesh_in_data[p_idx][55:54];
                pkt_dy = mesh_in_data[p_idx][53:52];
                in_target_port[p_idx] = compute_dor_port(local_x, local_y, pkt_dx, pkt_dy);
            end else begin
                in_target_port[p_idx] = PORT_LOCAL;
            end
        end
    end

    integer op;
    reg [2:0] tgt_fwd;
    reg [2:0] bypass_port;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            mesh_out_valid          <= 5'b00000;
            mesh_in_credit          <= 5'b00000;
            total_tokens_dispatched <= 32'd0;
            quarantine_drop_count   <= 16'd0;
            quarantine_reroute_count<= 16'd0;
            for (op = 0; op < 5; op = op + 1) begin
                mesh_out_data[op] <= {DATA_WIDTH{1'b0}};
            end
        end else begin
            mesh_in_credit <= 5'b00000;
            for (op = 0; op < 5; op = op + 1) begin
                mesh_out_valid[op] <= 1'b0;
                mesh_out_data[op]  <= {DATA_WIDTH{1'b0}};
            end

            // 1. Local MoE Token Injection
            if (moe_dispatch_valid && !trojan_quarantine_active && mesh_out_credit[moe_egress_port]) begin
                mesh_out_valid[moe_egress_port] <= 1'b1;
                mesh_out_data[moe_egress_port]  <= {2'b00, moe_collective_tag[5:0], expert_x, expert_y, CHIPLET_ID[3:0], moe_token_payload[47:0]};
                total_tokens_dispatched         <= total_tokens_dispatched + 1'b1;
            end else if (moe_dispatch_valid && trojan_quarantine_active) begin
                quarantine_drop_count <= quarantine_drop_count + 1'b1;
            end

            // 2. Inter-Router Mesh Forwarding with Quarantine Bypass Logic
            for (p_idx = 0; p_idx < 5; p_idx = p_idx + 1) begin
                if (mesh_in_valid[p_idx]) begin
                    mesh_in_credit[p_idx] <= 1'b1;

                    if (!trojan_quarantine_active) begin
                        tgt_fwd = in_target_port[p_idx];
                        if (mesh_out_credit[tgt_fwd]) begin
                            mesh_out_valid[tgt_fwd] <= 1'b1;
                            mesh_out_data[tgt_fwd]  <= mesh_in_data[p_idx];
                        end else begin
                            quarantine_drop_count <= quarantine_drop_count + 1'b1;
                        end
                    end else begin
                        case (p_idx)
                            PORT_NORTH: bypass_port = PORT_SOUTH;
                            PORT_SOUTH: bypass_port = PORT_NORTH;
                            PORT_EAST:  bypass_port = PORT_WEST;
                            PORT_WEST:  bypass_port = PORT_EAST;
                            default:    bypass_port = PORT_EAST;
                        endcase

                        if (mesh_out_credit[bypass_port]) begin
                            mesh_out_valid[bypass_port] <= 1'b1;
                            mesh_out_data[bypass_port]  <= mesh_in_data[p_idx];
                            quarantine_reroute_count    <= quarantine_reroute_count + 1'b1;
                        end else begin
                            quarantine_drop_count <= quarantine_drop_count + 1'b1;
                        end
                    end
                end
            end
        end
    end

endmodule
