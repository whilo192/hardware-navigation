#!/usr/bin/env python3

import os
import sys
import shutil

def generate_scalar_vector(dir, n, data_width, bin_pos):
    n2 = n ** 2
    
    with open(dir + rf"/scalvec{n}.v", 'w') as out_file:
        out_file.write(rf"module scalvec{n} #(parameter DATA_WIDTH={data_width}, parameter BIN_POS={bin_pos}, parameter VECTOR_SIZE={n}) (input wire [DATA_WIDTH - 1:0] a, input wire [(VECTOR_SIZE * DATA_WIDTH) - 1:0] b, output wire [(VECTOR_SIZE * DATA_WIDTH) - 1:0] scale);" + '\n')
        
        empty_bits = (n**2-1) * data_width
        
        for i in range(n2):
            out_file.write(rf"wire [DATA_WIDTH-1:0] w{i};" + '\n')
            
        for i in range(n2):
            i_str = rf"{i}*DATA_WIDTH+:DATA_WIDTH"
            out_file.write(rf"mul #(.DATA_WIDTH(DATA_WIDTH), .BIN_POS(BIN_POS)) m{i}(a, b[{i_str}], w{i});" + "\n")
        
        out_file.write(rf"assign scale = " + "{" + ",".join([rf"w{i}" for i in range(n2-1,-1,-1)]) + "};" + '\n')
        
        out_file.write(rf"endmodule" + '\n')

def generate_vector_vector(dir, n, data_width, bin_pos):
    with open(dir + rf"/vecvec{n}.v", 'w') as out_file:
        out_file.write(rf"module vecvec{n} #(parameter DATA_WIDTH={data_width}, parameter BIN_POS={bin_pos}, parameter VECTOR_SIZE={n}) (input wire clk, input wire rst, output reg complete = 0, input wire [(VECTOR_SIZE * DATA_WIDTH) - 1:0] a, input wire [(VECTOR_SIZE * DATA_WIDTH) - 1:0] b, output reg [DATA_WIDTH - 1:0] dot = 0);" + '\n')
        
        out_file.write(rf"reg [DATA_WIDTH-1:0] count = 0;"+ '\n')
        
        out_file.write(rf"reg [DATA_WIDTH-1:0] r_mul_lhs = 0;" + '\n')
        out_file.write(rf"reg [DATA_WIDTH-1:0] r_mul_rhs = 0;" + '\n')
        
        out_file.write(rf"wire [DATA_WIDTH-1:0] w_mul_out;" + '\n')
        out_file.write(rf"wire [DATA_WIDTH-1:0] w_add_out;" + '\n')
        
        out_file.write(rf"mul #(.DATA_WIDTH(DATA_WIDTH), .BIN_POS(BIN_POS)) m1(r_mul_lhs, r_mul_rhs, w_mul_out);" + '\n')
        
        out_file.write(rf"always @(posedge clk or posedge rst)" + '\n')
        out_file.write(rf"begin" + '\n')
        
        out_file.write(rf"if (rst)" + '\n')
        out_file.write(rf"begin" + '\n')
        out_file.write(rf"count = 0;" + '\n')
        out_file.write(rf"dot = 0;" + '\n')
        out_file.write(rf"complete = 0;" + '\n')
        out_file.write(rf"r_mul_lhs = 0;" + '\n')
        out_file.write(rf"r_mul_rhs = 0;" + '\n')
        out_file.write(rf"end" + '\n')
        
        for i in range(n):
            out_file.write(("else " if i > 0 else "") + rf"if (count == {i})" + '\n')
            out_file.write(rf"begin" + '\n')
            out_file.write(rf"r_mul_lhs = a[{i}*DATA_WIDTH+:DATA_WIDTH];" + '\n')
            out_file.write(rf"r_mul_rhs = b[{i}*DATA_WIDTH+:DATA_WIDTH];" + '\n')
            
            out_file.write(rf"#1" + '\n')
            
            out_file.write(rf"dot += w_mul_out;" + '\n')
            
            if i == n-1:
                out_file.write(rf"complete = 1;" + '\n')
                
            out_file.write(rf"count += 1;" + '\n')
            
            out_file.write(rf"end" + '\n')
            
        out_file.write(rf"end" + '\n')
        
        out_file.write(rf"endmodule" + '\n')

