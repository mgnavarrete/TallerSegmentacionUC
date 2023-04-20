import serial
import pygame
from time import sleep
from pygame.constants import JOYBUTTONDOWN

# Configura el puerto serie
ser = serial.Serial('COM15', 9600)  # Cambiar 'COM1' por el puerto serie correspondiente
ser.timeout = 1  # Espera máximo 1 segundo a recibir respuesta


pygame.init()

joysticks = []

for i in range(0, pygame.joystick.get_count()):
    joysticks.append(pygame.joystick.Joystick(i))
    joysticks[-1].init()
    
print(pygame.joystick.Joystick(0).get_name())
a = True
# Envia el mensaje
while a:
    for event in pygame.event.get():

        if event.type == 1538:
            if event.value == (0,0):
                print("Stoping")
                ser.write(bytes("S", 'ascii'))  # El mensaje debe ser en formato de bytes

            if event.value == (0,1):
                print("Going Forward")
                ser.write(bytes("F", 'ascii')) 

            if event.value == (0,-1):
                print("Going Backward")
                ser.write(bytes("B", 'ascii')) 

            if event.value == (-1,0):
                print("Going Left")
                ser.write(bytes("R", 'ascii')) 

            if event.value == (1,0):
                print("Going Right")
                ser.write(bytes("L", 'ascii')) 

        if event.type == JOYBUTTONDOWN:
            if event.button == 1: #B
                print("Quiting")
                a =False


     

# Cierra el puerto serie
ser.close()