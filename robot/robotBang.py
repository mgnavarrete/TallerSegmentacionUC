import numpy as np
import cv2
from cv2 import HoughCircles
import serial
from time import sleep
from pid import PID


nCam = 1 # Valor de la camara, 0 es la del notebook
cap = cv2.VideoCapture(nCam) 	
cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
cv2.resizeWindow('frame', 640, 480)
cv2.moveWindow('frame', 30, 100)

cv2.namedWindow('mask', cv2.WINDOW_NORMAL)
cv2.resizeWindow('mask', 640, 480)
cv2.moveWindow('mask', 1000, 100)

colorFront = [110, 193, 155]
colorBack =  [74, 131, 140]
colorGoal =  [ 33, 149, 180]

							#H   S   V
LowerColorError = np.array([-20,-35,-35]) 
UpperColorError = np.array([20,35,35])  


width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fov = 60  # Ángulo de visión horizontal de la cámara en grados
focal_length = (width // 2) / np.tan(fov * 0.5 * (np.pi / 180))   # Distancia focal de la cámara en píxeles
real_diameter_mm = 70  # 100 mm
real_diameter = real_diameter_mm / 1000


def detect_circle(image, mask):

    circles = HoughCircles(mask, cv2.HOUGH_GRADIENT, 1.2, 100, param1=5, param2=5, minRadius=0, maxRadius=20)
    
    if circles is not None:
        circles = np.uint16(np.around(circles))
        # print("Se encontró un círculo")
        for i in circles[0,:]:
            # Dibujar el círculo y el centro
            cv2.circle(image, (i[0], i[1]), i[2], (0, 255, 0), 2)
            cv2.circle(image, (i[0], i[1]), 2, (0, 0, 255), 3)
            return i[0], i[1], i[2]
    return None, None, None

def real_coordinates(pixel_coordinates, focal_length, real_diameter, pixel_radius):
    x_pixel, y_pixel = pixel_coordinates
    real_distance = (real_diameter * focal_length) / (2 * pixel_radius)
    real_x = (x_pixel - width / 2) * real_distance / focal_length
    real_y = (y_pixel - height / 2) * real_distance / focal_length
    return real_x, real_y

def angle_between_vectors(v1, v2):
    dot_product = np.dot(v1, v2)
    v1_magnitude = np.linalg.norm(v1)
    v2_magnitude = np.linalg.norm(v2)
    
    if v1_magnitude == 0 or v2_magnitude == 0:
        return 0.0

    cos_angle = dot_product / (v1_magnitude * v2_magnitude)
    angle_rad = np.arccos(cos_angle)
    angle_deg = np.degrees(angle_rad)

    # Calcular el vector perpendicular a v1 en sentido horario
    v1_perp = np.array([v1[1], -v1[0]])

    # Calcular el producto escalar entre v1_perp y v2
    dot_product_perp = np.dot(v1_perp, v2)

    # Si el producto escalar es positivo, el ángulo es negativo
    if dot_product_perp > 0:
        angle_deg = -angle_deg

    return angle_deg

ser = serial.Serial('COM15', 9600)  # Cambiar 'COM1' por el puerto serie correspondiente

def send_to_arduino(value, direction):
    ser.write(f"{value},{direction}\n".encode('utf-8'))

margen = 15

vmax = 255
vmin = 130

V = 150


		
while(True):

	ret, frame = cap.read()	
	# Convert BGR to HSV
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	LowerColor1 = colorFront + LowerColorError
	UpperColor1 = colorFront + UpperColorError	

	Color1Mask = cv2.inRange(hsv, LowerColor1, UpperColor1)
	Color1Res = cv2.bitwise_and(frame,frame, mask= Color1Mask)

	LowerColor2 = colorBack + LowerColorError
	UpperColor2 = colorBack + UpperColorError

	Color2Mask = cv2.inRange(hsv, LowerColor2, UpperColor2)
	Color2Res = cv2.bitwise_and(frame,frame, mask= Color2Mask)

	LowerColor3 = colorGoal + LowerColorError
	UpperColor3 = colorGoal + UpperColorError

	Color3Mask = cv2.inRange(hsv, LowerColor3, UpperColor3)
	Color3Res = cv2.bitwise_and(frame,frame, mask= Color3Mask)


	xf, yf, radiusf = detect_circle(frame, Color1Mask)
	xb, yb, radiusb = detect_circle(frame, Color2Mask)
	xg, yg, radiusg = detect_circle(frame, Color3Mask)

	res = Color1Res + Color2Res + Color3Res
		
	if xf is not None and yf is not None and xb is not None and yb is not None:
		cv2.line(frame, (xf, yf), (xb, yb), (0, 0, 255), 2)
		
	if xf is not None and yf is not None and xg is not None and yg is not None:
		cv2.line(frame, (xf, yf), (xg, yg), (0, 0, 255), 2)

	if xb is not None and yb is not None and xg is not None and yg is not None:
		cv2.line(frame, (xb, yb), (xg, yg), (0, 0, 255), 2)

	if xb is not None and yb is not None and xf is not None and yf is not None and xg is not None and yg is not None:
		
		real_xa, real_ya = real_coordinates((xb, yb), focal_length, real_diameter, radiusb)
		real_xb, real_yb = real_coordinates((xf, yf), focal_length, real_diameter, radiusf)
		real_xc, real_yc = real_coordinates((xg, yg), focal_length, real_diameter, radiusg)
		
		# Definimos los vectores BA y BC en coordenadas reales
		vector_ba = np.array([real_xb - real_xa, real_yb - real_ya])
		vector_bc = np.array([real_xc - real_xa, real_yc - real_ya])
		
		angle = angle_between_vectors(vector_ba, vector_bc)

		info_text = f"angulo: {angle}"
		font = cv2.FONT_HERSHEY_SIMPLEX
		scale = 1
		thickness = 2
		color = (0, 255, 255)  # Color en formato BGR (Cyan)
		x_offset = 50
		y_offset = 30
		cv2.putText(frame, info_text, (x_offset, y_offset), font, scale, color, thickness, cv2.LINE_AA)
		
       

		if -margen < angle < margen:
			
			print("Going Forward")
			send_to_arduino(255, 'F')  # Ajustar la velocidad según la necesidad (0 a 255)

		elif angle < -margen:
			print("Going Left")
			send_to_arduino(V, 'L')  # Ajustar la velocidad según la necesidad (0 a 255)

		elif angle > margen:
			print("Going Right")
			send_to_arduino(V, 'R')  # Ajustar la velocidad según la necesidad (0 a 255)

			

	else:
		print("No se objetivo")
		send_to_arduino(0, 'S')


	cv2.imshow('frame',frame)
	cv2.imshow('mask',res)
		
	if cv2.waitKey(1) & 0xFF == 27:
		send_to_arduino(0, 'S')

		break


cap.release() # Cuando se termina el programa, se libera la camara por parte del software
cv2.destroyAllWindows()