#!/usr/bin/env python3
 
import os
import sys
import subprocess
import random
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

def hex_to_dec(hex_in, width, bin_pos):
    int_in = int(hex_in, 16)
    
    if int_in & (1 << (width-1)): #Sign bit high
        int_in = int_in - (1 << width) 
        
    return int_in / (2 ** bin_pos)

def generate_numpy_vector_from_verilog_output(line, n, width, bin_pos):
    mat = line.split(":")[1][1:]
    
    step = width // 4
    
    matrix = np.empty((n,1))
    
    for row in range(n):
        pos = n - row - 1
        bit_slice = mat[pos * step:pos*step+step]
        
        val = hex_to_dec(bit_slice, width, bin_pos)
        
        matrix[row,0] = val
    
    return matrix

def generate_numpy_matrix_from_verilog_output(line, n, width, bin_pos):
    mat = line.split(":")[1][1:]
    
    step = width // 4
    
    matrix = np.empty((n,n))
    
    for row in range(n):
        for col in range(n):
            pos = (n - col - 1) * n + (n - row - 1)
            bit_slice = mat[pos * step:pos*step+step]
            
            val = hex_to_dec(bit_slice, width, bin_pos)
            
            matrix[col,row] = val
    
    return matrix

def generate_numpy_scalar_from_verilog_output(line, width, bin_pos):
    scal = line.split(":")[1][1:]
    
    val = hex_to_dec(scal, width, bin_pos)
    
    return val

def np_scal_diff(m1, m2):
    return ((m1 - m2) ** 2).mean() ** 0.5

def process_op(wk_dir, n, width, bin_pos, count, op):
    n2 = n**2
    
    with open(rf"test_{op}.v", 'r') as test_file:
        with open(wk_dir + rf"/test_{op}.v", 'w') as copy_file:
            buf = test_file.read()
            py_seed = random.randrange(1024);
            copy_file.write(buf.format(n=n, width=width, bin_pos=bin_pos, py_seed=py_seed, py_count=count))

    os.chdir(wk_dir)
    
    my_subprocess_run(["iverilog", "-o", rf"test_{op}", rf"test_{op}.v"] +  ["matdet" + str(i+2) +".v" for i in range(n-1)] + ["mul.v", "div.v"] + [rf"scalvec{n2}.v", rf"mattrans{n}.v", rf"vecvec{n}.v", rf"matmat{n}.v", rf"matinv{n}.v"])
    result = my_subprocess_run(["vvp", rf"test_{op}"], False)
    
    os.chdir("..")
    
    lines = result.split('\n')[1:-1] # Trim line about VCD output
    
    i = 0
    
    ok_count = 0
    
    total_err = 0
    
    while i < len(lines):
        if op == "dot":
            lhs = generate_numpy_vector_from_verilog_output(lines[i], n, width, bin_pos)
            rhs = generate_numpy_vector_from_verilog_output(lines[i + 1], n, width, bin_pos)
            dot = generate_numpy_scalar_from_verilog_output(lines[i + 2], width, bin_pos)
            
            np_dot = np.matmul(lhs.T, rhs)[0,0]
            
            err = np.abs(dot - np_dot)
            if err < 0.01:
                ok_count += 1
            else:
                print(lines[i])
                print(lines[i+1])
                print(lines[i+2])
                
                print()
                
                print(lhs)
                print(rhs)
                print(dot)
                
                print()
                
                print(np_dot)
                
                print()
                
                print(err)
            
            i += 3
        if op == "mul":
            lhs = generate_numpy_matrix_from_verilog_output(lines[i], n, width, bin_pos)
            rhs = generate_numpy_matrix_from_verilog_output(lines[i + 1], n, width, bin_pos)
            prod = generate_numpy_matrix_from_verilog_output(lines[i + 2], n, width, bin_pos)
            
            np_prod = np.matmul(lhs, rhs)
            
            err = np_scal_diff(prod, np_prod)
            
            if err < 0.01:
                ok_count += 1
            else:
                print(lines[i])
                print(lines[i+1])
                print(lines[i+2])
                
                print()
                
                print(lhs)
                print(rhs)
                print(prod)
                
                print()
                
                print(np_prod)
                
                print()
                
                print(err)
            
            i += 3
        elif op == "det":
            mat = generate_numpy_matrix_from_verilog_output(lines[i], n, width, bin_pos)
            det = generate_numpy_scalar_from_verilog_output(lines[i + 1], width, bin_pos)
            
            np_det = np.linalg.det(mat)
            
            err = np.abs(np_det - det)
            
            if err < 0.01:
                ok_count += 1
            else:
                print(lines[i])
                print(lines[i+1])
                
                print()
                
                print(mat)
                print(det)
                
                print()
            
                print(np_det)
                
                print()
                
                print(err)
            
            i += 2
        elif op == "trans":
            mat = generate_numpy_matrix_from_verilog_output(lines[i], n, width, bin_pos)
            trans = generate_numpy_matrix_from_verilog_output(lines[i + 1], n, width, bin_pos)
            
            np_trans = mat.T

            err = np_scal_diff(trans, np_trans)
            
            if err < 0.01:
                ok_count += 1
            else:
                print(lines[i])
                print(lines[i+1])
                
                print()
                
                print(mat)
                print(trans)
            
                print()
                
                print(np_trans)
                
                print()
                
                print(err)
                
            i += 2
        elif op == "inv":
            if lines[i] == "singular":
                i+= 1
                ok_count += 1
                err = 0
                print("Singular matrix")
            else:
                mat = generate_numpy_matrix_from_verilog_output(lines[i], n, width, bin_pos)
                inv = generate_numpy_matrix_from_verilog_output(lines[i + 1], n, width, bin_pos)
                det = generate_numpy_scalar_from_verilog_output(lines[i + 2], width, bin_pos)

                np_inv = np.linalg.inv(mat)
                np_det = np.linalg.det(mat)
                
                err = np_scal_diff(inv, np_inv)
                
                if err < 0.05:
                    ok_count += 1
                else:
                    print(lines[i])
                    print(lines[i+1])
                    print(lines[i+2])
                    
                    print()
                    
                    print(mat)
                    print(inv)
                    print(det)
                    
                    print()
                
                    print(np_inv)
                    print(np_det)
                    
                    print()
                    
                    print(err)
                    
                i += 3
                
        total_err += err
            
            
    avg_err = total_err / count
    
    return (count, ok_count, avg_err)

def main(wk_dir, n, width, bin_pos, count, ops):
    result = my_subprocess_run(["./gen_mat_operation.py", str(n), str(width), str(bin_pos)])
    
    for op in ops:
        
        (count, ok_count, avg_err) = process_op(wk_dir, n, width, bin_pos, count, op)
        
        print(f"{op}: {count} runs, {ok_count} successful. Average error: {avg_err}")
    
if __name__ == "__main__":
    #n, width, bin_pos, count
    main("src", int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), ["dot", "mul", "det", "trans", "inv"])
