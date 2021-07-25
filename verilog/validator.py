#!/usr/bin/env python3
 
import os
import sys
import subprocess
import numpy as np


def my_subprocess_run(command, print_stdout=True):
    result = subprocess.run(command, stdout=subprocess.PIPE)
    
    stdout = result.stdout.decode("utf-8")
    
    if print_stdout:
        print(stdout)
    
    if result.returncode != 0:
        print("Process " + ' '.join(command) + " exited with exit code " + str(result.returncode))
        sys.exit(result.returncode)
        
    return stdout

def main(wk_dir, n, width):
    step = width // 4
    s_max = 2 ** (width - 1) - 1
    u_max = 2 ** width
    
    def hex_to_dec(hex_in):
        int_in = int(hex_in, 16)
        
        if int_in > s_max:
            int_in = -(u_max - int_in)
            
        return int_in
    
    result = my_subprocess_run(["./gen_mat_operation.py", str(n), str(width)])

    with open("test.v", 'r') as test_file:
        with open(wk_dir + "/test.v", 'w') as copy_file:
            buf = test_file.read()
            copy_file.write(buf.format(n=n, width=width))

    os.chdir(wk_dir)
    
    
    my_subprocess_run(["iverilog", "-o", "test", "test.v"] +  ["matdet" + str(i+2) +".v" for i in range(n-1)] + ["mul.v", "add.v", "sub.v"])
    result = my_subprocess_run(["vvp", "test"], False)
    
    lines = result.split('\n')
    
    
    ok_count = 0
    runs = len(lines)//2
    
    for i in range(runs):
        mat = lines[2*i][5:]
        det = hex_to_dec(lines[2*i+1][5:])
        
        matrix = np.empty((n,n))
        
        for row in range(n):
            for col in range(n):
                #print(row, col)
                pos = (n - col - 1) * n + (n - row - 1)
                bit_slice = mat[pos * step:pos*step+step]
                
                #print(mat, bit_slice)
                val = hex_to_dec(bit_slice)
                
                matrix[col,row] = val
        
        np_det_float = np.linalg.det(matrix)
        np_det = int(round(np_det_float, 0))
        
        if np_det != det:
            print(f"Not working? numpy: {np_det}, Icarus: {det}")
            print("    Icarus matrix: " + mat)
            print("    Parsed matrix:")
            print("        " + str(matrix).replace("\n", "\n        "))
            print("    Icarus determinant: " + str(det))
            print("    Parsed matrix determinant: " + str(np_det_float))
        else:
            ok_count += 1
    
    print(f"{runs} runs, {ok_count} successful")
    
if __name__ == "__main__":
    main("src", int(sys.argv[1]), int(sys.argv[2]))
