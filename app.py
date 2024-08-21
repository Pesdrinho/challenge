#------------------------- DATABASE -------------------------#

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from time import sleep
import requests
from flask import Flask, request
from pprint import pprint

# # Configuração da URL de conexão com o PostgreSQL
# DATABASE_URL = 'postgresql://user:9090@localhost/whatsapp_db'

# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

# # Definição do modelo de dados para armazenar as mensagens
# class Message(Base):
#     __tablename__ = 'messages'

#     id = Column(Integer, primary_key=True, index=True)
#     sender = Column(String, index=True)
#     message = Column(Text)
#     timestamp = Column(DateTime, default=datetime.utcnow)

# Base.metadata.create_all(bind=engine)

# #------------------------- Funcões -------------------------#

app = Flask(__name__)

# def store_message(sender: str, message_text: str, timestamp: int):
#     db = SessionLocal()
#     # Converte o timestamp do Unix para datetime
#     message_timestamp = datetime.fromtimestamp(timestamp)
#     new_message = Message(sender=sender, message=message_text, timestamp=message_timestamp)
#     db.add(new_message)
#     db.commit()
#     db.refresh(new_message)
#     db.close()

@app.route("/bot", methods=["POST"])
def whatsapp_webhook():
    data = request.get_json()
    pprint(data)
    
    if data["event"] != "message":
        return f"Unknown event {data['event']}"
    
    payload = data["payload"]
    text = payload.get("body")
    if not text:
        return "OK"
    
    chat_id = payload["from"]
    message_id = payload['id']
    participant = payload.get('participant')
    timestamp = payload.get('timestamp')
    
    # Salva a mensagem no banco de dados
    # store_message(sender=chat_id, message_text=text, timestamp=timestamp)

    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)