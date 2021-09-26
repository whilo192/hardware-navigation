#!/usr/bin/env python3

import os
import sys
import shutil

current_indent = 0

def verilog_write(fd, line):
    global current_indent

    if line == "end":
        current_indent -= 1
    elif line == "endmodule":
        current_indent -= 1

    fd.write((" " * (4 * current_indent)) + line)
    fd.write('\n')

    if line == "begin":
        current_indent += 1
    elif line.startswith("module"):
        current_indent += 1

def generate_scalar_vector(dir, n, data_width, bin_pos):
    with open(dir + rf"/scalvec{n}.v", 'w') as out_file:
        verilog_write(out_file, rf"module scalvec{n} #(parameter DATA_WIDTH={data_width}, parameter BIN_POS={bin_pos}, parameter VECTOR_SIZE={n}) (input wire clk, input wire [DATA_WIDTH - 1:0] a, input wire [(VECTOR_SIZE * DATA_WIDTH) - 1:0] b, output wire [(VECTOR_SIZE * DATA_WIDTH) - 1:0] scale);")

        empty_bits = (n-1) * data_width

        for i in range(n):
            verilog_write(out_file, rf"wire [DATA_WIDTH-1:0] w{i};")

        for i in range(n):
            i_str = rf"{i}*DATA_WIDTH+:DATA_WIDTH"
            verilog_write(out_file, rf"mul #(.DATA_WIDTH(DATA_WIDTH), .BIN_POS(BIN_POS)) m{i}(clk, a, b[{i_str}], w{i});" + "\n")

        verilog_write(out_file, rf"assign scale = " + "{" + ",".join([rf"w{i}" for i in range(n-1,-1,-1)]) + "};")

        verilog_write(out_file, rf"endmodule")

def generate_vector_vector(dir, n, data_width, bin_pos):
    with open(dir + rf"/vecvec{n}.v", 'w') as out_file:
        verilog_write(out_file, rf"module vecvec{n} #(parameter DATA_WIDTH={data_width}, parameter BIN_POS={bin_pos}, parameter VECTOR_SIZE={n}) (input wire clk, input wire rst, output reg ready = 1, output reg complete = 0, input wire [(VECTOR_SIZE * DATA_WIDTH) - 1:0] a, input wire [(VECTOR_SIZE * DATA_WIDTH) - 1:0] b, output reg [DATA_WIDTH - 1:0] dot = 0);")

        verilog_write(out_file, rf"reg [DATA_WIDTH-1:0] count = 0;")

        verilog_write(out_file, rf"reg [DATA_WIDTH-1:0] r_mul_lhs = 0;")
        verilog_write(out_file, rf"reg [DATA_WIDTH-1:0] r_mul_rhs = 0;")

        verilog_write(out_file, rf"wire [DATA_WIDTH-1:0] w_mul_out;")
        verilog_write(out_file, rf"wire [DATA_WIDTH-1:0] w_add_out;")

        verilog_write(out_file, rf"mul #(.DATA_WIDTH(DATA_WIDTH), .BIN_POS(BIN_POS)) m1(clk, r_mul_lhs, r_mul_rhs, w_mul_out);")

        verilog_write(out_file, rf"always @(posedge clk)")
        verilog_write(out_file, rf"begin")

        verilog_write(out_file, rf"if (rst)")
        verilog_write(out_file, rf"begin")
        verilog_write(out_file, rf"ready = 1;")
        verilog_write(out_file, rf"count = 0;")
        verilog_write(out_file, rf"dot = 0;")
        verilog_write(out_file, rf"complete = 0;")
        verilog_write(out_file, rf"r_mul_lhs = 0;")
        verilog_write(out_file, rf"r_mul_rhs = 0;")
        verilog_write(out_file, rf"end")
        verilog_write(out_file, rf"else")
        verilog_write(out_file, rf"begin")
        verilog_write(out_file, rf"ready = 0;")
        for i in range(n+1):
            two_i = 2 * i
            two_i_plus_1 = 2 * i + 1
            verilog_write(out_file, ("else " if i > 0 else "") + rf"if (count == {two_i})")
            verilog_write(out_file, rf"begin")

            if i > 0:
                verilog_write(out_file, rf"dot = dot + w_mul_out;")

            if i == n:
                verilog_write(out_file, rf"complete = 1;")
            else:
                verilog_write(out_file, rf"r_mul_lhs = a[{i}*DATA_WIDTH+:DATA_WIDTH];")
                verilog_write(out_file, rf"r_mul_rhs = b[{i}*DATA_WIDTH+:DATA_WIDTH];")

            verilog_write(out_file, rf"count = count + 1;")

            verilog_write(out_file, rf"end")
            verilog_write(out_file, rf"else if (count == {two_i_plus_1})")
            verilog_write(out_file, rf"begin")
            verilog_write(out_file, rf"count = count + 1;")
            verilog_write(out_file, rf"end")

        verilog_write(out_file, rf"end")
        verilog_write(out_file, rf"end")

        verilog_write(out_file, rf"endmodule")

