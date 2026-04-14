"""
uazapi-bot — a real standalone WhatsApp bot using uazapi-python.

Zero CLI dependency: credentials come from:
  1. .env file / environment variables (UAZAPI_BASE_URL, UAZAPI_TOKEN)
  2. ~/.uazapi/config.json  (written by setup.py or save_config())

Start:
    uvicorn main:app --reload --port 8000
"""
import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request

from uazapi import AsyncUazapiClient, UazapiClient
from uazapi.exceptions import UazapiError

# Load .env if present (takes no effect when vars are already in the environment)
load_dotenv()

app = FastAPI(title="uazapi-bot")

# ---------------------------------------------------------------------------
# Synchronous client used for startup/shutdown and non-async endpoints
# ---------------------------------------------------------------------------
client = UazapiClient()          # reads env vars or ~/.uazapi/config.json


# ---------------------------------------------------------------------------
# Startup: register the webhook so UAZAPI knows where to send events
# ---------------------------------------------------------------------------
@app.on_event("startup")
def register_webhook() -> None:
    webhook_url = os.environ.get("WEBHOOK_URL", "")
    if not webhook_url:
        print(
            "[bot] WEBHOOK_URL not set — skipping webhook registration.\n"
            "      Set WEBHOOK_URL=https://your-public-url.com/webhook to enable it."
        )
        return

    client.webhook.set(
        url=f"{webhook_url}/webhook",
        events=["messages", "connection", "qrcode"],
        enabled=True,
    )
    print(f"[bot] Webhook registered at {webhook_url}/webhook")


# ---------------------------------------------------------------------------
# /status — quick health-check
# ---------------------------------------------------------------------------
@app.get("/status")
def status() -> dict:
    """Return the current WhatsApp connection status."""
    return client.instance.status()


# ---------------------------------------------------------------------------
# /send — programmatic message sending
# ---------------------------------------------------------------------------
@app.post("/send")
async def send_message(body: dict) -> dict:
    """
    POST /send
    {
      "number": "5511999999999",
      "text": "Hello from the bot!"
    }
    """
    number = body.get("number", "").strip()
    text = body.get("text", "").strip()

    if not number or not text:
        raise HTTPException(status_code=400, detail="number and text are required")

    async with AsyncUazapiClient() as ac:
        result = await ac.send.text(number=number, text=text, delay=500)
    return result


# ---------------------------------------------------------------------------
# /webhook — receives events from UAZAPI
# ---------------------------------------------------------------------------
@app.post("/webhook")
async def webhook(request: Request) -> dict:
    payload = await request.json()
    event = payload.get("event")

    if event == "messages":
        async with AsyncUazapiClient() as ac:
            for msg in payload.get("data", []):
                if msg.get("fromMe"):
                    continue  # ignore our own messages

                chatid: str = msg.get("chatid", "")
                number = chatid.replace("@s.whatsapp.net", "").replace("@g.us", "")
                body: str = msg.get("body", "").strip()
                is_group = chatid.endswith("@g.us")

                print(f"[bot] {'group' if is_group else 'DM'} from {number}: {body!r}")

                # ---------------------------------------------------------
                # Simple command router
                # ---------------------------------------------------------
                lower = body.lower()

                if lower in ("oi", "olá", "ola", "hi", "hello"):
                    await ac.send.text(
                        number=number,
                        text=(
                            "Olá! Sou um bot feito com *uazapi-python* 🐍\n\n"
                            "Comandos disponíveis:\n"
                            "• *status* — status da conexão\n"
                            "• *ping* — teste de latência\n"
                            "• *ajuda* — esta mensagem"
                        ),
                        delay=800,
                    )

                elif lower == "status":
                    info = client.instance.status()
                    connected = info.get("status", {}).get("connected", False)
                    await ac.send.text(
                        number=number,
                        text=f"WhatsApp: {'conectado ✅' if connected else 'desconectado ❌'}",
                    )

                elif lower == "ping":
                    await ac.send.text(number=number, text="pong 🏓")

                elif lower in ("ajuda", "help", "?"):
                    await ac.send.text(
                        number=number,
                        text=(
                            "*Comandos:*\n"
                            "• oi / olá — boas-vindas\n"
                            "• status — status da conexão\n"
                            "• ping — pong\n"
                            "• ajuda — este menu"
                        ),
                    )

    elif event == "connection":
        data = payload.get("data", {})
        print(f"[bot] Connection event: {data.get('status')}")

    elif event == "qrcode":
        data = payload.get("data", {})
        print(f"[bot] QR code updated — scan it to connect")

    return {"ok": True}
