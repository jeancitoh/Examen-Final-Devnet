import requests
import urllib.parse

ROUTE_URL = "https://graphhopper.com/api/1/route?"
key = "63bb55c9-c683-41a1-a2e9-dc0762110de4"


def geocoding(location, key):
    geocode_url = "https://graphhopper.com/api/1/geocode?"
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})

    reply = requests.get(url)
    status = reply.status_code
    json_data = reply.json()

    if status == 200 and len(json_data.get("hits", [])) > 0:
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
        name = json_data["hits"][0].get("name", location)
        country = json_data["hits"][0].get("country", "")
        new_loc = f"{name}, {country}" if country else name
        return status, lat, lng, new_loc
    else:
        return status, "null", "null", location


def main():
    while True:
        print("\n" + "=" * 55)
        print("   SISTEMA DE RUTAS CHILE - ARGENTINA  ")
        print("=" * 55)
        print("Ingrese 'v' o 'V' en cualquier momento para salir.\n")

        # 1. Solicitar ciudad de origen (Chile)
        loc1 = input("Ciudad de Origen (ej. Santiago, Chile): ").strip()
        if loc1.lower() == "v":
            print("\nSaliendo del programa...")
            break

        # 2. Solicitar ciudad de destino (Argentina)
        loc2 = input("Ciudad de Destino (ej. Mendoza, Argentina): ").strip()
        if loc2.lower() == "v":
            print("\nSaliendo del programa...")
            break

        # 3.transporte
        print("\nSeleccione el medio de transporte:")
        print("1. Automóvil")
        print("2. Bicicleta")
        print("3. A pie")
        vehicle_choice = input("Opción (1/2/3, por defecto 1): ").strip()

        if vehicle_choice.lower() == "v":
            print("\nSaliendo del programa...")
            break

        vehicle_map = {"1": "car", "2": "bike", "3": "foot"}
        vehicle = vehicle_map.get(vehicle_choice, "car")

        # Geocodificación de origen y destino
        orig_status, orig_lat, orig_lng, orig_name = geocoding(loc1, key)
        dest_status, dest_lat, dest_lng, dest_name = geocoding(loc2, key)

        if orig_status != 200 or orig_lat == "null":
            print(f"\n[!] Error: No se pudo geolocalizar el origen '{loc1}'. Reintente.")
            continue
        if dest_status != 200 or dest_lat == "null":
            print(f"\n[!] Error: No se pudo geolocalizar el destino '{loc2}'. Reintente.")
            continue

        print(f"\nOrigen validado : {orig_name} ({orig_lat:.4f}, {orig_lng:.4f})")
        print(f"Destino validado: {dest_name} ({dest_lat:.4f}, {dest_lng:.4f})")
        print(f"Medio transporte: {vehicle}")

        # 4 Rutas 
        route_params = {
            "point": [f"{orig_lat},{orig_lng}", f"{dest_lat},{dest_lng}"],
            "vehicle": vehicle,
            "locale": "es",
            "key": key,
            "instructions": "true",
        }
        encoded_query = urllib.parse.urlencode(route_params, doseq=True)
        final_route_url = ROUTE_URL + encoded_query

        route_reply = requests.get(final_route_url)
        route_status = route_reply.status_code
        route_json = route_reply.json()

        if route_status == 200:
            path_data = route_json["paths"][0]

            # Distancia en metros -> convertir a km y millas
            distance_meters = path_data["distance"]
            distance_km = distance_meters / 1000
            distance_miles = distance_km * 0.621371

            # Duración en milisegundos -> convertir a horas, minutos y segundos
            time_ms = path_data["time"]
            total_seconds = int(time_ms / 1000)
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60

            print("\n" + "-" * 55)
            print("                 RESUMEN DEL VIAJE")
            print("-" * 55)
            print(f"Distancia en Kilómetros : {distance_km:.2f} km")
            print(f"Distancia en Millas     : {distance_miles:.2f} millas")
            print(f"Duración estimada       : {hours:02d}h {minutes:02d}m {seconds:02d}s")
            print("-" * 55)

            # 5. Narrativa del viaje
            print("\nNARRATIVA DEL VIAJE:")
            instructions = path_data.get("instructions", [])
            for idx, step in enumerate(instructions, start=1):
                step_text = step.get("text", "")
                step_km = step.get("distance", 0) / 1000
                print(f"  {idx}. {step_text} ({step_km:.2f} km)")
            print("-" * 55)

        else:
            print(f"\n[!] Error en la API de Rutas (HTTP {route_status}):")
            print(route_json.get("message", "No se pudo calcular la ruta."))


if __name__ == "__main__":
    main()