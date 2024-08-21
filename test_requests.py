import random
from pprint import pprint
from time import sleep
import requests
from flask import Flask, request

app = Flask(__name__)

def get_messages(chat_id, limit=10, download_media=False):
    """
    Obtém as mensagens de um chat específico.

    :param chat_id: ID do chat do qual deseja obter as mensagens (ex.: "1234567890@c.us" para contatos individuais ou "1234567890@g.us" para grupos).
    :param limit: Número máximo de mensagens a serem retornadas.
    :param download_media: Se True, tenta baixar a mídia associada às mensagens.
    :return: Lista de mensagens ou uma mensagem de erro em caso de falha.
    """
    try:
        url = "http://localhost:3000/api/messages"
        params = {
            "chatId": chat_id,
            "downloadMedia": str(download_media).lower(),
            "limit": limit,
            "session": "default"
        }

        response = requests.get(url, params=params)
        response.raise_for_status()

        content_type = response.headers.get('Content-Type')
        print(f"Content-Type: {content_type}")

        if "application/json" in content_type:
            messages = response.json()
            return messages
        else:
            print("A resposta não está no formato JSON.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Erro ao obter mensagens: {e}")
        return None
    except ValueError as e:
        print(f"Erro ao converter a resposta em JSON: {e}")
        print(f"Resposta bruta: {response.text}")
        return None

@app.route("/")
def whatsapp_echo():
    return "WhatsApp Echo Bot is ready!"

@app.route("/bot", methods=["POST"])
def whatsapp_webhook():
    data = request.get_json()
    pprint(f"-------------------------------{data}")

    if data["event"] != "message":
        return f"Evento desconhecido {data['event']}"

    payload = data.get("payload")
    if not payload:
        print("Payload não encontrado na requisição.")
        return "OK"
    
    # Extraindo as informações principais do payload
    message_id = payload.get("id")
    timestamp = payload.get("timestamp")
    chat_id = payload.get("from")
    to = payload.get("to")
    text = payload.get("body")
    has_media = payload.get("hasMedia")
    ack = payload.get("ack")

    if not text:
        print("Nenhum texto na mensagem")
        return "OK"

    # Imprime detalhes da mensagem recebida para depuração
    print(f"Mensagem recebida de {chat_id}:")
    print(f"  - Texto: {text}")
    print(f"  - Enviada para: {to}")
    print(f"  - Timestamp: {timestamp}")
    print(f"  - ID da mensagem: {message_id}")
    print(f"  - Possui mídia: {has_media}")
    print(f"  - Status de confirmação (ack): {ack}")

    # Para depuração, obtenha mensagens recentes deste chat
    messages = get_messages(chat_id)
    if messages:
        print(f"Mensagens recentes de {chat_id}:")
        for message in messages:
            print(f"  - {message['from']}: {message['body']}")

    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
