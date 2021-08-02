module div #(parameter DATA_WIDTH=8) (input wire [DATA_WIDTH-1:0] a, input wire [DATA_WIDTH-1:0] b, output wire [DATA_WIDTH-1:0] quot);
    assign quot = a / b; //Can't actually be synthesized - but will do for now.
endmodule
