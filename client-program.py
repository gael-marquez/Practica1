#!/usr/bin python3

import socket

HOST = "localhost"  # Hostname o  dirección IP del servidor
PORT = 65432  # Puerto del servidor
buffer_size = 1024

def imprimir(matriz_cliente):
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
    for iii in range(num_cols):
        print((iii + 1), "|", end=" ")
        for jj in range(num_cols):
            print(matriz_cliente[iii][jj], end=" ")
        print()

def descubrir():
    print("")
    #descurbir matriz

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
    TCPClientSocket.connect((HOST, PORT))
    print("Conectando...")
    iniciar = input("¿Deseas iniciar el juego? (s/n): ").strip().lower()
    if iniciar == "s":
        TCPClientSocket.sendall(b"INICIAR")
        print("Esperando confirmación del servidor...")

    data = TCPClientSocket.recv(buffer_size).decode("utf-8")
    if data == "Juego iniciado":
        print("--------------------------BUSCAMINAS--------------------------")
        estado = 0
        data = TCPClientSocket.recv(buffer_size).decode("utf-8")
        num_cols = int(data)
        print("col: ", data)
        matriz_cliente = [["-" for _ in range(num_cols)] for _ in range(num_cols)]
        imprimir(matriz_cliente)
        while estado != 1:
            entrada = input("Ingrese la coordenada (ejem. A1): ").upper().strip().encode("utf-8")
            TCPClientSocket.sendall(entrada)
            data = TCPClientSocket.recv(buffer_size).decode("utf-8")
            if data == "GAMEOVER":
                print("PERDISTE. ¡PISASTE UNA BOMBA! Vuelve a intentarlo.")
                estado = 1
            elif data == "DESCUBIERTA":
                print("Casilla descubierta.")
                estado = 2
            elif data == "OTRA":
                print("Ingresaste una casilla incorrecta. Intenta con otra. Ejem. (A1)")


