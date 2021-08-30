module div #(parameter DATA_WIDTH=0, parameter BIN_POS=0) (input wire clk, input wire signed [DATA_WIDTH-1:0] a, input wire signed [DATA_WIDTH-1:0] b, output reg signed [DATA_WIDTH-1:0] quot);
    reg signed [2*DATA_WIDTH-1:0] r1;
    reg signed [2*DATA_WIDTH-1:0] r2;
    reg signed [3*DATA_WIDTH-1:0] r3;
    
    always @(posedge clk)
    begin
        r1 = a <<< DATA_WIDTH;
        r2 = r1 / b;
        r3 = r2 <<< BIN_POS;
        quot = r3 >>> DATA_WIDTH; //Can't actually be synthesized - but will do for now.
    end
endmodule
