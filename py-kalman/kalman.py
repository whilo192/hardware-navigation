#!/usr/bin/env python3

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def main():
    DT = 0.001
    
    GN = 10
      
    #State transition matrix
    F = np.matrix([[1, DT], [0, 1]])

    #Position estimation
    x = np.matrix([[0]] * 2)
    p = np.identity(2) * GN
    
    #Covariance of the process noise
    q = np.identity(2) * GN
    
    #Covariance of the observation noise
    r = np.identity(1) * GN

    #Control input model
    B = np.matrix([[0.5 * DT ** 2], [DT]])

    #Observation model
    H = np.matrix([[1, 0]])

    disp_x = []
    act_x = []

    x_old = 0
    v_old = 0

    t_vals = [x * DT for x in range(0,10000)]

    for i in t_vals:
        x_act = 10 * np.sin(np.pi * i)
        
        v_act = (x_act - x_old) / DT
        a_act = (v_act - v_old) / DT
        
        x_old = x_act
        v_old = v_act
        
        accel = a_act + float(np.random.normal(0, GN, (1, 1)))
        z = x_act + float(np.random.normal(0, GN, (1, 1)))
        
        x_new = F.dot(x) + accel * B
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
        act_x += [x_act]

    plt.plot(t_vals, list(disp_x))
    plt.plot(t_vals, list(act_x))
    plt.show()

if __name__ == "__main__":
    main()
