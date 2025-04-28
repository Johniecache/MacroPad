# MacroPad
### Overview
I've created my own hand-wired macro pad. It's a simple 3x3 keypad that has its own firmware i've created in C++. Along with that i've made a Python GUI that will display a 3x3 button matrix (see below) that allows the user to edit the macro of the corresponding button. There is also a Rustc executable that will analyze the .log file associated with the marco pad in a multithreaded analysis.
#### Features
* Hand-wired mechanical 3x3 keypad soldered together
* 3D printed custom case
* Custom C++ firmware compatible with ATmega32U4 microcontroller
* Python GUI for dynamically editing each key's macro/command execution
* Rust CLI for multithreaded log analysis

#### Architecture Diagram

#### How to Run
1. Flash firmware to ATmega32U4 Pro Micro
2. Run 'python3 MacroPadGUI.py' to edit key mappings
