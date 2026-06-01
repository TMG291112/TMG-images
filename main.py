from flask import Flask, render_template, request, jsonify
import requests
from urllib.parse import quote

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    prompt = data.get("prompt", "").strip()

    if not prompt:
        return jsonify({"error": "El prompt no puede estar vacío"}), 400

    encoded_prompt = quote(prompt)
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=768&height=768&nologo=true"

    try:
        response = requests.get(image_url, timeout=30)
        if response.status_code == 200:
            return jsonify({"image_url": image_url})
        else:
            return jsonify({"error": "No se pudo generar la imagen"}), 500
    except requests.exceptions.Timeout:
        return jsonify({"error": "La solicitud tardó demasiado, intenta de nuevo"}), 504
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

