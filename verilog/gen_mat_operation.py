#!/usr/bin/env python3

import os
import sys
import shutil

mul_count = 0
add_sub_count = 0

def generate_scalar_vector_matrix(dir, n, data_width):
    with open(dir + rf"/scalvecmat{n}.v", 'w') as out_file:
        out_file.write(rf"module scalvecmat{n} #(parameter DATA_WIDTH={data_width}, parameter VECTOR_SIZE={n}) (input wire [DATA_WIDTH - 1:0] a, input wire [(VECTOR_SIZE * DATA_WIDTH) - 1:0] b, output wire [(VECTOR_SIZE * DATA_WIDTH) - 1:0] scale);" + '\n')
        
        empty_bits = (n-1) * data_width
        
        out_file.write(rf"mul #(.DATA_WIDTH(DATA_WIDTH*VECTOR_SIZE)) m1(" + "{" + rf"{empty_bits}'b0, a" +"}" + rf", b, scale);" + '\n')
        out_file.write(rf"endmodule" + '\n')

def generate_vector_vector(dir, n, data_width):
    with open(dir + rf"/vecvec{n}.v", 'w') as out_file:
        out_file.write(rf"module vecvec{n} #(parameter DATA_WIDTH={data_width}, parameter VECTOR_SIZE={n}) (input wire [(VECTOR_SIZE * DATA_WIDTH) - 1:0] a, input wire [(VECTOR_SIZE * DATA_WIDTH) - 1:0] b, output wire [DATA_WIDTH - 1:0] dot);" + '\n')
        
        
        for i in range(n):
            out_file.write(rf"wire [DATA_WIDTH-1:0] w{i};" + '\n')
        
        for i in range(n-2):
            n_plus_i = n + i
            out_file.write(rf"wire [DATA_WIDTH-1:0] w{n_plus_i};" + '\n')
        
        for i in range(n):
            out_file.write(rf"mul #(.DATA_WIDTH(DATA_WIDTH)) m{i}(a[{i}*DATA_WIDTH+:DATA_WIDTH], b[{i}*DATA_WIDTH+:DATA_WIDTH], w{i});" + '\n')
        
        if n == 2:
            out_file.write(rf"add #(.DATA_WIDTH(DATA_WIDTH)) a{i}(w0, w1, dot);" + '\n')
        else:
            for i in range(n-1):
                n_plus_i = n + i
                i_plus_one = i + 1
                n_plus_i_minus_one = n + i - 1
                
                if i == 0:
                    out_file.write(rf"add #(.DATA_WIDTH(DATA_WIDTH)) a{i}(w{i}, w{i_plus_one}, w{n_plus_i});" + '\n')
                elif i == n-2:
                    out_file.write(rf"add #(.DATA_WIDTH(DATA_WIDTH)) a{i}(w{i_plus_one}, w{n_plus_i_minus_one}, dot);" + '\n')
                else:
                    out_file.write(rf"add #(.DATA_WIDTH(DATA_WIDTH)) a{i}(w{i_plus_one}, w{n_plus_i_minus_one}, w{n_plus_i});" + '\n')
                
        out_file.write(rf"endmodule" + '\n')

def generate_matrix_matrix(dir, n, data_width):
    n2 = n ** 2
    
    with open(dir + rf"/matmat{n}.v", 'w') as out_file:
        out_file.write(rf"module matmat{n} #(parameter DATA_WIDTH={data_width}, parameter MATRIX_SIZE={n2}) (input wire [(MATRIX_SIZE * DATA_WIDTH) - 1:0] a, input wire [(MATRIX_SIZE * DATA_WIDTH) - 1:0] b, output wire [(MATRIX_SIZE * DATA_WIDTH) - 1:0] mul);" + '\n')
        
        for i in range(n): #col
            for j in range(n): #row
                out_file.write(rf"wire [DATA_WIDTH-1:0] w{j}{i};" + '\n')
        
        mul_map_list = []
        
        for i in range(n): #col
            for j in range(n): #row
                row_map = "{" + ",".join(["a[" + str(j * n + x) + "*DATA_WIDTH+:DATA_WIDTH]" for x in range(n)]) + "}"
                col_map = "{" + ",".join(["b[" + str(i + n * x) + "*DATA_WIDTH+:DATA_WIDTH]" for x in range(n)]) + "}"
                
                mul_map_list += [rf"w{i}{j}"]
                
                out_file.write(rf"vecvec{n} #(.DATA_WIDTH({data_width}), .VECTOR_SIZE({n})) v{j}{i}({row_map}, {col_map}, w{j}{i});" + '\n')
        
        mul_map_list.reverse()
        
        mul_map = "{" + ",".join(mul_map_list) + "}"
                
        out_file.write(rf"assign mul = {mul_map};" + '\n')
                
        out_file.write(rf"endmodule" + '\n')


