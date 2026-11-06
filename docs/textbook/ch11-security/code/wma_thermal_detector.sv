//=============================================================================
// Module: wma_thermal_detector
// Description: Synthesizable Weighted Moving Average (WMA) Thermal Anomaly
//              Detector for Network-on-Chip (NoC) Routers.
//
// Grounded in IEEE TCAD 2026: "HeatSense: Intelligent Thermal Anomaly Detection
// for Securing NoC-Enabled MPSoCs" (Hasanzadeh et al.).
//
// Implements fixed-point EWMA tracking and adaptive threshold comparison
// using shift-and-add arithmetic (zero multiplier overhead) to detect
// thermal Hardware Trojans and malicious throttling attacks in real time.
//=============================================================================

`timescale 1ns/1ps

module wma_thermal_detector #(
    parameter DATA_WIDTH   = 16, // Fixed-point: 8-bit integer, 8-bit fraction
    parameter ALPHA_SHIFT  = 3,  // Weighting factor alpha = 1 / (2^ALPHA_SHIFT) = 1/8
    parameter SIGMA_FACTOR = 3   // Threshold multiplier K = 3 (approx 3-sigma)
)(
    input  wire                   clk,
    input  wire                   rst_n,
    input  wire                   sample_valid,
    input  wire [DATA_WIDTH-1:0]  raw_temp_sensor,     // Current temperature reading
    
    // Anomaly Status Outputs
    output reg                    anomaly_alert,        // Pulses high when anomaly detected
    output reg                    quarantine_req,       // Active high isolation signal
    output reg  [DATA_WIDTH-1:0]  wma_mean,             // Current estimated baseline mean
    output reg  [DATA_WIDTH-1:0]  wma_deviation         // Current mean absolute deviation
);

    // Internal Registers and Wires
    reg [DATA_WIDTH-1:0] mean_reg;
    reg [DATA_WIDTH-1:0] dev_reg;
    reg [3:0]            consecutive_anomalies;

    wire signed [DATA_WIDTH:0] diff_temp;
    wire signed [DATA_WIDTH:0] abs_diff;
    wire [DATA_WIDTH-1:0]      threshold;

    // Signed temperature difference: delta = raw_temp - mean
    assign diff_temp = $signed({1'b0, raw_temp_sensor}) - $signed({1'b0, mean_reg});
    assign abs_diff  = (diff_temp < 0) ? -diff_temp : diff_temp;

    // Threshold = K * deviation (computed via shift-and-add: 3*dev = (dev << 1) + dev)
    assign threshold = (dev_reg << 1) + dev_reg;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            mean_reg              <= {8'd45, 8'd0}; // Initial baseline 45.0 C
            dev_reg               <= {8'd2, 8'd0};  // Initial baseline deviation 2.0 C
            anomaly_alert         <= 1'b0;
            quarantine_req        <= 1'b0;
            consecutive_anomalies <= 4'd0;
        end else if (sample_valid) begin
            // 1. Evaluate Anomaly Condition
            if (abs_diff[DATA_WIDTH-1:0] > threshold) begin
                anomaly_alert <= 1'b1;
                if (consecutive_anomalies < 4'd15)
                    consecutive_anomalies <= consecutive_anomalies + 1'b1;
                
                // Assert hardware quarantine if anomaly persists for 3 consecutive samples
                if (consecutive_anomalies >= 4'd2)
                    quarantine_req <= 1'b1;
            end else begin
                anomaly_alert <= 1'b0;
                if (consecutive_anomalies > 4'd0)
                    consecutive_anomalies <= consecutive_anomalies - 1'b1;
                else
                    quarantine_req <= 1'b0;

                // 2. Update EWMA Mean (only on clean samples to prevent Trojan pollution)
                // mean_next = mean + (diff >>> ALPHA_SHIFT)
                if (diff_temp >= 0)
                    mean_reg <= mean_reg + (diff_temp[DATA_WIDTH-1:0] >> ALPHA_SHIFT);
                else
                    mean_reg <= mean_reg - (abs_diff[DATA_WIDTH-1:0] >> ALPHA_SHIFT);

                // 3. Update Deviation Estimate
                // dev_next = dev + (|diff| - dev) >>> ALPHA_SHIFT
                if (abs_diff[DATA_WIDTH-1:0] >= dev_reg)
                    dev_reg <= dev_reg + ((abs_diff[DATA_WIDTH-1:0] - dev_reg) >> ALPHA_SHIFT);
                else
                    dev_reg <= dev_reg - ((dev_reg - abs_diff[DATA_WIDTH-1:0]) >> ALPHA_SHIFT);
            end
        end else begin
            anomaly_alert <= 1'b0;
        end
    end

    // Assign outputs
    always @(*) begin
        wma_mean      = mean_reg;
        wma_deviation = dev_reg;
    end

endmodule
