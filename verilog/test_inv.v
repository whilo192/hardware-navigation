module test #(parameter WIDTH={width}, parameter BIN_POS={bin_pos}, parameter MATRIX_SIZE={n});
    reg [MATRIX_SIZE*MATRIX_SIZE*WIDTH-1:0] matrix;

    wire [MATRIX_SIZE*MATRIX_SIZE*WIDTH-1:0] inv;

    wire w_singular;
    
    matinv{n} #(.DATA_WIDTH(WIDTH), .BIN_POS(BIN_POS)) m1(matrix, inv, w_singular);
    
    integer count = 0;
    integer seed = {py_seed};
    
    always
    begin
        for (integer i = 0; i < MATRIX_SIZE*MATRIX_SIZE; i++)
        begin
            matrix[i*WIDTH+:WIDTH] = $random(seed) % 10 <<< BIN_POS | $urandom(seed) % 2 ** BIN_POS; // Golub and von Loam
        end

        #1;

        if (w_singular)
        begin
            $display("singular");
        end
        else
        begin
            $display("mat: %h", matrix);
            $display("inv: %h", inv);
        end
        
        count++;
        
        if (count == {py_count})
        begin
            $finish();
        end
    end
endmodule
