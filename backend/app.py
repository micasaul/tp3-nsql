from redis import Redis

r = Redis(host='localhost', port=6379, decode_responses=True)

def agregar_lugar(grupo, nombre, lat, lon):
    r.geoadd(grupo, (lon, lat, nombre))

def buscar_cercanos(grupo, lat, lon):
    return r.georadius(grupo, lon, lat, 5, unit="km")

def distancia(grupo, lugar1, lugar2):
    return r.geodist(grupo, lugar1, lugar2, unit="km")