def generate_matrix_matrix(dir, n, data_width, bin_pos):
    n2 = n ** 2

    def gen_row_col_map(j, i):
        row_map = "{" + ",".join(["a[" + str(j * n + x) + "*DATA_WIDTH+:DATA_WIDTH]" for x in range(n)]) + "}"
        col_map = "{" + ",".join(["b[" + str(i + n * x) + "*DATA_WIDTH+:DATA_WIDTH]" for x in range(n)]) + "}"

        return (row_map, col_map)

    with open(dir + rf"/matmat{n}.v", 'w') as out_file:
        verilog_write(out_file, rf"module matmat{n} #(parameter DATA_WIDTH={data_width}, parameter BIN_POS={bin_pos}, parameter MATRIX_SIZE={n}) (input wire clk, input wire rst, output reg ready = 1, output reg complete = 0, input wire [(MATRIX_SIZE * MATRIX_SIZE * DATA_WIDTH) - 1:0] a, input wire [(MATRIX_SIZE * MATRIX_SIZE * DATA_WIDTH) - 1:0] b, output reg [(MATRIX_SIZE * MATRIX_SIZE * DATA_WIDTH) - 1:0] mul = 0);")

        verilog_write(out_file, rf"reg [DATA_WIDTH-1:0] count = 0;")

        verilog_write(out_file, rf"wire subcomplete;")
        verilog_write(out_file, rf"wire subready;")
        verilog_write(out_file, rf"reg subrst = 0;")

        verilog_write(out_file, rf"reg [MATRIX_SIZE * DATA_WIDTH - 1:0] r_lhs = 0;")
        verilog_write(out_file, rf"reg [MATRIX_SIZE * DATA_WIDTH - 1:0] r_rhs = 0;")

        verilog_write(out_file, rf"wire [DATA_WIDTH-1:0] w_out;")

        verilog_write(out_file, rf"vecvec{n} #(.DATA_WIDTH(DATA_WIDTH), .VECTOR_SIZE(MATRIX_SIZE), .BIN_POS(BIN_POS)) v1(clk, subrst | rst, subready, subcomplete, r_lhs, r_rhs, w_out);")

        count = 0

        verilog_write(out_file, rf"always @(posedge clk)")
        verilog_write(out_file, rf"begin")

        (row_map, col_map) = gen_row_col_map(0, 0)

        verilog_write(out_file, rf"if (rst)")
        verilog_write(out_file, rf"begin")
        verilog_write(out_file, rf"count = 0;")
        verilog_write(out_file, rf"ready = 1;")
        verilog_write(out_file, rf"complete = 0;")
        verilog_write(out_file, rf"subrst = 0;")
        verilog_write(out_file, rf"r_lhs = {row_map};")
        verilog_write(out_file, rf"r_rhs = {col_map};")
        verilog_write(out_file, rf"mul = 0;")
        verilog_write(out_file, rf"end")
        verilog_write(out_file, rf"else if (subrst && subready)")
        verilog_write(out_file, rf"begin")
        verilog_write(out_file, rf"subrst = 0;")
        verilog_write(out_file, rf"end")
        verilog_write(out_file, rf"else if (!subrst)")
        verilog_write(out_file, rf"begin")
        verilog_write(out_file, rf"ready = 0;")

        for i in range(n): #col
            for j in range(n): #row
                (row_map, col_map) = gen_row_col_map(j, i)

                mat_count = j * n + i

                verilog_write(out_file, ("else " if count != 0 else "") +  rf"if (count == {count})")
                verilog_write(out_file, rf"begin")

                verilog_write(out_file, rf"r_lhs = {row_map};")
                verilog_write(out_file, rf"r_rhs = {col_map};")

                verilog_write(out_file, rf"if (subcomplete)")
                verilog_write(out_file, rf"begin")
                verilog_write(out_file, rf"mul[{mat_count}*DATA_WIDTH+:DATA_WIDTH] = w_out;")
                verilog_write(out_file, rf"subrst = 1;")
                verilog_write(out_file, rf"count = count + 1;")

                verilog_write(out_file, rf"end")
                verilog_write(out_file, rf"end")

                count += 1

        verilog_write(out_file, rf"else if (count == {count} && subcomplete)")
        verilog_write(out_file, rf"begin")
        verilog_write(out_file, rf"complete = 1;")
        verilog_write(out_file, rf"end")
        verilog_write(out_file, rf"end")
        verilog_write(out_file, rf"end")

        verilog_write(out_file, rf"endmodule")


