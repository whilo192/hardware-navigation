#!/usr/bin/env python3 

import validator
import matplotlib.pyplot as plt
import numpy as np

STEP = 4

matrix_size = 4
max_integer_width = 32
max_decimal_width = 64

int_widths = list(range(STEP, max_integer_width + STEP, STEP))
dec_widths = list(range(STEP, max_decimal_width + STEP, STEP))

nx = len(int_widths)
ny = len(dec_widths)

xv, yv = np.meshgrid(int_widths, dec_widths, sparse=False, indexing='xy')

results = np.empty((ny, nx))

for i in range(nx):
    for j in range(ny):
        avg_err_log = np.log(validator.main("src", matrix_size, int(xv[j, i] + yv[j, i]), int(yv[j, i]), 10, ["inv"]))

        results[j, i] = avg_err_log

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

print(xv)
print(yv)
print(results)

ax.plot_surface(xv, yv, results)
plt.xlabel("Integer width (bits)")
plt.ylabel("Decimal width (bits)")

plt.show()
