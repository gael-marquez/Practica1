#!/usr/bin python3

import socket

HOST = "localhost"  # Hostname o  dirección IP del servidor
PORT = 65432  # Puerto del servidor
buffer_size = 1024

def imprimir(matriz_cl):
    # letras

    letras_ = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P"]
    print("   ", end=" ")
    for ii in range(num_cols):
        print(letras_[ii], end=" ")
    print()
    # formato de lineas
    print("  ", end=" ")
    for _ in range(num_cols):
        print("--", end="")
    print()

    # numeros
    for iii in range(num_cols):
        print((iii + 1), "|", end=" ")
        for jj in range(num_cols):
            print(matriz_cl[iii][jj], end=" ")
        print()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
    TCPClientSocket.connect((HOST, PORT))
    print("Conectando...")
    iniciar = ""
    while iniciar != "s":
        iniciar = input("¿Deseas iniciar el juego? (s/n): ").strip().lower()
    TCPClientSocket.sendall(b"INICIAR")
    print("Esperando confirmación del servidor...")

    data = TCPClientSocket.recv(buffer_size).decode("utf-8")
    if data == "Juego iniciado":
        print("--------------------------BUSCAMINAS--------------------------")
        estado = 0
        data = TCPClientSocket.recv(buffer_size).decode("utf-8")
        num_cols = int(data)
        print("col: ", data)
        if num_cols == 4:
            bombas = 10
        elif num_cols == 16:
            bombas = 40
        letras = "ABCDEFGHIJKLMNOP"[:num_cols]
        matriz_cliente = [["-" for _ in range(num_cols)] for _ in range(num_cols)]
        imprimir(matriz_cliente)
        while estado != 1:
            coordenada = input("Ingrese la coordenada (ejem. A1): ").upper().strip()
            entrada = coordenada.encode("utf-8")
            TCPClientSocket.sendall(entrada)
            data = TCPClientSocket.recv(buffer_size).decode("utf-8")
            if data == "OTRA":
                print("Ingresaste una casilla inexistente. Ingresa otra (ej. B2).")
            else:
                if data == "GAMEOVER":
                    print("PERDISTE. ¡PISASTE UNA BOMBA! Vuelve a intentarlo.")
                    for _ in range(bombas):
                        longitud = int(TCPClientSocket.recv(2).decode("utf-8"))
                        coordenada = TCPClientSocket.recv(longitud).decode("utf-8")
                        fila = int(coordenada[0])
                        columna = int(coordenada[1:])
                        matriz_cliente[fila][columna] = "X"
                    tiempo_jugad = TCPClientSocket.recv(4).decode("utf-8")
                    print(f"Tiempo jugado  {tiempo_jugad} segundos!")
                    estado = 1

                elif data == "DESCUBIERTA":
                    print("Casilla descubierta.")
                    letra = coordenada[0]
                    numero = coordenada[1:]
                    numero = int(numero)
                    fila = numero - 1  # Convertir a índice de matriz
                    columna = letras.index(letra)  # Convertir la letra a índice de matriz
                    columna = int(columna)
                    matriz_cliente[fila][columna] = 0
                elif data == "REPETIDO":
                    print("Ingresaste una casilla repetida. Intenta con otra.")
                elif data == "GANASTE":
                    # print("""
                    #   (`\ .-') /`               .-') _  ,---. ,---. ,---.
                    #    `.( OO ),'              ( OO ) ) |   | |   | |   |
                    # ,--./  .--.    ,-.-')  ,--./ ,--,'  |   | |   | |   |
                    # |      |  |    |  |OO) |   \ |  |\  |   | |   | |   |
                    # |  |   |  |,   |  |  \ |    \|  | ) |   | |   | |   |
                    # |  |.'.|  |_)  |  |(_/ |  .     |/  |  .' |  .' |  .'
                    # |         |   ,|  |_.' |  |\    |   `--'  `--'  `--'
                    # |   ,'.   |  (_|  |    |  | \   |   .--.  .--.  .--.
                    # '--'   '--'    `--'    `--'  `--'   '--'  '--'  '--'
                    # """)
                    print("-------GANASTE EL BUSCAMINAS-------")
                    tiempo_jugado = TCPClientSocket.recv(4).decode("utf-8")  # Recibir y decodificar el tiempo
                    print(f"Lo hiciste en {tiempo_jugado} segundos!")

                    break
                imprimir(matriz_cliente)