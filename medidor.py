import requests

# ------------- Configuración -------------
API_KEY = "203e2c98-33a2-425a-80d9-70ea7e752a4c"
BASE_URL = "https://graphhopper.com/api/1"

transportes = {
    "1": "car",
    "2": "bike",
    "3": "foot"
}

# ------------- Geocodificación -------------
def geocode(ciudad):
    url = f"{BASE_URL}/geocode"
    params = {"q": ciudad, "locale": "es", "limit": 1, "key": API_KEY}
    respuesta = requests.get(url, params=params)
    if respuesta.status_code == 200 and respuesta.json().get("hits"):
        return respuesta.json()["hits"][0]["point"]
    else:
        return None

# ------------- Calcular ruta -------------
def calcular_ruta(origen, destino, modo):
    coords1 = geocode(origen + ", " + pais(origen))
    coords2 = geocode(destino + ", " + pais(destino))
    if not coords1 or not coords2:
        print("No se pudieron obtener coordenadas válidas.")
        return
    
    url = f"{BASE_URL}/route"
    params = {
        "point": [f"{coords1['lat']},{coords1['lng']}", f"{coords2['lat']},{coords2['lng']}"],
        "vehicle": modo,
        "locale": "es",
        "instructions": "true",
        "calc_points": "true",
        "key": API_KEY
    }

    res = requests.get(url, params=params)
    if res.status_code != 200:
        print("Error al obtener ruta:", res.json().get("message"))
        return
    
    data = res.json()["paths"][0]
    distancia_km = data["distance"] / 1000
    distancia_millas = distancia_km * 0.621371

    duracion_ms = data["time"]
    duracion_min_total = duracion_ms / 60000
    horas = int(duracion_min_total // 60)
    minutos = int(duracion_min_total % 60)

    print(f"\nDistancia: {distancia_km:.2f} km / {distancia_millas:.2f} millas")
    print(f"Tiempo estimado: {horas}h {minutos}min")

    print("\nNarrativa del viaje:")
    for instruccion in data["instructions"]:
        print("-", instruccion["text"])

def pais(ciudad):
    # Intenta determinar país por nombre sencillo
    nombre = ciudad.lower()
    if "arg" in nombre:
        return "Argentina"
    return "Chile"

# ------------- Programa principal -------------
while True:
    user_input = input("\nPresiona 'v' para salir o enter para continuar: ").strip().lower()
    if user_input == "v":
        print("Saliendo del programa...")
        break

    origen = input("Ciudad de origen (Chile): ").strip()
    destino = input("Ciudad de destino (Argentina): ").strip()
    
    print("\nMedios de transporte:")
    print("1. Vehículo")
    print("2. Bicicleta")
    print("3. A pie")
    opcion = input("Opción (1/2/3): ").strip()
    modo = transportes.get(opcion)

    if not modo:
        print("Opción inválida.")
        continue

    calcular_ruta(origen, destino, modo)
