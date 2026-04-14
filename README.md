# uazapi-bot

Bot WhatsApp standalone usando [uazapi-python](https://github.com/jonesfernandess/uazapi-python) + FastAPI. Sem CLI TypeScript, sem credenciais no código-fonte.

## Setup em 3 passos

### 1. Instalar dependências

```bash
cd uazapi-bot
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configurar credenciais

Copie o arquivo de exemplo e preencha com suas credenciais:

```bash
cp .env.example .env
```

```ini
# .env  ← nunca sobe pro git, já está no .gitignore
UAZAPI_BASE_URL=https://free.uazapi.com
UAZAPI_TOKEN=seu-token-aqui
UAZAPI_ADMIN_TOKEN=seu-admin-token-aqui  # opcional

BOT_PORT=8000
```

O `main.py` carrega o `.env` automaticamente via `python-dotenv` — nenhuma credencial fica no código.

### 3. Rodar o bot

```bash
uvicorn main:app --reload --port 8000
```

Para receber webhooks em dev local, use [ngrok](https://ngrok.com):

```bash
ngrok http 8000
```

```bash
# na outra aba, com a URL gerada pelo ngrok:
WEBHOOK_URL=https://xxxx.ngrok.io uvicorn main:app --reload
```

## Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/status` | Status da conexão WhatsApp |
| `POST` | `/send` | Envia mensagem programaticamente |
| `POST` | `/webhook` | Recebe eventos do UAZAPI |

### Exemplo de envio via curl

```bash
curl -X POST http://localhost:8000/send \
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

## Como funciona — sem credencial no código

O `main.py` usa `UazapiClient()` sem argumentos. O SDK ([uazapi-python](https://github.com/jonesfernandess/uazapi-python)) resolve as credenciais nesta ordem:

1. Variáveis de ambiente (`UAZAPI_BASE_URL`, `UAZAPI_TOKEN`) — carregadas do `.env`
2. `~/.uazapi/config.json` — para uso em máquina local sem `.env`
3. `~/.uazapi-cli/config.json` — fallback para quem usa a CLI TypeScript

```python
# main.py — sem nenhuma credencial hardcoded
load_dotenv()

client = UazapiClient()  # lê do ambiente
```

A CLI TypeScript (`uazapi-cli`) **não precisa estar instalada**.

## Licença

MIT
