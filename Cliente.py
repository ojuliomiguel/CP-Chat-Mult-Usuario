import socket
import threading

class Cliente:

    def __init__(self, host, porta, nickname):
        self.host = host
        self.porta = porta

        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cliente.connect((host, porta))  # conectando o cliente ao servido

        self.nickname = nickname
    
    def recebeMsg(self):
        while True:  # validando a conexão
            try:
                message = self.cliente.recv(1024).decode('utf8')
                if message == 'NICKNAME':
                    self.cliente.send(self.nickname.encode('utf8'))
                else:
                    print(message)
            except ValueError:  # reportando falha
                print("Um erro ocorreu!" + ValueError)
                self.cliente.close()
                break
        
    def enviarMsg(self):
        while True:  # mensagem formatação
            message = '{}: {}'.format(self.nickname, input(''))
            self.cliente.send(message.encode('utf8'))
    
    def inicializar(self):
        recebeMsg_thread = threading.Thread(
        target=self.recebeMsg)  # recebendo multiplas mensagens
        recebeMsg_thread.start()
        enviaMsg_thread = threading.Thread(target=self.enviarMsg)  # enviando
        enviaMsg_thread.start()


nickname = input("Escolha seu nickname: ")

host = 'localhost'
porta = 7000

cliente = Cliente(host, porta, nickname)
cliente.inicializar()
