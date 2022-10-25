import threading
import socket
import os
import base64


#localhost
hostname = socket.gethostname()
addr = socket.gethostbyname(hostname) #pegar endereço atual de IPv4
host = addr
port = 3000
print(addr)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #definindo protocolo (TCP)
server.bind((host, port)) #Associar o socket a host e porta ao server
server.listen() #esperando conexões

clients = [] #adiciona clientes a lista
names = [] #nome dos clientes

def transmitir(mensagem):
    for client in clients:
        client.send(mensagem)

def handle(client):
    while True:
        try:
            mensagem = client.recv(1024) #1024bytes / receber mensagem
            transmitir(mensagem)
        except: #termina conexão com o cliente caso falhe e remove da lista
            index = client.index(client)
            clients.remove(client)
            client.close()      
            name = names[index]
            transmitir(f'{name} saiu do chat'.encode('utf-8'))
            names.remove(name)
            break


def receive():
    while True:
        client, address = server.accept() #aceitar todas as conexões
        print(f"Conectado com {str(address)}")

        client.send('Nome'.encode('utf-8')) #Aguardando entrada do nome do Client
        name = client.recv(1024).decode('utf-8')
        names.append(name)
        clients.append(client)

        print(f'Nome do Usuário é {name}!')
        transmitir(f'{name} Entrou no chat!\n'.encode('utf-8'))
        client.send('Conectado ao Servidor!\n'.encode('utf-8'))
        thread = threading.Thread(target =handle, args=(client,))  #enviar uma thread para lidar com cada usuário ao mesmo tempo
        thread.start()

print("Servidor On! Aguardando conexões...")
receive()

