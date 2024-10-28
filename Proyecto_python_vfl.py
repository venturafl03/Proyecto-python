import requests  # Importa la biblioteca requests para realizar solicitudes HTTP

def obtener_datos(api_url: str) -> dict:
    try:
        respuesta = requests.get(api_url)  # Realiza una solicitud GET a la API
        respuesta.raise_for_status()  # Lanza un error si hay un código de error HTTP
        return respuesta.json()  # Devuelve el contenido de la respuesta en formato JSON
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")  # Muestra un mensaje de error si ocurre una excepción
        return None  # Devuelve None si la solicitud falla
def main():
    api_url = "https://api.batmanapi.com/v1/characters"  # URL de la API
    response_json = obtener_datos(api_url)  # Obtiene datos de la API

    if response_json and 'data' in response_json:  # Verifica la respuesta
        lista_personajes = [item['attributes'] for item in response_json['data']]  # Extrae personajes
        
        while True:  # Inicia el menú
            opcion = input("\nOpciones:\n1. Buscar personaje\n2. Filtrar por habilidad\n3. Salir\nSeleccione (1-3): ")
            
            if opcion == '1':  # Opción para buscar personaje
                nombre = input("Nombre del personaje: ")  # Solicita el nombre
                resultados = [p for p in lista_personajes if nombre.lower() in p['name'].lower()]  # Filtra por nombre
                
                if resultados:  # Si se encuentran resultados
                    for p in resultados:  # Itera sobre los resultados
                        alias = p.get('aliases', 'Sin alias')  # Obtiene el alias
                        habilidades = p.get('abilities', [])  # Obtiene habilidades
                        print(f"Nombre: {p['name']}\nAlias: {alias}\nHabilidades: {', '.join(habilidades) or 'Sin habilidades'}\n")
                else:
                    print("No encontrado.")  # Mensaje si no se encuentran resultados
                
            elif opcion == '2':  # Opción para filtrar por habilidad
                habilidad = input("Habilidad: ")  # Solicita la habilidad
                resultados = [p for p in lista_personajes if habilidad.lower() in (h.lower() for h in p.get('abilities', []))]  # Filtra por habilidad
                
                if resultados:  # Si se encuentran resultados
                    for p in resultados:  # Itera sobre los resultados
                        alias = p.get('aliases', 'Sin alias')  # Obtiene el alias
                        habilidades = p.get('abilities', [])  # Obtiene habilidades
                        print(f"Nombre: {p['name']}\nAlias: {alias}\nHabilidades: {', '.join(habilidades) or 'Sin habilidades'}\n")
                else:
                    print("No encontrado.")  # Mensaje si no se encuentran resultados
                
            elif opcion == '3':  # Opción para salir
                print("¡Hasta luego!")  # Mensaje de despedida
                break  # Sale del bucle
            
            else:  # Opción no válida
                print("Opción no válida.")  # Mensaje de error

    else:  # Si no se obtienen datos de la API
        print("Error al obtener información.")  # Muestra un mensaje de error

if __name__ == "__main__":  # Verifica si el script se ejecuta directamente
    main()  # Ejecuta la función principal
