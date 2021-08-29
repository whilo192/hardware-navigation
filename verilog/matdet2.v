module matdet2 #(parameter DATA_WIDTH=1, parameter BIN_POS=1, parameter MATRIX_SIZE=1) (input wire clk, input wire rst, output reg complete = 0, input wire [(DATA_WIDTH * MATRIX_SIZE * MATRIX_SIZE)-1:0] a, output reg [DATA_WIDTH-1:0] det=0);
    reg [DATA_WIDTH-1:0] r_mul_lhs;
    reg [DATA_WIDTH-1:0] r_mul_rhs;
    
    wire [DATA_WIDTH-1:0] w_out;
    
    reg [DATA_WIDTH-1:0] count = 0;
    
    mul #(.DATA_WIDTH(DATA_WIDTH), .BIN_POS(BIN_POS)) m1(r_mul_lhs, r_mul_rhs, w_out);
    
    always @(posedge clk or posedge rst)
    begin
        if (rst)
        begin
            complete = 0;
            count = 0;
            r_mul_lhs = 0;
            r_mul_rhs = 0;
        end
        else if (count == 0)
        begin
            r_mul_lhs = a[0*DATA_WIDTH+:DATA_WIDTH];
            r_mul_rhs = a[3*DATA_WIDTH+:DATA_WIDTH];
            #1
            det = w_out;
            count += 1;
        end
        else if (count == 1)
        begin
            r_mul_lhs = a[1*DATA_WIDTH+:DATA_WIDTH];
            r_mul_rhs = a[2*DATA_WIDTH+:DATA_WIDTH];
            #1
            det -= w_out;
            complete = 1;
            count += 1;
        end
    end
endmodule
