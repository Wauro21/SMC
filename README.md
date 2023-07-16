# Stepper-Motor-Controller

![smc_logo](tools/rsrcs/icon.png)

**Stepper-Motor-Controller (SMC)** is a project that provides a user-friendly driver and graphical user interface (GUI) for control of a stepper motor using and Arduino-based board in conjuction with the [Pololu DRV8825](https://www.pololu.com/product/2133) stepper driver board. 

The host suite is built on Python this allows that the [**SMC_core**](/tools/smc_core/) (the part the mediates between the user and the Arduino driver via serial port) could be deployed as a standalone component that could be easily integrated in any Python-based project. Additionally the GUI is built on top of PySide2 and can be easily customized for every projects needs!

The [driver](/driver/) for the Arduino is written in C++ and was developed using and Arduino-Uno board. 


## Index

