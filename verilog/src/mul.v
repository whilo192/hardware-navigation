module mul #(parameter DATA_WIDTH=8) (input wire [DATA_WIDTH-1:0] a, input wire [DATA_WIDTH-1:0] b, output wire [DATA_WIDTH-1:0] prod);
    assign prod = a * b; //Trivial case for now - we add fixed point multiplication later
endmodule

