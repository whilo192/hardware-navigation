module test #(parameter WIDTH={width}, parameter BIN_POS={bin_pos}, parameter MATRIX_SIZE={n});
    reg [MATRIX_SIZE*MATRIX_SIZE*WIDTH-1:0] matrix;

    wire [MATRIX_SIZE*MATRIX_SIZE*WIDTH-1:0] lu;
    wire [(MATRIX_SIZE+1)*WIDTH-1:0] p;

    wire singular;

    reg clk = 0;
    reg rst = 1;
    wire complete;
    wire ready;

    matlu{n} #(.DATA_WIDTH(WIDTH), .BIN_POS(BIN_POS), .MATRIX_SIZE(MATRIX_SIZE)) m1(clk, rst, ready, complete, matrix, lu, p, singular);

    integer count = 0;
    integer seed = {py_seed};

    initial
    begin
        $dumpfile("test_lu_waveform.vcd");
        $dumpvars(0, test);
        for (integer i = 0; i < MATRIX_SIZE*MATRIX_SIZE; i++)
        begin
            matrix[i*WIDTH+:WIDTH] = $random(seed) % 10 <<< BIN_POS | $urandom(seed) % 2 ** BIN_POS;
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
            if (singular)
            begin
                $display("singular");
            end
            else
            begin
            $display("mat: %h", matrix);
            $display("lu: %h", lu);
            $display("p: %h", p);
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
        end
    end
endmodule
