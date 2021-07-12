module matdet3 #(paramater DATA_WIDTH=8) (input wire [DATA_WIDTH:0] a [9:0], output wire [DATA_WIDTH:0] det)
wire [DATA_WIDTH:0] w0, w1, w2, w3, w4, w5, w6, w7;
matdet2({a[4], a[5], a[7], a[8]}, w0);
matdet2({a[3], a[5], a[6], a[8]}, w1);
matdet2({a[3], a[4], a[6], a[7]}, w2);
mul(a[0], w0, w3);
mul(a[1], w1, w4);
mul(a[2], w2, w5);
sub(w3, w4, w6);
add(w6, w5, det);
endmodule
