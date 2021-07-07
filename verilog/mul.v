module mul #(paramater DATA_WIDTH=9)(input wire [DATA_WIDTH:0] a, input wire [DATA_WIDTH:0] b, output wire [DATA_WIDTH:0] prod)
    assign prod = a * b; //Trivial case for now - we add fixed point multiplication later
endmodule

