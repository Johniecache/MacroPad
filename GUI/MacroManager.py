# macro_manager.py
import json
import os
from Settings import Settings
from Logger import Logger

'''
Manages what each macro button should do.
'''
class MacroManager:
    '''
    Default constructor.

    Parameters:
        self:
            instance of object
    '''
    def __init__(self):
        self.config_file = Settings.getConfigFile() # get the config file from settings (hard coded location)
        self.button_actions = self.loadActions() # get all the button actions

    '''
    Loads the macro actions.

    Parameters:
        self:
            instance of object
    '''
    def loadActions(self):
        if os.path.exists(self.config_file): # check if the config to file actually exists
            with open(self.config_file, 'r') as f: # open file for reading and parse json file
                return json.load(f) # return results
        else: # if the file doesn't exist
            return {f'Button {i} pressed': '' for i in range(1, 10)} # return fresh dictionary with keys with each action starting at empty

    '''
    Saves whatever's in button_actions back to the file.

    Parameters:
        self:
            instance of object
    '''
    def saveActions(self):
        with open(self.config_file, 'w') as f: # open config file for writing
            json.dump(self.button_actions, f, indent=4) # serialize button_actions into it

    '''
    Method to fetch the actions assigned to a specific button

    Parameters:
        self:
            instance of object
        button_name:
            unique identifier for the button
    '''
    def getAction(self, button_name):
        return self.button_actions.get(button_name, "") # gets the acitons of passed button

    '''
    Sets the aciton of a specific button

    Parameters:
        self:
            instance of object
        button_name:
            unique identifier for the button
        action:
            macro wanting to be assigned to the button
    '''
    def setActions(self, button_name, action):
        self.button_actions[button_name] = action # modifies action of button in memory
        self.saveActions() # immediately save everything to the file
        Logger.log("INFO", f"Updated {button_name} to {self.button_actions[button_name]}") # log the update of the button and what its new action is

    '''
    Gets all the actions of each button

    Parameters:
        self:
            instance of object
    '''
    def getAllActions(self):
        return self.button_actions # return all actions of each button
