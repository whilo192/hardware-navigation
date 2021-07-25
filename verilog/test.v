module test #(parameter WIDTH={width}, parameter MATRIX_SIZE={n});
    reg [MATRIX_SIZE*MATRIX_SIZE*WIDTH-1:0] matrix;

    wire [WIDTH-1:0] det;

    matdet{n} #(.DATA_WIDTH(WIDTH)) m1(matrix, det);
    
    integer count = 0;
    
    initial
    begin
        matrix = 'b0;
    end
    
    always
    begin
        for (integer i = 0; i < MATRIX_SIZE*MATRIX_SIZE; i++)
        begin
            matrix[i*WIDTH+:WIDTH] = $random%10;
        end
            
        #1;

        $display("mat: %h", matrix);
        $display("det: %h", det);
        
        count++;
        
        if (count == 1000)
        begin
            $finish();
        end
    end
endmodule
