import tkinter as tk
import threading
import subprocess
import time
from gui.UIController import UIController
from logic.AutoStartManager import AutoStartManager
from logic.ConnectionManager import ConnectionManager
from logic.Logger import Logger
from logic.MacroManager import MacroManager
from logic.SerialManager import SerialManager

class MacroPadApp:
    def __init__(self, master):
        self.master = master  # Main Tkinter window
        self.stop_event = threading.Event()  # Event to signal background threads to stop
        self.serial_manager = SerialManager()  # Initialize the serial manager
        self.macro_manager = MacroManager()  # Initialize the macro manager
        self.auto_start_manager = AutoStartManager()  # Initialize the auto-start manager
        self.logger = Logger() # initialize the logger
        self.connection_manager = ConnectionManager(
            self.serial_manager,
            self.macro_manager,
            self.updateStatus,
            self.toggleButtons,
            self.runAction
        )

        # Initialize UIController with the necessary managers
        self.ui_controller = UIController(
            master,
            self.serial_manager,
            self.macro_manager,
            self.auto_start_manager,
            self.connection_manager
        )

        # Create the widgets for the UI
        self.ui_controller.createWidgets()

        # Start the connection manager in a background thread
        threading.Thread(target=self.connection_manager.connectionManager, daemon=True).start()

        # Animate the status after a short delay
        self.master.after(10, lambda: threading.Thread(target=self.animateStatus, daemon=True).start())

    def animateStatus(self):
        # Animate "Connecting" status with dots
        dots = 0
        while True:
            if not self.serial_manager.isConnected():
                text = "Connecting" + "." * (dots + 1)  # Update status with dots
                self.ui_controller.updateStatus(text)  # Pass the new status to the UIController
                dots = (dots + 1) % 3  # Cycle through 1, 2, 3 dots
            time.sleep(0.5)  # Pause for half a second before updating again

    def updateStatus(self, message):
        # Update the connection status via the UIController
        self.ui_controller.updateStatus(message)

    def toggleButtons(self, enable):
        # Toggle button states based on the connection status
        self.ui_controller.toggleButtons(enable)

    def runAction(self, command):
    # Run the specified system command
        try:
            subprocess.Popen(command, shell=True)  # Execute the command
            print(f"Running command: {command}")  # Debugging line
            Logger.info(f"Running command: {command}")  # Log the action
        except Exception as e:
            Logger.error(f"Failed to run command {command}: {e}")  # Log error if the command fails



if __name__ == "__main__":
    root = tk.Tk()  # Create the main Tkinter window
    app = MacroPadApp(root)  # Initialize the MacroPadApp with the root window
    root.mainloop()  # Start the Tkinter event loop to keep the window open
