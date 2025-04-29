import tkinter as tk
from logic.AutoStartManager import AutoStartManager

'''
Creates and manages a popup information window for the device
'''
class InfoWindow:

    '''
        Default constructor for the InfoWindow class

        Parameters:
            self:
                instance of object
            master: 
                Parent class of the Tkinter import
            toggle_autostart: 
                Toggles the auto start variable
            check_autostart: 
                Checks whether or not the auto start is enabled
            button_status:
                Returns the status of the button (enabled, disabled, connected, disconnected). Defaults to None.
    '''
    def __init__(self, master, toggle_autostart, check_autostart, button_status=None):
        self.master = master # Tkinter as parent class
        self.top_level = tk.Toplevel(self.master) # creates new window that is child of the main window
        self.top_level.title("MacroPad Info") # title of the new window
        self.top_level.geometry("500x525") # size of the new window
        self.centerWindow() # call center window function to center the window when created and displayed
        self.toggle_autostart = toggle_autostart # create the toggle autostart widget
        self.check_autostart = check_autostart # create the check autostart widget
        self.button_status = button_status # create the button status widget
        self.createWidgets() # call create widgets to but them onto the new window

    '''
    Hanles the creation of the window and makes sure it doesn't already exist before creating a new one.

    Parameters:
        self:
            instance of object
    '''
    def createWindow(self):
        if self.top_level is not None and self.top_level.winfo_exists():  # check if window exists
            self.top_level.lift()  # bring the existing window to the front if it exists
            return  # exit if the window is already open

    '''
    Finds and then sets the created window to the center of the users screen.

    Parameters:
        self:
            instance of object
    '''
    def centerWindow(self):
        x_offset = self.master.winfo_x() + self.master.winfo_width() + 10 # gets the main window x cord and width then adds 10 (slight spacing between two windows)
        y_offset = self.master.winfo_y() # sets same y cord from main window
        self.top_level.geometry(f"+{x_offset}+{y_offset}") # sets these offsets to the info window

    '''
    Creates and handles the text fields, labels, checkboxes, etc

    Parameters:
        self:
            instance of object
    '''
    def createWidgets(self):
        info_label = tk.Label(self.top_level, text="MacroPad Info\n\nEnsure to connect your device...\n\n") # creates new label
        info_label.pack(padx=20, pady=20) # padding for the new label and add it to window

        self.autostart_var = tk.BooleanVar() # new parent variable
        self.autostart_var.set(self.check_autostart()) # checks the autostart and then sets the boolean variable to that value

        autostart_toggle = tk.Checkbutton( # creates new check box for autostart
            self.top_level, # put it above other labels (incase of overlap)
            text="Auto Start on Startup", # text next to the box so user knows what its for
            variable=self.autostart_var, # binds checkbox to the boolean variable
            command=self.toggleAutostart # checkbox toggle the auto start when clicked
        )
        autostart_toggle.pack(padx=20, pady=10) # adds padding and new checkbox + label to the window

        button_status_label = tk.Label(self.top_level, text="Button Connection Status") # new label to show the buttons status (subtitle)
        button_status_label.pack(padx=20, pady=(10, 2), anchor="w") # adds to window and then padding

        self.button_status_dict = {} # create a dictionary of button status's
        for i in range(1, 10): # loop through all the buttons 
            label_text = f"Button {i}: (Checking...)" # tell user that each button at i position is being checked
            label = tk.Label(self.top_level, text=label_text, anchor="w") # new label that will hold the label text
            label.pack(padx=20, pady=2, fill="x") # add to window and add padding
            self.button_status_dict[f"Button {i} pressed"] = label # add button pressed to the dictionary

        if self.button_status: # if the button status fucntion exists
            self.updateButtonStatus() # call updateButtonStatus to updat the button state

    '''
    Handles the status of buttons and updates them accordingly

    Parameters:
        self:
            instance of object
    '''
    def updateButtonStatus(self):
        status = self.button_status() # get the current status of the button
        if status: # if the status exists
            for name, state in status.items(): # go through each item in the status dictionary
                if name in self.button_status_dict: # check if the button name exists in the button status dictionary
                    self.button_status_dict[name].config( # update the label for the specific button
                        text=f"{name.replace(' pressed', '')}: ({state})" # replace the text with the new state
                    )
        self.top_level.after(1000, self.updateButtonStatus) # give 1 second before checking again

    '''
    Toggles whether or not the auto start is set.
    
    Parameters:
        self:
            instance of object
    '''
    def toggleAutostart(self):
        self.toggle_autostart(self.autostart_var.get()) # toggles the autostart setting when checkbox is clicked