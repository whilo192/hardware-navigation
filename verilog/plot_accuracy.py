#!/usr/bin/env python3

import validator
import matplotlib.pyplot as plt
import numpy as np

STEP = 8

matrix_size = 12
max_integer_width = 64
max_decimal_width = 64

int_widths = list(range(STEP, max_integer_width + STEP, STEP))
dec_widths = list(range(STEP, max_decimal_width + STEP, STEP))

nx = len(int_widths)
ny = len(dec_widths)

xv, yv = np.meshgrid(int_widths, dec_widths, sparse=False, indexing='xy')

results = np.empty((ny, nx))

for i in range(ny):
    for j in range(nx):
        while True:
            try:
                dec_width = int(yv[i, j])
                int_width = int(xv[i, j])

                whole_width = dec_width + int_width

                validator.my_subprocess_run(["./gen_mat_operation.py", str(matrix_size), str(whole_width), str(dec_width)])

                (count, ok_count, avg_err) = validator.process_op("src", matrix_size, whole_width, dec_width, 10, "det")

                avg_err_log = np.log(avg_err)

                results[i, j] = avg_err_log

                print(i, j, dec_width, int_width, whole_width, avg_err_log)

                break
            except np.linalg.LinAlgError:
                print("Singular matrix, trying again")

fig, ax = plt.subplots()
im = ax.imshow(results)

ax.set_xticks(np.arange(len(int_widths)))
ax.set_yticks(np.arange(len(dec_widths)))

ax.set_xticklabels(int_widths)
ax.set_yticklabels(dec_widths)

for i in range(ny):
    for j in range(nx):
        ax.text(j, i, "{:.2f}".format(results[i, j]), ha="center", va="center", color="w")

ax.set_title("Log of average error for diffferent fixed point data widths")

plt.xlabel("Integer width (bits)")
plt.ylabel("Decimal width (bits)")

plt.savefig("heatmap.pdf")
plt.show()

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

ax.set_title("Log of average error for diffferent fixed point data widths")
ax.plot_surface(xv, yv, results)
ax.set_xlabel("Integer width (bits)")
ax.set_ylabel("Decimal width (bits)")
ax.set_zlabel("Log of error")

plt.savefig("sfc_plot.pdf")
plt.show()
