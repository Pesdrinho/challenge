from flask import Flask, request, jsonify, render_template, redirect, url_for
import psycopg2
from datetime import datetime
import requests
import time
import base64

app = Flask(__name__)

# Filtro customizado para codificar em base64
@app.template_filter('b64encode')
def b64encode_filter(data):
    return base64.b64encode(data).decode('utf-8')

#------------------------- OBTER MENSAGENS -------------------------#
# Função existente para coletar mensagens do WhatsApp
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

#------------------------- DATABASE -------------------------#

# Função existente para se conectar ao banco de dados e armazenar mensagens
def store_messages_in_db(messages):
    try:
        # Conecta ao banco de dados PostgreSQL
        conn = psycopg2.connect("dbname=whatsapp_db user=postgres password=9090")
        cur = conn.cursor()

        # Insere as mensagens na tabela MESSAGES
        for msg in messages:
            cur.execute("""
                INSERT INTO MESSAGES (sender, message, timestamp)
                VALUES (%s, %s, %s)
            """, (msg["from"], msg["body"], datetime.fromtimestamp(msg["timestamp"])))

        # Commit para salvar as mudanças
        conn.commit()
        print("Mensagens inseridas com sucesso.")

        # Fecha o cursor e a conexão
        cur.close()
        conn.close()

    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")

#------------------------- INICIAR SESSÃO WHATSAPP -------------------------#
# Função para iniciar a sessão no WhatsApp
def start_whatsapp_session():
    url = "http://localhost:3000/api/sessions/start"
    data = {
        "name": "default",
        "config": {
            "proxy": None,
            "noweb": {
                "store": {
                    "enabled": True,
                    "fullSync": False
                }
            },
            "webhooks": [
                {
                    "url": "https://webhook.site/11111111-1111-1111-1111-11111111",
                    "events": ["message", "session.status"],
                    "hmac": None,
                    "retries": None,
                    "customHeaders": None
                }
            ],
            "debug": False
        }
    }

    try:
        response = requests.post(url, json=data)
        response.raise_for_status()

        # Verificar se a resposta indica que a sessão foi iniciada
        if response.status_code not in [422, 404]:
            session_status = response.json().get('status')
            if session_status == "STARTING":
                return True
            else:
                print(f"Unexpected session status: {session_status}")
                return False
        else:
            print(f"Unexpected status code: {response.status_code}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"Erro ao iniciar a sessão do WhatsApp: {e}")
        return False

# Função para parar a sessão no WhatsApp
def stop_whatsapp_session():
    url = "http://localhost:3000/api/sessions/stop"
    data = {"name": "default"}

    try:
        response = requests.post(url, json=data)
        response.raise_for_status()

        if response.status_code not in [422, 404]:
            return True
        else:
            return False

    except requests.exceptions.RequestException as e:
        print(f"Erro ao parar a sessão do WhatsApp: {e}")
        return False

# Função para obter o QR Code
def get_qr_code():
    time.sleep(2)

    url = "http://localhost:3000/api/screenshot?session=default"
    
    time.sleep(1)

    try:
        # Definir o cabeçalho 'Accept' como 'image/png'
        headers = {
            'accept': 'image/png'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Verificar se o conteúdo retornado é uma imagem
        if response.headers.get('Content-Type').startswith('image'):
            return response.content
        else:
            print(f"Resposta inesperada: {response.content}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Erro ao obter QR Code: {e}")
        return None
    
#------------------------- CRIAÇÃO DE GRUPO -------------------------#
# Função para criar um grupo no WhatsApp
def create_whatsapp_group(group_name, participants):
    url = "http://localhost:3000/api/default/groups"
    data = {
        "name": group_name,
        "participants": [{"id": participant} for participant in participants]
    }

    try:
        response = requests.post(url, json=data)
        response.raise_for_status()

        if response.status_code not in [422, 404]:
            return response.json().get("_serialized")
        else:
            return None

    except requests.exceptions.RequestException as e:
        print(f"Erro ao criar o grupo: {e}")
        return None

#------------------------- ROTAS FLASK -------------------------#
# Rota principal para exibir o formulário HTML
@app.route('/', methods=['GET', 'POST'])
def index():
    messages = None
    if request.method == 'POST':
        chat_id = request.form['chat_id']
        limit = int(request.form['limit'])

        messages = get_messages(chat_id, limit)

        if messages is None:
            return jsonify({"error": "Could not retrieve messages"}), 500

    return render_template('index.html', messages=messages)

# Rota para iniciar a sessão e redirecionar para a página de QR Code
@app.route('/start_session', methods=['POST'])
def start_session():
    if start_whatsapp_session():
        return redirect(url_for('show_qr_code'))
    else:
        return jsonify({"error": "Failed to start session"}), 500

# Rota para reiniciar a sessão e redirecionar para a página de QR Code
@app.route('/restart_session', methods=['POST'])
def restart_session():
    if stop_whatsapp_session() and start_whatsapp_session():
        return redirect(url_for('show_qr_code'))
    else:
        return jsonify({"error": "Failed to restart session"}), 500

# Rota para exibir o QR Code
@app.route('/qr_code')
def show_qr_code():
    qr_code = get_qr_code()
    
    if qr_code:
        return render_template('qr_code.html', qr_code=qr_code)
    else:
        return jsonify({"error": "Could not retrieve QR Code"}), 500

# Rota para criar um grupo
@app.route('/create_group', methods=['GET', 'POST'])
def create_group():
    if request.method == 'POST':
        group_name = request.form['group_name']
        participants = request.form['participants'].split(',')

        group_id = create_whatsapp_group(group_name, participants)

        if group_id:
            message = f"Grupo '{group_name}' criado com sucesso! ID do grupo: {group_id}"
            return render_template('create_group.html', message=message)
        else:
            return jsonify({"error": "Failed to create group"}), 500

    return render_template('create_group.html')

# Rota para exibir a página inicial a partir da página de QR Code
@app.route('/back_to_home', methods=['POST'])
def back_to_home():
    return redirect(url_for('index'))

# Rota para salvar mensagens manualmente
@app.route('/save_messages', methods=['POST'])
def save_messages():
    messages = request.form.get('messages')
    if messages:
        messages = eval(messages)  # Converte de string para lista de dicionários
        store_messages_in_db(messages)
        return render_template('index.html', messages=messages, success_message="Mensagens salvas com sucesso!")
    else:
        return render_template('index.html', error_message="Nenhuma mensagem para salvar.")

if __name__ == "__main__":
    app.run(debug=True)