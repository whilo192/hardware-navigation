module div #(parameter DATA_WIDTH=16, parameter BIN_POS=8) (input wire [DATA_WIDTH-1:0] a, input wire [DATA_WIDTH-1:0] b, output wire [DATA_WIDTH-1:0] quot);
    wire [2*DATA_WIDTH-1:0] w1;
    wire [2*DATA_WIDTH-1:0] w2;
    wire [3*DATA_WIDTH-1:0] w3;
    
    assign w1 = a <<< DATA_WIDTH;
    assign w2 = w1 / b;
    assign w3 = w2 <<< BIN_POS;
    assign quot = w3 >>> DATA_WIDTH; //Can't actually be synthesized - but will do for now.
endmodule
