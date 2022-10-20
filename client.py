from concurrent.futures import thread
import socket
import threading
import tkinter.scrolledtext
from tkinter import simpledialog
import datetime

host = '172.19.195.81'
port = 3000


class Client:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port)) #conectar ao host

        msg = tkinter.Tk()
        msg.withdraw()

        self.name = simpledialog.askstring('Nome', 'Digite seu nome', parent=msg)
        self.gui_done = False
        self.running = True

        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)

        gui_thread.start()
        receive_thread.start()

    def gui_loop(self):  #TELA E CONFIGURAÇÕES
        self.win = tkinter.Tk()
        self.win.configure(bg="lightgray")
        self.chat_label = tkinter.Label(self.win, text="Chat: ", bg="lightgray")
        self.chat_label.config(font=("Arial", 12))
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state='disabled')

        self.msg_label = tkinter.Label(self.win, text="Chat: ", bg="lightgray")
        self.msg_label.config(font=("Arial", 12))
        self.msg_label.pack(padx=20, pady=5)

        self.input_area = tkinter.Text(self.win, height=3)

        self.input_area.pack(padx = 20, pady=5)

        self.send_button = tkinter.Button(self.win, text="Enviar", command=self.write)
        self.send_button.config(font=("Arial", 12))
        self.send_button.pack(padx = 20, pady= 5)
        self.gui_done = True

        self.win.protocol("WM_DELETE_WINDOW", self.stop)

        self.win.mainloop()

    def write(self):
        hour = datetime.datetime.now().hour
        minute = datetime.datetime.now().minute
        mensagem = f"{self.name} {hour}:{minute} : {self.input_area.get('1.0', 'end')}"
        self.sock.send(mensagem.encode('utf-8'))
        self.input_area.delete('1.0', 'end')

    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

    def receive(self):
        while self.running:
            try:
                mensagem = self.sock.recv(1024).decode('utf-8')
                if mensagem == 'Nome':
                    self.sock.send(self.name.encode("utf-8"))
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end', mensagem)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')
            except ConnectionAbortedError:
                break
            except:
                print('ERROR')
                self.sock.close()
                break


client = Client(host, port)