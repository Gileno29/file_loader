import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

host = os.getenv('DB_HOST')
database = os.getenv('DB_DATABASE')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
port = os.getenv('DB_PORT')

def connect_and_query():
    try:
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )

        cur = conn.cursor()
        cur.execute('SELECT * FROM test LIMIT 5')

        rows = cur.fetchall()

        for row in rows:
            print(row)

        cur.close()
        conn.close()

    except Exception as error:
        print(f"Erro ao conectar ao banco de dados: {error}")

if __name__ == '__main__':
    connect_and_query()
