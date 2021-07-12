#!/usr/bin/env python3

import os
import shutil

DATA_WIDTH = 8

def generate_mat_det(dir, n):
    if n <= 2:
        if n == 2:
            shutil.copyfile("matdet2.v", dir + "/matdet2.v")
        return
    
    generate_mat_det(dir, n-1)
    
    n2 = n ** 2
    n_minus_1 = n - 1
    
    with open(dir + rf"/matdet{n}.v", 'w') as out_file:
        out_file.write(rf"module matdet{n} #(paramater DATA_WIDTH={DATA_WIDTH}) (input wire [DATA_WIDTH:0] a [{n2}:0], output wire [DATA_WIDTH:0] det)" + "\n")
        
        out_file.write(r"wire [DATA_WIDTH:0] " + ", ".join([rf"w{x}" for x in range(n * 3 - 1)]) + ";" + "\n")
            
        for i in range(n): #Column i
            elements = "{"
            
            non_column_nums = [x for x in range(n) if x != i]
            
            for j in range(len(non_column_nums)): #row
                for k in non_column_nums: #column
                    index = (j + 1) * n + k
                    elements += rf"a[{index}], "
                    
            elements = elements[:-2] + "}"
            out_file.write(rf"matdet{n_minus_1}({elements}, w{i});" + "\n")

        for i in range(n):
            i_plus_n = i + n
            out_file.write(rf"mul(a[{i}], w{i}, w{i_plus_n});" + "\n")

        for i in range(n-1):
            i_plus_n = i + n
            i_plus_n_plus_one = i + n + 1
            i_plus_two_n = i + 2 * n
            i_plus_two_bracket_n_minus_1_bracket_plus_1 = i + 2 * (n - 1) + 1
            
            op_str = "sub" if i % 2 == 0 else "add"
            
            if i == 0:
                out_file.write(rf"{op_str}(w{i_plus_n}, w{i_plus_n_plus_one}, w{i_plus_two_n});" + "\n")
            elif i == n - 2:
                out_file.write(rf"{op_str}(w{i_plus_two_bracket_n_minus_1_bracket_plus_1}, w{i_plus_n_plus_one}, det);" + "\n")
            else:
                out_file.write(rf"{op_str}(w{i_plus_two_bracket_n_minus_1_bracket_plus_1}, w{i_plus_n_plus_one}, w{i_plus_two_n});" + "\n")
                

        out_file.write(r"endmodule" + "\n")

def main(dir, depth):
    os.makedirs(dir, exist_ok=True)
    
    generate_mat_det(dir, depth)
    
if __name__ == "__main__":
    main("src", 4)
