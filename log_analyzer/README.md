# Rust Log Analyzer
A simple Rust-based CLI tool that parses and filters input logs from the MacroPad.

## Overview
This tool reads log files generated during MacroPad usage, applies various filters, and outputs a clean analysis of the key usage, timing, or error detection (depending on input) through a multithreaded program.

## Features
- Parses raw log files
- Filters based on key events, timing, or user-defined flags
- Fast execution with low memory usage

## Instructions for downloading .rs file directly
* Download the .rs file
* Open powershell
  * Enter: "cd FULL\\FILE\\LOCATION\\DIRECTORY"
  * Enter: Cargo build --release
* Move the created .exe into the "MacroPad" folder
