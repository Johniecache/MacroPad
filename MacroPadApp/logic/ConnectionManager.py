import threading
import time
from logic.Logger import Logger

'''
    Handles the connection process and serial communication with the device.
'''
class ConnectionManager:

    '''
        Initializes the connection manager.

        Parameters:
            serial_manager:
                instance of SerialManager for handling serial connection
            macro_manager:
                instance of MacroManager for retrieving actions
            update_status_callback:
                instance of update status callback to update the GUI status
            toggle_buttons_callback:
                instance of toggle buttons to enable/disable GUI buttons
            run_action_callback:
                instance of run action callback to execute received commands
        '''
    def __init__(self, serial_manager, macro_manager, update_status_callback, toggle_buttons_callback, run_action_callback):
        self.serial_manager = serial_manager # initialize serial manager
        self.macro_manager = macro_manager # initialize macro manager
        self.update_status = update_status_callback # initialize update status callback
        self.toggle_buttons = toggle_buttons_callback # initialize toggle buttons callback
        self.run_action = run_action_callback # initialize run action callback

        self.stop_event = threading.Event() # initialize new threading even
        self.listening = False # ensure listening is set to False by default
        self.running = True # ensure running is True by default

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
                    port = self.serial_manager.getPort() # gets the port to what the device is connected to
                    #Logger.info(f"Connected to {port}") # log the connected port
                    self.update_status(f"Connected: {port}") # update status to connected to port number
                    self.startSerialListener() # start listening for data from device
                    self.toggle_buttons(True) # allow user to edit buttons macros
                    retry_interval = 2 # reset interval to 2 for future
                else: # if failed connection to device
                    Logger.warning(f"Auto-connect failed. Retrying in {retry_interval} seconds...") # log the failed connection
                    self.toggle_buttons(False) # ensure user cannot edit buttons
                    self.update_status("Disconnected") # update status to disconnected
                    time.sleep(retry_interval) # wait time before retrying 
                    retry_interval = min(retry_interval * 2, max_interval) # double retry interval, cap at max
            else: # if device is connected already
                time.sleep(2) # wait 2 seconds before checking again

    '''
    Listens for data sent from device.
    
    Parameters:
        self:
            instance of object
    '''
    def startSerialListener(self):
        if not self.listening and self.serial_manager.isConnected(): # if serial listener isn't running and device is currently connected
            threading.Thread(target=self.serialListener, daemon=True).start() # create new thread that has serialListener running
            self.listening = True # set listening to true since thread for listening is created

    '''
    Continuously listens for input data from device.

    Parameters:
        self:
            instance of object
    '''
    def serialListener(self):
        while self.running: # while app is running
            line = self.serial_manager.readLine() # reads the line of the sent data and assigns it to a variable
            if line: # if there is data in the line
                for button_name, command in self.macro_manager.getAllActions().items(): # iterate over all buttons and check all their actions
                    if command == line: # if the command is the same as the line
                        self.run_action(command) # if it matches, then run that command
                        Logger.info(f"Executed action for {line} (mapped to {button_name})") # log that command was run
                        break # break out of the loop
                else: # if there is no matching command
                    Logger.warning(f"No action mapped for {line}") # log warning that command doesn't exist
            time.sleep(0.01) # allow time between checks

    '''
    Gracefully stops connection handling and serial listener.
    
    Parameters:
        self:
            instance of object
    '''
    def stop(self):
        self.running = False # ensure that the running boolean is set to false
        self.stop_event.set() # call stop even and set it
