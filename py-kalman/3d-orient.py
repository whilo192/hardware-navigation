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
B = np.matrix([[0, 0, 0, DT, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, DT, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, DT, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]])


noise_range = list(np.arange(0.005, 0.1, 0.005))
noise_range.reverse()

rms = np.empty((len(noise_range), 1))

for (j, GN) in enumerate(noise_range):
    p = np.identity(12) * GN

    kalman_state = np.empty((len(t_vals), 12))
    act_state = np.empty((len(t_vals), 12))

    cov_state = np.empty((len(t_vals), 12))

    x = np.empty((12, 1))
    x[0] = 0
    x[1] = np.sin(2 * np.pi / 3)
    x[2] = np.sin(4 * np.pi / 3)

    OMEGA = 10

    def gen_value(i, t):
        actual = np.matrix([[np.sin(OMEGA * t)], [np.sin(OMEGA * t + 2 * np.pi / 3)], [np.sin(OMEGA * t + 4 * np.pi / 3)], [OMEGA * np.cos(OMEGA * t)], [OMEGA * np.cos(OMEGA * t + 2 * np.pi / 3)], [OMEGA * np.cos(OMEGA * t + 4 * np.pi / 3)], [np.sin(OMEGA * t)], [np.sin(OMEGA * t + 2 * np.pi / 3)], [np.sin(OMEGA * t + 4 * np.pi / 3)], [0], [0], [0]])
        
        act_state[i] = actual.T
        
        return actual

    i_exit = 0

    for (i, t) in enumerate(t_vals):
        actual = gen_value(i, t)
        
        H = np.zeros((12, 12))
        H[3, 3] = 1
        H[4, 4] = 1
        H[5, 5] = 1
        H[0, 6] = 1
        H[1, 7] = 1
        H[2, 8] = 1
        H[6, 6] = 1
        H[7, 7] = 1
        H[8, 8] = 1
               
        u = np.copy(actual)
        u[0] = 0
        u[1] = 0
        u[2] = 0


        #Calculate our measurements
        z = H @ actual + np.random.normal(0, GN, (12, 1))
        z[9] = 0
        z[10] = 0
        z[11] = 0
        
        r = np.identity(12) * GN
        q = np.identity(12) * GN
        
        x_new = F @ x + B @ u + np.random.normal(0, GN, (12, 1))
        x_new[9] = 0
        x_new[10] = 0
        x_new[11] = 0
        
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
         
LINEWIDTH = 4
FONTSIZE = "xx-large"
         
(fig, axes) = plt.subplots(4, sharex=True, figsize=(15, 10))

axes[0].plot(t_vals, kalman_state[:, 0], label=r"$\theta_x$ ($rad$)", linewidth=LINEWIDTH)
axes[0].plot(t_vals, kalman_state[:, 1], label=r"$\theta_y$ ($rad$)", linewidth=LINEWIDTH)
axes[0].plot(t_vals, kalman_state[:, 2], label=r"$\theta_z$ ($rad$)", linewidth=LINEWIDTH)
axes[0].grid(True)
axes[0].set_title("Estimated Orientation", fontsize=FONTSIZE)
axes[0].set_ylabel("Orientation", fontsize=FONTSIZE)
axes[0].legend(fontsize=FONTSIZE)

axes[1].plot(t_vals, act_state[:, 0], linewidth=LINEWIDTH)
axes[1].plot(t_vals, act_state[:, 1], linewidth=LINEWIDTH)
axes[1].plot(t_vals, act_state[:, 2], linewidth=LINEWIDTH)
axes[1].grid(True)
axes[1].set_title(r"Actual Orientation", fontsize=FONTSIZE)
axes[1].set_ylabel("Orientation", fontsize=FONTSIZE)

axes[2].plot(t_vals, err_vals[:, 0], linewidth=LINEWIDTH)
axes[2].plot(t_vals, err_vals[:, 1], linewidth=LINEWIDTH)
axes[2].plot(t_vals, err_vals[:, 2], linewidth=LINEWIDTH)
axes[2].grid(True)
axes[2].set_title(r"Absolute Error of Orientation", fontsize=FONTSIZE)
axes[2].set_ylabel("Error", fontsize=FONTSIZE)

axes[3].semilogy(t_vals, cov_state[:, 0], linewidth=LINEWIDTH)
axes[3].semilogy(t_vals, cov_state[:, 1], linewidth=LINEWIDTH)
axes[3].semilogy(t_vals, cov_state[:, 2], linewidth=LINEWIDTH)
axes[3].grid(True)
axes[3].set_title(r"Covariance of the Estimate of Orientation", fontsize=FONTSIZE)
axes[3].set_xlabel("Time (s)", fontsize=FONTSIZE)
axes[3].set_ylabel("Covariance", fontsize=FONTSIZE)

plt.show()

(fig, axes) = plt.subplots(1, sharex=True, figsize=(15, 10))
axes.plot(noise_range, rms, label=r"RMS of Error", linewidth=LINEWIDTH)
axes.grid(True)
axes.set_title("RMS of Error vs. Estimated Noise", fontsize=FONTSIZE)
axes.set_ylabel("RMS of Error", fontsize=FONTSIZE)
axes.set_xlabel("Estimated Noise", fontsize=FONTSIZE)
#axes.legend()

plt.show()
