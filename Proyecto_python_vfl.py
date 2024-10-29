import requests

def obtener_datos(api_url):
    """Descarga datos JSON desde la URL dada."""
    try:
        respuesta = requests.get(api_url)
        respuesta.raise_for_status()
        return respuesta.json()['data']  # Devuelve solo los datos de personajes
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener datos: {e}")
        return []

def buscar_personaje(personajes):
    """Busca personajes por nombre."""
    nombre = input("Buscar personaje (nombre): ")
    if nombre:
        resultados = [p for p in personajes if nombre.lower() in p['attributes']['name'].lower()]
        if resultados:
            for p in resultados:
                mostrar_info_personaje(p)
        else:
            print("No se encontraron personajes con ese nombre.")

def filtrar_por_habilidad(personajes):
    """Filtra personajes por habilidad."""
    habilidad = input("Filtrar por habilidad: ")
    if habilidad:
        resultados = [p for p in personajes if habilidad.lower() in (h.lower() for h in p['attributes'].get('abilities', []))]
        if resultados:
            for p in resultados:
                mostrar_info_personaje(p)
        else:
            print("No se encontraron personajes con esa habilidad.")

def mostrar_info_personaje(personaje):
    """Muestra la información de un personaje."""
    atributos = personaje['attributes']
    nombre = atributos.get('name', 'Sin nombre')
    alias = atributos.get('alias', 'Sin alias')
    habilidades = atributos.get('abilities', [])
    print(f"Nombre: {nombre}\nAlias: {alias}\nHabilidades: {', '.join(habilidades) if habilidades else 'Sin habilidades'}\n")

def main():
    api_url = "https://api.batmanapi.com/v1/characters"
    personajes = obtener_datos(api_url)

    if not personajes:
        print("No se pudieron obtener personajes de la API.")
        return

    print("Datos obtenidos de la API:")
    for personaje in personajes:
        mostrar_info_personaje(personaje)

    while True:
        print("\nOpciones:")
        print("1. Buscar personaje")
        print("2. Filtrar por habilidad")
        print("3. Salir")
        
        opcion = input("Elige una opción (1-3): ")
        if opcion == '1':
            buscar_personaje(personajes)
        elif opcion == '2':
            filtrar_por_habilidad(personajes)
        elif opcion == '3':
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main()