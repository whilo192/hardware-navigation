module test #(parameter WIDTH={width}, parameter BIN_POS={bin_pos}, parameter MATRIX_SIZE={n});
    reg [MATRIX_SIZE*MATRIX_SIZE*WIDTH-1:0] matrix;

    wire [MATRIX_SIZE*MATRIX_SIZE*WIDTH-1:0] inv;

    reg clk = 0;
    reg rst = 0;
    wire complete;
    
    wire w_singular;
    
    matinv{n} #(.DATA_WIDTH(WIDTH), .BIN_POS(BIN_POS)) m1(clk, rst, complete, matrix, inv, w_singular);
    
    integer count = 0;
    integer seed = {py_seed};
    
    initial
    begin
        for (integer i = 0; i < MATRIX_SIZE*MATRIX_SIZE; i++)
        begin
            matrix[i*WIDTH+:WIDTH] = $random(seed) % 10 <<< BIN_POS | $urandom(seed) % 2 ** BIN_POS;
        end
    end
          
    always
    begin
        clk = ~clk;
    
        #1;

        if (complete)
        begin
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
            
            rst = 1;
                
            for (integer i = 0; i < MATRIX_SIZE*MATRIX_SIZE; i++)
            begin
                matrix[i*WIDTH+:WIDTH] = $random(seed) % 10 <<< BIN_POS | $urandom(seed) % 2 ** BIN_POS;
            end
            
            clk = ~clk;
            #1
            clk = ~clk;
            #1
            clk = ~clk;
            #1
            clk = ~clk;
            #1
            
            rst = 0;
        end
    end
endmodule
