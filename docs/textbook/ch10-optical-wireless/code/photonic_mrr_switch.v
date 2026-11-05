//=============================================================================
// Module: photonic_mrr_switch
// Description: Synthesizable 2x2 Photonic Micro-Ring Resonator (MRR)
//              Switching Element Controller with Closed-Loop Thermal
//              Resonance Tracking and PWM Heater Actuation.
//
// Grounded in:
// - W.-Y. Kao, T.-J. Lin, and Y.-W. Chang, "Provably Good Physically Aware
//   WRONoC Design...", IEEE TCAD 2026.
// - Y. Ye et al., "System-Level Modeling and Analysis of Thermal Effects
//   in Optical Networks-on-Chip", IEEE TVLSI 2013.
//=============================================================================

`timescale 1ns / 1ps

module photonic_mrr_switch #(
    parameter TEMP_WIDTH      = 10,  // Temperature sensor resolution (0.1°C LSB)
    parameter TARGET_TEMP     = 10'd550, // 55.0°C target locked temperature
    parameter PWM_WIDTH       = 8,   // 8-bit microheater DAC resolution
    parameter LOCK_TOLERANCE  = 10'd5   // ±0.5°C lock window
)(
    input  wire                   clk,
    input  wire                   rst_n,

    // Optical Switching Command Interface
    input  wire                   switch_cmd,    // 0 = Through State, 1 = Drop State
    output reg                    optical_state, // 0 = Through, 1 = Drop
    output reg                    switch_ready,  // 1 = Resonator thermally locked & operational

    // Digital Thermal Sensor Feedback
    input  wire [TEMP_WIDTH-1:0]  measured_temp,
    input  wire                   temp_valid,

    // Microheater Control Outputs
    output reg  [PWM_WIDTH-1:0]   heater_power_val,
    output wire                   heater_pwm_pulse,
    output reg                    thermal_alarm  // Asserted if temperature exceeds safe boundary
);

    // Internal State
    reg [PWM_WIDTH-1:0] pwm_counter;
    reg [TEMP_WIDTH-1:0] temp_error;
    reg error_sign; // 0 = measured < target (need heat), 1 = measured > target (too hot)

    // PWM Pulse Generator for Resistive Microheater
    assign heater_pwm_pulse = (pwm_counter < heater_power_val);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            pwm_counter <= {PWM_WIDTH{1'b0}};
        end else begin
            pwm_counter <= pwm_counter + 1'b1;
        end
    end

    // Proportional Thermal Tuning & Locking FSM
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            heater_power_val <= 8'd128; // Default 50% duty cycle
            optical_state    <= 1'b0;
            switch_ready     <= 1'b0;
            thermal_alarm    <= 1'b0;
            temp_error       <= {TEMP_WIDTH{1'b0}};
            error_sign       <= 1'b0;
        end else begin
            // Update thermal control when valid sensor reading arrives
            if (temp_valid) begin
                if (measured_temp < TARGET_TEMP) begin
                    temp_error <= TARGET_TEMP - measured_temp;
                    error_sign <= 1'b0;
                    // Proportional heating boost
                    if (heater_power_val < 8'd250)
                        heater_power_val <= heater_power_val + 8'd2;
                end else begin
                    temp_error <= measured_temp - TARGET_TEMP;
                    error_sign <= 1'b1;
                    // Reduce heating
                    if (heater_power_val > 8'd5)
                        heater_power_val <= heater_power_val - 8'd2;
                end

                // Thermal lock detection within tolerance window
                if ((measured_temp >= (TARGET_TEMP - LOCK_TOLERANCE)) &&
                    (measured_temp <= (TARGET_TEMP + LOCK_TOLERANCE))) begin
                    switch_ready  <= 1'b1;
                    thermal_alarm <= 1'b0;
                end else begin
                    switch_ready  <= 1'b0;
                    if (measured_temp > (TARGET_TEMP + 10'd200))
                        thermal_alarm <= 1'b1; // Severe overheat (>75°C)
                    else
                        thermal_alarm <= 1'b0;
                end
            end

            // Optical routing actuation
            if (switch_ready) begin
                optical_state <= switch_cmd;
            end else begin
                optical_state <= 1'b0; // Default safe to Through state if unlocked
            end
        end
    end

endmodule

//=============================================================================
// Self-Testing Verification Testbench
//=============================================================================
`ifdef TESTBENCH
module tb_photonic_mrr_switch;
    reg clk;
    reg rst_n;
    reg switch_cmd;
    wire optical_state;
    wire switch_ready;
    reg [9:0] measured_temp;
    reg temp_valid;
    wire [7:0] heater_power_val;
    wire heater_pwm_pulse;
    wire thermal_alarm;

    photonic_mrr_switch #(
        .TEMP_WIDTH(10),
        .TARGET_TEMP(10'd550),
        .PWM_WIDTH(8),
        .LOCK_TOLERANCE(10'd5)
    ) dut (
        .clk(clk),
        .rst_n(rst_n),
        .switch_cmd(switch_cmd),
        .optical_state(optical_state),
        .switch_ready(switch_ready),
        .measured_temp(measured_temp),
        .temp_valid(temp_valid),
        .heater_power_val(heater_power_val),
        .heater_pwm_pulse(heater_pwm_pulse),
        .thermal_alarm(thermal_alarm)
    );

    always #5 clk = ~clk; // 100 MHz clock

    initial begin
        clk = 0;
        rst_n = 0;
        switch_cmd = 0;
        measured_temp = 10'd450; // Cold at 45.0°C
        temp_valid = 0;

        #20 rst_n = 1;
        #10 temp_valid = 1;

        // Warm up cycle towards target (55.0°C = 550)
        repeat (30) begin
            #20;
            if (measured_temp < 10'd550)
                measured_temp = measured_temp + 10'd5;
        end

        // Assert drop command
        #40 switch_cmd = 1;
        #60;

        if (switch_ready && optical_state == 1'b1) begin
            $display("MRR Switch Self-Test PASSED! Thermally locked at %0d (0.1C) with state=%b",
                     measured_temp, optical_state);
        end else begin
            $display("MRR Switch Self-Test FAILED: ready=%b, state=%b", switch_ready, optical_state);
        end
        $finish;
    end
endmodule
`endif

