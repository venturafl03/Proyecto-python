import requests

def obtener_datos(api_url):
    """Obtiene datos JSON desde la API y devuelve una lista de personajes."""
    try:
        respuesta = requests.get(api_url)
        respuesta.raise_for_status()
        return respuesta.json().get('data', [])  # Extraemos el campo 'data' del JSON
    except requests.exceptions.RequestException:
        print("Error: No se pudo conectar a la API")
        return []

def buscar_personaje(personajes):
    """Busca un personaje por su nombre y muestra los resultados."""
    nombre = input("Buscar personaje (nombre): ")
    if nombre:
        # Filtra personajes que contienen el nombre ingresado (sin importar mayúsculas/minúsculas)
        resultados = [p for p in personajes if 'name' in p and nombre.lower() in p['name'].lower()]
        mostrar_resultados(resultados)

def filtrar_por_habilidad(personajes):
    """Filtra personajes por habilidad y muestra los resultados."""
    habilidad = input("Filtrar por habilidad: ")
    if habilidad:
        # Filtra personajes que tienen la habilidad ingresada
        resultados = [p for p in personajes if 'abilities' in p and habilidad.lower() in (h.lower() for h in p.get('abilities', []))]
        mostrar_resultados(resultados)

def mostrar_resultados(resultados):
    """Muestra los resultados en la consola."""
    if resultados:
        for p in resultados:
            alias = p.get('aliases', 'Sin alias')  # Manejo de alias
            habilidades = p.get('abilities', [])  # Manejo de habilidades
            print(f"Nombre: {p['name']}\nAlias: {alias}\nHabilidades: {', '.join(habilidades) or 'Sin habilidades'}\n")
    else:
        print("No se encontraron resultados.")

def main():
    api_url = "https://api.batmanapi.com/v1/characters"
    personajes = obtener_datos(api_url)  # Obtiene los personajes de la API

    if not personajes:
        print("No se encontraron personajes.")
        return

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
    main()  # Ejecuta la función principal al iniciar el script
