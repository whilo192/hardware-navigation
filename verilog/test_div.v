module test #(parameter WIDTH={width}, parameter BIN_POS={bin_pos});
    reg [WIDTH-1:0] num;
    reg [WIDTH-1:0] denom;

    wire [WIDTH-1:0] quot;

    reg clk = 0;
    reg rst = 1;
    wire complete;
    wire ready;
    wire div_zero;

    div #(.DATA_WIDTH(WIDTH), .BIN_POS(BIN_POS)) d1(clk, rst, ready, complete, num, denom, quot, div_zero);

    integer count = 0;
    integer seed = {py_seed};

    initial
    begin
        $dumpfile("test_div_waveform.vcd");
        $dumpvars(0, test);
        num = $random(seed) % 100 <<< BIN_POS | $urandom(seed) % 2 ** BIN_POS;
        denom = $random(seed) % 100 <<< BIN_POS | $urandom(seed) % 2 ** BIN_POS;
    end

    always
    begin
        clk = ~clk;

        #1;

        if (ready)
        begin
            rst = 0;
        end

        if (complete && !rst)
        begin
            $display("num: %h", num);
            $display("denom: %h", denom);

            if (div_zero)
            begin
                $display("divide by zero");
            end
            else
            begin
                $display("quot: %h", quot);
            end

            count++;

            if (count == {py_count})
            begin
                $finish();
            end

            rst = 1;

            num = $random(seed) % 100 <<< BIN_POS | $urandom(seed) % 2 ** BIN_POS;
            denom = $random(seed) % 100 <<< BIN_POS | $urandom(seed) % 2 ** BIN_POS;
        end
    end
endmodule
