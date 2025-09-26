#🔌 SerialCOM Interface — Comunicación Serial en Python
Es una aplicación sencilla escrita en Python que permite establecer comunicación serial con dispositivos conectados a puertos COM. Fue creada por necesidad en proyectos con microcontroladores PICAXE, módulos ESP WiFi, y Bluetooth HC-05, como alternativa libre al entorno de Arduino.

## 🎯 Funcionalidades principales
Nacio con la neceidad de controlar a detalle mis proyectos de PICAXE y hacer pruebas. Lo he usado para configurar modulos WIFI como los ESP y modulos BT como HC. Cualquier aporte es bienvenido, y se expondran mejoras para las versiones. Puedes usarlo para uso personal

- 🖥️ Interfaz gráfica simple y funcional El usuario ingresa el puerto COM deseado y configura los parámetros de conexión.
- ⚙️ Configuración personalizada Permite ajustar:
  - Baud rate (velocidad de transmisión)
  - Bits de parada
  - Paridad (si se desea extender)
- 📡 Comunicación serial bidireccional Escucha el puerto seleccionado y permite enviar comandos al dispositivo conectado.
- 🧪 Aplicaciones prácticas
  - Configuración de módulos ESP8266/ESP32 vía AT commands
  - Programación y prueba de módulos Bluetooth HC
  - Comunicación con microcontroladores PICAXE
  - Debugging de sensores y módulos seriales
 

## 🛠️ Tecnologías utilizadas
- [Python 3](https://www.python.org/)
- [PySerial](https://pypi.org/project/pyserial/) — Para manejo de puertos seriales
- [Tkinter](https://docs.python.org/3/library/tkinter.html) — Para la interfaz gráfica

## 🧠 Motivación
Este proyecto nació de la necesidad de contar con una herramienta libre, ligera y funcional para comunicarme con dispositivos seriales sin depender de entornos pesados o cerrados ya que en mis proyectos de electronica en la universidad los demandaba mucho.
