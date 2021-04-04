#!/usr/bin/env python3

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def main():
    DT = 0.001
    
    GN = 0.01
    
    #F = np.matrix([[1, DT, 0, 0, 0, 0], [0, 1, DT, 0, 0, 0], [0, 0, 1, 0, 0, 0], [0, 0, 0, 1, DT, 0], [0, 0, 0, 0, 1, DT], [0, 0, 0, 0, 0, 1]])
    F = np.matrix([[1, DT], [0, 1]])

    x = np.matrix([[0]] * 2)
    p = np.identity(2) * GN
    
    q = np.identity(2) * GN
    r = np.identity(2) * GN

    #H = np.matrix([[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1]])

    B = np.matrix([[0.5 * DT ** 2], [DT]])

    H = np.matrix([[0, 0], [0, 1]])

    disp_x = []

    t_vals = [x * DT for x in range(0,10000)]

    v_accum = 0

    for i in t_vals:
        acc = -10 * np.cos(np.pi * i)
        
        v_accum += acc * DT
        
        w = np.random.normal(0, GN, (2, 1))
        z = np.random.normal(0, GN, (2, 1)) + [[0], [v_accum]]
        
        x_new = F.dot(x) + acc * B + w
        p_new = F.dot(p).dot(F.T)
        
        y = z - H.dot(x_new)
        
        s = H.dot(p_new).dot(H.T) + r
        
        k = p_new.dot(H.T).dot(s.I)
        
        x_new_new = x_new + k.dot(y)
              
        p_new_new = (np.identity(2) - k.dot(H)).dot(p_new)
        
        y_new = z - H.dot(x_new_new)

        x = x_new_new
        p = p_new_new

        disp_x += [float(x[0])]

    plt.plot(t_vals, list(disp_x))
    plt.show()

if __name__ == "__main__":
    main()