def generate_matrix_matrix(dir, n, data_width, bin_pos):
    n2 = n ** 2
    
    with open(dir + rf"/matmat{n}.v", 'w') as out_file:
        out_file.write(rf"module matmat{n} #(parameter DATA_WIDTH={data_width}, parameter BIN_POS={bin_pos}, parameter MATRIX_SIZE={n}) (input wire clk, input wire rst, output reg complete = 0, input wire [(MATRIX_SIZE * MATRIX_SIZE * DATA_WIDTH) - 1:0] a, input wire [(MATRIX_SIZE * MATRIX_SIZE * DATA_WIDTH) - 1:0] b, output reg [(MATRIX_SIZE * MATRIX_SIZE * DATA_WIDTH) - 1:0] mul = 0);" + '\n')
        
        out_file.write(rf"reg [DATA_WIDTH-1:0] count = 0;"+ '\n')
        
        out_file.write(rf"wire subcomplete;"+ '\n')
        out_file.write(rf"reg subrst;"+ '\n')
        
        out_file.write(rf"reg [MATRIX_SIZE * DATA_WIDTH - 1:0] r_lhs = 0;" + '\n')
        out_file.write(rf"reg [MATRIX_SIZE * DATA_WIDTH - 1:0] r_rhs = 0;" + '\n')
        
        out_file.write(rf"wire [DATA_WIDTH-1:0] w_out;" + '\n')
        
        out_file.write(rf"vecvec{n} #(.DATA_WIDTH(DATA_WIDTH), .VECTOR_SIZE(MATRIX_SIZE), .BIN_POS(BIN_POS)) v1(clk, subrst | rst, subcomplete, r_lhs, r_rhs, w_out);" + '\n')
        
        count = 0
        
        out_file.write(rf"always @(posedge clk or posedge rst)" + '\n')
        out_file.write(rf"begin" + '\n')
        
        out_file.write(rf"if (rst)" + '\n')
        out_file.write(rf"begin" + '\n')
        out_file.write(rf"count = 0;" + '\n')
        out_file.write(rf"complete = 0;" + '\n')
        out_file.write(rf"subrst = 0;" + '\n')
        out_file.write(rf"r_lhs = 0;" + '\n')
        out_file.write(rf"r_rhs = 0;" + '\n')
        out_file.write(rf"end" + '\n')
        
        out_file.write(rf"if (subrst)" + '\n')
        out_file.write(rf"begin" + '\n')
        out_file.write(rf"subrst = 0;" + '\n')
        out_file.write(rf"end" + '\n')
        
        for i in range(n): #col
            for j in range(n): #row
                row_map = "{" + ",".join(["a[" + str(j * n + x) + "*DATA_WIDTH+:DATA_WIDTH]" for x in range(n)]) + "}"
                col_map = "{" + ",".join(["b[" + str(i + n * x) + "*DATA_WIDTH+:DATA_WIDTH]" for x in range(n)]) + "}"
                
                mat_count = j * n + i
                
                out_file.write(("else " if count != 0 else "") +  rf"if (count == {count})" + '\n')
                out_file.write(rf"begin" + '\n')
                               
                out_file.write(rf"if (subcomplete)" + '\n')
                out_file.write(rf"begin" + '\n')
                out_file.write(rf"mul[{mat_count}*DATA_WIDTH+:DATA_WIDTH] = w_out;" + '\n')
                out_file.write(rf"subrst = 1;" + '\n')
                out_file.write(rf"count += 1;" + '\n')
                
                out_file.write(rf"end" + '\n')
                
                out_file.write(rf"r_lhs = {row_map};" + '\n')
                out_file.write(rf"r_rhs = {col_map};" + '\n')
                
                out_file.write(rf"end" + '\n')
                
                count += 1
        
        out_file.write(rf"else if (count == {count} && subcomplete)" + '\n')
        out_file.write(rf"begin" + '\n')
        out_file.write(rf"complete = 1;" + '\n')
        out_file.write(rf"end" + '\n')
        
        out_file.write(rf"end" + '\n')
                
        out_file.write(rf"endmodule" + '\n')


