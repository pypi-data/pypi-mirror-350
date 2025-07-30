import pyodbc
import os
import json
from dotenv import load_dotenv
from datetime import datetime
from decimal import Decimal

class SQL_DW:
    def __init__(self):
        load_dotenv()
        self.server = os.getenv("DB_SERVER_CONSULTA")
        self.database = os.getenv("DB_DATABASE_CONSULTA")
        self.username = os.getenv("DB_USERNAME_CONSULTA")
        self.password = os.getenv("DB_PASSWORD_CONSULTA")
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            f'SERVER={self.server};'
            f'DATABASE={self.database};'
            f'UID={self.username};'
            f'PWD={self.password}'
        )
        self.cursor = self.conn.cursor()

    def execute_query(self, query):
        if self.cursor is None:
            raise Exception("Connection not established. Call connect() first.")
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def execute(self, query):
        self.cursor.execute(query)
        self.conn.commit()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def get_column_names(self, query):
        cursor = self.conn.cursor()
        cursor.execute(query)
        return [description[0] for description in cursor.description]

    def execute_query_as_json(self, query):
        if self.cursor is None:
            raise Exception("Connection not established. Call connect() first.")
        self.cursor.execute(query)
        colunas = [description[0] for description in self.cursor.description]
        resultados = self.cursor.fetchall()
        resultados_dict = [dict(zip(colunas, linha)) for linha in resultados]

        def converter_datetime(obj):
            if isinstance(obj, datetime):
                return obj.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(obj, Decimal):
                return float(obj)
            raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')

        return json.dumps(resultados_dict, default=converter_datetime, ensure_ascii=False, indent=4)