# Data fetcher Segura Challenge

## Contexto
A equipe de desenvolvimento da Segura necessita diariamente integrar com aplicações de terceiros e analisar seus dados. As vezes, essa integrações não são tão simples... 👽

## Objetivo
Criar um programa em Python que acesse um grupo no Whatsapp e obtenha o máximo de mensagens possíveis e armazene em um banco de dados.

## Entregáveis
- Consumir as mensagens de um grupo do Whatsapp. Qualquer grupo (pode ser um grupo só com você etc).
- Armazenar essas mensagens em um banco de dados.

## Bonus
- A aplicação poder ser executada utilizando docker.
- Utilizar Postgresql como banco de dados.

## Sugestões
- Utilizar a ferramenta Waha (https://waha.devlike.pro/) para facilitar a sua integração com o Whatsapp.
- Utilizar a Flask ou FastApi para criação de webhooks que recebem as mensagens.

## Entrega
Ao finalizar o desafio envie um email para people@sejasegura.com.br com o repositorio da sua submissão

---------------------------------------------------------------------------

# Quick Start - Aplicação Flask via Docker

Este guia rápido irá ajudá-lo a configurar e executar a aplicação Flask usando Docker.

## Pré-requisitos

Antes de começar, certifique-se de ter o Docker instalado na sua máquina. Se você ainda não o fez, pode seguir as instruções de instalação do Docker aqui: [Docker Installation](https://docs.docker.com/get-docker/).

## Passos para Configuração

### 1. Clone o Repositório

Clone o repositório do projeto para o seu ambiente local:

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

### 2. Construir a imagem

No diretório do projeto, construa a imagem Docker utilizando o Dockerfile:

```bash
docker build -t challenge .
```

### 3. Construir o container

Após a imagem ser construída com sucesso, execute o container:

```bash
docker run -d -p 8000:8000 challenge
```

### 4. Acessar a aplicação

Agora, você pode acessar a aplicação em seu navegador utilizando o endereço:

- Se estiver na mesma máquina onde o Docker está rodando:

```bash
http://localhost:8000/
```

- Se estiver em outra máquina na mesma rede, substitua localhost pelo endereço IP da máquina onde o Docker está rodando:

```bash
http://{ip-da-maquina}:8000/
```

### 5. Parar o Container

Para parar o container, primeiro obtenha o ID do container usando:

```bash
docker ps
```

Depois, pare o container usando o comando docker stop:

```bash
docker stop <container_id>
```


### Explicação

- **Clone o Repositório:** Instruções para clonar o repositório do projeto.
- **Construir a Imagem Docker:** Mostra como construir a imagem Docker do projeto.
- **Executar o Container:** Explica como rodar a aplicação dentro de um container Docker.
- **Acessar a Aplicação:** Explica como acessar a aplicação, tanto localmente quanto via rede.
- **Parar o Container:** Instruções para parar o container quando não for mais necessário.

