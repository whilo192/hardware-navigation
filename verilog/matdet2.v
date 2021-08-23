module matdet2 #(parameter DATA_WIDTH=0, parameter BIN_POS=0, parameter MATRIX_SIZE=0) (input wire [(DATA_WIDTH * MATRIX_SIZE * MATRIX_SIZE)-1:0] a, output wire [DATA_WIDTH-1:0] det);
    wire [DATA_WIDTH-1:0] w1, w2;
    
    //a * d
    mul #(.DATA_WIDTH(DATA_WIDTH), .BIN_POS(BIN_POS)) m1(a[0+:DATA_WIDTH], a[3*DATA_WIDTH+:DATA_WIDTH], w1);
    
    //b * c
    mul #(.DATA_WIDTH(DATA_WIDTH), .BIN_POS(BIN_POS)) m2(a[1*DATA_WIDTH+:DATA_WIDTH], a[2*DATA_WIDTH+:DATA_WIDTH], w2);
    
    //ad - bc
    assign det = w1 - w2;
endmodule
