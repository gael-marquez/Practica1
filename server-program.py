#!/usr/bin python3
import socket, random
HOST = "localhost"  # Direccion de la interfaz de loopback estándar (localhost)
PORT = 65432  # Puerto que usa el cliente  (los puertos sin provilegios son > 1023)
buffer_size = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
    TCPServerSocket.bind((HOST, PORT))
    TCPServerSocket.listen()
    while True:
        try:
            dificultad = int(input("Seleccione su dificultad, 1 para principiante (9x9 y 10 bombas), 2 para experto (16x16, 40 bombas): "))
            if dificultad in [1, 2]:
                break
            else:
                print("Por favor, ingrese 1 o 2.")
        except ValueError:
            print("Entrada no válida. Ingrese un número.")

    if dificultad == 2:
        num_rows = 9
        num_cols = 9
        bombas = 10
    else:
        num_rows = 16
        num_cols = 16
        bombas = 40
    matriz = []
    for i in range(num_rows):
        aux = 0
        matriz.append([])
        for j in range(num_cols):
            rand = (random.randint(0, 100) % 3)
            if aux <= bombas and rand == 0:
                matriz[i].append(1)
                aux += aux
            else:
                matriz[i].append(0)

    #impresión:
    for i in range(num_cols):
        for j in range(num_rows):
            print(matriz[j][i], end=" ")
        print()


    #Conexión:
    Client_conn, Client_addr = TCPServerSocket.accept()
    with Client_conn:
        print("Conectado a", Client_addr)
        while True:
            print("Esperando a recibir datos... ")
            data = Client_conn.recv(buffer_size)
            print ("Recibido,", data,"   de ", Client_addr)
            if not data:
                break
            print("Enviando respuesta a", Client_addr)
            Client_conn.sendall(data)

