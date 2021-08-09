module add #(parameter DATA_WIDTH=0, parameter BIN_POS=0) (input wire [DATA_WIDTH-1:0] a, input wire [DATA_WIDTH-1:0] b, output wire [DATA_WIDTH-1:0] sum);
    assign sum = a + b; //Trivial case for now
endmodule
