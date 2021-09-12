module test #(parameter WIDTH={width}, parameter BIN_POS={bin_pos}, parameter MATRIX_SIZE={n});
    reg [MATRIX_SIZE*MATRIX_SIZE*WIDTH-1:0] matrix;

    wire [MATRIX_SIZE*MATRIX_SIZE*WIDTH-1:0] trans;

    mattrans{n} #(.DATA_WIDTH(WIDTH), .BIN_POS(BIN_POS)) m1(matrix, trans);
    
    integer count = 0;
    integer seed = {py_seed};
    
    initial begin
        $dumpfile("test_trans_waveform.vcd");
        $dumpvars(0, test);
    end
    
    always
    begin
        for (integer i = 0; i < MATRIX_SIZE*MATRIX_SIZE; i++)
        begin
            matrix[i*WIDTH+:WIDTH] = $random(seed) % 10 <<< BIN_POS | $urandom(seed) % 2 ** BIN_POS;
        end
            
        #1;

        $display("mat: %h", matrix);
        $display("trans: %h", trans);
        
        count++;
        
        if (count == {py_count})
        begin
            $finish();
        end
    end
endmodule
