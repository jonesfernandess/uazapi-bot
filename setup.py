"""
One-time setup: saves credentials to ~/.uazapi/config.json
so you never need to pass them to UazapiClient() again.

Usage:
    python setup.py
"""
from uazapi import save_config

base_url = input("UAZAPI base URL (e.g. https://free.uazapi.com): ").strip()
token = input("Instance token: ").strip()
admin_token = input("Admin token (optional, press Enter to skip): ").strip()

path = save_config(base_url=base_url, token=token, admin_token=admin_token)
print(f"\nConfig saved to {path}")
print("You can now run the bot without setting any environment variables.")
