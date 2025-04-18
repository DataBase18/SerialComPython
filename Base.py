import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import serial
import serial.tools.list_ports
import threading
from tkinter import messagebox
import keyboard

class SerialRobotAbner:
    
    def getPorts(self):  
      portList = serial.tools.list_ports.comports() 
      ports = []
      for puerto in portList:
          ports.append(puerto.name)
      return ports
    
    def setPortsToCombo (self):
        portList  = self.getPorts()
        self.ports.configure(values=portList)

    def listenerPort (self, portName, baud, bits, bitStop, timeout=2, parity="N"):
        mgs = "s"
        try:
          self.comPortConnect= serial.Serial(port=portName, baudrate=baud, bytesize = int(bits),  parity=parity, stopbits= float (bitStop), timeout=timeout) 
        except Exception  as e:
            mgs= "No se pudo abrir el puerto " + portName + ". " , str(e)
            messagebox.showwarning("Error al abrir el puerto", mgs )
            return 
        
        msg = "Conexion exitosa en el puerto "+portName+ "!"
        messagebox.showwarning("Genial!", msg)


        #Si se conecta, cambiamos todo el ui  
        #btns and ui
        self.btnConnect.grid_remove() 
        self.btnDesconect.grid() 
        self.footer.grid(column=0, row=30, sticky="w", padx=10, pady=5)
        self.footer.config(text=f"Escuchando puerto: {portName}")
        
        self.sendLabel.grid(column=0, row=2, sticky="w" , padx=15, pady=5)  
        self.commandInput.grid(column=0, row=3,sticky="w", padx=15 )
        self.btnSend.grid(column=1, row=3,sticky="w", padx=5 )

        while True:  

            #Si se pierde la conexion, cambiamos todo
            if not self.comPortConnect.is_open or self.comPortConnect == None: 
              break
            
            #Si ahy conexion seguimos leyendo
            if self.comPortConnect.is_open  and self.comPortConnect.inWaiting() > 0:    
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
        #Change send area
        self.sendLabel.grid( )  
        self.commandInput.grid(  )
        self.btnSend.grid(  )

    def connectToComPort(self): 
        baud = self.baudInput.get() 
        bits = self.bitsInput.get() 
        stopBit = self.bitStopInput.get() 
        portName = self.ports.get()

        if baud == "" or baud is None :
           messagebox.showwarning("Error", "Ingrese el baudaje" )
           return 
        elif bits == "" or bits is None :
           messagebox.showwarning("Error", "Ingrese el la cantidad de bits" )
           return 
        elif stopBit == "" or stopBit is None :
           messagebox.showwarning("Error", "Ingrese la cantidad de bits de parada" )
           return 
        elif portName == "" or portName is None :
           messagebox.showwarning("Error", "Seleccione un puerto" )
           return 
        
        self.threadListener = threading.Thread(target=self.listenerPort, daemon=True, args=[ portName, baud, bits , stopBit])
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
        
        #Spacer 
        spacer = tk.Frame(self.rootUI, width=350, )  # Ajusta el tamaño del espacio
        spacer.grid(column=0, row=1, )
        #Iniciamos sin valores pues llamaos a la funcion setPorts
        self.ports = ttk.Combobox(rootUI, values=[], state="readonly", width=32)   
        self.ports.grid(column=0, row=1,sticky="nw", padx=15 )
        self.setPortsToCombo()
        self.ports.current(0)   

        #Refescar button
        self.btnRefreshComs = ttk.Button(rootUI, width=15, text="Refrescar", command=self.setPortsToCombo)
        self.btnRefreshComs.grid(column=0, row=1,sticky="e", padx=5 ) 

        # Valores baudaje, bits, bit, y paridad
        ##Baudaje
        baudLAbel = ttk.Label(rootUI, text="Baudaje",)
        baudLAbel.grid(column=1, row=0, sticky="w" , padx=5,  ) 

        self.baudInput = ttk.Entry(rootUI, width=15, )
        self.baudInput.grid(column=1, row=1,sticky="w", padx=5 )
        self.baudInput.insert(0, "9600") 

        ##Bits
        bitsLabel = ttk.Label(rootUI, text="Bits")
        bitsLabel.grid(column=2, row=0, sticky="w" , padx=5) 

        self.bitsInput = ttk.Entry(rootUI, width=15)
        self.bitsInput.grid(column=2, row=1,sticky="w", padx=5 )
        self.bitsInput.insert(0, "8") 

        ##Bit To Stop
        stopBitLabel = ttk.Label(rootUI, text="Bits de parada")
        stopBitLabel.grid(column=3, row=0, sticky="w" , padx=5) 

        self.bitStopInput = ttk.Entry(rootUI, width=15)
        self.bitStopInput.grid(column=3, row=1,sticky="w", padx=5 )
        self.bitStopInput.insert(0, "1") 

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
        self.sendLabel = ttk.Label(rootUI, text="Entrada de datos") 
        self.commandInput = ttk.Entry(rootUI, width=50)  
        self.btnSend = ttk.Button(rootUI, width=15, text="Enviar", command=self.sendCommand)
      
 

        ################  AREA LISTENER  ################### 
        self.contentReaderArea = scrolledtext.ScrolledText(rootUI)  
        self.contentReaderArea.configure(state="normal") 
        self.contentReaderArea.grid(column=0, row=5, columnspan=10, rowspan=6, padx=10, pady=10) 
  
        ###### FOOOTER ###############  
        self.footer = ttk.Label(rootUI, text=f"Esuchando: { self.comPortConnect}")
        


if __name__ == "__main__":
    rootUI= tk.Tk()
    SerialRobotAbner(rootUI)
    rootUI.mainloop()
