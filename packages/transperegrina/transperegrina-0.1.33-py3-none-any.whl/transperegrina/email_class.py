import os
from dotenv import load_dotenv
from hydra_email_manager import HydraEmailManager

class Email:
    def __init__(self):
        load_dotenv()
        self.username = os.getenv("EMAIL_USER")
        self.password = os.getenv("EMAIL_PASSWORD")
        self.manager = HydraEmailManager()
        if self.username == 'ti@transperegrina.com.br' and self.manager.verificar_senha(self.username, self.password):
            print("✅ Login bem-sucedido.")
        else:
            print("❌ Login incorreto!")

    def enviar_email(self, user_from, subject, body, attachment=None, users=None):
        if users:
            for user in users:
                self.manager.enviar_email(self.username, user, subject, body, attachment)
        self.manager.enviar_email(self.username, user_from, subject, body, attachment)

    def baixar_emails(self, folder_id, is_read=None, file_format="eml", subject_filter=None, from_filter=None, body_filter=None, order_by=None, limit=10, only_attachments=False, mark_as_read=False):
        return self.manager.baixar_emails(self.username, folder_id, is_read, file_format, subject_filter, from_filter, body_filter, order_by, limit, only_attachments, mark_as_read)

    def marcar_email_como_lido(self, email_id):
        self.manager.marcar_email_como_lido(self.username, email_id)

    def obter_id_pastas(self, parent_id=None):
        self.manager.obter_id_pastas(self.username, parent_id)

    def login(self, username, password):
        self.manager.verificar_senha(username, password)
        if self.manager.verificar_senha(username, password):
            return True
        else:
            return False

if __name__ == "__main__":
    email = Email()
    # Example usage
    res = email.baixar_emails(folder_id='AQMkADdiMDVjODcyLTkyMGYtNDkzYy1iNDhlLWYwOWNiZmMwOWMyMgAALgAAA6UWk04pGmtGo6Qh8ekR_hEBAOlav09_btVNjQXvUil-euQAAAIBDAAAAA==', from_filter='noreply@pacey.com.br', limit=20)