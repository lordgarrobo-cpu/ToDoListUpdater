# scripts/build.py
import os, io, json, requests, pandas as pd

ONEDRIVE_URL = os.environ.get("ONEDRIVE_URL", "").strip()
SHEET = os.environ.get("SHEET", "").strip()  # nombre o índice; vacío = primera hoja

if not ONEDRIVE_URL:
    raise SystemExit("Falta ONEDRIVE_URL")

r = requests.get(ONEDRIVE_URL, allow_redirects=True, timeout=60)
r.raise_for_status()

content = io.BytesIO(r.content)
# Intentar leer como Excel; si falla, tratar como CSV
try:
    if SHEET == "":
        df = pd.read_excel(content)
    else:
        try:
            df = pd.read_excel(content, sheet_name=int(SHEET))
        except ValueError:
            df = pd.read_excel(content, sheet_name=SHEET)
except Exception:
    content.seek(0)
    df = pd.read_csv(content)

os.makedirs("data", exist_ok=True)
df.to_json("data/tareas.json", orient="records", force_ascii=False)
df.to_csv("data/tareas.csv", index=False)
print(f"OK: filas={len(df)} -> data/tareas.json & data/tareas.csv")
