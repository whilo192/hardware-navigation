module mul #(parameter DATA_WIDTH=0, parameter BIN_POS=0) (input wire clk, input wire signed [DATA_WIDTH-1:0] a, input wire signed [DATA_WIDTH-1:0] b, output wire signed [DATA_WIDTH-1:0] prod);
    wire signed [2*DATA_WIDTH-1:0] r1;
    wire signed [2*DATA_WIDTH-1:0] r2;

    assign r1 = a;
    assign r2 = b;

    assign prod = (r1 * r2) >>> BIN_POS;
endmodule

