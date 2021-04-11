#!/usr/bin/env python3

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def main():
    DT = 0.001
    
    GN = 10
      
    #State transition matrix
    F = np.matrix([[1, DT, 0], [0, 1, DT], [0, 0, 1]])

    #Position estimation
    x = np.matrix([[0]] * 3)
    p = np.identity(3) * GN
    
    #Covariance of the process noise
    q = np.identity(3) * GN
    
    #Covariance of the observation noise
    r = np.identity(1) * GN

    #Control input model
    B = np.matrix([[0, 0, 0], [0, 0, 0], [0, 0, 1]])

    #Observation model
    H = np.matrix([[0, 0, 1]])

    t_vals = [x * DT for x in range(0,10000)]

    kalman_state = np.empty((len(t_vals), 3))
    act_state = np.empty((len(t_vals), 3))

    x_old = 0
    v_old = 0

    OMEGA = 2 * np.pi

    def gen_value(i,t):
        nonlocal x_old
        nonlocal v_old
        
        x_act = 10 * np.sin(OMEGA * t)
        #x_act = x_old + float(np.random.normal(0, GN / 1000, (1, 1)))
        #x_act = 10 * (i % 100 < 50)
        
        v_act = (x_act - x_old) / DT
        a_act = (v_act - v_old) / DT
        
        x_old = x_act
        v_old = v_act
        
        act_state[i] = np.matrix([x_act, v_act, a_act])

        return (x_act, a_act)

    for (i, t) in enumerate(t_vals):
        (x_act, a_act) = gen_value(i, t)
        
        accel = a_act + float(np.random.normal(0, GN, (1, 1)))
        z = a_act + float(np.random.normal(0, GN, (1, 1)))
        
        u = np.matrix([[0], [0], [accel]])
        
        x_new = F.dot(x) + B.dot(u)
        p_new = F.dot(p).dot(F.T) + q
        
        y = z - H.dot(x_new)

        s = H.dot(p_new).dot(H.T) + r
        
        k = p_new.dot(H.T).dot(s.I)
        
        x_new_new = x_new + k.dot(y)
              
        p_new_new = (np.identity(3) - k.dot(H)).dot(p_new)
        
        y_new = z - H.dot(x_new_new)

        x = x_new_new
        p = p_new_new

        kalman_state[i] = x.T

    (fig, axes) = plt.subplots(3, sharex=True)

    act_state = act_state[10:]
    kalman_state = kalman_state[10:]
    t_vals = t_vals[10:]

    axes[0].plot(t_vals, kalman_state[:, 0], label="Position ($m$)")
    axes[0].plot(t_vals, kalman_state[:, 1], label="Velocity ($ms^{-1}$)")
    #axes[0].plot(t_vals, kalman_state[:, 2], label="Acceleration ($ms^{-2}$)")
    axes[0].grid(True)
    axes[0].set_title("Estimated Position and Velocity")
    axes[0].set(ylabel = "Estimated State")
    axes[0].legend()
    
    axes[1].plot(t_vals, act_state[:, 0])
    axes[1].plot(t_vals, act_state[:, 1])
    #axes[1].plot(t_vals, act_state[:, 2])
    axes[1].grid(True)
    axes[1].set_title("Actual Position and Velocity")
    axes[1].set(ylabel = "Actual State")
    
    err_vals = kalman_state - act_state

    axes[2].plot(t_vals, err_vals[:, 0])
    axes[2].plot(t_vals, err_vals[:, 1])
    #axes[2].plot(t_vals, err_vals[:, 2])
    axes[2].grid(True)
    axes[2].set_title("Absolute Error of Position and Velocity")
    axes[2].set(xlabel = "Time (s)", ylabel = "Absolute Error")
    
    plt.show()

if __name__ == "__main__":
    main()
