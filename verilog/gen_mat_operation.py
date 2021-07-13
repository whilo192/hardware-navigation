#!/usr/bin/env python3

import os
import shutil

DATA_WIDTH = 8

mul_count = 0
add_sub_count = 0

def generate_mat_det(dir, n):
    global mul_count
    global add_sub_count
    
    if n <= 2:
        if n == 2:
            shutil.copyfile("matdet2.v", dir + "/matdet2.v")
            shutil.copyfile("add.v", dir + "/add.v")
            shutil.copyfile("sub.v", dir + "/sub.v")
            shutil.copyfile("mul.v", dir + "/mul.v")
        return
    
    generate_mat_det(dir, n-1)
    
    n2 = n ** 2
    n_minus_1 = n - 1
    
    with open(dir + rf"/matdet{n}.v", 'w') as out_file:
        out_file.write(rf"module matdet{n} #(parameter DATA_WIDTH={DATA_WIDTH}, parameter MATRIX_SIZE={n2}) (input wire [(MATRIX_SIZE * DATA_WIDTH) - 1:0] a, output wire [DATA_WIDTH-1:0] det);" + "\n")
        
        out_file.write(r"wire [DATA_WIDTH-1:0] " + ", ".join([rf"w{x}" for x in range(n * 3 - 1)]) + ";" + "\n")
            
        for i in range(n): #Column i
            elements = "{"
            
            non_column_nums = [x for x in range(n) if x != i]
            
            for j in range(len(non_column_nums)): #row
                for k in non_column_nums: #column
                    index = (j + 1) * n + k
                    
                    min_bit = DATA_WIDTH * index
                    max_bit = min_bit + (DATA_WIDTH - 1)
                    elements += rf"a[{max_bit}:{min_bit}], "
                    
            elements = elements[:-2] + "}"
            out_file.write(rf"matdet{n_minus_1} md{i}({elements}, w{i});" + "\n")

        for i in range(n):
            i_plus_n = i + n
            
            min_bit = DATA_WIDTH * i
            max_bit = min_bit + (DATA_WIDTH - 1)
            
            out_file.write(rf"mul m{i}(a[{max_bit}:{min_bit}], w{i}, w{i_plus_n});" + "\n")
            mul_count += n ** 2

        for i in range(n-1):
            i_plus_n = i + n
            i_plus_n_plus_one = i + n + 1
            i_plus_two_n = i + 2 * n
            i_plus_two_bracket_n_minus_1_bracket_plus_1 = i + 2 * (n - 1) + 1
            
            op_str = "sub" if i % 2 == 0 else "add"
            
            add_sub_count += n ** 2
            
            if i == 0:
                out_file.write(rf"{op_str} op{i}(w{i_plus_n}, w{i_plus_n_plus_one}, w{i_plus_two_n});" + "\n")
            elif i == n - 2:
                out_file.write(rf"{op_str} op{i}(w{i_plus_two_bracket_n_minus_1_bracket_plus_1}, w{i_plus_n_plus_one}, det);" + "\n")
            else:
                out_file.write(rf"{op_str} op{i}(w{i_plus_two_bracket_n_minus_1_bracket_plus_1}, w{i_plus_n_plus_one}, w{i_plus_two_n});" + "\n")
                

        out_file.write(r"endmodule" + "\n")

def main(dir, depth):
    global mul_count
    global add_sub_count
    
    os.makedirs(dir, exist_ok=True)
    
    generate_mat_det(dir, depth)
    
    print("Multiplier count:", mul_count)
    print("Adder / subtractor count:", add_sub_count)
    
if __name__ == "__main__":
    main("src", 12)
