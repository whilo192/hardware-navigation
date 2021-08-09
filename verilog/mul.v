module mul #(parameter DATA_WIDTH=16, parameter BIN_POS=8) (input wire [DATA_WIDTH-1:0] a, input wire [DATA_WIDTH-1:0] b, output wire [DATA_WIDTH-1:0] prod);
    wire [DATA_WIDTH*2-1:0] w1;
    assign w1 = (a*b);
    assign prod = w1 >>> BIN_POS;
endmodule