def generate_matrix_transpose(dir, n, data_width, bin_pos):
    n2 = n ** 2

    with open(dir + rf"/mattrans{n}.v", 'w') as out_file:
        verilog_write(out_file, rf"module mattrans{n} #(parameter DATA_WIDTH={data_width}, parameter BIN_POS={bin_pos}, parameter MATRIX_SIZE={n}) (input wire [(MATRIX_SIZE * MATRIX_SIZE * DATA_WIDTH) - 1:0] in, output wire [(MATRIX_SIZE * MATRIX_SIZE * DATA_WIDTH) - 1:0] out);")

        for i in range(n): #col
            for j in range(n): #row
                in_pos = j * n + i
                out_pos = i * n + j
                verilog_write(out_file, rf"assign out[{out_pos}*DATA_WIDTH+:DATA_WIDTH] = in[{in_pos}*DATA_WIDTH+:DATA_WIDTH];")

        verilog_write(out_file, rf"endmodule")

def generate_matrix_determinant(dir, n, data_width, bin_pos):   
    with open(dir + rf"/matdet{n}.v", 'w') as out_file:
        verilog_write(out_file, rf"module matdet{n} #(parameter DATA_WIDTH={data_width}, parameter BIN_POS={bin_pos}, parameter MATRIX_SIZE={n}) (input wire clk, input wire rst, output reg ready = 1, output reg complete = 0, input wire [(MATRIX_SIZE * MATRIX_SIZE * DATA_WIDTH) - 1:0] a, output reg [DATA_WIDTH-1:0] det = 0);")

        verilog_write(out_file, rf"wire [(MATRIX_SIZE * MATRIX_SIZE * DATA_WIDTH) - 1:0] lu;")
        verilog_write(out_file, rf"wire [((MATRIX_SIZE + 1) * DATA_WIDTH) - 1:0] p;")

        verilog_write(out_file, rf"wire lu_ready;")
        verilog_write(out_file, rf"wire lu_complete;")
        verilog_write(out_file, rf"wire singular;")
        verilog_write(out_file, rf"reg [DATA_WIDTH-1:0] count = 0;")
        verilog_write(out_file, rf"reg last_mul = 0;")

        verilog_write(out_file, rf"wire [DATA_WIDTH-1:0] mul_out;")
        verilog_write(out_file, rf"reg [DATA_WIDTH-1:0] mul_lhs = 0;")
        verilog_write(out_file, rf"reg [DATA_WIDTH-1:0] mul_rhs = 0;")

        verilog_write(out_file, rf"matlu{n} #(.DATA_WIDTH(DATA_WIDTH), .BIN_POS(BIN_POS), .MATRIX_SIZE(MATRIX_SIZE)) m1(clk, rst, lu_ready, lu_complete, a, lu, p, singular);")
        verilog_write(out_file, rf"mul #(.DATA_WIDTH(DATA_WIDTH), .BIN_POS(BIN_POS)) m2(clk, mul_lhs, mul_rhs, mul_out);")

        verilog_write(out_file, rf"always @(posedge clk)")
        verilog_write(out_file, rf"begin")

        verilog_write(out_file, rf"if (rst)")
        verilog_write(out_file, rf"begin")
        verilog_write(out_file, rf"ready = 1;")
        verilog_write(out_file, rf"complete = 0;")
        verilog_write(out_file, rf"count = 0;")
        verilog_write(out_file, rf"det = 0;")
        verilog_write(out_file, rf"mul_lhs = 0;")
        verilog_write(out_file, rf"mul_rhs = 0;")
        verilog_write(out_file, rf"last_mul = 0;")
        verilog_write(out_file, rf"end")
        verilog_write(out_file, rf"else")
        verilog_write(out_file, rf"begin")
        verilog_write(out_file, rf"if (lu_complete)")
        verilog_write(out_file, rf"begin")
        verilog_write(out_file, rf"if (singular)")
        verilog_write(out_file, rf"begin")
        verilog_write(out_file, rf"det = 0;")
        verilog_write(out_file, rf"complete = 1;")
        verilog_write(out_file, rf"end")
        verilog_write(out_file, rf"else")
        verilog_write(out_file, rf"begin")
        verilog_write(out_file, rf"if (last_mul)")
        verilog_write(out_file, rf"begin")
        verilog_write(out_file, rf"last_mul = 0;")
        verilog_write(out_file, rf"end")
        verilog_write(out_file, rf"else if (count == 0)")
        verilog_write(out_file, rf"begin")
        verilog_write(out_file, rf"last_mul = 1;")
        verilog_write(out_file, rf"mul_lhs = lu[0+:DATA_WIDTH];")
        verilog_write(out_file, rf"count = count + 1;")
        verilog_write(out_file, rf"mul_rhs = lu[(count+count*MATRIX_SIZE)*DATA_WIDTH+:DATA_WIDTH];")
        verilog_write(out_file, rf"end")
        verilog_write(out_file, rf"else if (count < MATRIX_SIZE - 1)")
        verilog_write(out_file, rf"begin")
        verilog_write(out_file, rf"last_mul = 1;")
        verilog_write(out_file, rf"det = mul_out;")
        verilog_write(out_file, rf"mul_lhs = det;")
        verilog_write(out_file, rf"count = count + 1;")
        verilog_write(out_file, rf"mul_rhs = lu[(count+count*MATRIX_SIZE)*DATA_WIDTH+:DATA_WIDTH];")
        verilog_write(out_file, rf"end")
        verilog_write(out_file, rf"else if (count == MATRIX_SIZE - 1)")
        verilog_write(out_file, rf"begin")
        verilog_write(out_file, rf"det = mul_out;")
        verilog_write(out_file, rf"complete = 1;")
        verilog_write(out_file, rf"count = count + 1;")
        verilog_write(out_file, rf"if ((p[MATRIX_SIZE*DATA_WIDTH+:DATA_WIDTH] - MATRIX_SIZE) & {data_width}'b1)")
        verilog_write(out_file, rf"begin")
        verilog_write(out_file, rf"det = ~det+1;")
        verilog_write(out_file, rf"end")
        verilog_write(out_file, rf"end")
        verilog_write(out_file, rf"end")
        verilog_write(out_file, rf"end")
        verilog_write(out_file, rf"end")

        verilog_write(out_file, rf"end")
        verilog_write(out_file, rf"endmodule")

