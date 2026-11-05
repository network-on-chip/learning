// Synthesizable 4-Input Triangular Matrix Arbiter (Strict Least-Recently-Used)
// Accompanying Code for Chapter 3: High-Performance Router Microarchitecture & Arbitration
// Fast 2-level gate delay grant computation with single-cycle triangular matrix update.

`timescale 1ns / 1ps

module matrix_arbiter_4port (
    input  wire        clk,
    input  wire        rst_n,
    input  wire [3:0]  req,       // Request lines from clients 0..3
    output reg  [3:0]  grant,     // One-hot grant lines to clients 0..3
    output wire [1:0]  grant_id   // Granted client index
);

    // Strict upper-triangular priority registers:
    // M[0][1], M[0][2], M[0][3], M[1][2], M[1][3], M[2][3]
    // M[i][j] == 1 means client i has priority over client j
    // M[j][i] is implicitly ~M[i][j] (anti-symmetric, M[i][i] = 0)
    reg m01, m02, m03;
    reg m12, m13;
    reg m23;

    // Combinational grant logic (2 gate levels: AND array followed by grant validation)
    wire g0 = req[0] & (~req[1] |  m01) & (~req[2] |  m02) & (~req[3] |  m03);
    wire g1 = req[1] & (~req[0] | ~m01) & (~req[2] |  m12) & (~req[3] |  m13);
    wire g2 = req[2] & (~req[0] | ~m02) & (~req[1] | ~m12) & (~req[3] |  m23);
    wire g3 = req[3] & (~req[0] | ~m03) & (~req[1] | ~m13) & (~req[2] | ~m23);

    wire [3:0] grant_comb = {g3, g2, g1, g0};

    // Encoder for grant ID
    assign grant_id = grant_comb[3] ? 2'd3 :
                      grant_comb[2] ? 2'd2 :
                      grant_comb[1] ? 2'd1 : 2'd0;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            grant <= 4'b0000;
            // Initialize: client 0 > 1 > 2 > 3
            m01 <= 1'b1; m02 <= 1'b1; m03 <= 1'b1;
            m12 <= 1'b1; m13 <= 1'b1;
            m23 <= 1'b1;
        end else begin
            grant <= grant_comb;

            // Update priority matrix: Winner becomes Least Recently Used
            case (grant_comb)
                4'b0001: begin // Client 0 won: row 0 -> 0 (all others have priority over 0)
                    m01 <= 1'b0; m02 <= 1'b0; m03 <= 1'b0;
                end
                4'b0010: begin // Client 1 won: col 1 -> 1, row 1 -> 0
                    m01 <= 1'b1;
                    m12 <= 1'b0; m13 <= 1'b0;
                end
                4'b0100: begin // Client 2 won: col 2 -> 1, row 2 -> 0
                    m02 <= 1'b1; m12 <= 1'b1;
                    m23 <= 1'b0;
                end
                4'b1000: begin // Client 3 won: col 3 -> 1 (all have priority over 3)
                    m03 <= 1'b1; m13 <= 1'b1; m23 <= 1'b1;
                end
                default: ; // No requests or conflicting grants
            endcase
        end
    end

endmodule
