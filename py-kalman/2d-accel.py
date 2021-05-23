#!/usr/bin/env python3

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

DT = 0.001

R = 0.7

#theta, theta_dot, x, x_dot, x_dot_dot, y, y_dot, y_dot_dot
F = np.matrix([[1, DT, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, DT, 0.5 * DT ** 2, 0, 0, 0], [0, 0, 0, 1, DT, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, DT, 0.5 * DT ** 2], [0, 0, 0, 0, 0, 0, 1, DT], [0, 0, 0, 0, 0, 0, 0, 0]])

t_vals = [x * DT for x in range(0,1000)]

B = np.matrix([[0, DT, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0.5 * DT ** 2, 0, 0, 0], [0, 0, 0, 0, DT, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0.5 * DT ** 2], [0, 0, 0, 0, 0, 0, 0, DT], [0, 0, 0, 0, 0, 0, 0, 1]])

H = np.matrix([[0, 1, 0, 0, 1, 0, 0, 1]])

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

x = np.matrix([[0], [THETA_DOT_INIT], [0], [0], [0], [0], [0], [0]])

def gen_value(i,t):
    theta_dot_dot = 0
    theta_dot = THETA_DOT_INIT
    theta = theta_dot * t

    r_dot_dot = -R * (theta_dot) ** 2
    phi_dot_dot = R * theta_dot_dot
    

    act_state[i] = np.matrix([theta, theta_dot, 0, 0, r_dot_dot, 0, 0, phi_dot_dot])

    return (theta, theta_dot, r_dot_dot, phi_dot_dot)
    
for (i, t) in enumerate(t_vals):
    (theta_act, theta_dot_act, r_dot_dot_act, phi_dot_dot_act) = gen_value(i, t)
    
    theta_dot = theta_dot_act + float(np.random.normal(0, GN, (1, 1)))
    r_dot_dot = r_dot_dot_act + float(np.random.normal(0, GN, (1, 1)))
    phi_dot_dot = phi_dot_dot_act + float(np.random.normal(0, GN, (1, 1)))
        
    z = np.array([theta_dot_act]) + np.random.normal(0, GN, (1, 1))
    
    
    r_corrected = r_dot_dot + R * theta_dot_act ** 2
    
    phi_corrected = phi_dot_dot
    
    theta = float(x[0])
    
    u = [[0], [theta_dot], [0], [0], [r_corrected * np.cos(theta) + phi_corrected * np.cos(theta + np.pi / 2)], [0], [0], [r_corrected * np.sin(theta) + phi_corrected * np.sin(theta + np.pi / 2)]]
        
    x_new = F.dot(x) + B.dot(u) + np.random.normal(0, GN, (8, 1))
    p_new = F.dot(p).dot(F.T) + q
      
    y = z - H.dot(x_new)

    s = H.dot(p_new).dot(H.T) + r
        
    k = p_new.dot(H.T).dot(s.I)
        
    x_new_new = x_new + k.dot(y)
              
    p_new_new = (np.identity(8) - k.dot(H)).dot(p_new)
        
    y_new = z - H.dot(x_new_new)

    x = x_new_new
    p = p_new_new
    
    kalman_state[i] = x.T
    cov_state[i] = [p[x,x] for x in range(len(F[0]))]
    
(fig, axes) = plt.subplots(4, sharex=True, figsize=(15, 10))

axes[0].plot(t_vals, kalman_state[:, 0], label="$\phi$ ($rad$)")
axes[0].plot(t_vals, kalman_state[:, 2], label="$x$ (m)")
axes[0].plot(t_vals, kalman_state[:, 5], label="$y$ (m)")
axes[0].grid(True)
axes[0].set_title("Estimated $\phi$, $x$, and $y$$")
axes[0].set(ylabel = "Estimated State")
axes[0].legend()

axes[1].plot(t_vals, act_state[:, 0])
axes[1].plot(t_vals, act_state[:, 2])
axes[1].plot(t_vals, act_state[:, 5])
axes[1].grid(True)
axes[0].set_title("Estimated $\phi$, $x$, and $y$$")
axes[1].set(ylabel = "Actual State")

err_vals = np.abs(kalman_state - act_state)

axes[2].plot(t_vals, err_vals[:, 0])
axes[2].plot(t_vals, err_vals[:, 2])
axes[2].plot(t_vals, err_vals[:, 5])
axes[2].grid(True)
axes[0].set_title("Estimated $\phi$, $x$, and $y$$")
axes[2].set(ylabel = "Absolute Error")

axes[3].semilogy(t_vals, cov_state[:, 0])
axes[3].semilogy(t_vals, cov_state[:, 2])
axes[3].semilogy(t_vals, cov_state[:, 5])
axes[3].grid(True)
axes[0].set_title("Estimated $\phi$, $x$, and $y$$")
axes[3].set(xlabel = "Time (s)", ylabel = "Covariance")

plt.show()
