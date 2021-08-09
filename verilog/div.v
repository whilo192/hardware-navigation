module div #(parameter DATA_WIDTH=16, parameter BIN_POS=8) (input wire [DATA_WIDTH-1:0] a, input wire [DATA_WIDTH-1:0] b, output wire [DATA_WIDTH-1:0] quot);
    assign quot = (a / b) <<< BIN_POS; //Can't actually be synthesized - but will do for now.
endmodule
