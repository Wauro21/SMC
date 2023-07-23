# Stepper-Motor-Controller

<p align="center">
  <img src="rsrcs/icon.png" />
</p>


**Stepper-Motor-Controller (SMC)** is a project that provides a user-friendly driver and graphical user interface (GUI) for control of a stepper motor using and Arduino-based board in conjuction with the [Pololu DRV8825](https://www.pololu.com/product/2133) stepper driver board. 

The host suite is built on Python this allows that the [**SMCC or SMC-Core**](https://github.com/Wauro21/SMCC) (the part the mediates between the user and the Arduino driver via serial port) could be deployed as a standalone component that could be easily integrated in any Python-based project. Additionally the GUI is built on top of PySide2 and can be easily customized for every projects needs!

The [**SMCD or SMC-Driver**](https://github.com/Wauro21/SMCD) for the Arduino is written in C++ and was developed using and Arduino-Uno board. 


## Index

- [Stepper-Motor-Controller](#stepper-motor-controller)
  - [Index](#index)
  - [Hardware Setup:](#hardware-setup)
  - [Installation:](#installation)
    - [From sources](#from-sources)
    - [From releases - Only Windows](#from-releases---only-windows)


## Hardware Setup:

Information about how to connect the Arduino and Pololu boards and how to burn the driver to the Arduino can be found on the driver repository: [SMCD](https://github.com/Wauro21/SMCD)!


## Installation: 

### From sources

For this kind of installation you just need to clone the repository and using `pipenv` install the necessary dependencies as follows:

```bash
$ pipenv install
```

Then you just run the following command to start the GUI:

```
$ pipenv shell
$ python SMC.py
```

<p align=center>
  <img src='./github_images/example_source_install.gif'>
</p>


### From releases - Only Windows

For Windows there is a `.exe` release packaged with PyInstaller. To install just download the latest release `SMC_release_exe.zip` and unzip it. Inside the extracted folder there is the `exe` file:

<p align=center>
  <img src='./github_images/example_windows_install.gif'>
</p>