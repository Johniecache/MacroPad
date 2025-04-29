# settings.py
import os

'''
Contains the settings (hard coded or global) variables that multiple files will use
'''
class Settings:
    CONFIG_FILE = 'macros.json'  # .json to hold saved macros
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # get the directory of the current script
    LOG_FILE = os.path.join(SCRIPT_DIR, 'MacroPad.log')  # log file path inside the GUI folder

    '''
    Getter for the config file
    '''
    @staticmethod
    def getConfigFile():
        return os.path.join(Settings.SCRIPT_DIR, Settings.CONFIG_FILE) # returns the config file location

    '''
    Getter for the log file
    '''
    @staticmethod
    def getLogFile():
        return Settings.LOG_FILE # returns the log file location