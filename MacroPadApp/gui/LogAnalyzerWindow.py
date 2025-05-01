# log_analyzer_window.py
import tkinter as tk
from tkinter import messagebox
import os
import subprocess
from logic.Logger import Logger

'''
Handles the logic and viewing of the log analyzer window and functionality
'''
class LogAnalyzerWindow:

    '''
    Default constructor for the LogAnalyzerWindow class

    Parameters:
        self:
            instance of object
        master:
            Tkinter parent class
    '''
    def __init__(self, master):
        self.master = master # set instance of parent class
        self.top_level = tk.Toplevel(self.master) # child window floating above main window
        self.top_level.title("Log Analyzer") # title of the popup window
        self.top_level.geometry("300x200") # size of the popup window
        self.createWidgets() # helper method to build buttons and textboxes

    '''
    Helper method to create text boxes and buttons in window

    Parameters:
        self:
            instance of object
    '''
    def createWidgets(self):
        tk.Label(self.top_level, text="Log Type:").pack() # text label for log type
        self.log_type_entry = tk.Entry(self.top_level) # textbox where user can type
        self.log_type_entry.pack() # stick it into the window

        tk.Label(self.top_level, text="Date Start (YYYY-MM-DD):").pack() # text label for the start date
        self.date_filter_entry = tk.Entry(self.top_level) # textbox where user can type
        self.date_filter_entry.pack() # stick it into the window

        tk.Label(self.top_level, text="Keyword:").pack() # text label for keyword
        self.keyword = tk.Entry(self.top_level) # textbox where user can type
        self.keyword.pack() # stick it into the window

        analyze_button = tk.Button(self.top_level, text="Analyze", command=self.runRustAnalysis) # add button that when pressed runs the rust log analysis
        analyze_button.pack(pady=10) # add to window and add padding

    '''
    Runs the rustc program executable

    Parameters:
        self:
            instance of object
    '''
    def runRustAnalysis(self):
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        exe_path = os.path.join(project_root, "log_analyzer.exe") # creates full path to executable file of the log analyzer
        if not os.path.isfile(exe_path): # if the executable is not found
            Logger.error(f"Executable not found: {exe_path}") # log the error
            messagebox.showerror("Executable Not Found", f"Could not find:\n{exe_path}\n\nMake sure the file exists.") # tell the user
            return # return early

        log_type = self.log_type_entry.get() # gets the value the user typed into the log type text field
        date_filter = self.date_filter_entry.get() # gets the value the user typed into the date entry start text field
        keyword = self.keyword.get() # gets the value the user typed into the keyword text field

        cmd = [exe_path] # list with executable fiel path is the first element, will contain full command line argument to run
        if log_type: # if there is a log type entered
            cmd.extend(["--type", log_type]) # add it to the cmd argument
        if date_filter: # if there is a start date entered
            cmd.extend(["--date", date_filter]) # add it to the cmd argument
        if keyword: # if there is a key word that was entered
            cmd.extend(["--keyword", keyword]) # add it to the cmd argument

        try: # handle errors with grace
            subprocess.run(cmd, check=True) # try to run executable file passing the cmd argument line
            Logger.info(f"Log analysis ran with: {' '.join(cmd)}") # log that the process was successfully executed
        except subprocess.CalledProcessError as e: # gracefully handle errors as to not crash program
            Logger.error(f"Log analysis failed: {e}") # log that the processes was unsuccessful
            messagebox.showerror("Analysis Failed", f"Log analysis failed to run.\nError: {e}") # tell the user of the failed execution
