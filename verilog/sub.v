module sub #(paramater DATA_WIDTH=9)(input wire [DATA_WIDTH:0] a, input wire [DATA_WIDTH:0] b, output wire [DATA_WIDTH:0] diff)
    assign diff = a - b; //Trivial case for now
endmodule
