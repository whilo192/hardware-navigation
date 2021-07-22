module add #(parameter DATA_WIDTH=8) (input wire [DATA_WIDTH-1:0] a, input wire [DATA_WIDTH-1:0] b, output wire [DATA_WIDTH-1:0] sum);
    assign sum = a + b; //Trivial case for now
endmodule
module sub #(parameter DATA_WIDTH=8) (input wire [DATA_WIDTH-1:0] a, input wire [DATA_WIDTH-1:0] b, output wire [DATA_WIDTH-1:0] diff);
    assign diff = a - b; //Trivial case for now
endmodule
module mul #(parameter DATA_WIDTH=8) (input wire [DATA_WIDTH-1:0] a, input wire [DATA_WIDTH-1:0] b, output wire [DATA_WIDTH-1:0] prod);
    assign prod = a * b; //Trivial case for now - we add fixed point multiplication later
endmodule
module matdet2 #(parameter DATA_WIDTH=8, parameter MATRIX_SIZE=4) (input wire [(DATA_WIDTH * MATRIX_SIZE)-1:0] a, output wire [DATA_WIDTH-1:0] det);
    wire [DATA_WIDTH-1:0] w1, w2;
    
    //a * d
    mul m1(a[7:0], a[31:24], w1);
    
    //b * c
    mul m2(a[15:8], a[23:16], w2);
    
    //ad - bc
    sub s1(w1, w2, det);
endmodule
module matdet3 #(parameter DATA_WIDTH=8, parameter MATRIX_SIZE=9) (input wire [(MATRIX_SIZE * DATA_WIDTH) - 1:0] a, output wire [DATA_WIDTH-1:0] det);
wire [DATA_WIDTH-1:0] w0, w1, w2, w3, w4, w5, w6, w7;
matdet2 md0({a[39:32], a[47:40], a[63:56], a[71:64]}, w0);
matdet2 md1({a[31:24], a[47:40], a[55:48], a[71:64]}, w1);
matdet2 md2({a[31:24], a[39:32], a[55:48], a[63:56]}, w2);
mul m0(a[7:0], w0, w3);
mul m1(a[15:8], w1, w4);
mul m2(a[23:16], w2, w5);
sub op0(w3, w4, w6);
add op1(w6, w5, det);
endmodule
module matdet4 #(parameter DATA_WIDTH=8, parameter MATRIX_SIZE=16) (input wire [(MATRIX_SIZE * DATA_WIDTH) - 1:0] a, output wire [DATA_WIDTH-1:0] det);
wire [DATA_WIDTH-1:0] w0, w1, w2, w3, w4, w5, w6, w7, w8, w9, w10;
matdet3 md0({a[47:40], a[55:48], a[63:56], a[79:72], a[87:80], a[95:88], a[111:104], a[119:112], a[127:120]}, w0);
matdet3 md1({a[39:32], a[55:48], a[63:56], a[71:64], a[87:80], a[95:88], a[103:96], a[119:112], a[127:120]}, w1);
matdet3 md2({a[39:32], a[47:40], a[63:56], a[71:64], a[79:72], a[95:88], a[103:96], a[111:104], a[127:120]}, w2);
matdet3 md3({a[39:32], a[47:40], a[55:48], a[71:64], a[79:72], a[87:80], a[103:96], a[111:104], a[119:112]}, w3);
mul m0(a[7:0], w0, w4);
mul m1(a[15:8], w1, w5);
mul m2(a[23:16], w2, w6);
mul m3(a[31:24], w3, w7);
sub op0(w4, w5, w8);
add op1(w8, w6, w9);
sub op2(w9, w7, det);
endmodule
