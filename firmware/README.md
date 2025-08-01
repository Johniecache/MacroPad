# Firmware
C++ firmware for the 3x3 MacroPad, built for the ATmega32U4 (Pro Micro).

## Overview
This firmware reads 9 directly-wired mechanical switches connected to digital pins, debounces the input, and sends key events over USB using HID or serial output.

## Features
- Polls 9 individual GPIO pins
- Basic debouncing logic
- Configurable keymap support via serial input
- HID keypress transmission to host PC

## Instructions (Build & Flash)
1. Open the firmware project in the Arduino IDE
2. Select the board: ATmega32U4 (Arduino Leonardo)
3. Connect the Pro Micro via USB
4. Check the COM#, this may cause issue when the MacroPadApp tries to connect to device
5. Flash the firmware

## Dependencies
- Arduino HID library
