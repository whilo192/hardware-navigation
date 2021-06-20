#!/usr/bin/env python3

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

DT = 0.001

R = 0.7

#theta, theta_dot, x, x_dot, x_dot_dot, y, y_dot, y_dot_dot
F = np.matrix([[1, DT, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, DT, 0.5 * DT ** 2, 0, 0, 0], [0, 0, 0, 1, DT, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, DT, 0.5 * DT ** 2], [0, 0, 0, 0, 0, 0, 1, DT], [0, 0, 0, 0, 0, 0, 0, 0]])

t_vals = [x * DT for x in range(0,1000)]

B = np.matrix([[0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]])

#Measurements of omega_dot and u_dot_dot from omega_dot
H = np.matrix([0, 1, 0, 0, 0, 0, 0, 0])

GN = 0.01

p = np.identity(8) * GN
q = np.identity(8) * GN
r = np.identity(1) * GN

kalman_state = np.empty((len(t_vals), 8))
act_state = np.empty((len(t_vals), 8))

cov_state = np.empty((len(t_vals), 8))

OMEGA = 2 * np.pi
A = 2

THETA_DOT_INIT = 1

x = np.matrix([[0], [THETA_DOT_INIT], [A], [0], [-A * OMEGA ** 2], [0], [A * OMEGA], [0]])

def gen_value(i,t):
    theta_dot = THETA_DOT_INIT
    theta = theta_dot * t

    x = A * np.cos(OMEGA * t)
    y = A * np.sin(OMEGA * t)

    x_dot = -A * OMEGA * np.sin(OMEGA * t)
    y_dot = A * OMEGA * np.cos(OMEGA * t)

    x_dot_dot = -A * OMEGA ** 2 * np.cos(OMEGA * t)
    y_dot_dot = -A * OMEGA ** 2 * np.sin(OMEGA * t)

    u_dot_dot = -R * theta_dot ** 2 + x_dot_dot * np.cos(theta) + y_dot_dot * np.sin(theta)
    v_dot_dot = x_dot_dot * np.sin(theta) + y_dot_dot * np.cos(theta) 

    act_state[i] = np.matrix([theta, theta_dot, x, x_dot, x_dot_dot, y, y_dot, y_dot_dot])

    return (theta, theta_dot, u_dot_dot, v_dot_dot)
    
for (i, t) in enumerate(t_vals):
    (theta_act, theta_dot_act, u_dot_dot_act, v_dot_dot_act) = gen_value(i, t)
    
    theta_dot = theta_dot_act + float(np.random.normal(0, GN, (1, 1)))
    u_dot_dot = u_dot_dot_act + float(np.random.normal(0, GN, (1, 1)))
    v_dot_dot = v_dot_dot_act + float(np.random.normal(0, GN, (1, 1)))
        
    theta = float(x[0])
        
    u_conv = u_dot_dot + R * theta_dot ** 2
        
    x_dot_dot = u_conv * np.cos(theta) + v_dot_dot * np.sin(theta)
    y_dot_dot = -u_conv * np.sin(theta) + v_dot_dot * np.cos(theta) 
        
    z = np.array([theta_dot]) + np.random.normal(0, GN, (1, 1))
    
    u = np.array([[0], [theta_dot], [0], [0], [0], [0], [0], [0]])
        
    x_new = F @ x + B @ u + np.random.normal(0, GN, (8, 1))
    p_new = F @ p @ F.T + q
      
    y = z - H @ x_new
    
    s = H @ p_new @ H.T + r
        
    k = p_new @ H.T @ s.I
    
    x_new_new = x_new + k @ y
    
    p_new_new = (np.identity(8) - k @ H) @ p_new
        
    y_new = z - H @ x_new_new

    x = x_new_new
    p = p_new_new
    
    kalman_state[i] = x.T
    cov_state[i] = [p[x,x] for x in range(len(F[0]))]
    
(fig, axes) = plt.subplots(4, sharex=True, figsize=(15, 10))

err_vals = np.abs(kalman_state - act_state)

axes[0].plot(t_vals, kalman_state[:, 0], label="$\phi$ ($rad$)")
axes[0].plot(t_vals, kalman_state[:, 1], label="$\omega$ ($rad \cdot s^{-1}$)")
axes[0].grid(True)
axes[0].set_title("Estimated $\phi$ and $\omega$")
axes[0].set(ylabel = "Estimated State")
axes[0].legend()

axes[1].plot(t_vals, act_state[:, 0])
axes[1].plot(t_vals, act_state[:, 1])
axes[1].grid(True)
axes[1].set_title("Actual $\phi$ and $\omega$")
axes[1].set(ylabel = "Actual State")

axes[2].plot(t_vals, err_vals[:, 0])
axes[2].plot(t_vals, err_vals[:, 1])
axes[2].grid(True)
axes[2].set_title("Absolute Error of $\phi$ and $\omega$")
axes[2].set(ylabel = "Absolute Error")

axes[3].semilogy(t_vals, cov_state[:, 0])
axes[3].semilogy(t_vals, cov_state[:, 1])
axes[3].grid(True)
axes[3].set_title("Covariance of $\phi$ and $\omega$")
axes[3].set(xlabel = "Time (s)", ylabel = "Covariance")

plt.show()

(fig, axes) = plt.subplots(3, sharex=True, figsize=(15, 10))

axes[0].plot(kalman_state[:, 2], kalman_state[:, 5])
axes[0].grid(True)
axes[0].set_title("Estimated Position")
axes[0].set(ylabel = "y (m)")

axes[1].plot(act_state[:, 2], act_state[:, 5])
axes[1].grid(True)
axes[1].set_title("Actual Position")
axes[1].set(ylabel = "y (m)")

axes[2].plot(err_vals[:, 2], err_vals[:, 5])
axes[2].grid(True)
axes[2].set_title("Absolute Error of Position")
axes[2].set(ylabel = "y (m)")

plt.show()
