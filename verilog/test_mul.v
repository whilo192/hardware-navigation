module test #(parameter WIDTH={width}, parameter BIN_POS={bin_pos}, parameter MATRIX_SIZE={n});
    reg [MATRIX_SIZE*MATRIX_SIZE*WIDTH-1:0] matrix_a;

    reg [MATRIX_SIZE*MATRIX_SIZE*WIDTH-1:0] matrix_b;
    
    wire [MATRIX_SIZE*MATRIX_SIZE*WIDTH-1:0] mul;
    
    reg clk = 0;
    reg rst = 0;
    wire complete;
    
    matmat{n} #(.DATA_WIDTH(WIDTH), .BIN_POS(BIN_POS)) m1(clk, rst, complete, matrix_a, matrix_b, mul);
    
    integer count = 0;
    integer seed = {py_seed};
    
    initial
    begin
        for (integer i = 0; i < MATRIX_SIZE*MATRIX_SIZE; i++)
        begin
            matrix_a[i*WIDTH+:WIDTH] = $random(seed) % 10 <<< BIN_POS | $urandom(seed) % 2 ** BIN_POS;
            matrix_b[i*WIDTH+:WIDTH] = $random(seed) % 10 <<< BIN_POS | $urandom(seed) % 2 ** BIN_POS;
        end
    end
    
    always
    begin
        clk = ~clk;
    
        #1;

        if (complete)
        begin
            $display("mat_a: %h", matrix_a);
            $display("mat_b: %h", matrix_b);
            $display("mul: %h", mul);
            
            count++;
            
            if (count == {py_count})
            begin
                $finish();
            end
            
            rst = 1;
            
            for (integer i = 0; i < MATRIX_SIZE*MATRIX_SIZE; i++)
            begin
                matrix_a[i*WIDTH+:WIDTH] = $random(seed) % 10 <<< BIN_POS | $urandom(seed) % 2 ** BIN_POS;
                matrix_b[i*WIDTH+:WIDTH] = $random(seed) % 10 <<< BIN_POS | $urandom(seed) % 2 ** BIN_POS;
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
