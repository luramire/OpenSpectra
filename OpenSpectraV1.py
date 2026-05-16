# -*- coding: utf-8 -*-
"""
****************************************ARDUINO SPECTROMETER PROGRAM
To use pyqtgraph: promote QWidget to pyqtgraph.h as PlotWidget in Designer
@author: Luis Felipe Ramirez Garcia. Universidad de Antioquia, 2026
"""
#Works
#Pending: generate executable and load to sourceforge and github

import sys, os
from PySide6.QtWidgets import QApplication, QFileDialog
from PySide6.QtCore import Signal, QObject
from PySide6.QtGui import QIcon
import time
import numpy as np
import threading
import pyqtgraph as pg
import serial
import serial.tools.list_ports

def resource_path(relative_path):
    """Get absolute path to resource, works for dev, PyInstaller onefile and onedir."""
    if hasattr(sys, "_MEIPASS"):  # onefile
        base_path = sys._MEIPASS
    else:  # onedir
        exe_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        internal_path = os.path.join(exe_dir, "_internal", relative_path)
        if os.path.exists(internal_path):
            return internal_path
        return os.path.join(exe_dir, relative_path)  # fallback (dev mode)
    return os.path.join(base_path, relative_path)

def load_stylesheet(filename):
    with open(filename, "r") as f:
        return f.read()

icons_dir = resource_path("icons")

uiclass, baseclass = pg.Qt.loadUiType('OpenSpectraUI_pyqtgraph.ui')

cal_data = np.loadtxt(resource_path("data/calib.txt")) #Load calibration data
cal_list = cal_data.tolist()
pixels=np.arange(288)
wavelength_array=cal_list[0]+pixels*cal_list[1]+pixels**2*cal_list[2]+pixels**3*cal_list[3]+pixels**3*cal_list[3]+pixels**5*cal_list[5]
#print(cal_list) For debugging

serial_port = serial.Serial() #Create an instance of the serial port
serial_port.baudrate = 115200

connected_flag=0 #To know whether if the serial port is conected or not.
pause_flag=False #To pause the spectrum

class Communicate(QObject): #Signal to allow threading function to communicate with the main GUI
    data_received_signal = Signal(str)


def serial_data_thread(signal): #Separate thread that emits the serial data (signal) when there is new data in the serial port (threading eliminates the problem of freezing GUIs)
    global connected_flag
    while threading.current_thread().is_alive():
        #signal.data_received_signal.emit("Hola") #For debugging
        time.sleep(0.01) #Neccesary to not freeze the plot controls
        if (serial_port.is_open and connected_flag==1): #If port is open and connection is active
            if(serial_port.in_waiting>0): #If data has arrived
                data = serial_port.readline().decode('utf-8').strip()
                signal.data_received_signal.emit(data)


class MainWindow(uiclass, baseclass):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.StatusText.setText("Not connected")
        self.start_thread()
        self.connectWidgets()
        self.refresh_com_ports()
        self.confplot("w")
    
    ######################### Main funcions
    def start_thread(self):
        self.comm = Communicate()
        self.comm.data_received_signal.connect(self.process_message) #When the signal data_receive_signal is received, the function (slot) process_message is called.
        self.thread = threading.Thread(target=serial_data_thread, args=(self.comm,))
        self.thread.daemon = True  # Allows the thread to be killed when the main program exits
        self.thread.start()

    def connectWidgets(self): #Function to connect widget events to functions
        self.connect_btn.clicked.connect(self.con_discon_serial)
        self.pause_btn.clicked.connect(self.pause_spectrum)
        self.pause_btn.setEnabled(False)
        self.set_int_time_btn.clicked.connect(self.set_int_time)
        self.set_int_time_btn.setEnabled(False)
        self.set_laser_btn.clicked.connect(self.toggle_laser)
        self.set_laser_btn.setEnabled(False)
        self.set_led_btn.clicked.connect(self.toggle_led)
        self.set_led_btn.setEnabled(False)
        self.save_btn.clicked.connect(self.save_plot_data)

    def refresh_com_ports(self):
        self.selectPort.clear()
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.selectPort.addItem(port.device)

    def confplot(self, bgcolor):
        self.graphwidget.setBackground("#0c0f13")
        styles = {"color": "#d7dde5", "font-size": "13px", "font-family": "Segoe UI"}
        self.graphwidget.setLabel("left", "Intensity (a.u. 10 bits)", **styles)
        self.graphwidget.setLabel("bottom", "Wavelength (nm)", **styles)
        axispen = pg.mkPen(color="#7f8c8d", width=1)
        self.graphwidget.plotItem.getAxis('left').setPen(axispen)
        self.graphwidget.plotItem.getAxis('bottom').setPen(axispen)
        self.graphwidget.plotItem.getAxis('left').setTextPen("#cfd6df")
        self.graphwidget.plotItem.getAxis('bottom').setTextPen("#cfd6df")
        self.graphwidget.showGrid(x=True, y=True, alpha=0.15)
        vLine = pg.InfiniteLine(angle=90, pos=300, movable=True, pen="#cfd6df") #Vertical cursor
        label = pg.InfLineLabel(vLine, text="x={value:.1f}", position=0.95, color='y')
        self.graphwidget.addItem(vLine)
        pen = pg.mkPen(color="#00e5ff", width=2) #define the line color of the plot
        self.plot_data=self.graphwidget.plot([], [], pen=pen, symbolPen ='r', symbolSize = 4)


