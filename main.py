from flask import Flask, render_template, request, jsonify
import requests
import base64
import os
app = Flask(__name__)
HF_TOKEN = os.environ.get("HF_TOKEN", TOKEN )
API_URL = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0"
def generar_imagen(prompt):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {
        "inputs": prompt,
        "parameters": {
            "num_inference_steps": 30,
            "guidance_scale": 7.5,
        }
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        # La respuesta es la imagen directamente en bytes
        image_bytes = response.content
        image_b64 = base64.b64encode(image_bytes).decode("utf-8")
        return image_b64, None
    elif response.status_code == 503:
        return None, "El modelo está cargando, espera unos segundos e intenta de nuevo."
    else:
        return None, f"Error {response.status_code}: {response.text}"
@app.route("/", methods=["GET", "POST"])
def inicio():
    imagen_b64 = None
    error = None
    prompt_usuario = ""
    if request.method == "POST":
        prompt_usuario = request.form.get("prompt_usuario", "")
        if prompt_usuario:
            imagen_b64, error = generar_imagen(prompt_usuario)
    return render_template("index.html",
                           imagen=imagen_b64,
                           error=error,
                           prompt=prompt_usuario)
if __name__ == "__main__":
    app.run(debug=True)
