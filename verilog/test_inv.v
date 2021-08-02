module test #(parameter WIDTH={width}, parameter MATRIX_SIZE={n});
    reg [MATRIX_SIZE*MATRIX_SIZE*WIDTH-1:0] matrix;

    wire [MATRIX_SIZE*MATRIX_SIZE*WIDTH-1:0] inv;

    matinv{n} #(.DATA_WIDTH(WIDTH)) m1(matrix, inv);
    
    integer count = 0;
    integer seed = {py_seed};
    
    always
    begin
        for (integer i = 0; i < MATRIX_SIZE*MATRIX_SIZE; i++)
        begin
            matrix[i*WIDTH+:WIDTH] = $random(seed) % 10;
        end
            
        #1;

        $display("mat: %h", matrix);
        $display("inv: %h", inv);
        
        count++;
        
        if (count == {py_count})
        begin
            $finish();
        end
    end
endmodule
