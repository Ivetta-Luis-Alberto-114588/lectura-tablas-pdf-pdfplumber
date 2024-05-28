from funciones import obtener_archivos_directorio, encontrar_tablas, ver_pdf

lista_archivos = obtener_archivos_directorio('01-Pdf originales')
# print(lista_archivos)
uno = lista_archivos[0]

print(uno)

lista_filas = encontrar_tablas( lista_archivos, "a) Carne c/hueso")
for item in lista_filas:
    print (item)
    
# print("paso a ver pdf")
# input("presine una tecla para continuar")
    

ver_pdf(lista_archivos[0],1)
