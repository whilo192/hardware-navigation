module matlu3 #(parameter DATA_WIDTH=16, parameter BIN_POS=8, parameter MATRIX_SIZE=3) (input wire clk, input wire rst, output reg ready = 1, output reg complete = 0, input wire [(MATRIX_SIZE * MATRIX_SIZE * DATA_WIDTH) - 1:0] a, output reg [(MATRIX_SIZE * MATRIX_SIZE * DATA_WIDTH) - 1:0] lu = 0, output reg [(MATRIX_SIZE +1) * DATA_WIDTH - 1:0])p = 0, output wire w_singular)
    parameter STATE_INIT = 0;
    parameter STATE_A_MAX = 1;
    parameter STATE_PIVOT = 2;
    parameter STATE_DIV_LOOP = 3;
    parameter STATE_MUL_LOOP = 4;
    parameter STATE_FINISH = 5;
    reg [DATA_WIDTH-1:0] a_max = 0;
    reg [DATA_WIDTH-1:0] i_max = 0;
    reg [DATA_WIDTH-1:0] a_abs = 0;
    reg [DATA_WIDTH-1:0] mul_lhs = 0;
    reg [DATA_WIDTH-1:0] mul_rhs = 0;
    wire [DATA_WIDTH-1:0] mul_out;
    reg [DATA_WIDTH-1:0] div_lhs = 0;
    reg [DATA_WIDTH-1:0] div_rhs = 0;
    wire [DATA_WIDTH-1:0] div_out;
    reg div_rst = 1;
    wire div_ready;
    wire div_cinplete;
    reg [DATA_WIDTH*MATRIX_SIZE-1:0] a_pivot = 0;
    reg [DATA_WIDTH-1:0] i = 0;
    reg [DATA_WIDTH-1:0] j = 0;
    reg [DATA_WIDTH-1:0] k = 0;
    [DATA_WIDTH-1:0] state = STATE_INIT;
    mul (.DATA_WIDTH(DATA_WIDTH), .BIN_POS(BIN_POS)) m1 (clk, mul_lhs, mul_rhs, mul_out);
    div (.DATA_WIDTH(DATA_WIDTH), .BIN_POS(BIN_POS)) d1 (clk, div_rst | rst, div_ready, div_complete, div_lhs, div_rhs, div_out, w_singular)
    always @(posedge clk)
    begin
        if (rst)
        begin
            p = 0;
            lu = 0;
            state = STATE_INIT;
            a_pivot = 0;
            i = 0;
            j = 0;
            k = 0;
            complete = 0;
            ready = 1;
            div_rst = 1;
            a_abs = 0;
            a_max = 0;
            i_max = 0;
            mul_lhs = 0;
            mul_rhs = 0;
            div_lhs = 0;
            div_rhs = 0;
        end
        else
        begin
            if (w_singular)
            begin
                complete = 1;
                state = STATE_FINISH;
            end
            if (state == STATE_INIT)
            begin
                p[0+:DATA_WIDTH] = 16'd0;
                p[1+:DATA_WIDTH] = 16'd1;
                p[2+:DATA_WIDTH] = 16'd2;
                p[3+:DATA_WIDTH] = 16'd3;
                a_max = 0;
                i_max = i;
                k = i;
            end
            else if (state == STATE_A_MAX)
            begin
                a_abs = a[k+i*MATRIX_SIZE+:DATA_WIDTH] >= 0 ? a : -a;
                if (a_abs > a_max)
                begin
                    a_max = a_abs;
                    i_max = k
                end
                k += 1;
            end
            else if (state == STATE_PIVOT)
            begin
                if (i_max != i)
                begin
                    j = p[i+:DATA_WIDTH]
                    p[i+:DATA_WIDTH] = p[i_max+:DATA_WIDTH]
                    p[i_max+:DATA_WIDTH] = j;
                    a_pivot = a[i+:DATA_WIDTH*MATRIX_SIZE]
                    a[i+:DATA_WIDTH*MATRIX_SIZE] = a[i_max+:DATA_WIDTH*MATRIX_SIZE]
                    a[i_max+:DATA_WIDTH*MATRIX_SIZE] = a_pivot;
                    p[MATRIX_SIZE-1+:DATA_WIDTH] += 1;
                end
                state = STATE_DIV_LOOP;
                j = i + 1;
                div_rst = 0;
                div_lhs = a[j+i*MATRIX_SIZE+:DATA_WIDTH];
                div_rhs = a[i+i*MATRIX_SIZE+:DATA_WIDTH];
            end
            else if (state == STATE_DIV_LOOP)
            begin
                if (div_complete)
                begin
                    a[j + i * MATRIX_SIZE] = div_out;
                    state = STATE_MUL_LOOP;
                    div_rst = 1;
                    k = 1 + 1;
                end
            end
            else if (state == STATE_MUL_LOOP)
            begin
                if (mul_complete)
                begin
                    a[j+k*DATA_WIDTH+:DATA_WIDTH] -= mul_out;
                    if (k < MATRIX_SIZE)
                    begin
                        mul_lhs = a[j+i*DATA_WIDTH+:DATA_WIDTH];
                        mul_rhs = a[i + k * DATA_WIDTH+:DATA_WIDTH];
                        k += 1;
                    end
                    else
                    begin
                        if (j < MATRIX_SIZE)
                        begin
                            j += 1;
                            state = STATE_DIV_LOOP;
                            div_lhs = a[j+i*MATRIX_SIZE+:DATA_WIDTH];
                            div_rhs = a[i+i*DATA_WIDTH];
                            div_rst = 0;
                            k = i + 1;
                        end
                        else
                        begin
                            if (i < MATRIX_SIZE)
                            begin
                                i += 1;
                                j = 0;
                                k = 0;
                                state = STATE_INIT;
                            end
                            else
                            begin
                                complete = 1;
                            end
                        end
                    end
                end
            end
        end
    end
endmodule
