import os
import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Obtener las claves secretas desde variables de entorno
CALENDLY_API_KEY = os.environ.get("CALENDLY_API_KEY")

# URIs de los eventos
EVENTO_CONSULTA = "https://api.calendly.com/event_types/8ce60840-4d6d-4dc5-8f2b-28e362a58452"
EVENTO_CIRUGIA = "https://api.calendly.com/event_types/9c40dfa7-79ea-4302-ae7e-e7237cc43692"

@app.route("/agendar", methods=["POST"])
def agendar():
    data = request.json

    # Validar que vengan los campos obligatorios
    campos_obligatorios = ["nombre", "edad", "email", "telefono", "fecha", "motivo", "tipo"]
    for campo in campos_obligatorios:
        if campo not in data:
            return jsonify({"error": f"Falta el campo obligatorio: {campo}"}), 400

    # Seleccionar evento según tipo de cita
    if data["tipo"].lower() == "consulta":
        evento_uri = EVENTO_CONSULTA
    elif data["tipo"].lower() == "cirugia":
        evento_uri = EVENTO_CIRUGIA
    else:
        return jsonify({"error": "Tipo de cita inválido. Usa 'consulta' o 'cirugia'."}), 400

    headers = {
        "Authorization": f"Bearer {CALENDLY_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "invitee": {
            "email": data["email"],
            "name": data["nombre"]
        },
        "event_type": evento_uri,
        "questions_and_answers": [
            {"question": "Edad", "answer": data["edad"]},
            {"question": "Teléfono", "answer": data["telefono"]},
            {"question": "Motivo de consulta", "answer": data["motivo"]}
        ],
        "start_time": data["fecha"] + "T10:00:00Z"  # simplificado, puede mejorarse
    }

    response = requests.post("https://api.calendly.com/scheduled_events", headers=headers, json=payload)

    if response.status_code in [200, 201]:
        return jsonify({"mensaje": "Cita agendada exitosamente."})
    else:
        return jsonify({"error": "No se pudo agendar la cita", "detalle": response.text}), response.status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
