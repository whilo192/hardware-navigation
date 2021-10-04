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
    mul #(.DATA_WIDTH(DATA_WIDTH)) m1(a[0+:DATA_WIDTH], a[3*DATA_WIDTH+:DATA_WIDTH], w1);
    
    //b * c
    mul #(.DATA_WIDTH(DATA_WIDTH)) m2(a[1*DATA_WIDTH+:DATA_WIDTH], a[2*DATA_WIDTH+:DATA_WIDTH], w2);
    
    //ad - bc
    sub #(.DATA_WIDTH(DATA_WIDTH)) s1(w1, w2, det);
endmodule

module matdet3 #(parameter DATA_WIDTH=32, parameter MATRIX_SIZE=9) (input wire [(MATRIX_SIZE * DATA_WIDTH) - 1:0] a, output wire [DATA_WIDTH-1:0] det);
wire [DATA_WIDTH-1:0] w0, w1, w2, w3, w4, w5, w6, w7;
matdet2 #(.DATA_WIDTH(DATA_WIDTH)) md0({a[128+:32], a[160+:32], a[224+:32], a[256+:32]}, w0);
matdet2 #(.DATA_WIDTH(DATA_WIDTH)) md1({a[96+:32], a[160+:32], a[192+:32], a[256+:32]}, w1);
matdet2 #(.DATA_WIDTH(DATA_WIDTH)) md2({a[96+:32], a[128+:32], a[192+:32], a[224+:32]}, w2);
mul #(.DATA_WIDTH(DATA_WIDTH)) m0(a[0+:32], w0, w3);
mul #(.DATA_WIDTH(DATA_WIDTH)) m1(a[32+:32], w1, w4);
mul #(.DATA_WIDTH(DATA_WIDTH)) m2(a[64+:32], w2, w5);
sub #(.DATA_WIDTH(DATA_WIDTH)) op0(w3, w4, w6);
add #(.DATA_WIDTH(DATA_WIDTH)) op1(w6, w5, det);
endmodule

module matdet4 #(parameter DATA_WIDTH=32, parameter MATRIX_SIZE=16) (input wire [(MATRIX_SIZE * DATA_WIDTH) - 1:0] a, output wire [DATA_WIDTH-1:0] det);
wire [DATA_WIDTH-1:0] w0, w1, w2, w3, w4, w5, w6, w7, w8, w9, w10;
matdet3 #(.DATA_WIDTH(DATA_WIDTH)) md0({a[160+:32], a[192+:32], a[224+:32], a[288+:32], a[320+:32], a[352+:32], a[416+:32], a[448+:32], a[480+:32]}, w0);
matdet3 #(.DATA_WIDTH(DATA_WIDTH)) md1({a[128+:32], a[192+:32], a[224+:32], a[256+:32], a[320+:32], a[352+:32], a[384+:32], a[448+:32], a[480+:32]}, w1);
matdet3 #(.DATA_WIDTH(DATA_WIDTH)) md2({a[128+:32], a[160+:32], a[224+:32], a[256+:32], a[288+:32], a[352+:32], a[384+:32], a[416+:32], a[480+:32]}, w2);
matdet3 #(.DATA_WIDTH(DATA_WIDTH)) md3({a[128+:32], a[160+:32], a[192+:32], a[256+:32], a[288+:32], a[320+:32], a[384+:32], a[416+:32], a[448+:32]}, w3);
mul #(.DATA_WIDTH(DATA_WIDTH)) m0(a[0+:32], w0, w4);
mul #(.DATA_WIDTH(DATA_WIDTH)) m1(a[32+:32], w1, w5);
mul #(.DATA_WIDTH(DATA_WIDTH)) m2(a[64+:32], w2, w6);
mul #(.DATA_WIDTH(DATA_WIDTH)) m3(a[96+:32], w3, w7);
sub #(.DATA_WIDTH(DATA_WIDTH)) op0(w4, w5, w8);
add #(.DATA_WIDTH(DATA_WIDTH)) op1(w8, w6, w9);
sub #(.DATA_WIDTH(DATA_WIDTH)) op2(w9, w7, det);
endmodule

