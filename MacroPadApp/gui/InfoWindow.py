import tkinter as tk
from logic.Logger import Logger
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
        if self.top_level and self.top_level.winfo_exists(): # check if the window already exists
            self.top_level.lift() # set window on top of all other windows
            return # return early

        try:
            self.top_level = tk.Toplevel(self.master) # creates new window that is child of the main window
            self.top_level.title("MacroPad Info") # title of the new window
            self.top_level.geometry("500x525") # size of the new window
            self.centerWindow() # call center window function to center the window when created and displayed
            self.createWidgets() # call create widgets to put them onto the new window
        except Exception as e:
            print(f"Error creating window: {e}") # log error
            self.top_level = None # ensure self.top_level is None on failure

    '''
    Finds and then sets the created window to the center of the users screen.

    Parameters:
        self:
            instance of object
    '''
    def centerWindow(self):
        try:
            x_offset = self.master.winfo_x() + self.master.winfo_width() + 10 # set the x offset
            y_offset = self.master.winfo_y() # set the y offset
            self.top_level.geometry(f"+{x_offset}+{y_offset}") # set the window from the set x/y position
        except tk.TclError:
            Logger.error("Could not center window from given x/y offsets") # log error
            self.top_level.geometry(f"+100+100")  # use default position.

    '''
    Creates and handles the text fields, labels, checkboxes, etc

    Parameters:
        self:
            instance of object
    '''
    def createWidgets(self):
        try:
            info_label = tk.Label(self.top_level, text="MacroPad Info\n\nEnsure to connect your device...\n\n") # create new label with the macro pad and the attempt to connect
            info_label.pack(padx=20, pady=20) # add to window 
            self.autostart_var = tk.BooleanVar() # a check for toggled auto start
            try:
                self.autostart_var.set(self.check_autostart()) # try to create the widgets
            except Exception as e:
                Logger.error("Could not set auto start")
                self.autostart_var.set(False)  # Or some other default value
                tk.messagebox.showwarning("Warning", "Could not determine autostart status.") # show the warning to user

            autostart_toggle = tk.Checkbutton(self.top_level,text="Auto Start on Startup",variable=self.autostart_var,command=self.toggleAutostart) # create checkbox for toggling autostart
            autostart_toggle.pack(padx=20, pady=10) # add checkbox to window

            button_status_label = tk.Label(self.top_level, text="Button Connection Status") # create label for button status section
            button_status_label.pack(padx=20, pady=(10, 2), anchor="w") # add label to window with padding

            self.button_status_dict = {} # dict to map button names to label widgets
            for i in range(1, 10): # loop through buttons 1 to 9
                label_text = f"Button {i}: (Checking...)" # default label text while checking status
                label = tk.Label(self.top_level, text=label_text, anchor="w") # create label for each button
                label.pack(padx=20, pady=2, fill="x") # add label to window
                self.button_status_dict[f"Button {i} pressed"] = label # map status key to label widget

            if self.button_status: # if a button status function is provided
                self.updateButtonStatus() # call it to update status in real-time
        except Exception as e:
            Logger.error(f"Error creating widgets {e}") # log error if widget creation fails
            self.top_level = None # ensure toplevel is None

    '''
    Handles the status of buttons and updates them accordingly

    Parameters:
        self:
            instance of object
    '''
    def updateButtonStatus(self):
        try:
            status = self.button_status() # get the current status of the button
            if status:
                for name, state in status.items(): # iterate through all button names and their states
                    if name in self.button_status_dict: # check if label for button exists
                        self.button_status_dict[name].config(
                            text=f"{name.replace(' pressed', '')}: ({state})" # update label text with current state
                        )
        except Exception as e:
            Logger.error(f"Error updating button status: {e}") # log error if update fails

        if self.top_level and self.top_level.winfo_exists(): # check if the window still exists.
            self.top_level.after(1000, self.updateButtonStatus) # if so then update the buttons status again after 1s


    '''
    Toggles whether or not the auto start is set.
    
    Parameters:
        self:
            instance of object
    '''
    def toggleAutostart(self):
        try:
            self.toggle_autostart(self.autostart_var.get()) # try to set autostart based on checkbox
        except Exception as e:
            Logger.error(f"Error toggling autostart: {e}") # log error if toggle fails
            tk.messagebox.showerror("Error", "Failed to toggle autostart.") # show error popup to user
            self.autostart_var.set(not self.autostart_var.get()) # revert the checkbox