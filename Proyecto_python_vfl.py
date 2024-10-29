import requests

def obtener_datos(api_url):
    """Descarga datos desde la API y los retorna como una lista de personajes."""
    try:
        respuesta = requests.get(api_url)
        respuesta.raise_for_status()
        return respuesta.json()  # Retorna el JSON completo
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        return []

def buscar_personaje(personajes):
    """Busca un personaje por nombre."""
    nombre = input("Nombre del personaje a buscar: ")
    if nombre:
        # Filtra personajes que contienen el nombre ingresado (sin importar mayúsculas/minúsculas)
        resultados = [p for p in personajes if 'name' in p and nombre.lower() in p['name'].lower()]
        mostrar_resultados(resultados)

def filtrar_por_habilidad(personajes):
    """Filtra personajes por habilidad."""
    habilidad = input("Filtrar por habilidad: ")
    if habilidad:
        # Filtra personajes que tienen la habilidad ingresada en sus 'powerstats'
        resultados = [p for p in personajes if 'powerstats' in p and habilidad.lower() in (v.lower() for v in p['powerstats'].values())]
        mostrar_resultados(resultados)

def mostrar_resultados(resultados):
    """Muestra los personajes encontrados."""
    if resultados:
        for p in resultados:
            habilidades = p.get('powerstats', {})
            print(f"Nombre: {p.get('name', 'Desconocido')}")
            print(f"Habilidades: {', '.join(habilidades.keys()) if habilidades else 'Sin habilidades'}")
            print("\n" + "-" * 20)
    else:
        print("No se encontraron resultados.")

def main():
    api_url = "https://akabab.github.io/superhero-api/api/all.json"  # API de superhéroes
    personajes = obtener_datos(api_url)

    if not personajes:
        print("No se encontraron personajes.")
        return

    while True:
        print("\nOpciones:")
        print("1. Buscar personaje por nombre")
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
