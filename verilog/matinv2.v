module matinv2 #(paramater DATA_WIDTH=8) (input wire [DATA_WIDTH:0] a [4:0], output wire [DATA_WIDTH:0] inv [4:0], output reg [1:0] error_line)
    wire [DATA_WIDTH:0] w1, w2, w3, w4, w5, w6;
    
    //a * d
    mul(a[0], a[4], w1);
    
    //b * c
    mul(a[1], a[2], w2);
    
    //ad - bc
    sub(w1, w2, w3);
    
    // 1 / (ad-bc)
    inv_mul(w3, w4, error_line);
    
    inv_add(a[1], w5);
    inv_add(a[2], w6);
    
    mul(w4, a[4], prod[0]);
    mul(w4, w5, prod[1]);
    mul(w4, w6, prod[2]);
    mul(w4, a[0], prod[3]);
endmodule
