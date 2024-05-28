https://github.com/jsvine/pdfplumber?tab=readme-ov-file

```python
import pdfplumber
pdf = pdfplumber.open(archivo)
pagina = pdf.pages[pagina]

#para ver la imagen pura, sin ningun tratamiento 
imagen = pagina.to_image(resolution=300)
imagen.show()
```

![](C:\Users\Usuario-\AppData\Roaming\marktext\images\2024-05-28-11-04-21-image.png)

```python
# depuración visual para ver que tablas reconoce
# las lineas rojas representa las lineas, los circulos azules son las intersecciones enter las lineas
# los pintado de celeste representa las celdas
imagen.debug_tablefinder().show() #si no muestra lineas azules y rojas, no encontro nada

# si no encuentra nada puedo empezar a parametrizar la busqueda con table_settings
```

![](C:\Users\Usuario-\AppData\Roaming\marktext\images\2024-05-28-11-06-50-image.png)

    

```python
 # parametrizar la deteccion de tablas con plumber
    table_settings = {
        "vertical_strategy": "text", #"lines", "lines_strict", "text", or "explicit"
        "horizontal_strategy": "text", #"lines", "lines_strict", "text", or "explicit"
        "snap_y_tolerance": 5,
        "intersection_x_tolerance": 1,
    }
imagen.reset().debug_tablefinder(table_settings).show()
```

![](C:\Users\Usuario-\AppData\Roaming\marktext\images\2024-05-28-11-09-17-image.png)

```python
    # ahora extraigo la tabla de acuerdo a table_settings
    tablas = pagina.extract_tables(table_settings)
    for row in tablas[:5]:
        print(row)  

   # se va a observar que respeta exactamente lo que encontro con table_settings
```

![](C:\Users\Usuario-\AppData\Roaming\marktext\images\2024-05-28-11-12-33-image.png)