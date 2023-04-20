# Se importan las librerías necesarias
import numpy as np
import cv2
from cv2 import HoughCircles

# Se establece el valor de la cámara, 0 es la cámara del notebook
nCam = 0

# Se crea un objeto VideoCapture para capturar video de la cámara especificada
cap = cv2.VideoCapture(nCam) 

# Se definen las matrices de numpy con valor de color inicial de 0 para las variables color1_hsv, color2_hsv y color3_hsv
color1_hsv = [110, 193, 155]
color2_hsv = [74, 131, 140]
color3_hsv = [ 33, 149, 180]

# Se definen los rangos de colores permitidos para la detección de objetos
LowerColorError = np.array([-30,-35,-35]) 
UpperColorError = np.array([30,35,300])  

# Se crea una ventana de visualización para la imagen original y la imagen segmentada de los tres colores
cv2.namedWindow('Imagen Original',  cv2.WINDOW_NORMAL )   
cv2.resizeWindow('Imagen Original', 640, 480)
cv2.moveWindow('Imagen Original', 30, 100)

cv2.namedWindow('Imagen Segmentada',  cv2.WINDOW_NORMAL)
cv2.resizeWindow('Imagen Segmentada', 640, 480)    
cv2.moveWindow('Imagen Segmentada', 700, 100)


def detect_circle(image, mask):

    circles = HoughCircles(mask, cv2.HOUGH_GRADIENT, 1.2, 100, param1=5, param2=5, minRadius=0, maxRadius=0)
    
    if circles is not None:
        circles = np.uint16(np.around(circles))
        # print("Se encontró un círculo")
        for i in circles[0,:]:
            # Dibujar el círculo y el centro
            cv2.circle(image, (i[0], i[1]), i[2], (0, 255, 0), 2)
            cv2.circle(image, (i[0], i[1]), 2, (0, 0, 255), 3)
            return i[0], i[1], i[2]
    return None, None, None
            
while(True):
    # Se lee un frame de la cámara
    ret, frame = cap.read()    
    
    # Se convierte el frame capturado a formato HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Se definen los límites de color permitidos para la detección de objetos para los tres colores
    LowerColor1 = color1_hsv + LowerColorError
    UpperColor1 = color1_hsv + UpperColorError    
    
    LowerColor2 = color2_hsv + LowerColorError
    UpperColor2 = color2_hsv + UpperColorError    
    
    LowerColor3 = color3_hsv + LowerColorError
    UpperColor3 = color3_hsv + UpperColorError    
    
    # Se aplican máscaras de color para detectar objetos para los tres colores
    Color1Mask = cv2.inRange(hsv, LowerColor1, UpperColor1)
    Color1Res = cv2.bitwise_and(frame,frame, mask= Color1Mask)

    Color2Mask = cv2.inRange(hsv, LowerColor2, UpperColor2)
    Color2Res = cv2.bitwise_and(frame,frame, mask= Color2Mask)

    Color3Mask = cv2.inRange(hsv, LowerColor3, UpperColor3)
    Color3Res = cv2.bitwise_and(frame,frame, mask= Color3Mask)

    # Se suman las imágenes segmentadas de los tres colores en una sola imagen
    SumRes = cv2.add(Color1Res, Color2Res)
    SumRes = cv2.add(SumRes, Color3Res)

    # Se detectan círculos en la imagen segmentada
    xf, yf, radiusf = detect_circle(frame, Color1Mask)
    xb, yb, radiusb = detect_circle(frame, Color2Mask)
    xg, yg, radiusg = detect_circle(frame, Color3Mask)

    if xf is not None and yf is not None and xb is not None and yb is not None:
        cv2.line(frame, (xf, yf), (xb, yb), (0, 0, 255), 2)
        
    if xf is not None and yf is not None and xg is not None and yg is not None:
        cv2.line(frame, (xf, yf), (xg, yg), (0, 0, 255), 2)

    if xb is not None and yb is not None and xg is not None and yg is not None:
        cv2.line(frame, (xb, yb), (xg, yg), (0, 0, 255), 2)

    # Se muestran las imágenes original y segmentada en las ventanas correspondientes
    cv2.imshow('Imagen Original',frame)    
    cv2.imshow('Imagen Segmentada',SumRes)

    # Si se presiona la tecla ESC, se cierran las ventanas y se libera la cámara
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Se libera la cámara cuando se termina el programa
cap.release()
# Se cierran todas las ventanas
cv2.destroyAllWindows()
