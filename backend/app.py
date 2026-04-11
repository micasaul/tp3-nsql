from flask import Flask, jsonify, request, send_from_directory
from redis import Redis

app = Flask(
    __name__,
    template_folder="../frontend",
    static_folder="../frontend",
    static_url_path=""
)
r = Redis(host='localhost', port=6379, decode_responses=True)

def get_data(requeridos):
    data = request.get_json()
    if not data:
        return None
    
    for campo in requeridos:
        if campo not in data:
            return None
    
    return data

def agregar_lugar(grupo, nombre, lat, lon):
    r.geoadd(grupo, (lon, lat, nombre))

def cargar_datos():
    if r.exists("cervecerias"):
        return

    agregar_lugar("cervecerias", "Tractor", -32.480, -58.238)
    agregar_lugar("cervecerias", "Ambar", -32.482, -58.232)

    agregar_lugar("universidades", "UNER", -32.47, -58.26)
    agregar_lugar("universidades", "FCYT-UADER", -32.47, -58.23)

    agregar_lugar("farmacias", "Farmacia Yrigoyen", -32.48, -58.24)
    agregar_lugar("farmacias", "Farmacia Alberdi", -32.48, -58.23)

    agregar_lugar("emergencias", "Hospital", -32.48, -58.26)

    agregar_lugar("supermercados", "Supermercado Dar", -32.48, -58.23)
    agregar_lugar("supermercados", "Supermercado Dia", -32.49, -58.24)

@app.route('/')
def home():
    return send_from_directory("../frontend",'index.html')

@app.route('/agregar', methods=['POST'])
def agregar():
    data = get_data(["grupo", "nombre", "lat", "lon"])
    if not data:
        return jsonify({"error": "Faltan datos"}), 400

    agregar_lugar(
        data["grupo"],
        data["nombre"],
        data["lat"],
        data["lon"]
    )

    return jsonify({"mensaje": "Lugar agregado"})

@app.route('/buscar', methods=['POST'])
def buscar():
    data = get_data(["grupo", "lat", "lon"])
    if not data:
        return jsonify({"error": "Faltan datos"}), 400

    lugares = r.georadius(
        data["grupo"],
        data["lon"],
        data["lat"],
        5,
        unit="km"
    )

    return jsonify(lugares)

@app.route('/distancia', methods=['POST'])
def distancia():
    data = get_data(["grupo", "origen", "destino"])
    if not data:
        return jsonify({"error": "Faltan datos"}), 400

    dist = r.geodist(
        data["grupo"],
        data["origen"],
        data["destino"],
        unit="km"
    )

    return jsonify({"distancia_km": dist})

if __name__ == '__main__':
    cargar_datos()
    app.run(debug=True)