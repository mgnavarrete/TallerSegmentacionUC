import serial
import pygame
from time import sleep


# Configura el puerto serie
ser = serial.Serial('COM15', 9600)  # Cambiar 'COM15' por el puerto serie correspondiente
ser.timeout = 1  # Espera máximo 1 segundo a recibir respuesta

pygame.init()
pygame.joystick.init()

joysticks = []
for i in range(pygame.joystick.get_count()):
    joysticks.append(pygame.joystick.Joystick(i))
    joysticks[-1].init()

def send_to_arduino(value, direction):
    ser.write(f"{value},{direction}\n".encode('utf-8'))

speed_levels = [130]
current_speed_index = 0
running = True

while running:
    for event in pygame.event.get():

        if event.type == pygame.JOYAXISMOTION:
            x_axis = joysticks[0].get_axis(0)
            y_axis = joysticks[0].get_axis(1)

            if abs(x_axis) > 0.1 or abs(y_axis) > 0.1:
                if y_axis <= -0.5 and abs(x_axis) < 0.5:
                    direction = 'F'  # Adelante
                elif y_axis >= 0.5 and abs(x_axis) < 0.5:
                    direction = 'B'  # Atrás
                elif x_axis >= 0.5 and abs(y_axis) < 0.5:
                    direction = 'R'  # Derecha
                elif x_axis <= -0.5 and abs(y_axis) < 0.5:
                    direction = 'L'  # Izquierda
                else:
                    direction = 'S'  # Detener

                speed = speed_levels[current_speed_index]
                send_to_arduino(speed, direction)
            else:
                send_to_arduino(0, 'S')

        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == 1:  # B
                print("Quiting")
                running = False
            elif event.button == 2:  # X
                current_speed_index = (current_speed_index + 1) % len(speed_levels)

# Cierra el puerto serie
ser.close()