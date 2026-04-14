# uazapi-bot

Bot WhatsApp standalone usando [uazapi-python](https://github.com/jonesfernandess/uazapi-python) + FastAPI. Sem CLI TypeScript, sem dependência externa além do próprio SDK.

## Setup em 3 passos

### 1. Instalar dependências

```bash
cd uazapi-bot
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configurar credenciais

**Opção A — setup interativo (recomendado para primeira vez):**
```bash
python setup.py
```
As credenciais são salvas em `~/.uazapi/config.json` e reutilizadas automaticamente em qualquer projeto que use o SDK.

**Opção B — variáveis de ambiente:**
```bash
cp .env.example .env
# edite o .env com suas credenciais
```

**Opção C — direto no código:**
```python
from uazapi import UazapiClient
client = UazapiClient(base_url="https://free.uazapi.com", token="seu-token")
```

### 3. Rodar o bot

```bash
uvicorn main:app --reload --port 8000
```

Para receber webhooks em dev local, use [ngrok](https://ngrok.com):
```bash
ngrok http 8000
# copie a URL https://xxxx.ngrok.io e defina:
WEBHOOK_URL=https://xxxx.ngrok.io uvicorn main:app --reload
```

## Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/status` | Status da conexão WhatsApp |
| `POST` | `/send` | Envia mensagem programaticamente |
| `POST` | `/webhook` | Recebe eventos do UAZAPI |

## Comandos do bot (via WhatsApp)

| Mensagem | Resposta |
|----------|----------|
| oi / olá | Boas-vindas + menu |
| status | Status da conexão |
| ping | pong |
| ajuda | Menu de comandos |

## Como funciona — sem CLI

Este projeto usa diretamente o [uazapi-python](https://github.com/jonesfernandess/uazapi-python). O SDK lê credenciais na seguinte ordem:

1. Argumentos do construtor: `UazapiClient(base_url=..., token=...)`
2. Variáveis de ambiente: `UAZAPI_BASE_URL`, `UAZAPI_TOKEN`
3. `~/.uazapi/config.json` (escrito por `save_config()` ou `setup.py`)

A CLI TypeScript (`uazapi-cli`) **não precisa estar instalada**.

## Licença

MIT
