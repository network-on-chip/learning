// Synthesizable Credit-Based Flow Control Interface (Sender & Receiver)
// Accompanying Code for Chapter 2: Switching Techniques, Flow Control & Buffer Management
// Demonstrates credit tracking, forward flit transmission, and credit pulse feedback.

`timescale 1ns / 1ps

module credit_flow_control_tx #(
    parameter DATA_WIDTH   = 64,
    parameter BUFFER_DEPTH = 8,
    parameter CREDIT_WIDTH = $clog2(BUFFER_DEPTH + 1)
)(
    input  wire                    clk,
    input  wire                    rst_n,

    // Upstream local core / crossbar request
    input  wire                    tx_valid_in,
    input  wire [DATA_WIDTH-1:0]   tx_data_in,
    output wire                    tx_ready_out,

    // Outgoing physical link to downstream router
    output reg                     flit_valid,
    output reg  [DATA_WIDTH-1:0]   flit_data,

    // Reverse credit input wire from downstream router
    input  wire                    credit_in
);

    reg [CREDIT_WIDTH-1:0] credit_count;

    // Upstream is ready if downstream buffer has at least 1 free slot
    assign tx_ready_out = (credit_count > 0);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            credit_count <= BUFFER_DEPTH[CREDIT_WIDTH-1:0];
            flit_valid   <= 1'b0;
            flit_data    <= {DATA_WIDTH{1'b0}};
        end else begin
            // 1. Manage Credit Counter
            case ({tx_valid_in && tx_ready_out, credit_in})
                2'b10: credit_count <= credit_count - 1'b1; // Sent flit, no credit returned
                2'b01: credit_count <= credit_count + 1'b1; // No flit sent, credit returned
                default: credit_count <= credit_count;       // Both or neither
            endcase

            // 2. Transmit flit onto physical link
            if (tx_valid_in && tx_ready_out) begin
                flit_valid <= 1'b1;
                flit_data  <= tx_data_in;
            end else begin
                flit_valid <= 1'b0;
            end
        end
    end

endmodule


module credit_flow_control_rx #(
    parameter DATA_WIDTH   = 64,
    parameter BUFFER_DEPTH = 8
)(
    input  wire                    clk,
    input  wire                    rst_n,

    // Incoming physical link from upstream router
    input  wire                    flit_valid,
    input  wire [DATA_WIDTH-1:0]   flit_data,

    // Local consumer interface
    output wire                    rx_valid_out,
    output wire [DATA_WIDTH-1:0]   rx_data_out,
    input  wire                    rx_pop_in,

    // Reverse credit pulse emitted back to upstream router
    output reg                     credit_out
);

    reg [DATA_WIDTH-1:0] fifo_mem [0:BUFFER_DEPTH-1];
    reg [$clog2(BUFFER_DEPTH)-1:0] wr_ptr;
    reg [$clog2(BUFFER_DEPTH)-1:0] rd_ptr;
    reg [$clog2(BUFFER_DEPTH+1)-1:0] count;

    assign rx_valid_out = (count > 0);
    assign rx_data_out  = fifo_mem[rd_ptr];

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            wr_ptr     <= 0;
            rd_ptr     <= 0;
            count      <= 0;
            credit_out <= 1'b0;
        end else begin
            // Credit pulse is emitted exactly 1 cycle after a flit is popped by local consumer
            credit_out <= (rx_pop_in && rx_valid_out);

            // Write incoming flit
            if (flit_valid) begin
                fifo_mem[wr_ptr] <= flit_data;
                wr_ptr           <= (wr_ptr == BUFFER_DEPTH - 1) ? 0 : wr_ptr + 1'b1;
            end

            // Read consumed flit
            if (rx_pop_in && rx_valid_out) begin
                rd_ptr <= (rd_ptr == BUFFER_DEPTH - 1) ? 0 : rd_ptr + 1'b1;
            end

            // Track buffer count
            case ({flit_valid, rx_pop_in && rx_valid_out})
                2'b10: count <= count + 1'b1;
                2'b01: count <= count - 1'b1;
                default: count <= count;
            endcase
        end
    end

endmodule
