# uazapi-bot

Bot WhatsApp usando [uazapi-python](https://github.com/jonesfernandess/uazapi-python) + FastAPI.

## Variáveis de ambiente

O bot não armazena credenciais em arquivos — tudo vem do ambiente:

| Variável | Obrigatória | Descrição |
|----------|-------------|-----------|
| `UAZAPI_BASE_URL` | sim | URL da instância UAZAPI |
| `UAZAPI_TOKEN` | sim | Token da instância |
| `UAZAPI_ADMIN_TOKEN` | não | Token admin |
| `WEBHOOK_URL` | não | URL pública para registrar o webhook no UAZAPI |

## Deploy

### Railway / Render / Heroku

1. Fork este repositório
2. Crie um serviço apontando para o repo
3. Defina as variáveis de ambiente no painel da plataforma
4. Deploy — o bot sobe automaticamente

### Docker

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

UAZAPI_BASE_URL=https://sua-instancia.uazapi.com \
UAZAPI_TOKEN=seu-token \
WEBHOOK_URL=https://seu-dominio.com \
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Desenvolvimento local

```bash
cp .env.example .env
# preencha o .env com suas credenciais
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
