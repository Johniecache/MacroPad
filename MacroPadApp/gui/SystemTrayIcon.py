import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
from logic.Logger import Logger
import threading

'''
Handles and manages the functionality of the system tray icon.
'''
class SystemTrayIcon:
    '''
    Default constructor for the SystemTrayIcon.

    Parameters:
        self:
            instance of object
        restore:
            restores the window
        quit:
            quit function to exit the window
    '''
    def __init__(self, restore, quit):
        self.icon = None # initialize icon variable
        self.restore = restore # store function to restore the main window
        self.quit = quit # store function to quit the main window
        self.icon_thread = None # initialize the icon thread

    '''
    Create and configure system tray icon.

    Parameters:
        self:
            instance of object
    '''
    def setupIcon(self):
        try: # handle errors with grace
            icon_image = Image.new('RGB', (64, 64), color=(255, 255, 255)) # create new image for system tray (blue square)
            draw = ImageDraw.Draw(icon_image) # draw object for the icon_image
            draw.rectangle((0, 0, 64, 64), fill="blue") # draw the blue square as the tray icon
        except Exception as e: # gracefully handle errors so program doesnt crash
            Logger.error(f"Error creating icon image: {e}") # log the error
            return # return to prevent further errors if image creation fails.

        '''
        Handles the restore action to restore the window after hiding.

        Parameters:
            icon:
                system tray icon
            item:
                menu item clicked
        '''
        def restoreWindow(icon, item):
            try: # handle errors with grace
                self.restore() # calls the restore function which will restore the window
                icon.visible = False # icon becomes invisible
            except Exception as e: # gracefully handle errors so program doesnt crash
                Logger.error(f"Error restoring window: {e}") # log error

        '''
        Handles the quit action when the app is quit out.

        Parameters:
            icon:
                system tray icon
            item:
                menu item clicked
        '''
        def quitIcon(icon, item):
            try: # handle errors with grace
                self.quit() # calls quit function which should close or terminate the application
                icon.stop() # stop showing the icon on the system tray
            except Exception as e:
                Logger.error(f"Error quitting application: {e}") # log error

        tray_menu = (item('Restore', restoreWindow), item('Quit', quitIcon)) # tuple that defines the tray menu
        try: # handle errors with grace
            self.icon = pystray.Icon("MacroPad", icon_image, menu=pystray.Menu(*tray_menu)) # creates the system tray icon using pystray
        except Exception as e: # gracefully handle errors so program doesnt crash
            Logger.error(f"Error creating system tray icon: {e}") # log the error
            self.icon = None # ensure self.icon is None to prevent further actions
            return # exit setupIcon

    '''
    Starts the system tray icon in a separate thread.

    Parameters:
        self:
            instance of object
    '''
    def run(self):
        if self.icon: # if icon exists
            '''
            Tries to run the icon on the system tray.
            '''
            def runIcon():
                try: # handle errors with grace
                    self.icon.run() # run the icon
                except Exception as e: # gracefully handle errors so program doesnt crash
                    Logger.error(f"Error running system tray icon: {e}") # log error
            self.icon_thread = threading.Thread(target=runIcon) # create thread
            self.icon_thread.daemon = True # set to daemon
            self.icon_thread.start() # start the thread

    '''
    Stops the system tray icon.

    Parameters:
        self:
            instance of object
    '''
    def stop(self):
        if self.icon: # if the icon exists
            try: # handle errors with grace
                self.icon.stop() # stop running the icon
            except Exception as e: # gracefully handle errors so program doesnt crash
                Logger.error(f"Error stopping system tray icon: {e}") # log error
        if self.icon_thread: # check if thread exists
            self.icon_thread.join() # join the thread.

    '''
    Toggles the visibility of the tray icon.

    Parameters:
        self:
            instance of object
        visible:
            boolean of whether system tray icon can be seen or not
    '''
    def setVisible(self, visible):
        if self.icon: # if the icon exists
            try: # handle errors with grace
                self.icon.visible = visible # change the icons visibility to passed boolean value
            except Exception as e: # gracefully handle errors so program doesnt crash
                Logger.error(f"Error setting icon visibility: {e}") # log the error
