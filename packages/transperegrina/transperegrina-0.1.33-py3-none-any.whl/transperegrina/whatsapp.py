import requests
import json
import os
from dotenv import load_dotenv
import base64

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

class MessageClient:
    def enviar_mensagem(self, numero, mensagem):
        raise NotImplementedError("Este método deve ser sobrescrito pelas subclasses")

class WhatsAppClient(MessageClient):
    def __init__(self, torre=False):
        if torre:
            self.url = os.getenv("ZAPI_MESSAGE_TORRE_URL")
        else:
            self.url = os.getenv("ZAPI_MESSAGE_URL")
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": os.getenv("ZAPI_AUTHORIZATION"),
            "Client-Token": os.getenv("ZAPI_CLIENT_TOKEN")
        }

    def enviar_mensagem(self, numeros, mensagem, anexo=None, tipo_anexo=None):
        if not isinstance(numeros, list):
            numeros = [numeros]
        
        for numero in numeros:
            payload = {
                "phone": numero,
                "caption": mensagem,
            }
            files = None
            if anexo:
                if tipo_anexo == "imagem":
                    payload["image"] = anexo
                    payload["viewOnce"] = False
                    url = f"{os.getenv('ZAPI_BASE_URL')}/send-image"
                elif tipo_anexo == "video":
                    payload["video"] = anexo
                    payload["viewOnce"] = False
                    url = f"{os.getenv('ZAPI_BASE_URL')}/send-video"
                elif tipo_anexo == "pdf":
                    try:
                        with open(anexo, 'rb') as f:
                            pdf_bytes = f.read()
                            pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')
                            base64_data = f"data:application/pdf;base64,{pdf_base64}"
    
                        payload["document"] = base64_data
                        payload["fileName"] = os.path.basename(anexo)
                        url = f"{os.getenv('ZAPI_BASE_URL')}/send-document/pdf"
                        print(f"PDF em base64 preparado para envio: {anexo}")
                    except Exception as e:
                        print(f"Erro ao ler ou codificar o arquivo PDF: {e}")
                        return
                else:
                    raise ValueError("Tipo de anexo não suportado. Use 'imagem', 'video' ou 'pdf'.")
            else:
                payload = {
                    "phone": numero,
                    "message": mensagem
                }
                url = self.url
            
            print(f"Enviando payload: {json.dumps(payload)[:500]}...")  # Log para verificar o payload
            response = requests.post(url, headers=self.headers, json=payload)
            
            if response.status_code == 200:
                print("Mensagem enviada com sucesso para", numero)
            else:
                print(f"Ocorreu um erro ao enviar a mensagem para {numero}: {response.status_code} - {response.text}")

    def criar_grupo(self, nome_grupo, telefones, imagem_perfil):
        url = os.getenv("ZAPI_CREATE_GROUP_URL")
        payload = {
            "groupName": nome_grupo,
            "phones": telefones,
            "profileImage": imagem_perfil
        }
        response = requests.post(url, headers=self.headers, data=json.dumps(payload))
        if response.status_code != 200:
            print(f"Erro na requisição: {response.status_code} - {response.text}")
        else:
            print(response.json())

    def obter_metadata_convite_grupo(self, url_convite):
        url = os.getenv("ZAPI_REQUEST_GROUP_URL")
        querystring = {"URL": url_convite}
        response = requests.get(url, headers=self.headers, params=querystring)
        if response.status_code != 200:
            print(f"Erro na requisição: {response.status_code} - {response.text}")
            return None
        else:
            return (response.json())

# Exemplo de uso da classe WhatsAppClient
if __name__ == "__main__":
    cliente_whatsapp = WhatsAppClient()
    numeros = ["5548996547434"]  # Lista de números de telefone dos destinatários
    mensagem = "Aqui está o documento solicitado."
    anexo = "emails/366253.pdf"  # Caminho para o arquivo PDF
    tipo_anexo = "pdf"
    
    cliente_whatsapp.enviar_mensagem(numeros, mensagem, anexo, tipo_anexo)