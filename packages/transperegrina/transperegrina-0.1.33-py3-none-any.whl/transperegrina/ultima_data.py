import os
from datetime import datetime

class UltimaData:
    DATA_FILE = 'ultima_data.txt'

    @classmethod
    def carregar_ultima_data(cls, filename):
        cls.DATA_FILE = filename
        if os.path.exists(cls.DATA_FILE):
            with open(cls.DATA_FILE, 'r') as arquivo:
                return arquivo.read().strip()
        current_year = datetime.now().year
        return f'{current_year}-01-01'

    @classmethod
    def salvar_ultima_data(cls, data):
        with open(cls.DATA_FILE, 'w') as arquivo:
            arquivo.write(data)