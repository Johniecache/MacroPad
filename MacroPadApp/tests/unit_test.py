import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # add parent directory to sys.path to allow imports

try:
    from gui.MacroPadGUI import MacroPadApp # try to import MacroPadApp
    print("MacroPadApp imported successfully!") # if successful then print success
except ModuleNotFoundError as e:
    print(f"Failed to import MacroPadApp: {e}")

try:
    from logic.MacroManager import MacroManager # try to import MacroManager
    print("MacroManager imported successfully!") # if successful then print success
except ModuleNotFoundError as e:
    print(f"Failed to import MacroManager: {e}") # otheriwse if failed print failed with the error message

try:
    from logic.SerialManager import SerialManager # try to import SerialManager
    print("SerialManager imported successfully!") # if successful then print success
except ModuleNotFoundError as e:
    print(f"Failed to import SerialManager: {e}") # otheriwse if failed print failed with the error message

try:
    from logic.AutoStartManager import AutoStartManager # try to import AutoStartManager
    print("AutoStartManager imported successfully!") # if successful then print success
except ModuleNotFoundError as e:
    print(f"Failed to import AutoStartManager: {e}") # otheriwse if failed print failed with the error message

try:
    from logic.ConnectionManager import ConnectionManager # try to import ConnectionManager
    print("ConnectionManager imported successfully!") # if successful then print success
except ModuleNotFoundError as e:
    print(f"Failed to import ConnectionManager: {e}") # otheriwse if failed print failed with the error message

'''
Unit tests for MacroPadApp class covering initialization, execution, and integration with managers.
'''
class TestMacroPadApp(unittest.TestCase):

    '''
    Set up a fresh Tk root for each test.

    Parameters:
        self:
            instance of object
    '''
    def setUp(self):
        self.root = tk.Tk()
        self.addCleanup(self.root.destroy)

    '''
    Test initialization of internal managers.
    '''
    @patch("threading.Thread.start")
    def test_app_initializes_components_and_managers(self, mock_thread_start):
        app = MacroPadApp(self.root) # set variable app to the MacroPadApp
        self.assertIsInstance(app.serial_manager, SerialManager) # initialization of SerialManager
        self.assertIsInstance(app.macro_manager, MacroManager) # initialization of MacroManager
        self.assertIsInstance(app.auto_start_manager, AutoStartManager) # initialization of AutoStartManager
        self.assertIsInstance(app.connection_manager, ConnectionManager) # initialization of ConnectionManager

    '''
    Ensure connection thread starts during app initialization.
    '''
    @patch("threading.Thread.start")
    def test_connection_manager_thread_starts(self, mock_thread_start):
        app = MacroPadApp(self.root) # set variable app to the MacroPadApp
        mock_thread_start.assert_called_once() # run thread for connection

    '''
    Validate that a shell command is executed correctly.
    '''
    @patch("subprocess.Popen")
    def test_runAction_runs_command(self, mock_popen):
        app = MacroPadApp(self.root) # set variable app to the MacroPadApp
        test_cmd = "echo hello" # variable for testing
        app.runAction(test_cmd) # pass the test variable
        mock_popen.assert_called_once_with(test_cmd, shell=True) # pass it through shell

    '''
    Ensure macros are loaded correctly via macro manager.
    '''
    def test_macro_manager_load(self):
        app = MacroPadApp(self.root) # set variable app to the MacroPadApp
        app.macro_manager.load_macros = MagicMock() # load macros as a mock variable
        app.macro_manager.load_macros.return_value = {'A': 'echo test'} # try to set new macro and return

        macros = app.macro_manager.load_macros() # load mock macros
        self.assertIn('A', macros) # set mock macro
        self.assertEqual(macros['A'], 'echo test') # check the set mock macro

    '''
    Check SerialManager connection status.
    '''
    def test_serial_manager_connection_check(self):
        app = MacroPadApp(self.root) # set variable app to the MacroPadApp
        app.serial_manager.is_connected = MagicMock(return_value=True) # make mock connection true
        self.assertTrue(app.serial_manager.is_connected()) # test if mock conneciton responds correctly

    '''
    Confirm AutoStartManager can enable autostart.
    '''
    def test_auto_start_enabled(self):
        app = MacroPadApp(self.root) # set variable app to the MacroPadApp
        app.auto_start_manager.enable = MagicMock() # make the auto start manager mock true
        app.auto_start_manager.enable() # endable the auto start manager
        app.auto_start_manager.enable.assert_called_once() # check if equal

    '''
    Verify retry behavior on connection fail.
    '''
    def test_connection_retry_logic(self):
        app = MacroPadApp(self.root) # set variable app to the MacroPadApp
        app.connection_manager.auto_connect = MagicMock() # create mock connection  manager
        app.connection_manager.retry_count = 0 # set retry count to 0
        app.connection_manager.auto_connect() # try to auto connect
        app.connection_manager.auto_connect.assert_called() # check if true

    '''
    Ensure runAction logs error when subprocess fails.
    '''
    @patch("gui.MacroPadGUI.Logger.error")
    @patch("subprocess.Popen", side_effect=OSError("Invalid command"))
    def test_runAction_handles_invalid_command(self, mock_popen, mock_logger_error):
        app = MacroPadApp(self.root) # set variable app to the MacroPadApp
        bad_cmd = "badcommand" # create fake bad command
        app.runAction(bad_cmd) # pass the mock variable
        mock_logger_error.assert_called_once() # check the call
        self.assertIn("Failed to run command", mock_logger_error.call_args[0][0]) # check if equal

    '''
    Check that logger outputs the run command.
    '''
    @patch("subprocess.Popen")
    def test_runAction_logs_output(self, mock_popen):
        mock_proc = MagicMock() # make a mock proc
        mock_popen.return_value = mock_proc # set mock variable and set it to the popen return value

        app = MacroPadApp(self.root) # set variable app to the MacroPadApp
        with patch("gui.MacroPadGUI.Logger.info") as mock_log: # assuming "" is mock log
            cmd = "echo test123" # create a mock variable
            app.runAction(cmd) # pass the mock variable
            mock_log.assert_any_call(f"Running command: {cmd}") # check if mock variable is passed

'''
Main entry to run tests.
'''
if __name__ == '__main__':
    unittest.main()