def generate_matrix_transpose(dir, n, data_width):
    n2 = n ** 2
    
    with open(dir + rf"/mattrans{n}.v", 'w') as out_file:
        out_file.write(rf"module mattrans{n} #(parameter DATA_WIDTH={data_width}, parameter MATRIX_SIZE={n2}) (input wire [(MATRIX_SIZE * DATA_WIDTH) - 1:0] in, output wire [(MATRIX_SIZE * DATA_WIDTH) - 1:0] out);" + '\n')
        
        for i in range(n): #col
            for j in range(n): #row
                in_pos = j * n + i
                out_pos = i * n + j
                out_file.write(rf"assign out[{out_pos}*DATA_WIDTH+:DATA_WIDTH] = in[{in_pos}*DATA_WIDTH+:DATA_WIDTH];" + '\n')
                
        out_file.write(rf"endmodule" + '\n')

def generate_matrix_determinant(dir, n, data_width):
    global mul_count
    global add_sub_count
    
    if n <= 2:
        return
    
    generate_matrix_determinant(dir, n-1, data_width)
    
    n2 = n ** 2
    n_minus_1 = n - 1
    
    with open(dir + rf"/matdet{n}.v", 'w') as out_file:
        out_file.write(rf"module matdet{n} #(parameter DATA_WIDTH={data_width}, parameter MATRIX_SIZE={n2}) (input wire [(MATRIX_SIZE * DATA_WIDTH) - 1:0] a, output wire [DATA_WIDTH-1:0] det);" + '\n')
        
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
            out_file.write(rf"matdet{n_minus_1} #(.DATA_WIDTH(DATA_WIDTH)) md{i}({elements}, w{i});" + '\n')

        for i in range(n):
            i_plus_n = i + n
            
            min_bit = data_width * i
            
            out_file.write(rf"mul #(.DATA_WIDTH(DATA_WIDTH)) m{i}(a[{min_bit}+:{data_width}], w{i}, w{i_plus_n});" + '\n')
            mul_count += n ** 2

        for i in range(n-1):
            i_plus_n = i + n
            i_plus_n_plus_one = i + n + 1
            i_plus_two_n = i + 2 * n
            i_plus_two_bracket_n_minus_1_bracket_plus_1 = i + 2 * (n - 1) + 1
            
            op_str = "sub" if i % 2 == 0 else "add"
            
            add_sub_count += n ** 2
            
            if i == 0:
                out_file.write(rf"{op_str} #(.DATA_WIDTH(DATA_WIDTH)) op{i}(w{i_plus_n}, w{i_plus_n_plus_one}, w{i_plus_two_n});" + '\n')
            elif i == n - 2:
                out_file.write(rf"{op_str} #(.DATA_WIDTH(DATA_WIDTH)) op{i}(w{i_plus_two_bracket_n_minus_1_bracket_plus_1}, w{i_plus_n_plus_one}, det);" + '\n')
            else:
                out_file.write(rf"{op_str} #(.DATA_WIDTH(DATA_WIDTH)) op{i}(w{i_plus_two_bracket_n_minus_1_bracket_plus_1}, w{i_plus_n_plus_one}, w{i_plus_two_n});" + '\n')
                

        out_file.write(r"endmodule" + '\n')

def generate_matrix_inverse(dir, n, data_width):
    with open(dir + rf"/matinv{n}.v", 'w') as out_file:
        out_file.write('\n')
    

def main(dir, depth, data_width):
    global mul_count
    global add_sub_count
    
    os.makedirs(dir, exist_ok=True)
    
    shutil.copyfile("matdet2.v", dir + "/matdet2.v")
    shutil.copyfile("add.v", dir + "/add.v")
    shutil.copyfile("sub.v", dir + "/sub.v")
    shutil.copyfile("mul.v", dir + "/mul.v")
    shutil.copyfile("div.v", dir + "/div.v")
    
    generate_scalar_vector_matrix(dir, depth, data_width)
    generate_vector_vector(dir, depth, data_width)    
    generate_matrix_matrix(dir, depth, data_width)
    generate_matrix_transpose(dir, depth, data_width)
    generate_matrix_determinant(dir, depth, data_width)
    generate_matrix_inverse(dir, depth, data_width)
    
    #print("Multiplier count:", mul_count)
    #print("Adder / subtractor count:", add_sub_count)
    
if __name__ == "__main__":
    main("src", int(sys.argv[1]), int(sys.argv[2]))
