// ============================================================================
// Module: turn_model_routing
// Description: Synthesizable Deadlock-Free Adaptive Routing Engine
//              Supports runtime selectable Turn Models (XY, West-First,
//              North-Last, Negative-First) with congestion-aware output port
//              selection based on downstream credit availability.
//
// Chapter 5: Deadlock Theory, Turn Models & Adaptive Routing
// Grounded in:
// - Glass & Ni, "The Turn Model for Adaptive Routing," JACM, 1994.
// - Duato, "A New Theory of Deadlock-Free Adaptive Routing," IEEE TPDS, 1993.
// ============================================================================

`timescale 1ns / 1ps

module turn_model_routing #(
    parameter COORD_WIDTH = 4,
    parameter ROUTING_MODE = 1  // 0: XY, 1: West-First, 2: North-Last, 3: Negative-First
)(
    input  wire                   clk,
    input  wire                   rst_n,

    // Routing packet request
    input  wire                   req_valid,
    input  wire [COORD_WIDTH-1:0] curr_x,
    input  wire [COORD_WIDTH-1:0] curr_y,
    input  wire [COORD_WIDTH-1:0] dest_x,
    input  wire [COORD_WIDTH-1:0] dest_y,
    input  wire [2:0]             in_port,      // Ingress port: 0:N, 1:S, 2:E, 3:W, 4:Local

    // Downstream credit status (congestion proxy: 1=has credits, 0=congested)
    input  wire [4:0]             free_credits, // [4:Local, 3:W, 2:E, 1:S, 0:N]

    // Selected output port [One-hot: 4:Local, 3:W, 2:E, 1:S, 0:N]
    output reg  [4:0]             out_port_grant,
    output reg                    out_valid
);

    localparam PORT_NORTH = 0;
    localparam PORT_SOUTH = 1;
    localparam PORT_EAST  = 2;
    localparam PORT_WEST  = 3;
    localparam PORT_LOCAL = 4;

    wire signed [COORD_WIDTH:0] dx;
    wire signed [COORD_WIDTH:0] dy;

    assign dx = $signed({1'b0, dest_x}) - $signed({1'b0, curr_x});
    assign dy = $signed({1'b0, dest_y}) - $signed({1'b0, curr_y});

    // Permissible minimal candidate ports
    reg [4:0] candidate_ports;

    always @(*) begin
        candidate_ports = 5'b00000;

        if (dx == 0 && dy == 0) begin
            // Destination reached: route to local core
            candidate_ports[PORT_LOCAL] = 1'b1;
        end else begin
            case (ROUTING_MODE)
                // -------------------------------------------------------------
                // Mode 0: Deterministic XY (DOR)
                // -------------------------------------------------------------
                0: begin
                    if (dx > 0)
                        candidate_ports[PORT_EAST] = 1'b1;
                    else if (dx < 0)
                        candidate_ports[PORT_WEST] = 1'b1;
                    else if (dy > 0)
                        candidate_ports[PORT_NORTH] = 1'b1;
                    else if (dy < 0)
                        candidate_ports[PORT_SOUTH] = 1'b1;
                end

                // -------------------------------------------------------------
                // Mode 1: West-First Turn Model (Glass & Ni)
                // If dx < 0, MUST route West first. Otherwise adaptive (E, N, S).
                // -------------------------------------------------------------
                1: begin
                    if (dx < 0) begin
                        candidate_ports[PORT_WEST] = 1'b1;
                    end else begin
                        if (dx > 0) candidate_ports[PORT_EAST]  = 1'b1;
                        if (dy > 0) candidate_ports[PORT_NORTH] = 1'b1;
                        if (dy < 0) candidate_ports[PORT_SOUTH] = 1'b1;
                    end
                end

                // -------------------------------------------------------------
                // Mode 2: North-Last Turn Model
                // Postpone North until all other minimal dimensions (E, W, S) are done.
                // -------------------------------------------------------------
                2: begin
                    if (dy > 0 && dx != 0) begin
                        if (dx > 0) candidate_ports[PORT_EAST]  = 1'b1;
                        if (dx < 0) candidate_ports[PORT_WEST]  = 1'b1;
                    end else begin
                        if (dx > 0) candidate_ports[PORT_EAST]  = 1'b1;
                        if (dx < 0) candidate_ports[PORT_WEST]  = 1'b1;
                        if (dy > 0) candidate_ports[PORT_NORTH] = 1'b1;
                        if (dy < 0) candidate_ports[PORT_SOUTH] = 1'b1;
                    end
                end

                // -------------------------------------------------------------
                // Mode 3: Negative-First Turn Model
                // Route negative directions (W, S) before positive (E, N).
                // -------------------------------------------------------------
                3: begin
                    if (dx < 0 || dy < 0) begin
                        if (dx < 0) candidate_ports[PORT_WEST]  = 1'b1;
                        if (dy < 0) candidate_ports[PORT_SOUTH] = 1'b1;
                    end else begin
                        if (dx > 0) candidate_ports[PORT_EAST]  = 1'b1;
                        if (dy > 0) candidate_ports[PORT_NORTH] = 1'b1;
                    end
                end

                default: begin
                    candidate_ports[PORT_LOCAL] = 1'b1;
                end
            endcase
        end
    end

    // Congestion-aware candidate arbiter: pick candidate with available credits
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            out_port_grant <= 5'b00000;
            out_valid      <= 1'b0;
        end else if (req_valid) begin
            out_valid <= 1'b1;
            if (candidate_ports[PORT_LOCAL]) begin
                out_port_grant <= 5'b10000;
            end else if ((candidate_ports & free_credits) != 5'b00000) begin
                // Pick the first permissible candidate that is uncongested
                if (candidate_ports[PORT_EAST] && free_credits[PORT_EAST])
                    out_port_grant <= 5'b00100;
                else if (candidate_ports[PORT_WEST] && free_credits[PORT_WEST])
                    out_port_grant <= 5'b01000;
                else if (candidate_ports[PORT_NORTH] && free_credits[PORT_NORTH])
                    out_port_grant <= 5'b00001;
                else if (candidate_ports[PORT_SOUTH] && free_credits[PORT_SOUTH])
                    out_port_grant <= 5'b00010;
                else
                    out_port_grant <= candidate_ports;
            end else begin
                // Fallback to first permissible candidate
                if (candidate_ports[PORT_EAST])
                    out_port_grant <= 5'b00100;
                else if (candidate_ports[PORT_WEST])
                    out_port_grant <= 5'b01000;
                else if (candidate_ports[PORT_NORTH])
                    out_port_grant <= 5'b00001;
                else if (candidate_ports[PORT_SOUTH])
                    out_port_grant <= 5'b00010;
                else
                    out_port_grant <= 5'b10000;
            end
        end else begin
            out_port_grant <= 5'b00000;
            out_valid      <= 1'b0;
        end
    end

endmodule
