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
from gui.SystemTrayIcon import SystemTrayIcon

'''
Controls the main functionalitu of the Macro Pad GUI
'''
class MacroPadApp:

    '''
    Default contructor for MacroPadApp

    Parameters:
        self:
            intance of object
        master:
            Tkinter parent
    '''
    def __init__(self, master):
        self.master = master  # main Tkinter window
        self.stop_event = threading.Event()  # event to signal background threads to stop
        self.serial_manager = SerialManager()  # initialize the serial manager
        self.macro_manager = MacroManager()  # initialize the macro manager
        self.auto_start_manager = AutoStartManager()  # initialize the auto-start manager
        self.logger = Logger() # initialize the logger
        self.connection_manager = ConnectionManager(self.serial_manager,self.macro_manager,self.updateStatus,self.toggleButtons,self.runAction) # initialize ConnectionManager
        self.ui_controller = UIController(master,self.serial_manager,self.macro_manager,self.auto_start_manager,self.connection_manager) # initialize UIController
        self.ui_controller.master.hideWindow = self.hideWindow # pass method from uicontroller of hideWindow
        self.tray_icon = SystemTrayIcon(self.restoreWindow, self.ui_controller.quitApplication) # initialize SystemTrayIcon
        self.tray_icon.setupIcon() # setup the icon for the systems tray

        self.ui_controller.createWidgets() # create widgets for the GUI

        threading.Thread(target=self.connection_manager.connectionManager, daemon=True).start() # start the connection manager in the background thread

        self.master.after(10, lambda: threading.Thread(target=self.animateStatus, daemon=True).start()) # animate the status after a short delay

    '''
    Handles the hidding of the gui.

    Parameters:
        self:
            instance of object
    '''
    def hideWindow(self):
        self.master.withdraw()  # hide the main window
        threading.Thread(target=self.tray_icon.run, daemon=True).start()  # show tray icon

    '''
    Handles the restoration of the gui after hiding.

    Parameters:
        self:
            instance of object
    '''
    def restoreWindow(self):
        self.master.deiconify()  # show the main window
        self.tray_icon.setVisible(False)  # hide the tray icon

    '''
    Animates the trailing dots in connecting.

    Parameters:
        self:
            intance of object
    '''
    def animateStatus(self):
        dots = 0 # default to 0 dots
        while True: # activate while unbroken
            if not self.serial_manager.isConnected(): # if not already connected
                text = "Connecting" + "." * (dots + 1)  # update status with dots
                self.ui_controller.updateStatus(text)  # pass the new status to the UIController
                dots = (dots + 1) % 3  # cycle through 1, 2, 3 dots
            time.sleep(0.5)  # pause for half a second before updating again

    '''
    Updates the status of the device connection to controller.

    Parameters:
        self:
            instance of object
        message:
            status of device connection
    '''
    def updateStatus(self, message):
        self.ui_controller.updateStatus(message) # update the connection status via the UIController

    '''
    Toggles the editablility of the main buttons.

    Parameters:
        self:
            instance of object
        toggled:
            True/False of whether buttons can be edited or not
    '''
    def toggleButtons(self, toggled):
        self.ui_controller.toggleButtons(toggled) # toggle button states based on the connection status

    '''
    Run the passed system command

    Parameters:
        self:
            instance of object
        command:
            the system command to be run
    '''
    def runAction(self, command):
        try: # handle errors with grace
            subprocess.Popen(command, shell=True)  # execute the command
            Logger.info(f"Running command: {command}")  # log the action
        except Exception as e: # gracefully handle errors as to not crash program
            Logger.error(f"Failed to run command {command}: {e}")  # log error if the command fails



if __name__ == "__main__":
    root = tk.Tk()  # create the main Tkinter window
    app = MacroPadApp(root)  # initialize the MacroPadApp with the root window
    root.mainloop()  # start the Tkinter event loop to keep the window open
