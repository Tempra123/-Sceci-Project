from flask import Flask, jsonify, abort
from flask_cors import CORS
import json
import os

app = Flask(__name__)

# Habilitar CORS es vital. Sin esto, tu frontend en HTML/JS será bloqueado 
# por el navegador cuando intente pedirle datos a este backend.
CORS(app)

# Ruta base segura para localizar la carpeta 'data' donde están los JSON
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

@app.route('/api/nivel/<int:nivel_id>', methods=['GET'])
def obtener_nivel(nivel_id):
    """
    Este endpoint recibe el número del nivel por la URL.
    Ejemplo: Si el frontend pide /api/nivel/4, Python busca nivel4.json
    """
    file_path = os.path.join(DATA_DIR, f'nivel{nivel_id}.json')
    
    # Si el Auxi o el usuario intenta entrar a un nivel que no existe (ej. nivel 10)
    if not os.path.exists(file_path):
        abort(404, description=f"El nivel {nivel_id} no fue encontrado o aún no ha sido desarrollado.")
        
    try:
        # Abrimos el JSON y lo mandamos al frontend
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return jsonify(data)
    except Exception as e:
        abort(500, description=f"Error del servidor al intentar leer el archivo: {str(e)}")


@app.route('/api/niveles', methods=['GET'])
def listar_niveles():
    """
    (Ruta extra) Revisa la carpeta 'data' y devuelve una lista con todos 
    los niveles disponibles. Muy útil para armar el menú principal del juego.
    """
    niveles = []
    if os.path.exists(DATA_DIR):
        for filename in sorted(os.listdir(DATA_DIR)):
            if filename.startswith('nivel') and filename.endswith('.json'):
                num_nivel = filename.replace('nivel', '').replace('.json', '')
                niveles.append({"nivel": int(num_nivel), "archivo": filename})
                
    return jsonify({"niveles_disponibles": niveles})


if __name__ == '__main__':
    print("🚀 Servidor Backend de DUOGIT encendido.")
    print("👉 Accede a http://localhost:5000/api/niveles para ver si detecta tus JSON.")
    # debug=True hace que el servidor se reinicie solo si haces cambios en el código
    app.run(debug=True, port=5000)