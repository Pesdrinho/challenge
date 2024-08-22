import psycopg2
from datetime import datetime

#  Dados de exemplo para inserir na tabela
messages = [
    {"sender": "Pedrin", "message": "Olá, como você está?", "timestamp": datetime(2024, 8, 20, 14, 30)},
    {"sender": "Bebeto", "message": "Estou bem, e você?", "timestamp": datetime(2024, 8, 20, 14, 31)},
]

try:
    # Connect to your postgres DB
    conn = psycopg2.connect("dbname=whatsapp_db user=postgres password=9090")

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Execute a query
    cur.execute("SELECT * FROM MESSAGES")
        # Inserir os dados na tabela MESSAGES
    for msg in messages:
        cur.execute("""
            INSERT INTO MESSAGES (sender, message, timestamp)
            VALUES (%s, %s, %s)
        """, (msg["sender"], msg["message"], msg["timestamp"]))

    # Commit para salvar as mudanças
    conn.commit()

    print("Mensagens inseridas com sucesso.")

    # Fechar o cursor e a conexão
    cur.close()
    conn.close()


except Exception as e:
    print(f"Erro ao conectar ao banco de dados: {e}")

