module matinv2 #(paramater DATA_WIDTH=8) (input wire [DATA_WIDTH:0] a [4:0], output wire [DATA_WIDTH:0] inv)
    wire [DATA_WIDTH:0] w1, w2
    
    //a * d
    mul(a[0], a[4], w1);
    
    //b * c
    mul(a[1], a[2], w2);
    
    //ad - bc
    sub(w1, w2, det);
endmodule
