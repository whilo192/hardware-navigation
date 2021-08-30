module mul #(parameter DATA_WIDTH=0, parameter BIN_POS=0) (input wire clk, input wire signed [DATA_WIDTH-1:0] a, input wire signed [DATA_WIDTH-1:0] b, output reg signed [DATA_WIDTH-1:0] prod);
    reg signed [2*DATA_WIDTH-1:0] r1;
    reg signed [2*DATA_WIDTH-1:0] r2;

    always @(posedge clk)
        begin
        r1 = a;
        r2 = b;

        prod = (r1 * r2) >>> BIN_POS;
    end
endmodule

