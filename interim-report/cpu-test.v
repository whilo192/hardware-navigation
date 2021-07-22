module cpu_test();
    reg clk = 0;
    
    wire [7:0] data_out;
    wire data_out_new;
    
    initial begin
        #200 $finish();
    end
    
    cpu c1(clk, data_out, data_out_new);
    
    always
    begin
        clk = 1;
        #1;
        if (data_out_new)
        begin
            $display("data: %d", data_out);
        end
        clk = 0;
        #1;
    end
endmodule
