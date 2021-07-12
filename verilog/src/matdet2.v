module matdet2 #(parameter DATA_WIDTH=8, parameter MATRIX_SIZE=4) (input wire [(DATA_WIDTH * MATRIX_SIZE)-1:0] a, output wire [DATA_WIDTH-1:0] det);
    wire [DATA_WIDTH-1:0] w1, w2;
    
    //a * d
    mul m1(a[7:0], a[31:24], w1);
    
    //b * c
    mul m2(a[15:8], a[23:16], w2);
    
    //ad - bc
    sub s1(w1, w2, det);
endmodule
