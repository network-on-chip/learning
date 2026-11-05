// ============================================================================
// Asynchronous Multi-Chiplet D2D Bridge with Credit Flow Control & CRC
//
// Grounded in:
// - Universal Chiplet Interconnect Express (UCIe 1.1/2.0) D2D Adapter Specs
// - P. Vivet et al., "IntAct: A 96-Core Processor With Six Chiplets 3D-Stacked
//   on an Active Interposer", IEEE JSSC 2021.
// - P. Wang et al., "In/Outbound Swap: A Backtracking-based Deadlock Recovery
//   Mechanism for Multi-Chiplet Networks", IEEE TCAD 2026.
// ============================================================================

`timescale 1ns / 1ps

module chiplet_bridge_protocol #(
    parameter integer FLIT_WIDTH    = 64,
    parameter integer FIFO_DEPTH    = 16,
    parameter integer ADDR_WIDTH    = 4   // 2^4 = 16
)(
    // --- Local Chiplet Router Domain ---
    input  wire                   clk_chiplet,
    input  wire                   rst_n_chiplet,
    input  wire                   flit_valid_in,
    input  wire [FLIT_WIDTH-1:0]  flit_data_in,
    output wire                   tx_ready_out,

    // --- Physical D2D Link Domain ---
    input  wire                   clk_d2d,
    input  wire                   rst_n_d2d,

    // Outbound Physical D2D Pins
    output reg                    d2d_tx_valid,
    output reg  [FLIT_WIDTH-1:0]  d2d_tx_data,
    output reg  [7:0]             d2d_tx_crc,
    input  wire                   d2d_remote_credit_in,

    // Inbound Physical D2D Pins
    input  wire                   d2d_rx_valid,
    input  wire [FLIT_WIDTH-1:0]  d2d_rx_data,
    input  wire [7:0]             d2d_rx_crc,
    output reg                    d2d_local_credit_out,

    // Local Inbound Flit Output to Chiplet Router
    output reg                    flit_valid_out,
    output reg  [FLIT_WIDTH-1:0]  flit_data_out,
    input  wire                   rx_ready_in,

    // Deadlock Recovery & Timeout Telemetry (In/Outbound Swap)
    output reg                    deadlock_timeout_strobe
);

    // ========================================================================
    // 1. Dual-Clock Asynchronous FIFO for Clock Domain Crossing (CDC)
    // ========================================================================
    reg [FLIT_WIDTH-1:0] mem [0:FIFO_DEPTH-1];

    reg [ADDR_WIDTH:0] wr_ptr_bin, wr_ptr_gray;
    reg [ADDR_WIDTH:0] rd_ptr_bin, rd_ptr_gray;

    // 2-Stage Synchronizers for Pointer Exchange
    reg [ADDR_WIDTH:0] wr_ptr_gray_sync1, wr_ptr_gray_sync2;
    reg [ADDR_WIDTH:0] rd_ptr_gray_sync1, rd_ptr_gray_sync2;

    // Binary to Gray code converter function
    function [ADDR_WIDTH:0] bin2gray(input [ADDR_WIDTH:0] bin);
        bin2gray = bin ^ (bin >> 1);
    endfunction

    // Write domain logic (clk_chiplet)
    wire [ADDR_WIDTH:0] wr_ptr_next = wr_ptr_bin + 1'b1;
    wire [ADDR_WIDTH:0] wr_ptr_gray_next = bin2gray(wr_ptr_next);

    // Full condition: MSBs invert while remaining bits match
    wire fifo_full = (wr_ptr_gray_next == {~rd_ptr_gray_sync2[ADDR_WIDTH:ADDR_WIDTH-1],
                                           rd_ptr_gray_sync2[ADDR_WIDTH-2:0]});
    assign tx_ready_out = !fifo_full;

    always @(posedge clk_chiplet or negedge rst_n_chiplet) begin
        if (!rst_n_chiplet) begin
            wr_ptr_bin   <= {(ADDR_WIDTH+1){1'b0}};
            wr_ptr_gray  <= {(ADDR_WIDTH+1){1'b0}};
            rd_ptr_gray_sync1 <= {(ADDR_WIDTH+1){1'b0}};
            rd_ptr_gray_sync2 <= {(ADDR_WIDTH+1){1'b0}};
        end else begin
            // Synchronize read pointer into write domain
            rd_ptr_gray_sync1 <= rd_ptr_gray;
            rd_ptr_gray_sync2 <= rd_ptr_gray_sync1;

            if (flit_valid_in && tx_ready_out) begin
                mem[wr_ptr_bin[ADDR_WIDTH-1:0]] <= flit_data_in;
                wr_ptr_bin  <= wr_ptr_next;
                wr_ptr_gray <= wr_ptr_gray_next;
            end
        end
    end

    // ========================================================================
    // 2. Read Domain & Outbound D2D Transmission (clk_d2d)
    // ========================================================================
    reg [7:0] remote_credit_counter;
    wire fifo_empty = (wr_ptr_gray_sync2 == rd_ptr_gray);

    // CRC-8 Checksum Function: x^8 + x^2 + x + 1 (ATM-8 polynomial)
    function [7:0] calc_crc8(input [FLIT_WIDTH-1:0] data);
        integer k;
        reg [7:0] crc;
        begin
            crc = 8'hFF;
            for (k = 0; k < FLIT_WIDTH; k = k + 1) begin
                if ((crc[7] ^ data[k]) == 1'b1)
                    crc = (crc << 1) ^ 8'h07;
                else
                    crc = (crc << 1);
            end
            calc_crc8 = crc;
        end
    endfunction

    always @(posedge clk_d2d or negedge rst_n_d2d) begin
        if (!rst_n_d2d) begin
            rd_ptr_bin            <= {(ADDR_WIDTH+1){1'b0}};
            rd_ptr_gray           <= {(ADDR_WIDTH+1){1'b0}};
            wr_ptr_gray_sync1     <= {(ADDR_WIDTH+1){1'b0}};
            wr_ptr_gray_sync2     <= {(ADDR_WIDTH+1){1'b0}};
            d2d_tx_valid          <= 1'b0;
            d2d_tx_data           <= {FLIT_WIDTH{1'b0}};
            d2d_tx_crc            <= 8'h00;
            remote_credit_counter <= FIFO_DEPTH[7:0];
        end else begin
            // Synchronize write pointer into read domain
            wr_ptr_gray_sync1 <= wr_ptr_gray;
            wr_ptr_gray_sync2 <= wr_ptr_gray_sync1;

            // Update credit count from incoming credit strobes
            if (d2d_remote_credit_in && (!d2d_tx_valid || remote_credit_counter == 0))
                remote_credit_counter <= remote_credit_counter + 1'b1;
            else if (!d2d_remote_credit_in && d2d_tx_valid && remote_credit_counter > 0)
                remote_credit_counter <= remote_credit_counter - 1'b1;

            // Dequeue flit and transmit across D2D if remote receiver has credit
            if (!fifo_empty && (remote_credit_counter > 0)) begin
                d2d_tx_valid <= 1'b1;
                d2d_tx_data  <= mem[rd_ptr_bin[ADDR_WIDTH-1:0]];
                d2d_tx_crc   <= calc_crc8(mem[rd_ptr_bin[ADDR_WIDTH-1:0]]);
                rd_ptr_bin   <= rd_ptr_bin + 1'b1;
                rd_ptr_gray  <= bin2gray(rd_ptr_bin + 1'b1);
            end else begin
                d2d_tx_valid <= 1'b0;
            end
        end
    end

    // ========================================================================
    // 3. Inbound Receiver Path & Deadlock Timeout Strobe
    // ========================================================================
    reg [9:0] timeout_counter;

    always @(posedge clk_d2d or negedge rst_n_d2d) begin
        if (!rst_n_d2d) begin
            d2d_local_credit_out    <= 1'b0;
            flit_valid_out          <= 1'b0;
            flit_data_out           <= {FLIT_WIDTH{1'b0}};
            deadlock_timeout_strobe <= 1'b0;
            timeout_counter         <= 10'd0;
        end else begin
            d2d_local_credit_out    <= 1'b0;
            deadlock_timeout_strobe <= 1'b0;

            if (d2d_rx_valid) begin
                // Verify CRC integrity
                if (calc_crc8(d2d_rx_data) == d2d_rx_crc) begin
                    flit_valid_out       <= 1'b1;
                    flit_data_out        <= d2d_rx_data;
                    d2d_local_credit_out <= 1'b1; // Send credit back to remote peer
                end
            end else if (rx_ready_in) begin
                flit_valid_out <= 1'b0;
            end

            // In/Outbound Swap Deadlock Monitor:
            // If valid flit is blocked at downstream interface for >512 cycles
            if (flit_valid_out && !rx_ready_in) begin
                timeout_counter <= timeout_counter + 1'b1;
                if (timeout_counter == 10'd512) begin
                    deadlock_timeout_strobe <= 1'b1; // Trigger In/Outbound Swap recovery
                end
            end else begin
                timeout_counter <= 10'd0;
            end
        end
    end

endmodule
