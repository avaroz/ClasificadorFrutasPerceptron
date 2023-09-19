"""
Este archivo recibe una foto
Luego recorta una parte en un rango desde el centro
Obtiene esos datos y los guarda en un excel.
"""
# importar libreria mumpy
import numpy as np
# Importar librería cv2
import cv2
# Importamos la libreria para acortar rutas
import os
dirname = os.path.dirname(__file__)
from pathlib import Path
# Importamos la libreria para guardar archivos en excel.
import pandas as pd

filename = Path(__file__).parent.parent / 'fotos/limones/limon_01.jpg'
def extraerdatosfoto (archivo, tipofruta):
    # Leer la imagen
    # Usamos str para pasar de instancia Path a cadena.
    imagen = cv2.imread(str(archivo))

    # Obtener las dimensiones de la imagen
    alto, ancho, canales = imagen.shape

    # Calcular las coordenadas del centro de la imagen
    centro_x = ancho // 2
    centro_y = alto // 2

    # Calcular las coordenadas del rectángulo de 7 x 7 píxeles que rodea al centro
    inicio_x = centro_x - 3
    fin_x = centro_x + 4
    inicio_y = centro_y - 3
    fin_y = centro_y + 4

    # Extraer el subarray de la imagen que corresponde al rectángulo
    subimagen = imagen[inicio_y:fin_y, inicio_x:fin_x]

    # Mostrar o guardar el subarray extraído en la carpeta resultados
    #cv2.imshow("Subimagen", subimagen)
    #rutaimagen = Path(__file__).parent.parent / 'resultados/fotocortada.jpg'
    #cv2.imwrite(str(rutaimagen), subimagen)

    
    #Pasamos el arreglo de 3 dimensiones a 2
    m,n,r = subimagen.shape
    out_arr = np.column_stack((np.repeat(np.arange(m),n),subimagen.reshape(m*n,-1)))
    df = pd.DataFrame(out_arr)

    #Establecemos la ruta del excel
    rutaexcel = str(Path(__file__).parent.parent) + '/datos/' + tipofruta + '.xlsx'
    
    #Guardamos los datos pero borramos los existentes
    #df.to_excel(str(rutaexcel),sheet_name='datos', index=False)

    #Guardamos los datos en excel abajo de los ya existentes
    excel_file = pd.read_excel(rutaexcel, sheet_name='datos')
    df_concat = pd.concat([excel_file, df])
    df_concat.to_excel(rutaexcel, sheet_name='datos')

    return 'completado'

extraerdatosfoto(filename, 'papas')