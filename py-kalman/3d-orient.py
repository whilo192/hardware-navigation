#!/usr/bin/env python3

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

DT = 0.001

R = 0.7

#orient_x, orient_y, orient_z, gyro_x, gyro_y, gyro_z, B_x, B_y, B_z, a_x, a_y, a_z
F = np.matrix([[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

t_vals = [x * DT for x in range(0,1000)]

#u_k is gyro, B, and g
B = np.matrix([[0, 0, 0, DT, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, DT, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, DT, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])


time_range = list(np.arange(0.005, 0.1, 0.005))

rms = np.empty((len(time_range), 1))

for (j, GN) in enumerate(time_range):
    p = np.identity(12) * GN

    kalman_state = np.empty((len(t_vals), 12))
    act_state = np.empty((len(t_vals), 12))

    cov_state = np.empty((len(t_vals), 12))

    x = np.empty((12, 1))

    OMEGA = 10

    def gen_value(i, t):
        actual = np.matrix([[np.sin(OMEGA * t)], [np.cos(OMEGA * t) - 1], [np.sin(OMEGA * t)], [OMEGA * np.cos(OMEGA * t)], [-OMEGA * np.sin(OMEGA * t)], [OMEGA * np.cos(OMEGA * t)], [0], [0], [0], [0], [0], [0]])
        
        act_state[i] = actual.T
        
        return actual

    for (i, t) in enumerate(t_vals):
        actual = gen_value(i, t)
        
        H = np.zeros((12, 12))
        H[0,3] = DT
        H[1,4] = DT
        H[2,5] = DT
        
        u = actual + np.random.normal(0, GN, (12, 1))
        u[0] = 0
        u[1] = 0
        u[2] = 0
        
        z = H @ actual
        
        r = np.random.normal(0, GN, (12, 12))
        q = np.random.normal(0, GN, (12, 1))
        
        
        x_new = F @ x + B @ u + np.random.normal(0, GN, (12, 1))
        p_new = F @ p @ F.T + q
        
        y = z - H @ x_new
        
        s = H @ p_new @ H.T + r
            
        k = p_new @ H.T @ s.I
        
        x_new_new = x_new + k @ y
        
        p_new_new = (np.identity(12) - k @ H) @ p_new
            
        y_new = z - H @ x_new_new

        x = x_new_new
        p = p_new_new
        
        kalman_state[i] = x.T
        cov_state[i] = [p[x,x] for x in range(len(F[0]))]
                     
    err_vals = np.abs(kalman_state - act_state)
    
    rms[j] = np.sqrt(np.mean(err_vals ** 2))
                     
(fig, axes) = plt.subplots(4, sharex=True, figsize=(15, 10))

axes[0].plot(t_vals, kalman_state[:, 0], label=r"$\theta_x$ ($rad$)")
axes[0].plot(t_vals, kalman_state[:, 1], label=r"$\theta_y$ ($rad$)")
axes[0].plot(t_vals, kalman_state[:, 2], label=r"$\theta_z$ ($rad$)")
axes[0].grid(True)
axes[0].set_title("Estimated angle")
axes[0].set(ylabel = "Estimated State")
axes[0].legend()

axes[1].plot(t_vals, act_state[:, 0])
axes[1].plot(t_vals, act_state[:, 1])
axes[1].plot(t_vals, act_state[:, 2])
axes[1].grid(True)
axes[1].set_title(r"Actual $\theta$")
axes[1].set(ylabel = "Actual State")

axes[2].plot(t_vals, err_vals[:, 0])
axes[2].plot(t_vals, err_vals[:, 1])
axes[2].plot(t_vals, err_vals[:, 2])
axes[2].grid(True)
axes[2].set_title(r"Absolute Error of $\theta$")
axes[2].set(ylabel = "Absolute Error")

axes[3].semilogy(t_vals, cov_state[:, 0])
axes[3].semilogy(t_vals, cov_state[:, 1])
axes[3].semilogy(t_vals, cov_state[:, 2])
axes[3].grid(True)
axes[3].set_title(r"Covariance of $\theta$")
axes[3].set(xlabel = "Time (s)", ylabel = "Covariance")

plt.show()

(fig, axes) = plt.subplots(1, sharex=True, figsize=(15, 10))
axes.plot(time_range, rms, label=r"RMS of Error")
axes.grid(True)
axes.set_title("RMS of Error over Estimated Measurement and State Transition Noise")
axes.set(ylabel = "RMS of Error")
axes.set(xlabel = "Estimated Noise")
axes.legend()

plt.show()
