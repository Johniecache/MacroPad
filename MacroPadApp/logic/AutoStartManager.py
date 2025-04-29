import winreg
import os
from logic.Logger import Logger

'''
Handles the functionality of auto start if it is toggled on by user.
'''
class AutoStartManager:
    APP_NAME = "MacroPadApp" # global variable of the name of the app

    '''
    Manages the startup behavior of the application.

    Parameters:
        enabled:
            whether auto start is enabled or not
    '''
    @staticmethod
    def setAutostart(enabled):
        key = winreg.HKEY_CURRENT_USER # defines the registry key that contains settings for the currently logged-in user
        path = r"SOFTWARE/Microsoft/Windows/CurrentVersion/Run" # registry path where auto-start entries are stored
        app_path = os.path.abspath(__file__) # absolute path of script
        try: # handle errors with grace
            with winreg.OpenKey(key, path, 0, winreg.KEY_WRITE) as registry_key: # opens the registry key for writing
                if enabled: # checks if auto start is enabled
                    winreg.SetValueEx(registry_key, AutoStartManager.APP_NAME, 0, winreg.REG_SZ, app_path) # set the value in registry to enabled auto start
                    Logger.info("MacroPad set to start on startup.") # log that its been active on auto start
                else: # if auto start isnt enabled
                    winreg.DeleteValue(registry_key, AutoStartManager.APP_NAME) # then delete the vaue if it exists
                    Logger.info("MacroPad removed from startup.") # log that its been removed from auto start
        except FileNotFoundError: # gracefully handle errors so the program doesnt crash
            Logger.warning("Warning: Windows Run key not found. Auto-start setting could not be changed.") # log the warning that the windows key wasnt found
        except Exception as e: # gracefully handle errors so the program doesnt crash
            Logger.error(f"Failed to update startup registry: {e}") # log that there was an error updating startup registry and the error message

    '''
    Checks whether or not the application is set to auto start.
    '''
    @staticmethod
    def isAutostartEnabled():
        key = winreg.HKEY_CURRENT_USER # defines the registry key that contains settings for the currently logged-in user 
        path = r"SOFTWARE/Microsoft/Windows/CurrentVersion/Run" # registry path where auto-start entries are stored
        try: # handle errors with grace
            with winreg.OpenKey(key, path, 0, winreg.KEY_READ) as registry_key: # opens the registry key for reading
                winreg.QueryValueEx(registry_key, AutoStartManager.APP_NAME) # queries the registry for the application entry
                return True # then return true 
        except FileNotFoundError: # gracefully handle errors so the program doesnt crash
            return False # return false
        except Exception as e: # gracefully handle errors so the program doesnt crash
            Logger.error(f"Error checking autostart status: {e}") # log the error and the error message
            return False # assume false