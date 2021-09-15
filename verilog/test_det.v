module test #(parameter WIDTH={width}, parameter BIN_POS={bin_pos}, parameter MATRIX_SIZE={n});
    reg [MATRIX_SIZE*MATRIX_SIZE*WIDTH-1:0] matrix;

    wire [WIDTH-1:0] det;

    reg clk = 0;
    reg rst = 1;
    wire complete;
    wire ready;

    matdet{n} #(.DATA_WIDTH(WIDTH), .BIN_POS(BIN_POS), .MATRIX_SIZE(MATRIX_SIZE)) m1(clk, rst, ready, complete, matrix, det);

    integer count = 0;
    integer seed = {py_seed};

    initial
    begin
        $dumpfile("test_det_waveform.vcd");
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
            $display("mat: %h", matrix);
            $display("det: %h", det);

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