######################## Functions deployed by pressing buttons
    def con_discon_serial(self): #Connect or disconnect serial
        global connected_flag
        selected_port = self.selectPort.currentText()
        number_ports = self.selectPort.count() #Count the number of items (ports) in the Qcombobox
        if serial_port.is_open: #If port is open
            connected_flag = 0
            time.sleep(0.1) #To be sure the last data has arrived before disconnecting
            serial_port.close()
            if(not serial_port.is_open): #Check if really closed
                self.connect_btn.setText("Connect")
                self.StatusText.setText("Not connected")
                self.set_int_time_btn.setEnabled(False)
                self.set_laser_btn.setEnabled(False)
                self.set_led_btn.setEnabled(False)
                self.save_btn.setEnabled(False)
                self.pause_btn.setEnabled(False)        
        else: #If port is not opened
            if(number_ports > 0): #Check first if at least there is one port in the list
                serial_port.port=selected_port
                serial_port.open()
                if(serial_port.is_open): #Check if really opened
                    self.connect_btn.setText("Disconnect")
                    self.StatusText.setText("Connected to "+selected_port)
                    self.pause_btn.setEnabled(True)
                    connected_flag = 1
                else:
                    self.StatusText.setText("Failed to connect to "+selected_port)
            else:
                self.StatusText.setText("No ports were found. Check connections and tray again.")

    def pause_spectrum(self):
        global pause_flag
        pause_flag=not pause_flag
        self.StatusText.setText("Paused spectra acquistion")

    def toggle_laser(self):
        #Toggle built-in UV laser
        serial_port.write(('U').encode('utf-8'))

    def toggle_led(self):
        #Toggle built-in white led
        serial_port.write(('L').encode('utf-8'))

    def set_int_time(self):
        #Set integration time in microseconds
        serial_port.write(('I'+self.int_time_box.text()).encode('utf-8'))

    def save_plot_data(self):
        # Open file dialog to select file name and location
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save data as:", "", "Text file (*.txt);;All files (*)", options=options)
        
        if file_name:
            # Query data from graphwidget plot
            x, y = self.plot_data.getData()
            ylabel = self.graphwidget.plotItem.getAxis('left').labelText
            xlabel = self.graphwidget.plotItem.getAxis('bottom').labelText
            header="Spectrometer data. Integration time (us): "+self.int_time_box.text()+"\r\n\r\n"

            # Save data to file
            with open(file_name, 'w') as file:
                file.write("")
                file.write(header)
                file.write(xlabel+"\t"+ylabel+"\n")
                for x_val, y_val in zip(x, y):
                    file.write("{:.3f}".format(x_val)+"\t"+"{:.3f}".format(y_val)+"\n")
            self.StatusText.setText("Spectrum saved to text file")
##########################Auxiliry functions
    def plot(self, xdata, ydata):
        self.plot_data.setData(xdata, ydata)
##########################Funcions deployed by threads

    def process_message(self, message):
        global spec_data
        global wavelength_array
        #print(message) #For debugging
        #print("-")
        if ((',' in message) and pause_flag==False):
            self.StatusText.setText("Spectrum acquired")
            self.set_int_time_btn.setEnabled(True)
            self.set_laser_btn.setEnabled(True)
            self.set_led_btn.setEnabled(True)
            self.save_btn.setEnabled(True)
            
            spec_data=np.fromstring(message, dtype=int, sep=",")
            wavelength_array=np.arange(len(spec_data))*cal_list[1]+cal_list[0] #Taken from calibration file
            #print(spec_data) For debugging
            #self.plot(np.arange(len(spec_data)),spec_data) For debugging
            self.plot(wavelength_array,spec_data)
            return

app = QApplication(sys.argv)
style_file = resource_path("style.css")
app.setStyleSheet(load_stylesheet(style_file))
app.setWindowIcon(QIcon(os.path.join(icons_dir, "app_icon.ico")))
window = MainWindow()
window.show()
app.exec()
