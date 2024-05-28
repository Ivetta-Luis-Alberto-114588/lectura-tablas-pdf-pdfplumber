import os
import sys
import pdfplumber
import pandas as pd

def obtener_archivos_directorio(directorio):
    """
    Esta función toma un directorio como entrada y devuelve una lista de todos los archivos en ese directorio.

    Primero, la función verifica si se está ejecutando como un ejecutable o como un script de Python. Si se está ejecutando como un ejecutable, establece el directorio del ejecutable como el directorio de trabajo. Si se está ejecutando como un script de Python, establece el directorio del script como el directorio de trabajo.

    Luego, la función obtiene el directorio padre del directorio proporcionado y une el directorio padre y el directorio proporcionado para obtener la ruta completa del directorio.

    Finalmente, la función lista todos los archivos en el directorio y devuelve esta lista.

    Parámetros:
    directorio (str): La ruta del directorio para listar los archivos.

    Devuelve:
    lista_archivos (list): Una lista de los nombres de los archivos en el directorio proporcionado.
    """
    
    dir_name = ""
    
    # si es un ejectuable, le establezco el directorio
    if getattr( sys, "frozen", False):
        dir_name= os.path.dirname(os.path.abspath(sys.executable))
    else:
        # si no es un ejecutable, le establezco el directorio del script actual
        dir_name = os.path.dirname(os.path.abspath(__file__))
    
    #directorio padre
    directorio_padre = os.path.dirname(os.path.abspath(directorio))
    
    #ruta completo
    directorio_destino = os.path.join(directorio_padre, directorio) 
    
    # print ("dir_name: ", dir_name)
    
    lista_nombre_archivos = os.listdir(directorio_destino)
    
    lista_directorio_y_nombre = []
    for item in lista_nombre_archivos:
        lista_directorio_y_nombre.append(os.path.join(directorio_destino, item))
    
    
    
    return lista_directorio_y_nombre


def encontrar_tablas(lista_pdf, titulo, palabras_buscadas):
    """
    Esta función recibe una lista de rutas de archivos PDF, un título y una palabra. Busca en cada archivo PDF
    las líneas que comienzan con el título especificado, y luego busca las líneas que comienzan con la palabra especificada.
    Devuelve una lista de las líneas que comienzan con la palabra especificada en cada archivo PDF después del título.

    Args:
        lista_pdf (list): Una lista de rutas a los archivos PDF en los que buscar.
        titulo (str): El título que debe aparecer antes de las líneas que comienzan con la palabra especificada.
        palabras_buscadas (str): La palabra con la que debe comenzar la línea después del título.

    Returns:
        list: Una lista de las líneas que comienzan con la palabra especificada en cada archivo PDF después del título.

    Ejemplo de uso:
        >>> encontrar_tablas(['ruta/a/tu/archivo1.pdf', 'ruta/a/tu/archivo2.pdf'], 'Titulo', 'Palabra')
    """
    # Inicializa una lista vacía para almacenar los resultados
    resultados = []

    # Recorre cada ruta de PDF
    for ruta_pdf in lista_pdf:
        # print(ruta_pdf)
        # Abre el archivo PDF
        with pdfplumber.open(ruta_pdf) as pdf:
            # Recorre cada página en el PDF
            for pagina in pdf.pages:
                # Extrae el texto de la página
                texto = pagina.extract_text()
                # Divide el texto en líneas
                lineas = texto.split('\n')
                # Inicializa una variable para rastrear si hemos encontrado el título
                titulo_encontrado = False
                # Inicializa una variable para almacenar los últimos 10 caracteres de la línea "PERIODO"
                periodo = None
                # Recorre cada línea
                for i, linea in enumerate(lineas):
                    # Si la línea comienza con "PERIODO"
                    if linea.startswith("PERIODO"):
                        # Almacena los últimos 10 caracteres de la línea
                        periodo = linea[-10:]
                    # Si la línea comienza con el título especificado
                    elif linea.startswith(titulo):
                        # Marca que hemos encontrado el título
                        titulo_encontrado = True
                    # Si hemos encontrado el título y la línea comienza con la palabra especificada
                    elif titulo_encontrado and linea.startswith(palabras_buscadas):
                        # Agrega la línea y el periodo a la lista de resultados
                        resultados.append(periodo + " " + linea)
                        # Rompe el bucle, ya que solo queremos el primer hallazgo después del título
                        break

    # Devuelve la lista de resultados
    return resultados

import pandas as pd

def generar_dataframe(lista):
    # Inicializa las listas para almacenar los datos
    periodos = []
    productos = []
    precios = []

    # Recorre cada elemento en la lista
    for elemento in lista:
        # Divide el elemento en tres partes
        periodo, _, resto = elemento.partition("a)")
        producto, _, resto = resto.partition("kg.")
        precio = resto.strip()

        # Agrega las partes a las listas correspondientes
        periodos.append(periodo.strip())
        productos.append(producto.strip())
        precios.append(precio)

    # Crea un DataFrame de pandas a partir de las listas
    df = pd.DataFrame({
        "periodo": periodos,
        "carne con hueso": productos,
        "precio": precios
    })

    # Devuelve el DataFrame
    print(df)
    return df





