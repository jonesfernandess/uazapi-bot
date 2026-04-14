# uazapi-bot

Bot WhatsApp usando [uazapi-python](https://github.com/jonesfernandess/uazapi-python) + FastAPI.

## Variáveis de ambiente

O bot não armazena credenciais em arquivos. Tudo vem do ambiente:

| Variável | Obrigatória | Descrição |
|----------|-------------|-----------|
| `UAZAPI_BASE_URL` | sim | URL da instância UAZAPI |
| `UAZAPI_TOKEN` | sim | Token da instância |
| `UAZAPI_ADMIN_TOKEN` | não | Token admin |
| `WEBHOOK_URL` | não | URL pública para registrar o webhook no UAZAPI |

## Deploy

### Railway / Render / Heroku

1. Faça fork ou clone deste repositório
2. Crie um novo serviço apontando para o repo
3. Defina as variáveis de ambiente no painel da plataforma
4. Deploy — o bot sobe automaticamente

### Docker

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker build -t uazapi-bot .
docker run -p 8000:8000 \
  -e UAZAPI_BASE_URL=https://sua-instancia.uazapi.com \
  -e UAZAPI_TOKEN=seu-token \
  -e WEBHOOK_URL=https://seu-dominio.com \
  uazapi-bot
```

### VPS

```bash
git clone https://github.com/jonesfernandess/uazapi-bot
cd uazapi-bot
pip install -r requirements.txt

export UAZAPI_BASE_URL=https://sua-instancia.uazapi.com
export UAZAPI_TOKEN=seu-token
export WEBHOOK_URL=https://seu-dominio.com

uvicorn main:app --host 0.0.0.0 --port 8000
```

## Desenvolvimento local

```bash
cp .env.example .env
# preencha o .env com suas credenciais de dev
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Para expor o webhook localmente, use [ngrok](https://ngrok.com):

```bash
ngrok http 8000
# use a URL gerada como WEBHOOK_URL no .env
```

## Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/status` | Status da conexão WhatsApp |
| `POST` | `/send` | Envia mensagem programaticamente |
| `POST` | `/webhook` | Recebe eventos do UAZAPI |

```bash
# Enviar mensagem via API
curl -X POST https://seu-dominio.com/send \
  -H "Content-Type: application/json" \
  -d '{"number": "5511999999999", "text": "Olá!"}'
```

## Comandos do bot (via WhatsApp)

| Mensagem | Resposta |
|----------|----------|
| oi / olá | Boas-vindas + menu |
| status | Status da conexão |
| ping | pong |
| ajuda | Menu de comandos |

## Licença

MIT
