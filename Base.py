import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import serial
import serial.tools.list_ports
import threading
from tkinter import messagebox
import keyboard

class SerialRobotAbner:
    
    def getPorts():  
      portList = serial.tools.list_ports.comports() 
      ports = []
      for puerto in portList:
          ports.append(puerto.name)
      return ports
    

    def listenerPort (self, portName, baud, bits, bitStop, timeout=2):
      
        self.comPortConnect= serial.Serial(port=portName, baudrate=baud, timeout=timeout) 
        while True:  

          #Si se pierde la conexion, cambiamos todo
          if not self.comPortConnect.is_open or self.comPortConnect == None: 
             break
          
          #Si ahy conexion seguimos leyendo
          if  self.comPortConnect.inWaiting() > 0:    
              response =  self.comPortConnect.read_until(b'\r\n').decode('latin-1').strip() 
              if(response != ""): 
                self.contentReaderArea.insert(tk.END, f"\n{response}")
                self.contentReaderArea.see(tk.END)   

      
    def disconnectComPort(self):  
        #Close port
        self.comPortConnect.close()
        self.comPortConnect = None
        #ChangeVisivily
        self.btnDesconect.grid_remove() 
        self.btnConnect.grid() 

    def connectToComPort(self): 
        baud = self.baudInput.get() 
        bits = self.bitsInput.get() 
        stopBit = self.bitStopInput.get() 
        portName = self.ports.get()

        #btns and ui
        self.btnConnect.grid_remove() 
        self.btnDesconect.grid() 
        self.footer.grid(column=0, row=30, sticky="w")
        self.footer.config(text=f"Escuchando puerto: {portName}")
 
        self.threadListener = threading.Thread(target=self.listenerPort, daemon=True, args=[ portName, baud, bits, stopBit])
        self.threadListener.start()


    def sendCommand(self):
        command = self.commandInput.get()
        if command:
           self.comPortConnect.write((command + "\r\n").encode())   
           self.commandInput.delete(0, tk.END)  


    def keyPressed(self, key):
        actualInputFocus = self.rootUI.focus_get()
        if key =="enter" and actualInputFocus == self.commandInput:
          self.sendCommand()


    def __init__(self, rootUI):
        self.rootUI = rootUI
        self.comPortConnect = None

        self.rootUI.title("Robot Abner - Serial Ports")
        self.rootUI.geometry("800x550")
        self.rootUI.resizable(False, False)

        #Listener de keys 
        keyboard.on_press(self.keyPressed)

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
         ##ConnectButton 
        self.btnDesconect = ttk.Button(rootUI, width=15, text="Desconectar", command=self.disconnectComPort)
        self.btnDesconect.grid(column=4, row=1,sticky="w", padx=5 )
        self.btnConnect = ttk.Button(rootUI, width=15, text="Conectar", command=self.connectToComPort)
        self.btnConnect.grid(column=4, row=1,sticky="w", padx=5 )


        ################  AREA SEND  ###################
        sendLabel = ttk.Label(rootUI, text="Entrada de datos")
        sendLabel.grid(column=0, row=2, sticky="w" , padx=15, pady=5) 

        self.commandInput = ttk.Entry(rootUI, width=50)
        self.commandInput.grid(column=0, row=3,sticky="w", padx=15 )

        self.btnSend = ttk.Button(rootUI, width=15, text="Enviar", command=self.sendCommand)
        self.btnSend.grid(column=1, row=3,sticky="w", padx=5 )




        ################  AREA LISTENER  ###################
 
        self.contentReaderArea = scrolledtext.ScrolledText(rootUI)  
        self.contentReaderArea.grid(column=0, row=5, columnspan=10, rowspan=6, padx=10, pady=10)

  
        ###### FOOOTER ###############  
        self.footer = ttk.Label(rootUI, text=f"Esuchando: { self.comPortConnect}")
        


if __name__ == "__main__":
    rootUI= tk.Tk()
    SerialRobotAbner(rootUI)
    rootUI.mainloop()
