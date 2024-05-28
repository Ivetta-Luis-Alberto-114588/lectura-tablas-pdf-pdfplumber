from funciones import obtener_archivos_directorio, encontrar_tablas, ver_pdf, generar_dataframe

# busca los archivos pdf en el directorio
lista_archivos = obtener_archivos_directorio('01-Pdf originales')

# sobre los archivos encontrados busca las tablas que contienen la palabra "VACUNA" y despues LA PRIMER "a) Carne c/hueso"
lista_filas_buscadas = encontrar_tablas( lista_archivos,"VACUNA" ,"a) Carne c/hueso")
# print(lista_filas_buscadas)
    
#solo a los efectos de conocer pdfplumber
# ver_pdf(lista_archivos[0],1)

generar_dataframe(lista_filas_buscadas)
