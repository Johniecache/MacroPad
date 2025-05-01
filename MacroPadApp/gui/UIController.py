import tkinter as tk
from tkinter import simpledialog
from logic.Logger import Logger
from gui.InfoWindow import InfoWindow
from gui.LogAnalyzerWindow import LogAnalyzerWindow


class UIController:
    def __init__(self, master, serial_manager, macro_manager, auto_start_manager, connection_manager):
        self.master = master  # Tkinter master window passed in
        self.serial_manager = serial_manager  # Manages serial connection
        self.macro_manager = macro_manager  # Manages macros
        self.auto_start_manager = auto_start_manager  # Handles autostart
        self.connection_manager = connection_manager  # Manages the connection process

        self.buttons = {}  # Dictionary to store buttons
        self.button_states = {f"Button {i} pressed": "Disabled" for i in range(1, 10)}  # Track each button's state
        self.status_label = tk.Label(self.master, text="Connecting.")  # Label to show status
        self.status_label.grid(row=0, column=0, columnspan=3)  # Place status label on the window grid

    def createWidgets(self):
        keypad_order = [
            [7, 8, 9],  # Top row
            [4, 5, 6],  # Middle row
            [1, 2, 3]   # Bottom row
        ]

        # Create buttons for each keypad number (3x3 grid)
        for i in range(3):
            for j in range(3):
                idx = keypad_order[i][j]  # Get number from keypad order at i j position
                btn_name = f'Button {idx} pressed'  # Unique name for the button
                button = tk.Button(
                    self.master,  # Tkinter parent passed
                    text=f'Button {idx}',  # Set button text
                    width=10,  # Width of the button
                    height=5,  # Height of the button
                    command=lambda b=btn_name: self.editAction(b),  # When pressed, edit action for button
                    state='disabled'  # Initially disabled until connected
                )
                button.grid(row=i + 1, column=j, padx=5, pady=5)  # Place button on the grid
                self.buttons[btn_name] = button  # Store the button in the dictionary
                self.button_states[btn_name] = 'Disabled'  # Set initial button state

        # Quit button
        self.quit_button = tk.Button(self.master, text="Quit", width=10, command=self.quitApplication)
        self.quit_button.grid(row=4, column=0, padx=5, pady=10)  # Position on grid

        # Info button
        self.info_button = tk.Button(self.master, text="Info", width=10, command=self.openInfoWindow)
        self.info_button.grid(row=4, column=1, padx=5, pady=10)

        # Analyze Log button
        self.analyze_log_button = tk.Button(self.master, text="Analyze Log", width=10, command=self.openAnalyzerWindow)
        self.analyze_log_button.grid(row=4, column=2, padx=5, pady=10)

    def updateStatus(self, message):
        # Update the status label text
        self.master.after(0, lambda: self.status_label.config(text=message))

    def toggleButtons(self, enable):
        # Enable or disable buttons based on the connection status
        state = 'normal' if enable else 'disabled'  # Set button state to 'normal' or 'disabled'
        status = "Connected" if enable else "Disconnected"  # Set the status message accordingly
        for btn_name, button in self.buttons.items():  # Loop through each button
            button.config(state=state)  # Update button state
            self.button_states[btn_name] = status  # Update button state in the dictionary

    def editAction(self, button_name):
        # Edit the action associated with the button (macro editing)
        current_action = self.macro_manager.getAction(button_name)  # Get the current action for the button
        if not current_action:
            current_action = "EMPTY"  # If no action is assigned, set it as "EMPTY"
        new_command = simpledialog.askstring(
            "Edit Command",  # Title of the dialog window
            f"Enter new command for {button_name}:",  # Instruction for the user
            initialvalue=current_action  # Set the initial value of the text box to the current action
        )
        if new_command is not None:  # Check if the user entered a new command
            action_to_save = "" if new_command == "EMPTY" else new_command  # If "EMPTY", reset the action
            self.macro_manager.setAction(button_name, action_to_save)  # Save the new action to the manager

            # Format the command for serial communication
            button_number = int(button_name.split()[1])  # Extract button number from the name
            if self.serial_manager.isConnected():  # Check if the device is connected
                command_to_send = f"SET{button_number}{action_to_save}\n"  # Prepare the command to send
                self.serial_manager.write(command_to_send.encode('utf-8'))  # Send the command via serial

    def quitApplication(self):
        # Handle the quit application process
        Logger.info("Quit button pressed. Closing application.")  # Log quit action
        if self.serial_manager.isConnected():
            self.serial_manager.close()  # Close the serial connection if open
        self.master.destroy()  # Destroy the main window (exit the application)

    def openInfoWindow(self):
        # Open the info window or bring it to the front if already open
        if not hasattr(self, 'info_window') or not self.info_window.top_level.winfo_exists():
            self.info_window = InfoWindow(
                self.master,
                self.auto_start_manager.setAutostart,
                self.auto_start_manager.isAutostartEnabled,
                self.getButtonStatus
            )

    def openAnalyzerWindow(self):
        # Open the log analyzer window or bring it to the front if already open
        if not hasattr(self, 'log_analyzer_window') or not self.log_analyzer_window:
            self.log_analyzer_window = LogAnalyzerWindow(self.master)
        else:
            self.log_analyzer_window.top_level.lift()

    def getButtonStatus(self):
        # Return the current button states
        return self.button_states
