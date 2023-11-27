import matplotlib.pyplot as plt
import requests
from io import BytesIO
import base64

from rentcar.utils import getCompaniesSortByProfits



def generar_grafico():
    
    data = getCompaniesSortByProfits()

    x_datos = [item[0] for item in data] 
    y_datos = [item[1] for item in data] 

    # Crear el gráfico
    plt.bar(x_datos, y_datos)

    # Guardar el gráfico en un BytesIO
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)

    # Convertir la imagen a base64 para incrustarla en la plantilla
    img_str = "data:image/png;base64," + base64.b64encode(image_stream.read()).decode("utf-8")

    return img_str