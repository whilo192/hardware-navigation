module test #(parameter WIDTH={width}, parameter BIN_POS={bin_pos}, parameter MATRIX_SIZE={n});
    reg [MATRIX_SIZE*MATRIX_SIZE*WIDTH-1:0] matrix;

    wire [MATRIX_SIZE*MATRIX_SIZE*WIDTH-1:0] inv;

    reg clk = 0;
    reg rst = 1;
    wire complete;
    wire ready;

    wire w_singular;

    matinv{n} #(.DATA_WIDTH(WIDTH), .BIN_POS(BIN_POS), .MATRIX_SIZE(MATRIX_SIZE)) m1(clk, rst, ready, complete, matrix, inv, w_singular);

    integer count = 0;
    integer seed = {py_seed};

    initial
    begin
        //$dumpfile("test_inv_waveform.vcd");
        //$dumpvars(0, test);
        for (integer i = 0; i < MATRIX_SIZE*MATRIX_SIZE; i++)
        begin
            if (BIN_POS < 32)
            begin
                matrix[i*WIDTH+:WIDTH] = $random(seed) % 10 <<< BIN_POS | $urandom(seed) % 2 ** BIN_POS;
            end
            else
            begin
                matrix[i*WIDTH+:WIDTH] = $random(seed) % 10 <<< BIN_POS | ($urandom(seed) << (BIN_POS - 32));
            end
        end
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
                if (BIN_POS < 32)
                begin
                    matrix[i*WIDTH+:WIDTH] = $random(seed) % 10 <<< BIN_POS | $urandom(seed) % 2 ** BIN_POS;
                end
                else
                begin
                    matrix[i*WIDTH+:WIDTH] = $random(seed) % 10 <<< BIN_POS | ($urandom(seed) << (BIN_POS - 32));
                end
            end
        end
    end
endmodule
