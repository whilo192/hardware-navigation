module mul #(parameter DATA_WIDTH=0, parameter BIN_POS=0) (input wire signed [DATA_WIDTH-1:0] a, input wire signed [DATA_WIDTH-1:0] b, output wire signed [DATA_WIDTH-1:0] prod);
    wire signed [2*DATA_WIDTH-1:0] w1;
    wire signed [2*DATA_WIDTH-1:0] w2;

    assign w1 = a;
    assign w2 = b;

    assign prod = (w1 * w2) >>> BIN_POS;
endmodule

