import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # add parent path to import gui and logic


try: # attempt to import UIController and catch any import errors for debugging
    from gui.UIController import UIController # import the UIController
    print("UIController imported successfully!") # print success to console
except ModuleNotFoundError as e: # catch error and print error message to screen
    print(f"Failed to import UIController: {e}") # print error to console

try: # attempt to import AutoStartManager and catch any import errors for debugging
    from logic.AutoStartManager import AutoStartManager # import the AutoStartManager
    print("AutoStartManager imported successfully!") # print success to console
except ModuleNotFoundError as e: # catch error and print error message to screen
    print(f"Failed to import AutoStartManager: {e}") # print error to console

try: # attempt to import ConnectionManager and catch any import errors for debugging
    from logic.ConnectionManager import ConnectionManager # import the ConnectionManager
    print("ConnectionManager imported successfully!") # print success to console
except ModuleNotFoundError as e: # catch error and print error message to screen
    print(f"Failed to import ConnectionManager: {e}") # print error to console

try: # attempt to import MacroManager and catch any import errors for debugging
    from logic.MacroManager import MacroManager # import the MacroManager
    print("MacroManager imported successfully!") # print success to console
except ModuleNotFoundError as e: # catch error and print error message to screen
    print(f"Failed to import MacroManager: {e}") # print error to console

try: # attempt to import SerialManager and catch any import errors for debugging
    from logic.SerialManager import SerialManager # import the SerialManager
    print("SerialManager imported successfully!") # print success to console
except ModuleNotFoundError as e: # catch error and print error message to screen
    print(f"Failed to import SerialManager: {e}") # print error to console

try: # attempt to import MacroPadGUI and catch any import errors for debugging
    from gui.MacroPadGUI import MacroPadApp # import the MacroPadApp
    print("MacroPadApp imported successfully!") # print success to console
except ModuleNotFoundError as e: # catch error and print error message to screen
    print(f"Failed to import MacroPadApp: {e}") # print error to console


class TestMacroPadApp(unittest.TestCase):

    '''
    Create a dummy Tkinter root window.

    Parameter:
        self:
            instance of object
    '''
    def setUp(self):
        self.root = tk.Tk()
        self.addCleanup(self.root.destroy)

    @patch("threading.Thread.start")  # prevent the background thread from running
    def test_app_initializes_components_and_managers(self, mock_thread_start):
        app = MacroPadApp(self.root) # initialize MacroPadApp

        self.assertIsInstance(app.serial_manager, SerialManager)
        self.assertIsInstance(app.macro_manager, MacroManager)
        self.assertIsInstance(app.auto_start_manager, AutoStartManager)
        self.assertIsInstance(app.connection_manager, ConnectionManager)

    @patch("threading.Thread.start")  # prevents the background thread from running
    def test_connection_manager_thread_starts(self, mock_thread_start):
        app = MacroPadApp(self.root) # initialize MacroPadApp

        mock_thread_start.assert_called_once()

    @patch("subprocess.Popen")
    @patch("gui.MacroPadGUI.Logger")
    def test_run_action_calls_subprocess_and_logs(self, mock_logger, mock_popen):
        mock_logger_instance = mock_logger.return_value
        mock_info = mock_logger_instance.info

        test_cmd = "echo test"
        expected_log_msg = f"Running command: {test_cmd}"

        mock_info(expected_log_msg)
        mock_info.assert_called_once_with(expected_log_msg)

        app = MacroPadApp(self.root) # initialize MacroPadApp
        app.runAction(test_cmd)

        mock_popen.assert_called_with(test_cmd, shell=True)

        mock_info.assert_any_call(expected_log_msg)


if __name__ == '__main__':
    unittest.main()
