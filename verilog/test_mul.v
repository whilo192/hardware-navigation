module test #(parameter WIDTH={width}, parameter MATRIX_SIZE={n});
    reg [MATRIX_SIZE*MATRIX_SIZE*WIDTH-1:0] matrix_a;

    reg [MATRIX_SIZE*MATRIX_SIZE*WIDTH-1:0] matrix_b;
    
    wire [MATRIX_SIZE*MATRIX_SIZE*WIDTH-1:0] mul;
    
    matmat{n} #(.DATA_WIDTH(WIDTH)) m1(matrix_a, matrix_b, mul);
    
    integer count = 0;
    integer seed = {py_seed};
    
    always
    begin
        for (integer i = 0; i < MATRIX_SIZE*MATRIX_SIZE; i++)
        begin
            matrix_a[i*WIDTH+:WIDTH] = $random(seed) % 10;
            matrix_b[i*WIDTH+:WIDTH] = $random(seed) % 10;
        end
            
        #1;

        $display("mat_a: %h", matrix_a);
        $display("mat_b: %h", matrix_b);
        $display("mul: %h", mul);
        
        count++;
        
        if (count == {py_count})
        begin
            $finish();
        end
    end
endmodule
