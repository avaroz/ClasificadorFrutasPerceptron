import random
import matplotlib.pyplot as plt
import numpy as np
import cv2, imutils, os
import time,serial

# Establece la conexión con el Arduino
arduino = serial.Serial('COM5', 9600) 

# Función para mover el servo en una dirección específica
def mover_servo(direccion):
    arduino.write(str(direccion).encode())
    time.sleep(2)  # Espera 2 segundos para que el servo se mueva

# Definición de clases
class DatosEntrenamiento:
    def __init__(self, R, G, B, clase):
        self.R = R
        self.G = G
        self.B = B
        self.clase = clase

class DatosVerificacion:
    def __init__(self, R, G, B):
        self.R = R
        self.G = G
        self.B = B

class Perceptron:
    K_A = 0.05  # Constante de aprendizaje
    Bias = 1    # Entrada del bias

    def __init__(self, cantidad):
        self.Peso_Entrada = [0.0] * 3  # Pesos para las entradas
        self.Peso_Bias = 0.0            # Peso para el bias
        self.n = cantidad
        self.Generador_RandomPesos()

    def Entrenamiento(self, Datos_Entrada, Epocas):
        Fase_Entrenamiento = "\n-------FASE ENTRENAMIENTO------"
        Cantidad_Datos = len(Datos_Entrada)
        errores = []  # Lista para almacenar los errores por época

        for i in range(Epocas):
            Fase_Entrenamiento += "\nEpoca N° " + str(i + 1) + ""
            error_epoca = 0

            for j in range(Cantidad_Datos):
                ObtuveEntradas = [Datos_Entrada[j].R, Datos_Entrada[j].G, Datos_Entrada[j].B]
                ValorObtenido = self.Funcion_Activacion(self.sumatoria(ObtuveEntradas))
                error = Datos_Entrada[j].clase - ValorObtenido
                error_epoca += abs(error)

                for k in range(self.n):
                    self.Peso_Entrada[k] += self.K_A * error * ObtuveEntradas[k]

                self.Peso_Bias += self.K_A * error * self.Bias

            errores.append(error_epoca)

        plt.plot(range(1, Epocas + 1), errores, marker='o')
        plt.title('Épocas vs. Error')
        plt.xlabel('Época')
        plt.ylabel('Error')
        plt.grid(True)
        plt.show()

        return Fase_Entrenamiento

    def Verificacion(self, Datos_verificacion):
        ObtuveEntradas = [Datos_verificacion.R, Datos_verificacion.G, Datos_verificacion.B]
        ValorVerificacion = self.Funcion_Activacion(self.sumatoria(ObtuveEntradas))
        return ValorVerificacion

    def sumatoria(self, entradas):
        sum = 0
        for o in range(self.n):
            sum += entradas[o] * self.Peso_Entrada[o]
        sum += self.Peso_Bias
        return sum

    def Funcion_Activacion(self, sum):
        return 1 if sum >= 0 else -1

    def Generador_RandomPesos(self):
        for p in range(self.n):
            self.Peso_Entrada[p] = random.uniform(-1, 1)
        self.Peso_Bias = random.uniform(-1, 1)

# Principal
if __name__ == "__main__":
    Datos = 'imagenes'
    if not os.path.exists(Datos):
        print('Carpeta creada:', Datos)
        os.makedirs(Datos)

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    # Inicializar perceptrón
    perceptron = Perceptron(3)

    x1, y1 = 190, 80
    x2, y2 = 450, 398

    count = 0
    informacion_colores = []

    while True:
        ret, frame = cap.read()
        if ret == False:
            break

        imAux = frame.copy()
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
        area_cuadro = frame[y1:y2, x1:x2]
        color_promedio = np.mean(np.mean(area_cuadro, axis=0), axis=0).astype(int)
        color_rgb = (color_promedio[2], color_promedio[1], color_promedio[0])
        cv2.putText(frame, f'Color: ({color_promedio[2]}, {color_promedio[1]}, {color_promedio[0]})', (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow('frame', frame)

        k = cv2.waitKey(1)
        if k == ord('t'):
            cv2.imwrite(Datos + '/objeto_{}.jpg'.format(count), area_cuadro)
            print('Imagen guardada:' + '/objeto_{}.jpg'.format(count))
            count = count + 1
            print(f'Color capturado: RGB({color_rgb[0]}, {color_rgb[1]}, {color_rgb[2]})')
            
            informacion_colores.append(color_rgb)
            
        if k == ord('m'):
            print("Información de colores capturados:")
            matriz_colores = np.array(informacion_colores)
            print(matriz_colores)

        if k == ord('e'):
            print("Iniciando entrenamiento del perceptrón...")
            matriz_entrenamiento = np.array(informacion_colores)
            datos_entrenamiento = []
            
            
            for idx, color_rgb in enumerate(matriz_entrenamiento):
                R, G, B = color_rgb
                if idx < 5:  # Los primeros 10 datos son "correctos"
                    clase = 1
                else:  # Los demás datos son "incorrectos"
                    clase = -1
                datos_entrenamiento.append(DatosEntrenamiento(R, G, B, clase))
                
            entrenamiento_perceptron = perceptron.Entrenamiento(datos_entrenamiento, 30)
            print(entrenamiento_perceptron)

        if k == ord('v'):
            print("Realizando verificación del perceptrón...")
            if len(informacion_colores) > 0:
                #color_verificar = informacion_colores[-1]
                #print(f'Color capturado: RGB({color_verificar[0]}, {color_verificar[1]}, {color_verificar[2]})')
                print(f'Color capturado: RGB({color_rgb[0]}, {color_rgb[1]}, {color_rgb[2]})')
                color_rgb = (color_promedio[2], color_promedio[1], color_promedio[0])
                # Convertir el último color capturado en una matriz 1x3
                matriz_color_verificar = np.array([color_rgb])
                print("Matriz del color a verificar:")
                print(matriz_color_verificar)
                valor_clase = perceptron.Verificacion(DatosVerificacion(matriz_color_verificar[0][0], matriz_color_verificar[0][1], matriz_color_verificar[0][2]))
                if valor_clase == 1:
                    print("El perceptrón clasifica este color como Clase 1.")
                    mover_servo(1)
                else:
                    print("El perceptrón clasifica este color como Clase -1.")
                    mover_servo(2)
            else:
                print("No hay datos para verificar. Captura al menos un color antes de verificar.")

        if k == ord('q'):
            print("Saliendo")
            break

    cap.release()
    cv2.destroyAllWindows()
