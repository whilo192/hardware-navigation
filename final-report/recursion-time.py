#!/usr/bin/env python3

import sys
import numpy as np

def mat_det(matrix):
    n = len(matrix)
    
    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    
    det = 0    
    sign = 1
    
    for k in range(n):
        minor = np.empty((n-1, n-1))
        
        for i in range(n-1): # row
            matrix_row = i + 1
            for j in range(n-1): # col
                matrix_col = j if j < k else j + 1
                minor[i, j] = matrix[matrix_row, matrix_col]
            
        print(minor)
        det += sign * matrix[0, k] * mat_det(minor)
        sign *= -1
        
    return det

if __name__ == "__main__":
    print(mat_det(np.matrix(eval(sys.argv[1]))))
