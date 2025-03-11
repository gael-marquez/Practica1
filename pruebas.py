import random

def imprimir(matriz_imp):
    #letras
    letras  = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P"]
    print("   ", end=" ")
    for ii in range(num_cols):
        print(letras[ii],  end=" ")
    print()
    # formato de lineas
    print("  ", end=" ")
    for _ in range(num_cols):
        print("--",  end="")
    print()

    #numeros
    for iii in range(num_rows):
        print((iii+1), "|", end=" ")
        for jj in range(num_cols):
            print(matriz_imp[iii][jj], end=" ")
        print()


def coordenadas():
    letras = "ABCDEFGHIJKLMNOP"[:num_cols]  # Ajusta a la cantidad de columnas
    while True:
        entrada = input("Ingrese la coordenada (ejem. A1): ").upper().strip()

        if len(entrada) < 2 or len(entrada) > 3:  # Para casos como 'A1' o 'A10'
            print("Coordenadas incorrectas, debe tener una letra y un número válido. Ejemplo: B3")
            # return coordenada incorrecta

            continue

        letra = entrada[0]
        numero = entrada[1:]

        if letra not in letras:
            print(f"Coordenadas incorrecta, la letra debe estar entre {letras[0]} y {letras[-1]}.")
            # return coordenada incorrecta
            continue

        if not numero.isdigit():
            print("Coordenadas incorrecta, debe poner un número después de la letra.")
            # return coordenada incorrecta
            continue

        numero = int(numero)

        if numero < 1 or numero > num_rows:
            print(f"Coordenada incorrecta, el número debe estar entre 1 y {num_rows}.")
            # return coordenada incorrecta
            continue

        fila = numero - 1  # Convertimos a índice de matriz
        columna = letras.index(letra)  # Convertimos la letra a índice de matriz
        return fila, columna

while True:
    try:
        dificultad = int(input(
            "Seleccione su dificultad, 1 para principiante (9x9 y 10 bombas), 2 para experto (16x16, 40 bombas): "))
        if dificultad in [1, 2]:
            break
        else:
            print("Por favor, ingrese 1 o 2.")
    except ValueError:
        print("Entrada no válida. Ingrese un número.")

if dificultad == 1:
    num_rows = 9
    num_cols = 9
    bombas = 10
else:
    num_rows = 16
    num_cols = 16
    bombas = 40

matriz = [[0 for _ in range(num_cols)] for _ in range(num_rows)]
aux = 0

while aux < bombas:
    for i in range(num_rows):
        for j in range(num_cols):
            if aux < bombas:
                rand = random.randint(0, 5)
                if rand == 0 and matriz[i][j] == 0:
                    matriz[i][j] = 1
                    aux += 1
    print("Colocación de bombas: ", aux)
imprimir(matriz)


estado = 0

while estado == 0:
    fila_eleg, col_eleg = coordenadas()
    if matriz[fila_eleg][col_eleg] == 1:
       print("¡Pisaste una bomba! Perdiste.")
       matriz[fila_eleg][col_eleg] = 3
       estado = 1
       continue
    elif matriz[fila_eleg][col_eleg] == 0:
        print("Casilla descubierta")
        matriz[fila_eleg][col_eleg] = 2
    else:
        print("La casilla ya estaba descubierta, elige otra")
    imprimir(matriz)
