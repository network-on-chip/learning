// ============================================================================
// 3D-NoC 7-Port Router Vertical TSV Link Arbiter with Fault Bypass
//
// Grounded in:
// - I. Loi et al., "Characterization and Implementation of Fault-Tolerant
//   Vertical Links for 3-D Networks-on-Chip", IEEE TCAD 2011.
// - A. More et al., "Vertical Arbitration-Free 3-D NoCs", IEEE TCAD 2018.
// ============================================================================

`timescale 1ns / 1ps

module tsv_arbiter_3d #(
    parameter integer NUM_INPUTS = 5 // Local, North, South, East, West
)(
    input  wire                    clk,
    input  wire                    rst_n,

    // Vertical Allocation Requests from planar inputs (0:Local, 1:N, 2:S, 3:E, 4:W)
    input  wire [NUM_INPUTS-1:0]   req_up,
    input  wire [NUM_INPUTS-1:0]   req_down,

    // TSV Bundle Physical Health Status (from BIST / built-in boundary scan)
    input  wire                    tsv_up_faulty,
    input  wire                    tsv_down_faulty,

    // Grant outputs to input ports for Up/Down TSV links
    output reg  [NUM_INPUTS-1:0]   grant_up,
    output reg  [NUM_INPUTS-1:0]   grant_down,

    // Status and Defect Bypass Flags
    output wire                    tsv_up_busy,
    output wire                    tsv_down_busy,
    output reg  [NUM_INPUTS-1:0]   bypass_planar_up,
    output reg  [NUM_INPUTS-1:0]   bypass_planar_down
);

    // Rotating Round-Robin Priority Pointers for Vertical Channels
    reg [2:0] priority_up_ptr;
    reg [2:0] priority_down_ptr;

    // Up TSV Arbitration Logic
    integer i;
    reg [NUM_INPUTS-1:0] masked_req_up;
    reg [NUM_INPUTS-1:0] unmasked_grant_up;
    reg [NUM_INPUTS-1:0] masked_grant_up;

    assign tsv_up_busy   = (|grant_up);
    assign tsv_down_busy = (|grant_down);

    always @(*) begin
        grant_up         = {NUM_INPUTS{1'b0}};
        bypass_planar_up = {NUM_INPUTS{1'b0}};

        if (tsv_up_faulty) begin
            // TSV bundle is defective: signal planar bypass to steer packet along horizontal tile
            bypass_planar_up = req_up;
        end else if (|req_up) begin
            // Priority-driven Round-Robin Grant
            for (i = 0; i < NUM_INPUTS; i = i + 1) begin
                if (req_up[(priority_up_ptr + i) % NUM_INPUTS]) begin
                    grant_up[(priority_up_ptr + i) % NUM_INPUTS] = 1'b1;
                    // Break loop on first granted input
                    i = NUM_INPUTS;
                end
            end
        end
    end

    // Down TSV Arbitration Logic
    integer j;
    always @(*) begin
        grant_down         = {NUM_INPUTS{1'b0}};
        bypass_planar_down = {NUM_INPUTS{1'b0}};

        if (tsv_down_faulty) begin
            bypass_planar_down = req_down;
        end else if (|req_down) begin
            for (j = 0; j < NUM_INPUTS; j = j + 1) begin
                if (req_down[(priority_down_ptr + j) % NUM_INPUTS]) begin
                    grant_down[(priority_down_ptr + j) % NUM_INPUTS] = 1'b1;
                    j = NUM_INPUTS;
                end
            end
        end
    end

    // Sequential Pointer Update
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            priority_up_ptr   <= 3'd0;
            priority_down_ptr <= 3'd0;
        end else begin
            if (|grant_up) begin
                for (i = 0; i < NUM_INPUTS; i = i + 1) begin
                    if (grant_up[i]) priority_up_ptr <= (i + 1) % NUM_INPUTS;
                end
            end
            if (|grant_down) begin
                for (j = 0; j < NUM_INPUTS; j = j + 1) begin
                    if (grant_down[j]) priority_down_ptr <= (j + 1) % NUM_INPUTS;
                end
            end
        end
    end

endmodule
