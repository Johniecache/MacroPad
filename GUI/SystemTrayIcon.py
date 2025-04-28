import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
from Logger import Logger

'''
Handles and manages the functionality of the system tray icon.
'''
class SystemTrayIcon:
    '''
    Default constructor for the SystemTrayIcon
    '''
    def __init__(self, restore, quit):
        self.icon = None # initialize icon variable
        self.restore = restore # store function to restore the main window
        self.quit = quit # store function to quit the main window

    '''
    Create and configure system tray icon.

    Parameters:
        self:
            instance of object
    '''
    def setupIcon(self):
        icon_image = Image.new('RGB', (64, 64), color=(255, 255, 255)) # create new image for system tray (blue square)
        draw = ImageDraw.Draw(icon_image) # draw object for the icon_image
        draw.rectangle((0, 0, 64, 64), fill="blue") # draw the blue square as the tray icon

        '''
        Handles the restore action to restore the window after hiding.

        Parameters:
            icon:
                system tray icon
            item:
                menu item clicked
        '''
        def restoreWindow(icon, item):
            self.restore() # calls the restore function which will restore the window
            icon.visible = False # icon becomes invisible 

        '''
        Handles the quit action when the app is quit out.

        Parameters:
            icon:
                system tray icon
            item:
                menu item clicked
        '''
        def quitIcon(icon, item):
            self.quit() # calls quit function which should close or terminate the application
            icon.stop() # stop showing the icon on the system tray

        tray_menu = (item('Restore', restoreWindow), item('Quit', quitIcon)) # tuple that defines the tray menu
        self.icon = pystray.Icon("MacroPad", icon_image, menu=pystray.Menu(*tray_menu)) # creates the system tray icon using pystray

    '''
    Starts the system tray icon.

    Parameters:
        self:
            instance of object
    '''
    def run(self):
        if self.icon: # if icon exists 
            self.icon.run() # run the icon

    '''
    Stops the system tray icon.

    Parameters:
        self:
            instance of object
    '''
    def stop(self):
        if self.icon: # if the icon exists
            self.icon.stop() # stop running the icon

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
            self.icon.visible = visible # change the icons visibility to passed boolean value
