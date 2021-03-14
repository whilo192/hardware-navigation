# hardware-navigation

The aim of this project is to create an open source Verilog core for processing (in realtime) measurements from accelerometers, gyroscopes, and magnetometers to estimate the orientation and position of an object. This will be implemented on an FPGA to make an inertial navigation unit. This will then be compared to a software implementation in Python in order to validate performance.

## Objectives

* Design a Kalman filter architecture
* Implement in Python and plot output, produce input/output sample graphs
* Make a Verilog testbench
* Implement the filter as a Verilog module
* Implement on FPGA
* Make ineritial navigation unit from a Tang Nano and an SPI IMU module
* Test and evaluate accuracy
* Validate its performance compared to the Python software implementation

## Future work

* Add GNSS support
* Implement in silicon
