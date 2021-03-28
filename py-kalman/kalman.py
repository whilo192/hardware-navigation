#!/usr/bin/env python3

import numpy as np

def main():
    DT = 0.1
    
    GN = 0.01
    
    F = np.matrix([[1, DT, 0, 0, 0, 0], [0, 1, DT, 0, 0, 0], [0, 0, 1, 0, 0, 0], [0, 0, 0, 1, DT, 0], [0, 0, 0, 0, 1, DT], [0, 0, 0, 0, 0, 1]])

    x = np.matrix([[0]] * 6)
    p = np.identity(6) * GN
    
    q = np.identity(6) * GN
    r = np.identity(6) * GN

    H = np.matrix([[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1]])

    for i in range(0,10):
        w = np.random.normal(0, GN, (6, 1, 1))[0]
        z = np.random.normal(0, GN, (1, 6, 1))[0]
        
        x_new = F.dot(x) # + B dot u
        p_new = F.dot(p).dot(F.T)
        
        y = z - H.dot(x_new)
        
        s = H.dot(p_new).dot(H.T) + r
        
        k = p_new.dot(H.T).dot(s.I)
        
        x_new_new = x_new + k.dot(y)
              
        p_new_new = (np.identity(6) - k.dot(H)).dot(p_new)
        
        y_new = z - H.dot(x_new_new)

        x = x_new_new
        p = p_new_new
        
    print(x)
    print(p)

if __name__ == "__main__":
    main()
