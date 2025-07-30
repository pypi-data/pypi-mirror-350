import os
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

load_dotenv()

def validar_email(email):
    padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(padrao, email) is not None

class EmailSender:
    def __init__(self, destinatarios, assunto, mensagem_html, caminho_diretorio=None, ext_arquivo='.txt', notfis=False):
        self.destinatarios = [email for email in destinatarios if validar_email(email)]
        self.assunto = assunto
        self.mensagem_html = mensagem_html
        self.caminho_diretorio = caminho_diretorio
        self.ext_arquivo = ext_arquivo
        self.notfis = notfis
        self.remetente = os.getenv("EMAIL_USER")
        self.senha = os.getenv("EMAIL_PASSWORD")
        self.email = MIMEMultipart()
    
    def configurar_email(self):
        if not self.destinatarios:
            raise ValueError("Nenhum destinatário válido encontrado.")
        self.email['From'] = self.remetente
        self.email['To'] = ', '.join(self.destinatarios)
        self.email['Subject'] = self.assunto
        self.email.attach(MIMEText(self.mensagem_html, 'html'))
    
    def verificar_diretorio(self):
        return os.path.isdir(self.caminho_diretorio) if self.caminho_diretorio else False

    def listar_arquivos(self):
        if not self.verificar_diretorio():
            print(f"Erro: Diretório não encontrado: {self.caminho_diretorio}")
            return []
        exts = [ext.strip() for ext in self.ext_arquivo.split(',')]
        return [f for f in os.listdir(self.caminho_diretorio) if f.lower().endswith(tuple(exts))]
    
    def definir_nome_anexo(self, arquivo):
        if self.notfis:
            return "NOTFIS CROSS.txt" if "cross" in arquivo.lower() else "NOTFIS.txt"
        return arquivo
    
    def adicionar_anexo(self, arquivo):
        caminho_arquivo = os.path.join(self.caminho_diretorio, arquivo)
        nome_arquivo = self.definir_nome_anexo(arquivo)
        try:
            with open(caminho_arquivo, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f'attachment; filename="{nome_arquivo}"')
                self.email.attach(part)
        except Exception as e:
            print(f"Erro ao adicionar anexo {arquivo}: {e}")
    
    def adicionar_anexos(self):
        arquivos = self.listar_arquivos()
        for arquivo in arquivos:
            self.adicionar_anexo(arquivo)
    
    def enviar_email(self):
        try:
            self.configurar_email()
            if self.verificar_diretorio():
                self.adicionar_anexos()
            host = os.getenv("EMAIL_HOST")
            port = os.getenv("EMAIL_PORT")
            with smtplib.SMTP(host, port) as server:
                server.starttls()
                server.login(self.remetente, self.senha)
                server.sendmail(self.remetente, self.destinatarios, self.email.as_string())
            print("E-mail enviado com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao enviar email: {e}")
            return False
    
    def excluir_arquivos_enviados(self):
        if self.verificar_diretorio():
            for arquivo in self.listar_arquivos():
                os.remove(os.path.join(self.caminho_diretorio, arquivo))
                print(f"Arquivo {arquivo} excluído após envio.")
    
    def processar_envio(self):
        if self.enviar_email():
            self.excluir_arquivos_enviados()
