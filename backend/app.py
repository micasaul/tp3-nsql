from flask import Flask, jsonify, request
from redis import Redis

app = Flask(__name__)
r = Redis(host='localhost', port=6379, decode_responses=True)

def get_lat_lon():
    data = request.get_json()
    if not data or "lat" not in data or "lon" not in data:
        return None, None
    return data["lat"], data["lon"]

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

@app.route('/agregar/<string:grupo>/<string:nombre>', methods=['POST'])
def agregar_lugar(grupo, nombre, lat, lon):
    lat, lon = get_lat_lon()
    if lat is None or lon is None:
        return jsonify({"error": "Faltan lat/lon"}), 400
    
    r.geoadd(grupo, (lon, lat, nombre))
    return jsonify({"mensaje": "Lugar agregado"})

@app.route('/buscar/<string:grupo>', methods=['POST'])
def buscar_cercanos(grupo, lat, lon):
    lat, lon = get_lat_lon()
    if lat is None or lon is None:
        return jsonify({"error": "Faltan lat/lon"}), 400

    lugares = r.georadius(grupo, lon, lat, 5, unit="km")
    return jsonify(lugares)

@app.route('/distancia/<string:grupo>/<string:lugar1>/<string:lugar2>', methods=['GET'])
def distancia(grupo, lugar1, lugar2):
    dist = r.geodist(grupo, lugar1, lugar2, unit="km")
    return jsonify({"distancia_km": dist})

if __name__ == '__main__':
    cargar_datos()
    app.run(debug=True)