import os

'''
Contains the settings (hard coded or global) variables that multiple files will use
'''
class Settings:
    CONFIG_FILE = 'macros.json'  # .json to hold saved macros
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # get the directory of the current script
    RESOURCES_DIR = os.path.join(SCRIPT_DIR, '..', 'resources')  # path to the resources folder
    LOG_FILE = os.path.join(SCRIPT_DIR, 'MacroPad.log')  # log file path inside the GUI folder

    if not os.path.exists(RESOURCES_DIR): # ensure that the path to the resources folder exists
        os.makedirs(RESOURCES_DIR) # make the directory to the resources folder

    '''
    Getter for the config file
    '''
    @staticmethod
    def getConfigFile():
        return os.path.join(Settings.RESOURCES_DIR, Settings.CONFIG_FILE)  # Return the path inside the resources folder

    '''
    Getter for the log file
    '''
    @staticmethod
    def getLogFile():
        return Settings.LOG_FILE  # returns the log file location
