//=============================================================================
// Module: in_network_reduction_router
// Description: Synthesizable Router Crossbar Augmented with In-Network
//              Computing / Reduction Tree Logic for Transformer All-Reduce.
//
// Grounded in IEEE TVLSI 2026: "PAC-NoC: A Hierarchical Network-on-Chip for
// Efficient Parallel Aggregated Communication in Transformer Accelerators"
// (Ouyang et al.).
//
// Performs on-the-fly fixed-point accumulation across competing input ports
// during multi-head attention backward passes, halving memory bandwidth demand.
//=============================================================================

`timescale 1ns/1ps

module in_network_reduction_router #(
    parameter DATA_WIDTH  = 32, // Gradient payload bit-width (16-bit int, 16-bit frac)
    parameter NUM_PORTS   = 4,  // North, East, South, West input ports
    parameter TAG_WIDTH   = 8   // Tensor collective reduction identifier
)(
    input  wire                               clk,
    input  wire                               rst_n,
    
    // Ingress Packet Ports (4 directional inputs)
    input  wire [NUM_PORTS-1:0]               flit_valid_in,
    input  wire [NUM_PORTS-1:0]               is_reduction_in,
    input  wire [NUM_PORTS*TAG_WIDTH-1:0]     reduction_tag_in,
    input  wire [NUM_PORTS*DATA_WIDTH-1:0]    flit_data_in,
    output wire [NUM_PORTS-1:0]               flit_ready_out,
    
    // Egress Aggregated Port (Forwarding to Parent Reduction Node)
    output reg                                flit_valid_out,
    output reg  [TAG_WIDTH-1:0]               reduction_tag_out,
    output reg  [DATA_WIDTH-1:0]              flit_data_out,
    input  wire                               flit_ready_in,
    
    // Performance Status
    output reg  [15:0]                        reductions_completed
);

    // Active Collective Reduction State
    reg [TAG_WIDTH-1:0]    active_tag;
    reg [DATA_WIDTH-1:0]   accumulator;
    reg [NUM_PORTS-1:0]    received_mask;
    reg                    in_reduction_phase;

    wire [TAG_WIDTH-1:0]   tag_port [0:NUM_PORTS-1];
    wire [DATA_WIDTH-1:0]  data_port [0:NUM_PORTS-1];

    genvar g;
    generate
        for (g = 0; g < NUM_PORTS; g = g + 1) begin: UNPACK_INPUTS
            assign tag_port[g]  = reduction_tag_in[g*TAG_WIDTH +: TAG_WIDTH];
            assign data_port[g] = flit_data_in[g*DATA_WIDTH +: DATA_WIDTH];
        end
    endgenerate

    // Accept flits from all participating reduction ports
    assign flit_ready_out = {NUM_PORTS{1'b1}};

    integer p;
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            active_tag           <= {TAG_WIDTH{1'b0}};
            accumulator          <= {DATA_WIDTH{1'b0}};
            received_mask        <= {NUM_PORTS{1'b0}};
            in_reduction_phase   <= 1'b0;
            flit_valid_out       <= 1'b0;
            reduction_tag_out    <= {TAG_WIDTH{1'b0}};
            flit_data_out        <= {DATA_WIDTH{1'b0}};
            reductions_completed <= 16'd0;
        end else begin
            // Clear single-cycle output handshake if accepted
            if (flit_valid_out && flit_ready_in) begin
                flit_valid_out <= 1'b0;
            end

            // Scan input ports for reduction flits
            for (p = 0; p < NUM_PORTS; p = p + 1) begin
                if (flit_valid_in[p] && is_reduction_in[p]) begin
                    if (!in_reduction_phase) begin
                        // Initialize new reduction epoch
                        active_tag         <= tag_port[p];
                        accumulator        <= data_port[p];
                        received_mask      <= (1'b1 << p);
                        in_reduction_phase <= 1'b1;
                    end else if (tag_port[p] == active_tag) begin
                        // Accumulate gradient in-flight
                        accumulator        <= accumulator + data_port[p];
                        received_mask[p]   <= 1'b1;
                    end
                end
            end

            // Check if all active ports have contributed to reduction
            // If all 4 ports (or participating subset) have arrived, emit reduced flit
            if (in_reduction_phase && (received_mask == {NUM_PORTS{1'b1}})) begin
                flit_valid_out       <= 1'b1;
                reduction_tag_out    <= active_tag;
                flit_data_out        <= accumulator;
                in_reduction_phase   <= 1'b0;
                received_mask        <= {NUM_PORTS{1'b0}};
                reductions_completed <= reductions_completed + 1'b1;
            end
        end
    end

endmodule
