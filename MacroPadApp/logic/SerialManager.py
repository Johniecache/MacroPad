import serial
import serial.tools.list_ports
import time
from logic.Logger import Logger

'''
Handles the serial data sent and received from device.
'''
class SerialManager:

    '''
    Default constructor for SerialManager class.

    Parameters:
        self:
            instance of object
        baudrate:
            update tick rate of how fast data is transferred (default is 9600)
    '''
    def __init__(self, baudrate=9600):
        self.baudrate = baudrate # rate at which data is transferred
        self.serial_port = None # port number that the device will connect to
        self.ser = None # serial object once it connects
        self.connected = False # checks whether serial connection is established (default false)

    '''
    Lists all available serial ports on the system.

    Parameters:
        self:
            instance of object
    Returns:
        list of potential serial ports
    '''
    def listSerialPorts(self):
        return [port.device for port in serial.tools.list_ports.comports()] # iterable of abailable serial ports then creates a list of device attributes which are names of the serial ports

    '''
    Attempts to automatically connect to a serial port by cycling through available ports.

    Parameters:
        self:
            instance of object
    Returns:
        whether or not a connection was established
    '''
    def autoConnect(self):
        ports = self.listSerialPorts() # list of abailable serial ports
        for port in ports: # for each port in the ports list
            try: # handle errors with grace
                ser = serial.Serial(port, self.baudrate, timeout=1) # tries to open the serial port with the specified baudrate
                time.sleep(2) # pause for 2 seconds to ensure the connection is established
                ser.flushInput() # flushes the input buffer incase of pre existing data
                self.ser = ser # set instance ser as ser object
                self.serial_port = port # set instance serial port as the object port
                self.connected = True # change connection status to true
                Logger.info(f"Connected to {self.serial_port}") # log that device is successfully connected with its port number
                return True # return true
            except (serial.SerialException, OSError) as e: # gracefully handle errors so program doesnt crash
                Logger.info(f"Failed to connect to {port}: {e}") # log the error and its error message
                continue # allow passing of except block
        return False # default assume there was no connection

    '''
    Checks whether or not a device is connected or not

    Parameters:
        self:
            instance of object
    Return:
        boolean value of if a device was connected or not
    '''
    def isConnected(self):
        return self.ser is not None and self.ser.is_open and self.connected # if ser object exists, if serial poort is open, and if connected is flagged as true

    '''
    Gets the connected device port.

    Parameters:
        self:
            instance of object
    Returns:
        serial port of connected device
    '''
    def getPort(self):
        return self.serial_port # returns the serial port

    '''
    sends data to the serial port if connected.

    Parameters:
        self:
            instance of object
        data:
            data to send over serial to the port that the device is connected to
    '''
    def write(self, data):
        if self.isConnected(): # if there is a device connected 
            try: # handle errors with grace
                self.ser.write(data) # sends data to the serial connection
                Logger.info(f"Sent to Arduino: {data.decode('utf-8').strip()}") # log that ther has been data sent with the data from bytes to a 'UTF-8'
            except serial.SerialException as e: # gracefully handle errors so program doesnt crash
                Logger.error(f"Error writing to serial port: {e}") # log the error with the error message
                self.disconnect() # pass over to disconnected method to handle disconnection of device

    '''
    Reads line of data from the serial port if available.

    Parameters:
        self:
            instance of object
    Returns:
        line of data sent from device
    '''
    def readLine(self):
        if self.isConnected() and self.ser.in_waiting: # if there is a connection and data waiting to be read
            try: # handle errors with grace
                line = self.ser.readline().decode('utf-8', errors='ignore').strip() # reads the data and decodes the byte data to a 'UTF-8' string
                Logger.info(f"Received from serial: {line}") # log that data has been recieved from device with the data that was sent
                return line # return line of data that was sent from device
            except serial.SerialException as e: # gracefully handle errors so program doesnt crash
                Logger.error(f"Serial read error: {e}") # log the error and the error message
                self.disconnect() # send to disconnect method ot handle the disconnection of device
        return None # 

    '''
    Handles the disconnection of a device so that there are no lingering problems (zombie ports, leaked data, etc).

    Parameters:
        self:
            instance of object
    '''
    def close(self):
        if self.ser: # if there is a serial connection
            try: # handle errors with grace
                self.ser.close() # close the serial connection
                self.ser = None # set serial connection to none
                self.serial_port = None # set the port to none
                self.connected = False # sent connection to false
                Logger.info("Serial port closed.") # log that the serial port has been closed
            except serial.SerialException as e: # gracefully handle errors so program doesnt crash
                Logger.error(f"Error closing serial port: {e}") # log the error with the error message