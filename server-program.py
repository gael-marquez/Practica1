#!/usr/bin python3
import socket, random
import time

HOST = "localhost"  # Direccion de la interfaz de loopback estándar (localhost)
PORT = 65432  # Puerto que usa el cliente  (los puertos sin provilegios son > 1023)
buffer_size = 1024

def imprimir(matriz_imp):
    # letras
    letras = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P"]
    print("   ", end=" ")
    for ii in range(num_cols):
        print(letras[ii], end=" ")
    print()
    # formato de lineas
    print("  ", end=" ")
    for _ in range(num_cols):
        print("--", end="")
    print()

    # numeros
    for iii in range(num_rows):
        print((iii + 1), "|", end=" ")
        for jj in range(num_cols):
            print(matriz_imp[iii][jj], end=" ")
        print()

#quitar whiles, ciclo infinito
def coordenadas(entrada):
    letras = "ABCDEFGHIJKLMNOP"[:num_cols]  # Ajusta a la cantidad de columnas
    if len(entrada) < 2 or len(entrada) > 3:  # Para casos como 'A1' o 'A10'
        print("Coordenadas incorrectas, debe tener una letra y un número válido. Ejemplo: B3")
        # return coordenada incorrecta
        return -1, -1

    letra = entrada[0]
    numero = entrada[1:]

    if letra not in letras:
        print(f"Coordenadas incorrecta, la letra debe estar entre {letras[0]} y {letras[-1]}.")
        # return coordenada incorrecta
        return -1, -1

    if not numero.isdigit():
        print("Coordenadas incorrecta, debe poner un número después de la letra.")
        # return coordenada incorrecta
        return -1, -1

    numero = int(numero)

    if numero < 1 or numero > num_rows:
        print(f"Coordenada incorrecta, el número debe estar entre 1 y {num_rows}.")
        # return coordenada incorrecta
        return -1, -1

    fila = numero - 1  # Convertimos a índice de matriz
    columna = letras.index(letra)  # Convertimos la letra a índice de matriz
    return fila, columna

def buscamina(fila, columna, tamano):
    _estado = 0
    ganaste = 1
    for i_ in range(tamano):
        for j_ in range(tamano):
            if matriz[i_][j_] == 0:
                ganaste = 0
    if ganaste == 0:
        if matriz[fila][columna] == 1:
            print("¡Pisaste una bomba! Perdiste.")
            matriz[fila][columna] = 3
            _estado = 1
        elif matriz[fila][columna] == 0:
            print("Casilla descubierta")
            matriz[fila][columna] = 2
            _estado = 2
        else:
            print("La casilla ya estaba descubierta, elige otra")
            _estado = 3
        imprimir(matriz)
    elif ganaste == 1:
        print("El jugador ganó!")
        _estado = 4
    return _estado


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
    TCPServerSocket.bind((HOST, PORT))
    TCPServerSocket.listen()
    print("Esperando conexión...")
    Client_conn, Client_addr = TCPServerSocket.accept()
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
        #juego preparado
    imprimir(matriz)

    #Empieza conexión
    with Client_conn:
        print("Conectado a", Client_addr)
        while True:
            try:
                data = Client_conn.recv(buffer_size).decode("utf-8")
                if data == "INICIAR":
                    print("El cliente ha iniciado el juego.")
                    Client_conn.sendall(b"Juego iniciado")
                    tamano_matriz = str(num_cols).encode("utf-8")
                    Client_conn.sendall(tamano_matriz)
                    inicio = time.time()
                    estado = 0
                    while estado != 1:
                        data = Client_conn.recv(buffer_size).decode("utf-8")
                        print("coordenada enviada: ", data)
                        fila_eleg, col_eleg = coordenadas(data)
                        msj = ""
                        if fila_eleg != -1 and col_eleg != -1:
                            estado = buscamina(fila_eleg, col_eleg, num_cols)
                            if estado == 1:
                                msj = "GAMEOVER"
                            elif estado == 2:
                                msj = "DESCUBIERTA"
                            elif estado == 3:
                                msj = "REPETIDO"
                            elif estado == 4:
                                msj = "GANASTE"
                                Client_conn.sendall(msj.encode("utf-8"))
                                break
                        else:
                            msj = "OTRA"
                        Client_conn.sendall(msj.encode("utf-8"))
                        if estado == 1:
                            # Se envían todos los valores de las bombas
                            for i in range(num_rows):
                                for j in range(num_cols):
                                    if matriz[i][j] == 1 or matriz[i][j] == 3:
                                        bomba = f"{i}{j}"
                                        longitud = f"{len(bomba):02}".encode("utf-8")
                                        Client_conn.sendall(longitud)  # Enviar la longitud de la coordenada
                                        Client_conn.sendall(bomba.encode("utf-8"))  # Enviar la coordenada
                        fin = time.time()
                        duracion = fin - inicio
                        Client_conn.sendall(msj.encode("utf-8"))
                        print("Duración: %.2f" % duracion)
                    break
            except ConnectionResetError:
                print("Conexión perdida.")
                break