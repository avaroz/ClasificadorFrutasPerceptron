#Prueba de encender y apagar un led desde python a arduino

import serial # Importar el módulo serial para comunicarse con el Arduino
import time # Importar el módulo time para usar la función sleep

arduino = serial.Serial('COM5', 9600) # Crear un objeto serial con el puerto y la velocidad del Arduino
time.sleep(2) # Esperar dos segundos para que se establezca la conexión

salir = False # Variable para controlar la salida del programa
while not salir: # Repetir el menú hasta que el usuario quiera salir
  print("Menú de opciones:") # Mostrar el menú
  print("1. Prender el LED 13")
  print("2. Apagar el LED 13")
  print("3. Salir")
  opcion = input("Elige una opción: ") # Leer la opción
  if opcion == "1": # Si la opción es 1
    arduino.write(b'1') # Enviar el caracter '1' al Arduino
    print("LED 13 encendido") # Mostrar un mensaje de confirmación
  elif opcion == "2": # Si la opción es 2
    arduino.write(b'0') # Enviar el caracter '0' al Arduino
    print("LED 13 apagado") # Mostrar un mensaje de confirmación
  elif opcion == "3": # Si la opción es 3
    print("Adiós") # Despedirse del usuario
    salir = True # Cambiar la variable de control para salir del programa
  else: # Si la opción no es ninguna de las anteriores
    print("Opción no válida, inténtalo de nuevo") # Mostrar un mensaje de error

arduino.close() # Cerrar la conexión con el Arduino
