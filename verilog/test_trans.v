module test #(parameter WIDTH={width}, parameter MATRIX_SIZE={n});
    reg [MATRIX_SIZE*MATRIX_SIZE*WIDTH-1:0] matrix;

    wire [MATRIX_SIZE*MATRIX_SIZE*WIDTH-1:0] trans;

    mattrans{n} #(.DATA_WIDTH(WIDTH)) m1(matrix, trans);
    
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
        $display("trans: %h", trans);
        
        count++;
        
        if (count == {py_count})
        begin
            $finish();
        end
    end
endmodule
