import tkinter as tk
from tkinter import simpledialog
from logic.Logger import Logger
from gui.InfoWindow import InfoWindow
from gui.LogAnalyzerWindow import LogAnalyzerWindow

'''
Controlls the UI functionality and handles the updating of the GUI
'''
class UIController:
    '''
    Default constructor for UIController

    Parameters:
        self:
            instance of object
        master:
            Tkinter parent
        serial_manager:
            instance of serial manager
        macro_manager:
            instance of macro manager
        auto_start_manager:
            instance of auto start manager
        connection_manager:
            instance of connection manager
    '''
    def __init__(self, master, serial_manager, macro_manager, auto_start_manager, connection_manager):
        self.master = master # Tkinter master window passed in
        self.serial_manager = serial_manager # initialize SerialManager
        self.macro_manager = macro_manager # initialize MacroManager
        self.auto_start_manager = auto_start_manager # initialize AutoStartManager
        self.connection_manager = connection_manager # initialize ConnectionManager

        self.buttons = {} # dictionary to store buttons
        self.button_states = {f"Button {i} pressed": "Disabled" for i in range(1, 10)} # track each button's state
        self.status_label = tk.Label(self.master, text="Connecting.") # label to show status
        self.status_label.grid(row=0, column=0, columnspan=3) # place status label on the window grid

    '''
    Creates, handles and manages widgets on the screen

    Parameters:
        self:
            instance of object
    '''
    def createWidgets(self):
        keypad_order = [
            [7, 8, 9], # top row
            [4, 5, 6], # middle row
            [1, 2, 3] # bottom row
        ]

        for i in range(3):
            for j in range(3): # loop through 2d array
                idx = keypad_order[i][j] # get number from keypad order at i j position
                btn_name = f'Button {idx} pressed' # unique name for the button
                button = tk.Button(
                    self.master, # Tkinter parent passed
                    text=f'Button {idx}', # set button text
                    width=10, # width of the button
                    height=5, # height of the button
                    command=lambda b=btn_name: self.editAction(b), # when pressed, edit action for button
                    state='disabled' # initially disabled until connected
                )
                button.grid(row=i + 1, column=j, padx=5, pady=5) # place button on the grid
                self.buttons[btn_name] = button # store the button in the dictionary
                self.button_states[btn_name] = 'Disabled' # set initial button state

        self.quit_button = tk.Button(self.master, text="Quit", width=10, command=self.quitApplication) # quit button
        self.quit_button.grid(row=4, column=0, padx=5, pady=10) # position on grid

        self.info_button = tk.Button(self.master, text="Info", width=10, command=self.openInfoWindow) # info button
        self.info_button.grid(row=4, column=1, padx=5, pady=10) # position on grid

        self.analyze_log_button = tk.Button(self.master, text="Analyze Log", width=10, command=self.openAnalyzerWindow) # analyze log button
        self.analyze_log_button.grid(row=4, column=2, padx=5, pady=10) # position on grid

        self.hide_button = tk.Button(self.master, text="Hide", width=10, command=self.master.hideWindow) # hide button
        self.hide_button.grid(row=5, column=0, padx=5, pady=5) # position on grid


    '''
    Updates status of the GUI based on passed message.

    Parameters:
        self:
            instance of object
        message:
            status of the device
    '''
    def updateStatus(self, message):
        self.master.after(0, lambda: self.status_label.config(text=message)) # sets the status label as the passed status message

    '''
    Toggles the editablility of the main buttons.

    Parameters:
        self:
            instance of object
        toggled:
            True/False of whether buttons can be edited or not
    '''
    def toggleButtons(self, toggled):
        state = 'normal' if toggled else 'disabled' # set button state to 'normal' or 'disabled'
        status = "Connected" if toggled else "Disconnected" # set the status message accordingly
        for btn_name, button in self.buttons.items(): # loop through each button
            button.config(state=state) # update button state
            self.button_states[btn_name] = status # update button state in the dictionary

    '''
    Edits the action of the passed button name.

    Parameters:
        self:
            instance of object
        button_name:
            Unique name of the button
    '''
    def editAction(self, button_name):
        current_action = self.macro_manager.getAction(button_name) # get the current action for the button
        if not current_action: # checks if there is a current action assign to that key
            current_action = "EMPTY" # if no action is assigned, set it as "EMPTY"
        new_command = simpledialog.askstring(
            "Edit Command", # title of the dialog window
            f"Enter new command for {button_name}:", # instruction for the user
            initialvalue=current_action # set the initial value of the text box to the current action
        )
        if new_command is not None: # check if the user entered a new command
            action_to_save = "" if new_command == "EMPTY" else new_command # if "EMPTY", reset the action
            self.macro_manager.setActions(button_name, action_to_save) # save the new action to the manager

            button_number = int(button_name.split()[1]) # extract button number from the name
            if self.serial_manager.isConnected(): # check if the device is connected
                command_to_send = f"SET{button_number}{action_to_save}\n" # prepare the command to send
                self.serial_manager.write(command_to_send.encode('utf-8')) # send the command via serial

    '''
    Quits out the application safely.

    Parameters:
        self:
            instance of object
    '''
    def quitApplication(self):
        Logger.info("Quit button pressed. Closing application.") # log quit action
        if self.serial_manager.isConnected(): # checks to see if there is a serial connection
            self.serial_manager.close() # close the serial connection if so
        self.master.destroy() # destroy the main window (exit the application)

    '''
    Handles the opening of the info window.

    Parameters:
        self:
            instance of object
    '''
    def openInfoWindow(self):
        if not hasattr(self, 'info_window') or not self.info_window.top_level.winfo_exists(): # if the window is not open or not at the top of the window
            self.info_window = InfoWindow(self.master,self.auto_start_manager.setAutostart,self.auto_start_manager.isAutostartEnabled,self.getButtonStatus) # create info window

    '''
    Handles the opening of the analyzer window.

    Parameter:
        self:
            instance of object
    '''
    def openAnalyzerWindow(self):
        if not hasattr(self, 'log_analyzer_window') or not self.log_analyzer_window: # if the log analyzer window is not open or doesnt exist
            self.log_analyzer_window = LogAnalyzerWindow(self.master) # create new window
        else: # if it does exist
            self.log_analyzer_window.top_level.lift() # bring the window to the font of the screen

    '''
    Gets the button status.

    Parameters:
        self:
            instance of object
    '''
    def getButtonStatus(self):
        return self.button_states # return the current button states
