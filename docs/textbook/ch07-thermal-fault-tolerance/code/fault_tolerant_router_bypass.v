// ============================================================================
// Fault-Tolerant Router Port Bypass & ZoneDefense Logic (Synthesizable)
//
// Grounded in:
// - B. Fu, Y. Han, H. Li, X. Li, "ZoneDefense: A Fault-Tolerant Routing for
//   2-D Meshes Without Virtual Channels", IEEE TVLSI 2014.
// - Built-In Self-Test (BIST) runtime link fault detection and perimeter detour.
// ============================================================================

`timescale 1ns / 1ps

module fault_tolerant_router_bypass #(
    parameter integer MY_X      = 2,
    parameter integer MY_Y      = 2,
    parameter integer MESH_W    = 4,
    parameter integer MESH_H    = 4
)(
    input  wire        clk,
    input  wire        rst_n,

    // Runtime Link Fault Status (from BIST / CRC link error detectors)
    // Bit 0: East, Bit 1: West, Bit 2: North, Bit 3: South, Bit 4: Local
    input  wire [4:0]  link_fault_in,

    // ZoneDefense Convex Faulty Block Boundaries [X_min, X_max, Y_min, Y_max]
    input  wire [2:0]  fb_xmin,
    input  wire [2:0]  fb_xmax,
    input  wire [2:0]  fb_ymin,
    input  wire [2:0]  fb_ymax,
    input  wire        fb_valid,

    // Incoming Packet Header & Desired Direction (from nominal XY DOR)
    input  wire        req_valid,
    input  wire [2:0]  dest_x,
    input  wire [2:0]  dest_y,
    input  wire [2:0]  nominal_port,  // 0: Local, 1: East, 2: West, 3: North, 4: South

    // Safe Routed Output Port and Bypass Control
    output reg  [2:0]  safe_port,
    output reg         bypass_active,
    output reg         defense_zone_hit,
    output reg         packet_dropped
);

    // Port Enumeration Constants
    localparam PORT_LOCAL = 3'd0;
    localparam PORT_EAST  = 3'd1;
    localparam PORT_WEST  = 3'd2;
    localparam PORT_NORTH = 3'd3;
    localparam PORT_SOUTH = 3'd4;

    // Registered Fault Status
    reg [4:0] link_fault_q;
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            link_fault_q <= 5'b00000;
        end else begin
            link_fault_q <= link_fault_in;
        end
    end

    // ZoneDefense Detection: Check if current router lies within the Defense Zone
    // A router is in the defense zone if its column falls within [fb_xmin, fb_xmax]
    wire in_col_zone = fb_valid && (MY_X >= fb_xmin) && (MY_X <= fb_xmax);
    wire in_row_zone = fb_valid && (MY_Y >= fb_ymin) && (MY_Y <= fb_ymax);

    // Check if target step enters the convex faulty block
    wire next_east_faulty  = (MY_X + 1 >= fb_xmin) && (MY_X + 1 <= fb_xmax) && in_row_zone;
    wire next_west_faulty  = (MY_X - 1 >= fb_xmin) && (MY_X - 1 <= fb_xmax) && in_row_zone;
    wire next_north_faulty = in_col_zone && (MY_Y + 1 >= fb_ymin) && (MY_Y + 1 <= fb_ymax);
    wire next_south_faulty = in_col_zone && (MY_Y - 1 >= fb_ymin) && (MY_Y - 1 <= fb_ymax);

    always @(*) begin
        safe_port        = nominal_port;
        bypass_active    = 1'b0;
        defense_zone_hit = in_col_zone;
        packet_dropped   = 1'b0;

        if (req_valid) begin
            if (dest_x == MY_X[2:0] && dest_y == MY_Y[2:0]) begin
                // Packet reached local destination
                safe_port = PORT_LOCAL;
            end else begin
                case (nominal_port)
                    PORT_EAST: begin
                        // If East link is physically faulty or leads into faulty block
                        if (link_fault_q[0] || (fb_valid && next_east_faulty)) begin
                            bypass_active = 1'b1;
                            // Detour along vertical boundary (North or South depending on destination)
                            if (dest_y >= MY_Y[2:0] && !link_fault_q[2] && (MY_Y < MESH_H - 1))
                                safe_port = PORT_NORTH;
                            else if (!link_fault_q[3] && (MY_Y > 0))
                                safe_port = PORT_SOUTH;
                            else if (!link_fault_q[1] && (MY_X > 0))
                                safe_port = PORT_WEST; // Backtrack / alternate detour
                            else
                                packet_dropped = 1'b1;
                        end else begin
                            safe_port = PORT_EAST;
                        end
                    end

                    PORT_WEST: begin
                        if (link_fault_q[1] || (fb_valid && next_west_faulty)) begin
                            bypass_active = 1'b1;
                            if (dest_y >= MY_Y[2:0] && !link_fault_q[2] && (MY_Y < MESH_H - 1))
                                safe_port = PORT_NORTH;
                            else if (!link_fault_q[3] && (MY_Y > 0))
                                safe_port = PORT_SOUTH;
                            else
                                packet_dropped = 1'b1;
                        end else begin
                            safe_port = PORT_WEST;
                        end
                    end

                    PORT_NORTH: begin
                        if (link_fault_q[2] || (fb_valid && next_north_faulty)) begin
                            bypass_active = 1'b1;
                            // Detour East or West around faulty block perimeter
                            if (dest_x >= MY_X[2:0] && !link_fault_q[0] && (MY_X < MESH_W - 1))
                                safe_port = PORT_EAST;
                            else if (!link_fault_q[1] && (MY_X > 0))
                                safe_port = PORT_WEST;
                            else
                                packet_dropped = 1'b1;
                        end else begin
                            safe_port = PORT_NORTH;
                        end
                    end

                    PORT_SOUTH: begin
                        if (link_fault_q[3] || (fb_valid && next_south_faulty)) begin
                            bypass_active = 1'b1;
                            if (dest_x >= MY_X[2:0] && !link_fault_q[0] && (MY_X < MESH_W - 1))
                                safe_port = PORT_EAST;
                            else if (!link_fault_q[1] && (MY_X > 0))
                                safe_port = PORT_WEST;
                            else
                                packet_dropped = 1'b1;
                        end else begin
                            safe_port = PORT_SOUTH;
                        end
                    end

                    default: safe_port = PORT_LOCAL;
                endcase
            end
        end
    end

endmodule
