import socket
import threading

class Servidor:
    
    def __init__(self, host, porta):
        self.host = host
        self.porta = porta
        self.clientes = []
        self.nicknames = []

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.porta))
        self.server.listen()
        print('A sala de conversa foi iniciada...')
    
    def ouvirMsgs(self, cliente):
        while True:
            try:  # recebendo mensagens do cliente
                message = cliente.recv(1024)
                self.broadcast(message)
            except:  # removendo clientes
                index = self.clientes.index(cliente)
                self.clientes.remove(cliente)
                cliente.close()
                nickname = self.nicknames[index]
                self.broadcast('{} left!'.format(nickname).encode('utf8'))
                self.nicknames.remove(nickname)
                break
    
    def inicializar(self):  # aceitando multiplos clientes
        while True:
            cliente, address = self.server.accept()
            print("Conectado com {}".format(str(address)))
            cliente.send('NICKNAME'.encode('utf8'))
            nickname = cliente.recv(1024).decode('utf8')
            self.nicknames.append(nickname)
            self.clientes.append(cliente)
            print("Nickname é {}".format(nickname))
            self.broadcast("{} entrou!".format(nickname).encode('utf8'))
            cliente.send('Conectou no servidor!'.encode('utf8'))
            thread = threading.Thread(target=self.ouvirMsgs, args=(cliente,))
            thread.start()
    
    def broadcast(self,message):  
        for cliente in self.clientes:
            cliente.send(message)



host = 'localhost'
porta = 7000

servidor = Servidor(host, porta)
servidor.inicializar()