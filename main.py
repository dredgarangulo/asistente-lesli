import os
import requests
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# Obtener las claves secretas desde variables de entorno
CALENDLY_API_KEY = os.environ.get("CALENDLY_API_KEY")

# URIs de los eventos
EVENTO_CONSULTA = "https://api.calendly.com/event_types/8ce60840-4d6d-4dc5-8f2b-28e362a58452"
EVENTO_CIRUGIA = "https://api.calendly.com/event_types/9c40dfa7-79ea-4302-ae7e-e7237cc43692"

# Modelo para los datos recibidos
class CitaRequest(BaseModel):
    nombre: str
    edad: int
    email: str
    telefono: str
    fecha: str
    motivo: str
    tipo: str

@app.get("/")
def read_root():
    return {"message": "Asistente Lesli está en funcionamiento."}

@app.post("/agendar")
def agendar(cita: CitaRequest):
    # Seleccionar evento según tipo de cita
    if cita.tipo.lower() == "consulta":
        evento_uri = EVENTO_CONSULTA
    elif cita.tipo.lower() == "cirugia":
        evento_uri = EVENTO_CIRUGIA
    else:
        return {"error": "Tipo de cita inválido. Usa 'consulta' o 'cirugia'."}, 400

    headers = {
        "Authorization": f"Bearer {CALENDLY_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "invitee": {
            "email": cita.email,
            "name": cita.nombre
        },
        "event_type": evento_uri,
        "questions_and_answers": [
            {"question": "Edad", "answer": cita.edad},
            {"question": "Teléfono", "answer": cita.telefono},
            {"question": "Motivo de consulta", "answer": cita.motivo}
        ],
        "start_time": cita.fecha + "T10:00:00Z"  # simplificado, puede mejorarse
    }

    response = requests.post("https://api.calendly.com/scheduled_events", headers=headers, json=payload)

    if response.status_code in [200, 201]:
        return {"mensaje": "Cita agendada exitosamente."}
    else:
        return {"error": "No se pudo agendar la cita", "detalle": response.text}, response.status_code

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