def generate_matrix_lu(dir, n, data_width, bin_pos):
    with open(dir + rf"/matlu{n}.v", 'w') as out_file:
        verilog_write(out_file, rf"module matlu{n} #(parameter DATA_WIDTH={data_width}, parameter BIN_POS={bin_pos}, parameter MATRIX_SIZE={n}) (input wire clk, input wire rst, output reg ready = 1, output reg complete = 0, input wire [(MATRIX_SIZE * MATRIX_SIZE * DATA_WIDTH) - 1:0] a, output reg [(MATRIX_SIZE * MATRIX_SIZE * DATA_WIDTH) - 1:0] lu = 0, output reg [(MATRIX_SIZE + 1) * DATA_WIDTH - 1:0] p = 0, output reg r_singular = 0);")

        verilog_write(out_file, rf"parameter STATE_INIT = 0;")
        verilog_write(out_file, rf"parameter STATE_LOOP_INIT = 1;")
        verilog_write(out_file, rf"parameter STATE_A_MAX = 2;")
        verilog_write(out_file, rf"parameter STATE_PIVOT = 3;")
        verilog_write(out_file, rf"parameter STATE_DIV_LOOP = 4;")
        verilog_write(out_file, rf"parameter STATE_MUL_LOOP = 5;")
        verilog_write(out_file, rf"parameter STATE_FINISH = 6;")

        verilog_write(out_file, rf"parameter ROW_SIZE = MATRIX_SIZE * DATA_WIDTH;")

        verilog_write(out_file, rf"reg [DATA_WIDTH-1:0] a_max = 0;")
        verilog_write(out_file, rf"reg [DATA_WIDTH-1:0] i_max = 0;")
        
        verilog_write(out_file, rf"reg last_mul = 1;")

        verilog_write(out_file, rf"reg [DATA_WIDTH-1:0] a_abs = 0;")

        verilog_write(out_file, rf"reg [DATA_WIDTH-1:0] mul_lhs = 0;")
        verilog_write(out_file, rf"reg [DATA_WIDTH-1:0] mul_rhs = 0;")
        verilog_write(out_file, rf"wire [DATA_WIDTH-1:0] mul_out;")

        verilog_write(out_file, rf"reg [DATA_WIDTH-1:0] div_lhs = 0;")
        verilog_write(out_file, rf"reg [DATA_WIDTH-1:0] div_rhs = 0;")
        verilog_write(out_file, rf"wire [DATA_WIDTH-1:0] div_out;")

        verilog_write(out_file, rf"wire w_singular;")

        verilog_write(out_file, rf"reg div_rst = 1;")
        verilog_write(out_file, rf"wire div_ready;")
        verilog_write(out_file, rf"wire div_cinplete;")

        verilog_write(out_file, rf"reg [DATA_WIDTH*MATRIX_SIZE-1:0] a_pivot = 0;")

        verilog_write(out_file, rf"reg [DATA_WIDTH-1:0] i = 0;")
        verilog_write(out_file, rf"reg [DATA_WIDTH-1:0] j = 0;")
        verilog_write(out_file, rf"reg [DATA_WIDTH-1:0] k = 0;")

        verilog_write(out_file, rf"reg [DATA_WIDTH-1:0] state = STATE_INIT;")

        verilog_write(out_file, rf"mul #(.DATA_WIDTH(DATA_WIDTH), .BIN_POS(BIN_POS)) m1(clk, mul_lhs, mul_rhs, mul_out);")
        verilog_write(out_file, rf"div #(.DATA_WIDTH(DATA_WIDTH), .BIN_POS(BIN_POS)) d1(clk, div_rst | rst, div_ready, div_complete, div_lhs, div_rhs, div_out, w_singular);")

        verilog_write(out_file, rf"always @(posedge clk)")
        verilog_write(out_file, rf"begin")

        verilog_write(out_file, rf"if (rst)")
        verilog_write(out_file, rf"begin")
        verilog_write(out_file, rf"p = 0;")
        verilog_write(out_file, rf"lu = 0;")
        verilog_write(out_file, rf"state = STATE_INIT;")
        verilog_write(out_file, rf"a_pivot = 0;")
        verilog_write(out_file, rf"i = 0;")
        verilog_write(out_file, rf"j = 0;")
        verilog_write(out_file, rf"k = 0;")
        verilog_write(out_file, rf"complete = 0;")
        verilog_write(out_file, rf"ready = 1;")
        verilog_write(out_file, rf"div_rst = 1;")
        verilog_write(out_file, rf"a_abs = 0;")
        verilog_write(out_file, rf"a_max = 0;")
        verilog_write(out_file, rf"i_max = 0;")
        verilog_write(out_file, rf"mul_lhs = 0;")
        verilog_write(out_file, rf"mul_rhs = 0;")
        verilog_write(out_file, rf"div_lhs = 0;")
        verilog_write(out_file, rf"div_rhs = 0;")
        verilog_write(out_file, rf"r_singular = 0;")
        verilog_write(out_file, rf"last_mul = 1;")
        verilog_write(out_file, rf"end")
        verilog_write(out_file, rf"else")
        verilog_write(out_file, rf"begin")

        verilog_write(out_file, rf"ready = 0;")
        verilog_write(out_file, rf"if (last_mul)")
        verilog_write(out_file, rf"begin")
        verilog_write(out_file, rf"last_mul = 0;")
        verilog_write(out_file, rf"end")
        verilog_write(out_file, rf"else if (state == STATE_INIT)")
        verilog_write(out_file, rf"begin")
        verilog_write(out_file, rf"lu = a;")
        verilog_write(out_file, rf"state = STATE_LOOP_INIT;")
        verilog_write(out_file, rf"end")
        verilog_write(out_file, rf"else if (state == STATE_LOOP_INIT)")
        verilog_write(out_file, rf"begin")

        for i in range(n+1):
            verilog_write(out_file, rf"p[{i}*DATA_WIDTH+:DATA_WIDTH] = {data_width}'d{i};")

        verilog_write(out_file, rf"a_max = 0;")
        verilog_write(out_file, rf"i_max = i;")

        verilog_write(out_file, rf"k = i;")
        verilog_write(out_file, rf"state = STATE_A_MAX;")

        verilog_write(out_file, rf"end")


        verilog_write(out_file, rf"else if (state == STATE_A_MAX)")
        verilog_write(out_file, rf"begin")

        verilog_write(out_file, rf"if (k < MATRIX_SIZE)")
        verilog_write(out_file, rf"begin")

        verilog_write(out_file, rf"a_abs = lu[(i+k*MATRIX_SIZE)*DATA_WIDTH+:DATA_WIDTH] >= 0 ? a : -a;")

        verilog_write(out_file, rf"if (a_abs > a_max)")
        verilog_write(out_file, rf"begin")

        verilog_write(out_file, rf"a_max = a_abs;")
        verilog_write(out_file, rf"i_max = k;")

        verilog_write(out_file, rf"end")

        verilog_write(out_file, rf"k = k + 1;")

        verilog_write(out_file, rf"end")
        verilog_write(out_file, rf"else")
        verilog_write(out_file, rf"begin")
        verilog_write(out_file, rf"state = STATE_PIVOT;")
        verilog_write(out_file, rf"end")
        verilog_write(out_file, rf"end")

        verilog_write(out_file, rf"else if (state == STATE_PIVOT)")
        verilog_write(out_file, rf"begin")

        verilog_write(out_file, rf"if (a_max == 0)")
        verilog_write(out_file, rf"begin")
        verilog_write(out_file, rf"r_singular = 1;")
        verilog_write(out_file, rf"state = STATE_FINISH;")
        verilog_write(out_file, rf"end")
        verilog_write(out_file, rf"else if (i_max != i)")
        verilog_write(out_file, rf"begin")

        verilog_write(out_file, rf"j = p[i*DATA_WIDTH+:DATA_WIDTH];")
        verilog_write(out_file, rf"p[i*DATA_WIDTH+:DATA_WIDTH] = p[i_max*DATA_WIDTH+:DATA_WIDTH];")
        verilog_write(out_file, rf"p[i_max*DATA_WIDTH+:DATA_WIDTH] = j;")

        verilog_write(out_file, rf"a_pivot = lu[i*ROW_SIZE+:ROW_SIZE];")
        verilog_write(out_file, rf"lu[i*ROW_SIZE+:ROW_SIZE] = lu[i_max*ROW_SIZE+:ROW_SIZE];")
        verilog_write(out_file, rf"lu[i_max*ROW_SIZE+:ROW_SIZE] = a_pivot;")

        verilog_write(out_file, rf"p[MATRIX_SIZE*DATA_WIDTH+:DATA_WIDTH] = p[MATRIX_SIZE*DATA_WIDTH+:DATA_WIDTH] + 1;")

        verilog_write(out_file, rf"end")
        verilog_write(out_file, rf"state = STATE_DIV_LOOP;")
        verilog_write(out_file, rf"j = i + 1;")
        verilog_write(out_file, rf"if (j < MATRIX_SIZE)")
        verilog_write(out_file, rf"begin")
        verilog_write(out_file, rf"div_rst = 0;")
        verilog_write(out_file, rf"div_lhs = lu[(i+j*MATRIX_SIZE)*DATA_WIDTH+:DATA_WIDTH];")
        verilog_write(out_file, rf"div_rhs = lu[(i+i*MATRIX_SIZE)*DATA_WIDTH+:DATA_WIDTH];")
        verilog_write(out_file, rf"end")
        verilog_write(out_file, rf"else")
        verilog_write(out_file, rf"begin")
        verilog_write(out_file, rf"state = STATE_FINISH;")
        verilog_write(out_file, rf"complete = 1;")
        verilog_write(out_file, rf"end")
        verilog_write(out_file, rf"end")

        verilog_write(out_file, rf"else if (state == STATE_DIV_LOOP)")
        verilog_write(out_file, rf"begin")

        verilog_write(out_file, rf"if (div_complete)")
        verilog_write(out_file, rf"begin")
        verilog_write(out_file, rf"lu[(i+j*MATRIX_SIZE)*DATA_WIDTH+:DATA_WIDTH] = div_out;")
        verilog_write(out_file, rf"state = STATE_MUL_LOOP;")
        verilog_write(out_file, rf"div_rst = 1;")
        verilog_write(out_file, rf"k = i + 1;")
        verilog_write(out_file, rf"mul_lhs = lu[(i+j*MATRIX_SIZE)*DATA_WIDTH+:DATA_WIDTH];")
        verilog_write(out_file, rf"mul_rhs = lu[(k+i*MATRIX_SIZE)*DATA_WIDTH+:DATA_WIDTH];")
        verilog_write(out_file, rf"last_mul = 1;")

        verilog_write(out_file, rf"end")
        verilog_write(out_file, rf"end")

        verilog_write(out_file, rf"else if (state == STATE_MUL_LOOP)")
        verilog_write(out_file, rf"begin")

        verilog_write(out_file, rf"last_mul = 1;")
        verilog_write(out_file, rf"lu[(k+j*MATRIX_SIZE)*DATA_WIDTH+:DATA_WIDTH] = lu[(k+j*MATRIX_SIZE)*DATA_WIDTH+:DATA_WIDTH] - mul_out;")
        verilog_write(out_file, rf"k = k + 1;")
        verilog_write(out_file, rf"if (k < MATRIX_SIZE)")
        verilog_write(out_file, rf"begin")

        verilog_write(out_file, rf"mul_lhs = lu[(i+j*MATRIX_SIZE)*DATA_WIDTH+:DATA_WIDTH];")
        verilog_write(out_file, rf"mul_rhs = lu[(k+i*MATRIX_SIZE)*DATA_WIDTH+:DATA_WIDTH];")
        verilog_write(out_file, rf"end")

        verilog_write(out_file, rf"else")
        verilog_write(out_file, rf"begin")

        verilog_write(out_file, rf"j = j + 1;")
        verilog_write(out_file, rf"if (j < MATRIX_SIZE)")
        verilog_write(out_file, rf"begin")

        verilog_write(out_file, rf"state = STATE_DIV_LOOP;")

        verilog_write(out_file, rf"div_rst = 0;")
        verilog_write(out_file, rf"k = i + 1;")

        verilog_write(out_file, rf"div_lhs = lu[(i+j*MATRIX_SIZE)*DATA_WIDTH+:DATA_WIDTH];")
        verilog_write(out_file, rf"div_rhs = lu[(i+i*MATRIX_SIZE)*DATA_WIDTH+:DATA_WIDTH];")

        verilog_write(out_file, rf"end")
        verilog_write(out_file, rf"else")
        verilog_write(out_file, rf"begin")

        verilog_write(out_file, rf"i = i + 1;")
        verilog_write(out_file, rf"if (i < MATRIX_SIZE)")
        verilog_write(out_file, rf"begin")
        verilog_write(out_file, rf"j = 0;")
        verilog_write(out_file, rf"k = 0;")
        verilog_write(out_file, rf"state = STATE_LOOP_INIT;")
        verilog_write(out_file, rf"end")
        verilog_write(out_file, rf"else")
        verilog_write(out_file, rf"begin")
        verilog_write(out_file, rf"state = STATE_FINISH;")
        verilog_write(out_file, rf"complete = 1;")
        verilog_write(out_file, rf"end")
        verilog_write(out_file, rf"end")
        verilog_write(out_file, rf"end")
        verilog_write(out_file, rf"end")
        verilog_write(out_file, rf"end")
        verilog_write(out_file, rf"end")
        verilog_write(out_file, rf"endmodule")

