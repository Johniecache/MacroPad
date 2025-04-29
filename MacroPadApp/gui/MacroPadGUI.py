import tkinter as tk
from tkinter import simpledialog, Menu
import threading
import subprocess
import time
import os


script_dir = os.path.dirname(os.path.abspath(__file__)) # get the absolute path fo the script directory
project_root = os.path.abspath(os.path.join(script_dir, "..")) # get the aboslute path of the project root
logic_folder = os.path.join(project_root, "logic") # get the logic directory

from logic.SerialManager import SerialManager
from logic.MacroManager import MacroManager
from logic.AutoStartManager import AutoStartManager
from logic.Logger import Logger
from gui.InfoWindow import InfoWindow
from gui.LogAnalyzerWindow import LogAnalyzerWindow

'''
Main class that handles the connection process and actions
'''
class MacroPadApp:
    '''
    Initializes GUI and background processes.

    Parameters:
        self: 
            instance of MacroPadApp class
        master:
            parent Tkinter widget
    '''
    def __init__(self, master):
        self.master = master # instance parent as passed parent
        self.stop_event = threading.Event() # initialize flag to signal to stop threads
        self.serial_connection = None # initialize serial connection
        #self.is_connected = False # initialize connection status
        #self.connection_thread = None # initialize connection management thread
        master.title("MacroPad Configurator") # set the title of the window

        window_width = 270 # set the width of the window
        window_height = 350 # set the height of the window
        screen_width = master.winfo_screenwidth() # get users screen width
        screen_height = master.winfo_screenheight() # get users screen height
        x_coordinate = int((screen_width / 2) - (window_width / 2)) # get x cord by finding center of screen (width)
        y_coordinate = int((screen_height / 2) - (window_height / 2)) # get y cord by finding center of screen (height)
        master.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}") # set the window at the found x and y cords
        master.protocol("WM_DELETE_WINDOW", self.onClose) # when (X) is pressed make it close the window

        self.serial_manager = SerialManager() # initialize serial manager
        self.macro_manager = MacroManager() # initialize macro manager
        self.auto_start_manager = AutoStartManager() # initialize auto start manager

        self.listening = False # check for if listner thread is active
        self.buttons = {} # button dictionary by name
        self.button_states = {f"Button {i} pressed": "Disabled" for i in range(1, 10)} # tracks each buttons state

        self.status_label = tk.Label(self.master, text="Connecting.") # create a label inside the window
        self.status_label.grid(row=0, column=0, columnspan=3) # place label at the top and center of the window

        self.createWidgets() # make keypad and control buttons

        self.running = True # make check to see if app is running
        threading.Thread(target=self.connectionManager, daemon=True).start() # background thread to try and auto-connect to hardware

        self.master.after(10, lambda: threading.Thread(target=self.animateStatus, daemon=True).start()) # after delay make another thread to animate connecting with dots 

        self.info_window = None # placeholder for info window
        self.log_analyzer_window = None # placeholder for analyzer window

    '''
    creates buttons to show on the window.

    Parameters:
        self:
            pass instance object to method
    '''
    def createWidgets(self):
        keypad_order = [ # MacroPad layout as standard keypad (w/o 0)
            [7, 8, 9], # top row
            [4, 5, 6], # middle row
            [1, 2, 3] # bottom row
        ]

        for i in range(3):
            for j in range(3): # loop through 2d array to create buttons 
                idx = keypad_order[i][j] # get number from keypad order at i j position
                btn_name = f'Button {idx} pressed' # unique button name per button
                button = tk.Button( # create button widget
                    self.master, # Tkinter parent passed
                    text=f'Button {idx}', # set the text of the button to "Button (at index)"
                    width=10, # width of button
                    height=5, # height of button
                    command=lambda b=btn_name: self.editAction(b), # when pressed allow user to edit macro of button
                    state='disabled' # initially make disabled till connected to device
                )
                button.grid(row=i + 1, column=j, padx=5, pady=5) # places button on window in a grid layout
                self.buttons[btn_name] = button # add button to dictionary with unique identifier button name
                self.button_states[btn_name] = 'Disabled' # track state of button and initialize as 'Disabled'

        self.quit_button = tk.Button( # create quit button
            self.master, # Tkinter parent class passed
            text="Quit", # set text to tell user what the button does
            width=10, # width of button
            command=self.quitApplication # pass to quitApplication method if pressed
        )
        self.quit_button.grid(row=4, column=0, padx=5, pady=10) # set on grid (bottom left)

        self.info_button = tk.Button( # create info button
            self.master, # Tkinter parent class passed
            text="Info", # set text to tell user what the button does
            width=10, # set width of button
            command=self.openInfoWindow # pass to openInfoWindow method if pressed
        )
        self.info_button.grid(row=4, column=1, padx=5, pady=10) # put on grid (bottom middle)

        self.analyze_log_button = tk.Button( # create analyze log button
            self.master, # Tkinter parent class passed
            text="Analyze Log", # set text to tell user what button does
            width=10, # set width of button
            command=self.openAnalyzerWindow # pass to openAnalyzerWindow when pressed
        )
        self.analyze_log_button.grid(row=4, column=2, padx=5, pady=10) # set on grid (bottom right)

    '''
    Attempts to auto-connect to device and retries until connection is successful.

    Parameters:
        self:
            pass instance object
    '''
    def connectionManager(self):
        retry_interval = 2 # increase after failed attempt
        max_interval = 60 # maximum interval retry can reach (1 min)

        while not self.stop_event.is_set(): # runs until stop event is flagged
            if not self.serial_manager.isConnected(): # if not currently connected to device
                Logger.info("Attempting auto-connect...") # log that there is an attempt to auto connect
                if self.serial_manager.autoConnect(): # calls autoConnect and if successful connection...
                    port = self.serial_manager.get_port() # gets the port to what the device is connected to
                    Logger.info(f"Connected to {port}") # log the conneted port
                    self.updateStatus(f"Connected: {port}") # update status to connected to port number
                    self.startSerialListener() # start listening for data from device
                    self.toggleButtons(True) # allow user to edit buttons macros
                    retry_interval = 2 # reset interval to 2 for future
                else: # if failed connection to device
                    Logger.warning(f"Auto-connect failed. Retrying in {retry_interval} seconds...") # log the failed connection
                    self.toggleButtons(False) # ensure user cannot edit buttons
                    self.updateStatus("Disconnected") # update status to disconnected
                    time.sleep(retry_interval) # wait time before retrying 
                    retry_interval = min(retry_interval * 2, max_interval) # double the retry interval and if its lower then max use that otherwise use max
            else: # if device is connected already
                time.sleep(2) # wait 2 seconds before checking again

    '''
    Listens for data sent from device.
    
    Parameters:
        self:
            instance of object
    '''
    def startSerialListener(self):
        if not self.listening and self.serial_manager.isConnected(): # if serial listener isnt running and device is currently connected
            threading.Thread(target=self.serialListener, daemon=True).start() # create new thread that has serialListener running then make sure thread stops when window is closed
            self.listening = True # set listening to true since thread for listening is created

    '''
    Animates the dots after connecting to show as if the program is constantly looking for device.
    
    Parameters:
        self:
            instance of object
    '''
    def animateStatus(self):
        dots = 0 # initially set dots after connecting to none
        while self.running: # while the window is up
            if not self.serial_manager.isConnected(): # if the device is not connected
                text = "Connecting" + "." * (dots + 1) # show Connecting with 1 dot after it then set dots to +1
                self.updateStatus(text) # pass the text to updateStatus
                dots = (dots + 1) % 3 # make sure it wraps back to 0 once 3 is hit
            time.sleep(0.5) # pause the animation for half a second before updating again

    '''
    Sets the windows connection status of the passed message.
    
    Parameters:
        self:
            instance of object
        message:
            message to set to the window
    '''
    def updateStatus(self, message):
        self.master.after(0, lambda: self.status_label.config(text=message)) # set the label of the window to the passed message after 0 seconds (immediately)

    '''
    Sets the editablility of windows buttons
    
    Parameters:
        self:
            instance of object
        enable:
            toggled values to set the buttons status
    '''
    def toggleButtons(self, enable):
        state = 'normal' if enable else 'disabled' # determines buttons state between normal or disabled
        status = "Connected" if enable else "Disconnected" # determains buttons status between connected or disconnected
        for btn_name, button in self.buttons.items(): # loop through all buttons
            button.config(state=state) # update each buttons state with these defined status and state
            self.button_states[btn_name] = status # update status in button dictionary

    '''
    Getter for the buttons status

    Parameters:
        self:
            insatnce of object
    '''
    def getButtonStatus(self):
        return self.button_states # return the buttons state

    '''
    Edits the marcros within each unique button.

    Parameters:
        self:
            instance of object
        button_name:
            unique identifier for the button thats getting updated
    '''
    def editAction(self, button_name):
        current_action = self.macro_manager.getAction(button_name) # holds command for the current macro thats associated with passed button
        if not current_action: # if there is not current action (ie its empty)
            current_action = "EMPTY" # tell user clearly that its empty
        new_command = simpledialog.askstring( # creates a new window for editiing name command
            "Edit Command", # title of the new window
            f"Enter new command for {button_name}:", # tell user what to do and for what button (make it clear)
            initialvalue=current_action # set text box value as current action
        )
        if new_command is not None: # check whether user entered new command or not
            action_to_save = "" if new_command == "EMPTY" else new_command # if command is empty set to "EMPTY" otherwise set to entered command
            self.macro_manager.setAction(button_name, action_to_save) # send to setAction method passing the unique button and the entered macro

            button_number = int(button_name.split()[1]) # extract button number from name by getting the end and setting that as an integer
            if self.serial_manager.isConnected(): # check if device is connected
                command_to_send = f"SET{button_number}{action_to_save}\n" # format macro to set new button over serial
                self.serial_manager.write(command_to_send.encode('utf-8')) # send new command encoded as UTF-8

    '''
    Uses passed command to execute through system.

    Parameters:
        self:
            instance of object
        command:
            string value of the command to be executed
    '''
    def runAction(self, command):
        try: # handle errors with grace (since its user input)
            subprocess.Popen(command, shell=True) # attempt to run command that was passed
            Logger.info(f"Running command: {command}") # log the attempt of running command
        except Exception as e: # gracefully handle errors without crashing program
            Logger.error(f"Failed to run command {command}: {e}") # if there is an error log it with the command trying to be executed and the error

    '''
    Continuously listens for input data from device.

    Parameters:
        self:
            instance of object
    '''
    def serialListener(self):
        while self.running: # while app is running
            line = self.serial_manager.readLine() # reads the line of the sent data and assigns it to a variable
            if line: # if there is data in the liine
                for button_name, command in self.macro_manager.getAllActions().items(): # iterate over all buttons and check all their actions
                    if command == line: # if the command is the same as the line
                        self.runAction(command) # if it matches them run that command
                        Logger.info(f"Executed action for {line} (mapped to {button_name})") # log that command was run
                        break # break out of the loop
                else: # if there is no command
                    Logger.warning(f"No action mapped for {line}") # log warning that command doesnt exist
            time.sleep(0.01) # allow time between checks

    '''
    Gracefully shutdown the application.
    
    Parameters:
        self:
            instance of object
    '''
    def quitApplication(self):
        Logger.info("Quit button pressed. Closing application.") # log that the program is being shutdown
        self.stop_event.set() # set the stop event to true
        if self.serial_connection and self.serial_connection.is_open: # checks if theres a connection and whether it was open
            self.serial_connection.close() # closes connection if it is open
        if self.master and self.master.winfo_exists(): # ensure main window exists before destroying
            self.master.destroy() # destroys main Tkinter window

    '''
    Executes when the window is being closed.

    Parameters:
        self:
            instance of object
    '''
    def onClose(self):
        if self.master and self.master.winfo_exists(): # if the main window exists before destroying it
            self.quitApplication() # pass to method quitApplication
            #self.master.destroy() # destory the main window

    '''
    Handles the opening of info window.

    Parameters:
        self:
            instance of object
    '''
    def openInfoWindow(self):
        if self.info_window is None or not self.info_window.top_level.winfo_exists(): # check if info window already exists
            self.info_window = InfoWindow( # make new window called info and pass it to the class
                self.master, # Tkinter parent passed
                self.toggleAutostart, # enable/disable autostart
                self.checkAutostart, # checks if autostart is true/false
                self.getButtonStatus # gets the button status
            )
        else: # if the window already exists
            if self.info_window.top_level: # check if the info window is on the top level
                self.info_window.top_level.lift() # bring the already created window to the font of the screen (since it might be hidden behind something else)

    '''
    Handles the hiding of program GUI.

    Parameters:
        self:
            instance of object
    '''
    def hideWindow(self):
        self.master.withdraw() # hides the window without closing it

    '''
    Handles the restoring of program GUI.

    Parameters:
        self:
            instance of object
    '''
    def restoreWindow(self):
        self.master.deiconify() # reshow the window if hidden

    '''
    Handles the autostart functionality.

    Parameters:
        self:
            instance of object
        enabled:
            true/false value of if autostart is enabled
    '''
    def toggleAutostart(self, enabled):
        self.auto_start_manager.setAutostart(enabled) # pass whether or not the 

    '''
    checks if autostart is enabled or not. (expand on later)

    Parameters:
        self:
            instance of object
    '''
    def checkAutostart(self):
        return self.auto_start_manager.isAutostartEnabled() # returns the value of whether or not autostart is enabled

    '''
    Handles the opening and some functionality of the Log Analyzer window.

    Parameters:
        self:
            instance of object
    '''
    def openAnalyzerWindow(self):
        if not self.log_analyzer_window: # if there is no log analyzer window already open
            self.log_analyzer_window = LogAnalyzerWindow(self.master) # create one passing it to the class
        else: # if there already is a log analyzer window open
            self.log_analyzer_window.top_level.lift() # move the window to the front of the screen (could be behind other windows)

if __name__ == "__main__": # main run loop
    root = tk.Tk() # Tkinter is the parent
    app = MacroPadApp(root) # pass root as self in application
    root.mainloop() # run loop to show and update window