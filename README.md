# MacroPad
## Overview
I've created my own hand-wired macro pad. It's a simple 3x3 keypad that has its own firmware i've created in C++. Along with that i've made a Python GUI that will display a 3x3 button matrix (see below) that allows the user to edit the macro of the corresponding button. There is also a Rustc executable that will analyze the .log file associated with the marco pad in a multithreaded analysis.
## Features
* Hand-wired mechanical 3x3 keypad soldered together
* 3D printed custom case
* Custom C++ firmware compatible with ATmega32U4 microcontroller
* Python GUI for dynamically editing each key's macro/command execution
* Rust CLI for multithreaded log analysis

## Components
| Item | Description | Link |
|------|-------------|------|
| ATmega32U4 | Microcontroller | [Amazon](https://www.amazon.com/dp/B0B6HYLC44?ref_=ppx_hzsearch_conn_dt_b_fed_asin_title_1) |
| Outemu Switches | Standard 2-pin Keyboard Switches | [Amazon](https://www.amazon.com/dp/B073WC1NXL?ref_=ppx_hzsearch_conn_dt_b_fed_asin_title_3&th=1) |
Full Bill of Materials in /BOM.md

## Architecture Diagram
![architecture_diagram](https://github.com/user-attachments/assets/a1dcac8c-d3f3-4a46-a603-4205250ca172)

## Instructions (download):
1. Download the .zip file
2. Extract the file anywhere
3. Place one of if not both shortcuts on desktop if wanted
4. Open firmware file in Arduino IDE
5. Flash firmware to ATmega32U4
6. Run the Applicaiton

## License
MIT

## Author
Caleb Thomas - 2025
