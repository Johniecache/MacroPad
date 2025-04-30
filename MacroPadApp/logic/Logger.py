import logging
import sys
import os

'''
Class logger that wraps the built in logger inside of it
'''
class Logger:
    logger = None # placeholder for variable _logger

    '''
    Handles the initialization of logger
    '''
    @staticmethod # static method
    def initialize(): # sets up logger configuration
        if Logger.logger is None: # if no logger has been created yet
            Logger.logger = logging.getLogger("MacroPadLogger") # set new logger called MacroPadLogger
            Logger.logger.setLevel(logging.DEBUG) # minimum severity as debug
            Logger.logger.propagate = False

        if not Logger.logger.handlers: # check if handlers are attached, if not add them
            log_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resources', 'MacroPad.log') # get the log path (from MacroPad to resoruces) to update log file
            file_handler = logging.FileHandler(log_path) # pass the log path (resource folder) to append the already existing log file
            file_handler.setLevel(logging.DEBUG) # log everything from debug
            file_format = logging.Formatter('%(levelname)s (%(asctime)s): %(message)s', datefmt='%Y-%m-%d %H:%M:%S') # define format for logs
            file_handler.setFormatter(file_format) # attach defined format to file writer

            console_handler = logging.StreamHandler(sys.stdout) # writes logs to standard output
            console_handler.setLevel(logging.DEBUG) # minimum level to debug
            console_format = ColorFormatter() # allow for custom colors in console
            console_handler.setFormatter(console_format) # attach color formatter to console

            Logger.logger.addHandler(file_handler) # add file handler to the logger
            Logger.logger.addHandler(console_handler) # add console handler to logger

            print("Logger handler count:", len(Logger.logger.handlers))

    '''
    Handles the information types of logger

    Parameters:
        message:
            message associated with the log
    '''
    @staticmethod # static method
    def info(message):
        Logger.initialize() # call initialize
        Logger.logger.info(message) # log message at info level

    '''
    Handles the warning types of logger

    Parameters:
        message:
            message associated with the log
    '''
    @staticmethod # static method
    def warning(message):
        Logger.initialize() # call initialize
        Logger.logger.warning(message) # log message at warning level

    '''
    Handles the error types of logger

    Parameters:
        message:
            message associated with the log
    '''
    @staticmethod # static method
    def error(message):
        Logger.initialize() # call initialize
        Logger.logger.error(message) # log message at error level

    '''
    Handles the debug types of logger

    Parameters:
        message:
            message associated with the log
    '''
    @staticmethod # static method
    def debug(message):
        Logger.initialize() # call initialize
        Logger.logger.debug(message) # log message at debug level


class ColorFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': "\033[37m",    # white in console for debugging
        'INFO': "\033[36m",     # cyan in console for information
        'WARNING': "\033[33m",  # yellow in console for warnings
        'ERROR': "\033[31m",    # red in console for errors
        'CRITICAL': "\033[41m"  # red background in console for critical notifications
    }
    RESET = "\033[0m" # resets the color

    '''
    Handles the formatting of different levels and what their color should be

    Parameters:
        self:
            instance of object
        record:
            LogRecord object to be passed
    '''
    def format(self, record):
        color = self.COLORS.get(record.levelname, self.RESET) # grab color based on log level
        message = super().format(record) # set the message as that color
        return f"{color}{message}{self.RESET}" # reset the color after to make sure it doesnt carry into other lines
 