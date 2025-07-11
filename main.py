from fastapi import FastAPI, File, UploadFile, HTTPException
from openai import OpenAI
import base64
import os

app = FastAPI()
client = OpenAI(api_key="")  # Tu clave va acá

@app.post("/estimacion")
async def estimacion(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="El archivo no es una imagen.")

    contenido = await file.read()
    imagen_base64 = base64.b64encode(contenido).decode("utf-8")

    try:
        respuesta = client.chat.completions.create(
            model="gpt-4o",

            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "¿Qué comida hay en esta imagen? Estima cuántas calorías puede tener."},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{imagen_base64}"}}
                    ],
                }
            ],
            max_tokens=300
        )
        return {"respuesta": respuesta.choices[0].message.content}
    except Exception as e:
        print(f"❌ Error procesando imagen: {e}")
        raise HTTPException(status_code=500, detail=str(e))
