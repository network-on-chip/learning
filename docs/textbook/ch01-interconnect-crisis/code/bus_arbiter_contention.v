// Synthesizable Round-Robin Shared Bus Arbiter for N=4 Masters
// Accompanying Code for Chapter 1: The Multi-Core Communication Crisis
// Demonstrates centralized arbitration bottlenecks and grant serialization.

`timescale 1ns / 1ps

module bus_arbiter_contention #(
    parameter NUM_MASTERS = 4
)(
    input  wire                     clk,
    input  wire                     rst_n,
    input  wire [NUM_MASTERS-1:0]   req,        // Requests from Master 0..3
    output reg  [NUM_MASTERS-1:0]   grant,      // One-hot grant output
    output reg  [1:0]               grant_id,   // Granted master index
    output wire                     bus_busy    // High if any master is currently granted
);

    reg [NUM_MASTERS-1:0] priority_ptr; // Current priority token

    assign bus_busy = |grant;

    // Round-robin arbitration logic
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            grant        <= {NUM_MASTERS{1'b0}};
            grant_id     <= 2'b00;
            priority_ptr <= 4'b0001; // Master 0 has initial priority
        end else begin
            grant <= {NUM_MASTERS{1'b0}};

            // Check requests in cyclic priority order
            case (priority_ptr)
                4'b0001: begin
                    if      (req[0]) begin grant <= 4'b0001; grant_id <= 2'd0; priority_ptr <= 4'b0010; end
                    else if (req[1]) begin grant <= 4'b0010; grant_id <= 2'd1; priority_ptr <= 4'b0100; end
                    else if (req[2]) begin grant <= 4'b0100; grant_id <= 2'd2; priority_ptr <= 4'b1000; end
                    else if (req[3]) begin grant <= 4'b1000; grant_id <= 2'd3; priority_ptr <= 4'b0001; end
                end
                4'b0010: begin
                    if      (req[1]) begin grant <= 4'b0010; grant_id <= 2'd1; priority_ptr <= 4'b0100; end
                    else if (req[2]) begin grant <= 4'b0100; grant_id <= 2'd2; priority_ptr <= 4'b1000; end
                    else if (req[3]) begin grant <= 4'b1000; grant_id <= 2'd3; priority_ptr <= 4'b0001; end
                    else if (req[0]) begin grant <= 4'b0001; grant_id <= 2'd0; priority_ptr <= 4'b0010; end
                end
                4'b0100: begin
                    if      (req[2]) begin grant <= 4'b0100; grant_id <= 2'd2; priority_ptr <= 4'b1000; end
                    else if (req[3]) begin grant <= 4'b1000; grant_id <= 2'd3; priority_ptr <= 4'b0001; end
                    else if (req[0]) begin grant <= 4'b0001; grant_id <= 2'd0; priority_ptr <= 4'b0010; end
                    else if (req[1]) begin grant <= 4'b0010; grant_id <= 2'd1; priority_ptr <= 4'b0100; end
                end
                4'b1000: begin
                    if      (req[3]) begin grant <= 4'b1000; grant_id <= 2'd3; priority_ptr <= 4'b0001; end
                    else if (req[0]) begin grant <= 4'b0001; grant_id <= 2'd0; priority_ptr <= 4'b0010; end
                    else if (req[1]) begin grant <= 4'b0010; grant_id <= 2'd1; priority_ptr <= 4'b0100; end
                    else if (req[2]) begin grant <= 4'b0100; grant_id <= 2'd2; priority_ptr <= 4'b1000; end
                end
                default: priority_ptr <= 4'b0001;
            endcase
        end
    end

endmodule