def generate_matrix_transpose(dir, n, data_width, bin_pos):
    n2 = n ** 2
    
    with open(dir + rf"/mattrans{n}.v", 'w') as out_file:
        out_file.write(rf"module mattrans{n} #(parameter DATA_WIDTH={data_width}, parameter BIN_POS={bin_pos}, parameter MATRIX_SIZE={n}) (input wire [(MATRIX_SIZE * MATRIX_SIZE * DATA_WIDTH) - 1:0] in, output wire [(MATRIX_SIZE * MATRIX_SIZE * DATA_WIDTH) - 1:0] out);" + '\n')
        
        for i in range(n): #col
            for j in range(n): #row
                in_pos = j * n + i
                out_pos = i * n + j
                out_file.write(rf"assign out[{out_pos}*DATA_WIDTH+:DATA_WIDTH] = in[{in_pos}*DATA_WIDTH+:DATA_WIDTH];" + '\n')
                
        out_file.write(rf"endmodule" + '\n')

def generate_matrix_determinant(dir, n, data_width, bin_pos):   
    if n <= 2:
        return
    
    generate_matrix_determinant(dir, n-1, data_width, bin_pos)
    
    n2 = n ** 2
    n_minus_1 = n - 1
    
    with open(dir + rf"/matdet{n}.v", 'w') as out_file:
        out_file.write(rf"module matdet{n} #(parameter DATA_WIDTH={data_width}, parameter BIN_POS={bin_pos}, parameter MATRIX_SIZE={n}) (input wire [(MATRIX_SIZE * MATRIX_SIZE * DATA_WIDTH) - 1:0] a, output wire [DATA_WIDTH-1:0] det);" + '\n')
               
        out_file.write(r"wire [DATA_WIDTH-1:0] " + ", ".join([rf"w{x}" for x in range(n * 3 - 1)]) + ";" + '\n')
            
        for i in range(n): #Column i
            elements = "{"
            
            non_column_nums = [x for x in range(n) if x != i]
            
            for j in range(len(non_column_nums)): #row
                for k in non_column_nums: #column
                    index = (j + 1) * n + k
                    
                    min_bit = data_width * index
                    elements += rf"a[{min_bit}+:{data_width}], "
                    
            elements = elements[:-2] + "}"
            out_file.write(rf"matdet{n_minus_1} #(.DATA_WIDTH(DATA_WIDTH), .BIN_POS(BIN_POS), .MATRIX_SIZE(MATRIX_SIZE-1)) md{i}({elements}, w{i});" + '\n')

        for i in range(n):
            i_plus_n = i + n
            
            min_bit = data_width * i
            
            out_file.write(rf"mul #(.DATA_WIDTH(DATA_WIDTH), .BIN_POS(BIN_POS)) m{i}(a[{min_bit}+:{data_width}], w{i}, w{i_plus_n});" + '\n')

        for i in range(n-1):
            i_plus_n = i + n
            i_plus_n_plus_one = i + n + 1
            i_plus_two_n = i + 2 * n
            i_plus_two_bracket_n_minus_1_bracket_plus_1 = i + 2 * (n - 1) + 1
            
            op_str = "-" if i % 2 == 0 else "+"
            
            
            if i == 0:
                out_file.write(rf"assign w{i_plus_two_n} = w{i_plus_n} {op_str} w{i_plus_n_plus_one};" + '\n')
            elif i == n - 2:
                out_file.write(rf"assign det = w{i_plus_two_bracket_n_minus_1_bracket_plus_1} {op_str} w{i_plus_n_plus_one};" + '\n')
            else:
                out_file.write(rf"assign w{i_plus_two_n} = w{i_plus_two_bracket_n_minus_1_bracket_plus_1} {op_str} w{i_plus_n_plus_one};" + '\n')
                

        out_file.write(r"endmodule" + '\n')

