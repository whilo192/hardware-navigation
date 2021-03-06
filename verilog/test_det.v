module test #(parameter WIDTH={width}, parameter BIN_POS={bin_pos}, parameter MATRIX_SIZE={n});
    reg [MATRIX_SIZE*MATRIX_SIZE*WIDTH-1:0] matrix;

    wire [WIDTH-1:0] det;

    matdet{n} #(.DATA_WIDTH(WIDTH), .BIN_POS(BIN_POS), .MATRIX_SIZE(MATRIX_SIZE)) m1(matrix, det);
    
    integer count = 0;
    integer seed = {py_seed};
    
    always
    begin
        for (integer i = 0; i < MATRIX_SIZE*MATRIX_SIZE; i++)
        begin
            matrix[i*WIDTH+:WIDTH] = $random(seed) % 10 <<< BIN_POS | $urandom(seed) % 2 ** BIN_POS;
        end
            
        #1;

        $display("mat: %h", matrix);
        $display("det: %h", det);
        
        count++;
        
        if (count == {py_count})
        begin
            $finish();
        end
    end
endmodule