def ver_pdf(archivo, pagina):
    
    # https://github.com/jsvine/pdfplumber?tab=readme-ov-file
    pdf = pdfplumber.open(archivo)
    pagina = pdf.pages[pagina]
    
    #para ver la imagen pura, sin ningun tratamiento 
    imagen = pagina.to_image(resolution=150)
    # imagen.show()
    
    # ---------------- PARA VER VISUALMENTE QUE ES LO QUE ENCUENTRA PLUMBER
    # depuración visual para ver que tablas reconoce
    # las lineas rojas representa las lineas, los circulos azules son las intersecciones enter las lineas
    # los pintado de celeste representa las celdas
    # imagen.debug_tablefinder().show() #si no muestra lineas azules y rojas, no encontro nada
    
    # si no encuentra nada puedo empezar a parametrizar la busqueda con table_settings
    
    
    # ---------------------- PARA EXTRAER LAS PALABRAS SOLAMENTE
    
    # imagen.draw_rects(pagina.extract_words()).show()
    # imagen.draw_line(((60, 135), (60, 380)), stroke=(255, 0, 0), stroke_width=10).show()
    # draw_line es para dibujar una linea
    # draw_lines es para dibujar lineas
    # el primer parametro es la coordenada de inicio (x,y) y el segundo la coordenada de fin (x,y)
    # stroke es el color de la linea
    # stroke_width es el ancho de la linea
    
    recorte = imagen.draw_rect((85, 175, 510, 255), stroke=(255, 0, 0), stroke_width=10)
    # recorte.show()
    # draw_rect es para dibujar un rectangulo
    # draw_rects es para dibujar rectangulos
    pagina_recortada = pagina.within_bbox((85, 175, 510, 255))
    
    
    # draw_circle es para dibujar un circulo
    # draw_circles es para dibujar circulos

    
    # ---------------------------- TABLE_SETTINGS
    # parametrizar la deteccion de tablas con plumber
    table_settings = {
        "vertical_strategy": "text", #"lines", "lines_strict", "text", or "explicit"
        "horizontal_strategy": "text", #"lines", "lines_strict", "text", or "explicit"
        "snap_y_tolerance": 5,
        "intersection_x_tolerance": 1,
    }
    # imagen.reset().debug_tablefinder(table_settings).show()
    
    # ahora extraigo la tabla de acuerdo a table_settings
    # tablas = pagina.extract_tables(table_settings)
    # for row in tablas[:5]:
    #     print(row)
    
    
    
    # ------------------------- PARA EXTRAER LA TABLA    
    # tabla = pagina.extract_table()
    # if tabla is None:
    #     print("No existen tablas")
    # else:
    #     for item in tabla:
    #         print(item)
    
    # --------------------- PARA VER QUE ES LO QUE DETECTA 
    # para ver que tabla detecta plumber
    # imagen.reset()
    # imagen.debug_tablefinder().show()
    
    
   # ----------------------- PARAMETRIZAR LA BUSQUEDA 
    # parametrizar la deteccion de tablas con plumber
    # table_settings = {
        # "vertical_strategy": "text", #"lines", "lines_strict", "text", or "explicit"
        # "horizontal_strategy": "text", #"lines", "lines_strict", "text", or "explicit"
        # "snap_y_tolerance": 5,
        #"intersection_x_tolerance": 15,
    # }
    
    # imagen = imagen.reset().debug_tablefinder(table_settings)
    # imagen.show()
    
    #------------------------ EXTRAER PERIODO DE UNA ZONA EN PARTICULAR
    # corte = pagina.within_bbox((0, 129, pagina.width, 145))
    # corte.to_image().show()
    # texto = corte.extract_text()
    # print(texto)
    
    
    #------------------ DETECTAR TODOS LOS CARACTERES Y EXTRAER EL TEXTO
    #ahora se va a ver que caracarters detecta plumber
    # imagen.reset().draw_rects(pagina.chars).show()
    
    #ahora se a extraer todo el texto, incluyendo los espacios en blanco
    
    # text = pagina_recortada.extract_text(keep_blank_chars=True)
    # print(text)
    
    
    
    # ------------- PARA EXTRAER LA TABLA CON LOS SETTINGS QUE ANDABA
    # para extraer la tabla
    # table = pagina.extract_table(table_settings)
    
    # for item in table:
    #     print(item)
    
     
    # tablas_encontradas = pagina.extract_tables(table_settings)
    # cortada = tablas_encontradas[1:14]
    
    
 