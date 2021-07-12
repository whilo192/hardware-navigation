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