def generate_matrix_inverse(dir, n, data_width, bin_pos):
    n_minus_one = n-1

    n2 = n ** 2

    whole_bits = data_width - bin_pos

    with open(dir + rf"/matinv{n}.v", 'w') as out_file:
        verilog_write(out_file, rf"module matinv{n} #(parameter DATA_WIDTH={data_width}, parameter BIN_POS={bin_pos}, parameter MATRIX_SIZE={n}) (input wire clk, input wire rst, output reg ready = 1, output reg complete = 0, input wire [(MATRIX_SIZE * MATRIX_SIZE * DATA_WIDTH) - 1:0] a, output wire [(MATRIX_SIZE * MATRIX_SIZE * DATA_WIDTH) - 1:0] inv, output wire w_singular);")

        verilog_write(out_file, rf"wire [DATA_WIDTH-1:0] wdet;")
        verilog_write(out_file, rf"wire [DATA_WIDTH-1:0] wdetdiv;")

        verilog_write(out_file, rf"reg div_rst = 1;")
        verilog_write(out_file, rf"wire div_ready;")
        verilog_write(out_file, rf"wire div_complete;")
        verilog_write(out_file, rf"wire div_zero;")

        verilog_write(out_file, rf"wire mdet_complete;")
        verilog_write(out_file, rf"wire mdet_ready;")

        verilog_write(out_file, rf"wire [(MATRIX_SIZE*MATRIX_SIZE*DATA_WIDTH)-1:0] m_trans;")

        verilog_write(out_file, rf"matdet{n} #(.DATA_WIDTH(DATA_WIDTH), .BIN_POS(BIN_POS), .MATRIX_SIZE(MATRIX_SIZE)) mdet(clk, rst, mdet_ready, mdet_complete, a, wdet);")

        verilog_write(out_file, r"div #(.DATA_WIDTH(DATA_WIDTH), .BIN_POS(BIN_POS)) d1 (clk, rst | div_rst, div_ready, div_complete, {" + rf"{whole_bits}'b1, {bin_pos}'b0" + "}, wdet, wdetdiv, div_zero);")

        verilog_write(out_file, rf"scalvec{n2} #(.DATA_WIDTH(DATA_WIDTH), .BIN_POS(BIN_POS), .VECTOR_SIZE(MATRIX_SIZE * MATRIX_SIZE)) svm1(clk, wdetdiv, m_trans, inv);")

        verilog_write(out_file, rf"assign w_singular = (wdet == 0 || div_zero) && mdet_complete;")

        verilog_write(out_file, rf"reg [DATA_WIDTH-1:0] count = 0;")

        verilog_write(out_file, rf"reg subrst = 0;")

        if n == 2:
            verilog_write(out_file, rf"wire [DATA_WIDTH-1:0] w1;")
            verilog_write(out_file, rf"wire [DATA_WIDTH-1:0] w2;")

            verilog_write(out_file, rf"assign w1 = 64'b0 - a[1*DATA_WIDTH+:DATA_WIDTH];")
            verilog_write(out_file, rf"assign w2 = 64'b0 - a[2*DATA_WIDTH+:DATA_WIDTH];")

            verilog_write(out_file, rf"assign m_trans = " + "{a[0*DATA_WIDTH+:DATA_WIDTH], w2, w1, a[3*DATA_WIDTH+:DATA_WIDTH]};")

        else:
            verilog_write(out_file, rf"wire [DATA_WIDTH-1:0] w_sub_det;")

            verilog_write(out_file, rf"reg [(MATRIX_SIZE-1) * (MATRIX_SIZE-1) * DATA_WIDTH - 1:0] r_submatrix = 0;")

            verilog_write(out_file, rf"wire subready;")
            verilog_write(out_file, rf"wire subcomplete;")

            verilog_write(out_file, rf"matdet{n_minus_one} #(.DATA_WIDTH(DATA_WIDTH), .BIN_POS(BIN_POS), .MATRIX_SIZE(MATRIX_SIZE-1)) mdetn(clk, rst | subrst, subready, subcomplete, r_submatrix, w_sub_det);")

            for i in range(n): # row
                for j in range(n): # col
                    verilog_write(out_file, rf"reg [DATA_WIDTH-1:0] r_adj_{i}_{j} = 0;")

            trans_list = []

            for i in range(n-1,-1,-1): # row
                for j in range(n-1,-1,-1): # col
                    trans_list += [rf"r_adj_{j}_{i}"]

            trans = "{" + ",".join(trans_list) + "}"

            verilog_write(out_file, rf"assign m_trans={trans};")

        verilog_write(out_file, rf"always @(posedge clk)")
        verilog_write(out_file, rf"begin")

        verilog_write(out_file, rf"if (rst)")
        verilog_write(out_file, rf"begin")
        verilog_write(out_file, rf"count = 0;")
        verilog_write(out_file, rf"ready = 1;")
        verilog_write(out_file, rf"div_rst = 1;")
        verilog_write(out_file, rf"complete = 0;")

        if n > 2:
            for i in range(n): # row
                for j in range(n): # col
                    verilog_write(out_file, rf"r_adj_{i}_{j} = 0;")

            verilog_write(out_file, rf"r_submatrix = 0;")

        cond = "" if n == 2 else " && subready"

        verilog_write(out_file, rf"subrst = 0;")
        verilog_write(out_file, rf"end")
        verilog_write(out_file, rf"else if (subrst{cond})")
        verilog_write(out_file, rf"begin")
        verilog_write(out_file, rf"subrst = 0;")
        verilog_write(out_file, rf"end")
        verilog_write(out_file, rf"else if (!subrst)")
        verilog_write(out_file, rf"begin")
        verilog_write(out_file, rf"ready = 0;")

        count = 0

        if n > 2:
            for i in range(n): # row
                for j in range(n): # col
                    indicies = []

                    pos = 0

                    for y in range(n):
                        for x in range(n):
                            if x != j and y != i:
                                indicies += [rf"a[{pos}*DATA_WIDTH+:DATA_WIDTH]"]

                            pos += 1

                    indicies.reverse()

                    sub_matrix = "{" + ",".join(indicies) + "}"

                    verilog_write(out_file, ("else " if count != 0 else "") +  rf"if (count == {count})")
                    verilog_write(out_file, rf"begin")

                    verilog_write(out_file, rf"if (subcomplete)")
                    verilog_write(out_file, rf"begin")

                    if (-1)**j * (-1)**i == 1: # positive
                        verilog_write(out_file, rf"r_adj_{i}_{j} = w_sub_det;")
                    else:
                        verilog_write(out_file, rf"r_adj_{i}_{j} = {data_width}'b0 - w_sub_det;")

                    verilog_write(out_file, rf"subrst = 1;")
                    verilog_write(out_file, rf"count = count + 1;")

                    verilog_write(out_file, rf"end")

                    verilog_write(out_file, rf"r_submatrix = {sub_matrix};")

                    verilog_write(out_file, rf"end")

                    count += 1

            verilog_write(out_file, rf"else if (count == {count} && subcomplete && mdet_complete)")
            verilog_write(out_file, rf"begin")
            verilog_write(out_file, rf"count = count + 1;")
            verilog_write(out_file, rf"end");

            count += 1

            verilog_write(out_file, rf"else if (count == {count} && div_complete)")
            verilog_write(out_file, rf"begin")
            verilog_write(out_file, rf"complete = 1;")
            verilog_write(out_file, rf"end");
        else:
            verilog_write(out_file, rf"if (count == {count} && mdet_complete && div_complete)")
            verilog_write(out_file, rf"begin")
            verilog_write(out_file, rf"complete = 1;")
            verilog_write(out_file, rf"end")

        verilog_write(out_file, rf"if (mdet_complete)")
        verilog_write(out_file, rf"begin")
        verilog_write(out_file, rf"div_rst = 0;")
        verilog_write(out_file, rf"end")

        verilog_write(out_file, rf"if (mdet_complete && w_singular)")
        verilog_write(out_file, rf"begin")
        verilog_write(out_file, rf"complete = 1;")
        verilog_write(out_file, rf"end")


        verilog_write(out_file, rf"end");
        verilog_write(out_file, rf"end");
        verilog_write(out_file, r"endmodule")


def main(dir, depth, data_width, bin_pos):

    shutil.rmtree("src", ignore_errors=True)

    os.makedirs(dir, exist_ok=True)

    shutil.copyfile("mul.v", dir + "/mul.v")
    shutil.copyfile("div.v", dir + "/div.v")

    generate_scalar_vector(dir, depth ** 2, data_width, bin_pos)
    generate_vector_vector(dir, depth, data_width, bin_pos)    
    generate_matrix_matrix(dir, depth, data_width, bin_pos)
    generate_matrix_transpose(dir, depth, data_width, bin_pos)
    generate_matrix_lu(dir, depth, data_width, bin_pos)
    generate_matrix_determinant(dir, depth, data_width, bin_pos)
    generate_matrix_lu(dir, depth-1, data_width, bin_pos)
    generate_matrix_determinant(dir, depth-1, data_width, bin_pos)
    generate_matrix_inverse(dir, depth, data_width, bin_pos)

if __name__ == "__main__":
    main("src", int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
