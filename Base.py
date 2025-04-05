import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import serial
import serial.tools.list_ports

class SerialRobotAbner:
    
    def getPorts():  
      portList = serial.tools.list_ports.comports() 
      ports = []
      for puerto in portList:
          ports.append(puerto.name)
      return ports
    
    def connectToComPort(self): 
        baud = self.baudInput.get() 
        bits = self.bitsInput.get() 
        stopBit = self.bitStopInput.get() 
        portName = self.ports.get()



    def __init__(self, rootUI):
        self.rootUI = rootUI

        self.rootUI.title("Robot Abner - Serial Ports")
        self.rootUI.geometry("800x550")

        # Listamos lls puertos
        portComLabel = ttk.Label(rootUI, text="Puerto")
        portComLabel.grid(column=0, row=0,  sticky="nw", padx=15)
        
        portList  = SerialRobotAbner.getPorts()
        self.ports = ttk.Combobox(rootUI, values=portList, state="readonly", width=45)   
        self.ports.grid(column=0, row=1,sticky="nw", padx=15 )
        self.ports.current(0)   

        # Valores baudaje, bits, bit, y paridad
        ##Baudaje
        baudLAbel = ttk.Label(rootUI, text="Baudaje")
        baudLAbel.grid(column=1, row=0, sticky="w" , padx=5) 

        self.baudInput = ttk.Entry(rootUI, width=15)
        self.baudInput.grid(column=1, row=1,sticky="w", padx=5 )

        ##Bits
        bitsLabel = ttk.Label(rootUI, text="Bits")
        bitsLabel.grid(column=2, row=0, sticky="w" , padx=5) 

        self.bitsInput = ttk.Entry(rootUI, width=15)
        self.bitsInput.grid(column=2, row=1,sticky="w", padx=5 )

        ##Bit To Stop
        stopBitLabel = ttk.Label(rootUI, text="Bits de parada")
        stopBitLabel.grid(column=3, row=0, sticky="w" , padx=5) 

        self.bitStopInput = ttk.Entry(rootUI, width=15)
        self.bitStopInput.grid(column=3, row=1,sticky="w", padx=5 )

         ##Bit To Stop
        stopBitLabel = ttk.Label(rootUI, text="Bits de parada")
        stopBitLabel.grid(column=3, row=0, sticky="w" , padx=5) 

        ##ConnectButton
        self.btnConnectOrDesconect = ttk.Button(rootUI, width=15, text="Conectar", command=self.connectToComPort)
        self.btnConnectOrDesconect.grid(column=4, row=1,sticky="w", padx=5 )


        ################  AREA SEND  ###################
        sendLabel = ttk.Label(rootUI, text="Entrada de datos")
        sendLabel.grid(column=0, row=2, sticky="w" , padx=15, pady=5) 

        self.bitStopInput = ttk.Entry(rootUI, width=50)
        self.bitStopInput.grid(column=0, row=3,sticky="w", padx=15 )

        self.btnSend = ttk.Button(rootUI, width=15, text="Enviar")
        self.btnSend.grid(column=1, row=3,sticky="w", padx=5 )




        ################  AREA LISTENER  ###################
 
        self.contentReaderArea = scrolledtext.ScrolledText(rootUI)  
        self.contentReaderArea.grid(column=0, row=5, columnspan=10, rowspan=6, padx=10, pady=10)

  



if __name__ == "__main__":
    rootUI= tk.Tk()
    SerialRobotAbner(rootUI)
    rootUI.mainloop()
