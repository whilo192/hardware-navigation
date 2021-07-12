module sub #(parameter DATA_WIDTH=8) (input wire [DATA_WIDTH-1:0] a, input wire [DATA_WIDTH-1:0] b, output wire [DATA_WIDTH-1:0] diff);
    assign diff = a - b; //Trivial case for now
endmodule
