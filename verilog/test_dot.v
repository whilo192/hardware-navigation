module test #(parameter WIDTH={width}, parameter BIN_POS={bin_pos}, parameter VECTOR_SIZE={n});
    reg [VECTOR_SIZE*VECTOR_SIZE*WIDTH-1:0] vec_a;

    reg [VECTOR_SIZE*VECTOR_SIZE*WIDTH-1:0] vec_b;
    
    wire [WIDTH-1:0] dot;
    
    reg clk = 0;
    reg rst = 0;
    wire complete;
    
    vecvec{n} #(.DATA_WIDTH(WIDTH), .BIN_POS(BIN_POS)) v1(clk, rst, complete, vec_a, matrix_b, dot);
    
    integer count = 0;
    integer seed = {py_seed};
    
    initial
    begin
        for (integer i = 0; i < VECTOR_SIZE; i++)
        begin
            vec_a[i*WIDTH+:WIDTH] = $random(seed) % 10 <<< BIN_POS | $urandom(seed) % 2 ** BIN_POS;
            vec_b[i*WIDTH+:WIDTH] = $random(seed) % 10 <<< BIN_POS | $urandom(seed) % 2 ** BIN_POS;
        end
    end       
    
    always
    begin
        clk = ~clk;
    
        #1;

        if (complete)
        begin
            $display("vec_a: %h", vec_a);
            $display("vec_b: %h", vec_b);
            $display("dot: %h", dot);
            
            count++;
            
            if (count == {py_count})
            begin
                $finish();
            end
            
            rst = 1;
            
            clk = ~clk;
            #1
            clk = ~clk;
            #1
            
            for (integer i = 0; i < VECTOR_SIZE; i++)
            begin
                vec_a[i*WIDTH+:WIDTH] = $random(seed) % 10 <<< BIN_POS | $urandom(seed) % 2 ** BIN_POS;
                vec_b[i*WIDTH+:WIDTH] = $random(seed) % 10 <<< BIN_POS | $urandom(seed) % 2 ** BIN_POS;
            end
            
            rst = 0;
        end
    end
endmodule
