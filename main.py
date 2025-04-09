from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()

# Modelo de datos esperados
class Consulta(BaseModel):
    nombre: str
    email: str
    telefono: str
    fecha: str  # ISO 8601 e.g. 2025-05-02T14:00:00Z
    motivo: str

# Token y URI de Calendly
CALENDLY_TOKEN = "eyJraWQiOiIxY2UxZTEzNjE3ZGNmNzY2YjNjZWJjY2Y4ZGM1YmFmYThhNjVlNjg0MDIzZjdjMzJiZTgzNDliMjM4MDEzNWI0IiwidHlwIjoiUEFUIiwiYWxnIjoiRVMyNTYifQ.eyJpc3MiOiJodHRwczovL2F1dGguY2FsZW5kbHkuY29tIiwiaWF0IjoxNzQ0MDc4MDY1LCJqdGkiOiI1YjQyZDc3MC00YzM5LTQ0NTYtYjQ0ZS03M2RmZTBiMWJiNzkiLCJ1c2VyX3V1aWQiOiI2NGFjN2I3Yi1lNDI5LTQ4NzgtYjZiMC1mY2UwMDVlZWFiY2EifQ.emAYqc00dN6EQOnU0xGM0bCY64UXsLAHgVrDgGFTsJU31XzcZlSQADs7oBiICot2VCZe23kYvGJ7vsqMvwdXmA"
EVENT_TYPE_URI = "https://api.calendly.com/event_types/8ce60840-4d6d-4dc5-8f2b-28e362a58452"

@app.post("/agendar-consulta")
def agendar_consulta(consulta: Consulta):
    url = "https://api.calendly.com/scheduled_events"

    payload = {
        "invitee": {
            "email": consulta.email,
            "name": consulta.nombre,
            "text_reminder_number": consulta.telefono
        },
        "event_type": EVENT_TYPE_URI,
        "start_time": consulta.fecha,
        "custom_fields": {
            "Motivo": consulta.motivo
        }
    }

    headers = {
        "Authorization": f"Bearer {CALENDLY_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.post("https://api.calendly.com/scheduled_events", json=payload, headers=headers)

    if response.status_code != 201:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return {"mensaje": "Consulta agendada con éxito", "datos": response.json()}
