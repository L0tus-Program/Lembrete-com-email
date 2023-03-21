import time
import threading
import smtplib
from email.mime.text import MIMEText
from plyer import notification

from tkinter import *

class Application:
    def __init__(self, master=None):
        # variaveis do objeto

        self.assunto = "Lembrete"
        #self.conteudo = ""
        
        self.fontePadrao = ("Arial", "10")
        self.primeiroContainer = Frame(master)
        self.primeiroContainer["pady"] = 10
        self.primeiroContainer.pack()

        self.segundoContainer = Frame(master)
        self.segundoContainer["padx"] = 20
        self.segundoContainer.pack()

        self.terceiroContainer = Frame(master)
        self.terceiroContainer["padx"] = 20
        self.terceiroContainer.pack()

        self.quartoContainer = Frame(master)
        self.quartoContainer["pady"] = 20
        self.quartoContainer.pack()

        self.quintoContainer = Frame(master)
        self.quintoContainer["pady"] = 20
        self.quintoContainer.pack()

        # configuração do título
        self.titulo = Label(self.primeiroContainer, text="Lembrete com timer")
        self.titulo["font"] = ("Arial", "10", "bold")
        self.titulo.pack()

        # configuração do campo de lembrete
        self.lembrarLabel = Label(self.segundoContainer,text="O que deve ser lembrado ?", font=self.fontePadrao)
        self.lembrarLabel.pack(side=LEFT)

        self.lembrar = Entry(self.segundoContainer)
        self.lembrar["width"] = 30
        self.lembrar["font"] = self.fontePadrao
        self.lembrar.pack(side=LEFT)

        # inserção de e-mail (opcional)
        self.emailLabel = Label(self.terceiroContainer, text="E-mail para receber lembrete (em branco não envia): ", font=self.fontePadrao)
        self.emailLabel.pack(side=LEFT)

        self.email = Entry(self.terceiroContainer)
        self.email["width"] = 30
        self.email["font"] = self.fontePadrao
        #self.email["show"] = "*" Vou usar posteriormente pra uma pagina de configuração de e-mail
        self.email.pack(side=LEFT)

        # inserção timer
        self.clockLabel = Label(self.quartoContainer, text="Quanto tempo para o lembrete ? ", font=self.fontePadrao)
        self.clockLabel.pack(side=LEFT)
        self.clock = Entry(self.quartoContainer)
        self.clock["width"] = 30
        self.clock["font"] = self.fontePadrao
        self.clock.pack()

        self.registrar = Button(self.quintoContainer)
        self.registrar["text"] = "Registrar"
        self.registrar["font"] = ("Calibri", "8")
        self.registrar["width"] = 12
        self.registrar["command"] = self.main
        self.registrar.pack()
        #print("Botão construido")

        #self.c1 = Checkbutton(window, text='Python',variable=var1, onvalue=1, offvalue=0, command=print_selection)
        #self.c1.pack()
        
        

    def main(self): 
        #print("Entrando na função main")
        # Iniciando o timer em uma thread separada
       
        t = threading.Thread(target=lambda: self.start())
        
        t.start()
        #print("Passou thread")
       
            
    def start(self):
        self.timer()
        self.notification()
        
        

    def timer(self):
        self.time = self.clock.get()
        self.time = float(self.time)
        
        time.sleep(self.time*60)
        if self.email != "": # corrigir tratamento de e-mail
            try:
                self.mail()
            except:
                #print("ERRO EMAIL")
                pass
        else:
            pass


    def notification(self):
        try : #constrói e exibe a notificação do lembrete
            notification.notify(
                title = "LEMBRETE",
                message = self.conteudo,
                timeout = 10,
            )
        except Exception as e:
            #print(f'Erro notificação {e}' )
            pass


    def mail(self):
        #print("Entrando na função mail")
         # Dados de autenticação
        self.username = "felipe@brasildosparafusos.com.br"
        self.password = "Flg@1999"
        self.emailDestino = self.email.get()
        self.conteudo = self.lembrar.get()
        # Criação do objeto MIMEText
        msg = MIMEText(self.conteudo, 'plain', 'utf-8') # é necessário codificar o objeto para utf-8 para poder enviar acentos
        msg['To'] = self.emailDestino
        msg['From'] = self.username
        msg['Subject'] = self.assunto

        # Adicionando cabeçalhos de conteúdo
        msg.add_header('Content-Type', 'text/plain; charset=UTF-8')

        # Enviando o e-mail
        with smtplib.SMTP("email-ssl.com.br", 587) as server:
            server.starttls()
            server.login(self.username, self.password)
            server.sendmail(self.username, self.emailDestino, msg.as_string())

        #print("E-mail enviado com sucesso!")

    
root = Tk()
root.iconbitmap('lembret.ico')

Application(root)
root.mainloop()