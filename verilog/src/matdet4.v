module matdet4 #(paramater DATA_WIDTH=8) (input wire [DATA_WIDTH:0] a [16:0], output wire [DATA_WIDTH:0] det)
wire [DATA_WIDTH:0] w0, w1, w2, w3, w4, w5, w6, w7, w8, w9, w10;
matdet3({a[5], a[6], a[7], a[9], a[10], a[11], a[13], a[14], a[15]}, w0);
matdet3({a[4], a[6], a[7], a[8], a[10], a[11], a[12], a[14], a[15]}, w1);
matdet3({a[4], a[5], a[7], a[8], a[9], a[11], a[12], a[13], a[15]}, w2);
matdet3({a[4], a[5], a[6], a[8], a[9], a[10], a[12], a[13], a[14]}, w3);
mul(a[0], w0, w4);
mul(a[1], w1, w5);
mul(a[2], w2, w6);
mul(a[3], w3, w7);
sub(w4, w5, w8);
add(w8, w6, w9);
sub(w9, w7, det);
endmodule
