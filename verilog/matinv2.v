module matinv2 #(parameter DATA_WIDTH=1, parameter BIN_POS=1, parameter MATRIX_SIZE=1) (input wire clk, input wire rst, output wire complete, input wire [(MATRIX_SIZE * MATRIX_SIZE * DATA_WIDTH) - 1:0] a, output wire [(MATRIX_SIZE * MATRIX_SIZE * DATA_WIDTH) - 1:0] inv, output wire w_singular);
        wire [DATA_WIDTH-1:0] wdet;
        wire [DATA_WIDTH-1:0] wdetdiv;
        
        assign w_singular = wdet == 0;
        
        wire [(MATRIX_SIZE*MATRIX_SIZE*DATA_WIDTH)-1:0] m_trans;
        
        matdet2 #(.DATA_WIDTH(DATA_WIDTH), .BIN_POS(BIN_POS), .MATRIX_SIZE(MATRIX_SIZE)) mdet(clk, rst, complete, a, wdet);
                
        div #(.DATA_WIDTH(DATA_WIDTH), .BIN_POS(BIN_POS)) d1 ({" + rf"{whole_bits}'b1, {bin_pos}'b0" + "}, wdet, wdetdiv);
        
        wire [DATA_WIDTH-1:0] w1;
        wire [DATA_WIDTH-1:0] w2;
            
        assign w1 = {data_width}'b0 - a[1*DATA_WIDTH+:DATA_WIDTH];
        assign w2 = {data_width}'b0 - a[2*DATA_WIDTH+:DATA_WIDTH];
            
        assign m_trans = {a[0*DATA_WIDTH+:DATA_WIDTH], w2, w1, a[3*DATA_WIDTH+:DATA_WIDTH]};
            
        scalvec4 #(.DATA_WIDTH(DATA_WIDTH), .BIN_POS(BIN_POS), .VECTOR_SIZE(MATRIX_SIZE * MATRIX_SIZE)) svm1(wdetdiv, m_trans, inv);
endmodule