def generate_matrix_inverse(dir, n, data_width, bin_pos):
    n_minus_one = n-1
    
    n2 = n ** 2
    
    whole_bits = data_width - bin_pos
    
    with open(dir + rf"/matinv{n}.v", 'w') as out_file:
        out_file.write(rf"module matinv{n} #(parameter DATA_WIDTH={data_width}, parameter BIN_POS={bin_pos}, parameter MATRIX_SIZE={n}) (input wire [(MATRIX_SIZE * MATRIX_SIZE * DATA_WIDTH) - 1:0] a, output wire [(MATRIX_SIZE * MATRIX_SIZE * DATA_WIDTH) - 1:0] inv, output wire w_singular);" + '\n')
        
        out_file.write(rf"wire [DATA_WIDTH-1:0] wdet;" + '\n')
        out_file.write(rf"wire [DATA_WIDTH-1:0] wdetdiv;" + '\n')
        
        out_file.write(rf"assign w_singular = wdet == 0;" + '\n')
        
        out_file.write(rf"wire [(MATRIX_SIZE*MATRIX_SIZE*DATA_WIDTH)-1:0] m_trans;" + '\n')
        
        out_file.write(rf"matdet{n} #(.DATA_WIDTH(DATA_WIDTH), .BIN_POS(BIN_POS), .MATRIX_SIZE(MATRIX_SIZE)) mdet(a, wdet);" + '\n')
                
        out_file.write(r"div #(.DATA_WIDTH(DATA_WIDTH), .BIN_POS(BIN_POS)) d1 ({" + rf"{whole_bits}'b1, {bin_pos}'b0" + "}, wdet, wdetdiv);" + '\n')
        
        if n == 2:
            out_file.write(rf"wire [DATA_WIDTH-1:0] w1;" + '\n')
            out_file.write(rf"wire [DATA_WIDTH-1:0] w2;" + '\n')
            
            out_file.write(rf"assign w1 = {data_width}'b0 - a[1*DATA_WIDTH+:DATA_WIDTH];" + '\n')
            out_file.write(rf"assign w2 = {data_width}'b0 - a[2*DATA_WIDTH+:DATA_WIDTH];" + '\n')
            
            out_file.write(r"assign m_trans = {a[0*DATA_WIDTH+:DATA_WIDTH], w2, w1, a[3*DATA_WIDTH+:DATA_WIDTH]};" + '\n')
            
            out_file.write(rf"scalvec{n2} #(.DATA_WIDTH(DATA_WIDTH), .BIN_POS(BIN_POS), .VECTOR_SIZE({n2})) svm1(wdetdiv, m_trans, inv);" + '\n')
            
            out_file.write(r"endmodule" + '\n')
            return
        
        
        for i in range(n): # row
            for j in range(n): # col
                out_file.write(rf"wire [DATA_WIDTH-1:0] w_min_{i}_{j};" + '\n')
                out_file.write(rf"wire [DATA_WIDTH-1:0] w_adj_{i}_{j};" + '\n')
                
                
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
        
                out_file.write(rf"matdet{n_minus_one} #(.DATA_WIDTH(DATA_WIDTH), .BIN_POS(BIN_POS), .MATRIX_SIZE(MATRIX_SIZE-1)) m{i}_{j}({sub_matrix}, w_min_{i}_{j});" + '\n')
                
        pos = 0
        trans_list = []
        
        for i in range(n): # row
            for j in range(n): # col
                if (-1)**j * (-1)**i == 1: # positive
                    out_file.write(rf"assign w_adj_{i}_{j} = w_min_{i}_{j};" + '\n')
                else:
                    out_file.write(rf"assign w_adj_{i}_{j} = {data_width}'b0 - w_min_{i}_{j};" + '\n')
                
                pos += 1
                
        for i in range(n-1,-1,-1): # row
            for j in range(n-1,-1,-1): # col
                trans_list += [rf"w_adj_{j}_{i}"]
                
        trans = "{" + ",".join(trans_list) + "}"
            
        out_file.write(rf"assign m_trans={trans};" + '\n')
            
        out_file.write(rf"scalvec{n2} #(.DATA_WIDTH(DATA_WIDTH), .BIN_POS(BIN_POS), .VECTOR_SIZE({n2})) svm1(wdetdiv, m_trans, inv);" + '\n')
            
        out_file.write(r"endmodule" + '\n')
    

def main(dir, depth, data_width, bin_pos):
    
    shutil.rmtree("src", ignore_errors=True)
    
    os.makedirs(dir, exist_ok=True)
    
    shutil.copyfile("matdet2.v", dir + "/matdet2.v")
    shutil.copyfile("mul.v", dir + "/mul.v")
    shutil.copyfile("div.v", dir + "/div.v")
    
    generate_scalar_vector(dir, depth ** 2, data_width, bin_pos)
    generate_vector_vector(dir, depth, data_width, bin_pos)    
    generate_matrix_matrix(dir, depth, data_width, bin_pos)
    generate_matrix_transpose(dir, depth, data_width, bin_pos)
    generate_matrix_determinant(dir, depth, data_width, bin_pos)
    generate_matrix_inverse(dir, depth, data_width, bin_pos)
    
if __name__ == "__main__":
    main("src", int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
