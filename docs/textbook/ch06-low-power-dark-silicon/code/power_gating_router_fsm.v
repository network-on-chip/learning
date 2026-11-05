// ============================================================================
// Module: power_gating_router_fsm
// Description: Synthesizable Run-Time Power-Gating Controller for On-Chip
//              Router Virtual Channel / Crossbar Slice with Lookahead Early
//              Wake-up and Isolation Cell Handshaking.
//
// Chapter 6: Low-Power Architectures & Dark Silicon Dynamics
// Grounded in:
// - Matsutani et al., "Performance, Area, and Power Evaluations of
//   Ultrafine-Grained Run-Time Power-Gating Routers," IEEE TCAD, 2011.
// ============================================================================

`timescale 1ns / 1ps

module power_gating_router_fsm #(
    parameter IDLE_THRESHOLD = 8,  // Clock cycles of inactivity before sleep
    parameter WAKE_CYCLES    = 4   // Cycles required to charge virtual VDD rail
)(
    input  wire       clk,
    input  wire       rst_n,

    // Packet activity monitors
    input  wire       flit_valid_in,       // Incoming flit at input buffer
    input  wire       early_wakeup_req,    // Lookahead wakeup from upstream router

    // Power gating cell control signals
    output reg        ps_sleep,            // Power switch sleep control (1: SLEEP, 0: ACTIVE)
    output reg        iso_en,              // Isolation cell enable (1: ISOLATE, 0: PASS)
    output reg        clk_gate_en,         // Local clock gating enable

    // Router slice status
    output reg        slice_ready,         // Slice is awake and ready for traffic
    output wire [2:0] fsm_state_dbg
);

    // FSM State Encoding
    localparam ST_ACTIVE     = 3'b000;
    localparam ST_IDLE_COUNT = 3'b001;
    localparam ST_SLEEP_REQ  = 3'b010;
    localparam ST_SLEEP      = 3'b011;
    localparam ST_WAKE_REQ   = 3'b100;
    localparam ST_WAKE_WAIT  = 3'b101;

    reg [2:0] state, next_state;
    reg [7:0] idle_counter;
    reg [3:0] wake_counter;

    assign fsm_state_dbg = state;

    // FSM State Transition
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state        <= ST_ACTIVE;
            idle_counter <= 8'd0;
            wake_counter <= 4'd0;
        end else begin
            state <= next_state;

            // Idle countdown
            if (state == ST_IDLE_COUNT) begin
                idle_counter <= idle_counter + 8'd1;
            end else begin
                idle_counter <= 8'd0;
            end

            // Wakeup rail charging counter
            if (state == ST_WAKE_WAIT) begin
                wake_counter <= wake_counter + 4'd1;
            end else begin
                wake_counter <= 4'd0;
            end
        end
    end

    // Next State Logic
    always @(*) begin
        next_state = state;

        case (state)
            ST_ACTIVE: begin
                if (!flit_valid_in && !early_wakeup_req)
                    next_state = ST_IDLE_COUNT;
            end

            ST_IDLE_COUNT: begin
                if (flit_valid_in || early_wakeup_req)
                    next_state = ST_ACTIVE;
                else if (idle_counter >= IDLE_THRESHOLD - 1)
                    next_state = ST_SLEEP_REQ;
            end

            // Safe shutdown: assert isolation first to prevent floating input crowbar current
            ST_SLEEP_REQ: begin
                next_state = ST_SLEEP;
            end

            ST_SLEEP: begin
                if (flit_valid_in || early_wakeup_req)
                    next_state = ST_WAKE_REQ;
            end

            // Turn on power switch, wait for rail stabilization
            ST_WAKE_REQ: begin
                next_state = ST_WAKE_WAIT;
            end

            ST_WAKE_WAIT: begin
                if (wake_counter >= WAKE_CYCLES - 1)
                    next_state = ST_ACTIVE;
            end

            default: next_state = ST_ACTIVE;
        endcase
    end

    // Output Control Signals
    always @(*) begin
        case (state)
            ST_ACTIVE: begin
                ps_sleep    = 1'b0;  // Power switch ON (Active)
                iso_en      = 1'b0;  // Normal signal propagation
                clk_gate_en = 1'b0;  // Clock active
                slice_ready = 1'b1;  // Ready to process flits
            end

            ST_IDLE_COUNT: begin
                ps_sleep    = 1'b0;
                iso_en      = 1'b0;
                clk_gate_en = 1'b0;
                slice_ready = 1'b1;
            end

            ST_SLEEP_REQ: begin
                ps_sleep    = 1'b0;
                iso_en      = 1'b1;  // Freeze boundary signals
                clk_gate_en = 1'b1;  // Stop local clock tree
                slice_ready = 1'b0;
            end

            ST_SLEEP: begin
                ps_sleep    = 1'b1;  // Open power switch (CUT LEAKAGE)
                iso_en      = 1'b1;  // Keep boundary isolated
                clk_gate_en = 1'b1;  // Clock gated
                slice_ready = 1'b0;
            end

            ST_WAKE_REQ: begin
                ps_sleep    = 1'b0;  // Close power switch (CHARGE VDD_VIRTUAL)
                iso_en      = 1'b1;  // Keep isolated during rail ramp
                clk_gate_en = 1'b1;
                slice_ready = 1'b0;
            end

            ST_WAKE_WAIT: begin
                ps_sleep    = 1'b0;
                iso_en      = 1'b1;  // Isolate until voltage reaches 95% nominal
                clk_gate_en = 1'b0;  // Clock starts
                slice_ready = 1'b0;
            end

            default: begin
                ps_sleep    = 1'b0;
                iso_en      = 1'b0;
                clk_gate_en = 1'b0;
                slice_ready = 1'b1;
            end
        endcase
    end

endmodule
