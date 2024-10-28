import requests  # Importa la biblioteca requests para realizar solicitudes HTTP
import tkinter as tk  # Importa tkinter para la creación de interfaces gráficas
from tkinter import messagebox, simpledialog  # Importa messagebox y simpledialog para mostrar diálogos y mensajes

def obtener_datos(api_url: str) -> dict:
    """Función para obtener datos de la API."""
    try:
        respuesta = requests.get(api_url)  # Realiza una solicitud GET a la API
        respuesta.raise_for_status()  # Lanza un error si hay un código de error HTTP
        return respuesta.json()  # Devuelve el contenido de la respuesta en formato JSON
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Error al obtener datos de la API: {e}")  # Muestra un mensaje de error
        return None  # Devuelve None si la solicitud falla

def buscar_personaje():
    """Función para buscar un personaje por nombre."""
    nombre = simpledialog.askstring("Buscar Personaje", "Nombre del personaje:")  # Solicita el nombre del personaje
    if nombre:
        # Filtra personajes que contienen el nombre ingresado
        resultados = [p for p in lista_personajes if nombre.lower() in p['name'].lower()]
        mostrar_resultados(resultados, f"Resultados para '{nombre}'")  # Muestra los resultados

def filtrar_por_habilidad():
    """Función para filtrar personajes por habilidad."""
    habilidad = simpledialog.askstring("Filtrar por Habilidad", "Habilidad:")  # Solicita la habilidad
    if habilidad:
        # Filtra personajes que tienen la habilidad ingresada
        resultados = [p for p in lista_personajes if habilidad.lower() in (h.lower() for h in p.get('abilities', []))]
        mostrar_resultados(resultados, f"Resultados para habilidad '{habilidad}'")  # Muestra los resultados

def mostrar_resultados(resultados, titulo):
    """Función para mostrar los resultados en la interfaz gráfica."""
    text_area.delete("1.0", tk.END)  # Limpia el área de texto
    text_area.insert(tk.END, f"{titulo}:\n\n")  # Inserta el título de los resultados
    
    if resultados:
        for p in resultados:
            # Obtiene alias y habilidades del personaje
            alias = p.get('aliases', 'Sin alias')
            habilidades = p.get('abilities', [])
            # Muestra el nombre, alias y habilidades del personaje en el área de texto
            text_area.insert(tk.END, f"Nombre: {p['name']}\nAlias: {alias}\nHabilidades: {', '.join(habilidades) or 'Sin habilidades'}\n\n")
    else:
        text_area.insert(tk.END, "No se encontraron resultados.")  # Muestra mensaje si no hay resultados

def main():
    """Función principal para iniciar la interfaz gráfica."""
    global lista_personajes, text_area  # Declara variables globales
    
    api_url = "https://api.batmanapi.com/v1/characters"  # URL de la API
    response_json = obtener_datos(api_url)  # Obtiene datos de la API

    if response_json and 'data' in response_json:
        # Extrae la lista de personajes de los datos obtenidos
        lista_personajes = [item['attributes'] for item in response_json['data']]
        
        # Crea la ventana principal
        root = tk.Tk()
        root.title("Aplicación de Personajes")
        
        # Crea el área de texto para mostrar resultados
        text_area = tk.Text(root, wrap="word", width=60, height=20)
        text_area.pack(padx=10, pady=10)
        
        # Crea un botón para buscar personaje
        btn_buscar = tk.Button(root, text="Buscar Personaje", command=buscar_personaje)
        btn_buscar.pack(pady=5)
        
        # Crea un botón para filtrar por habilidad
        btn_filtrar = tk.Button(root, text="Filtrar por Habilidad", command=filtrar_por_habilidad)
        btn_filtrar.pack(pady=5)
        
        # Crea un botón para salir de la aplicación
        btn_salir = tk.Button(root, text="Salir", command=root.quit)
        btn_salir.pack(pady=5)
        
        # Ejecuta el bucle principal de la interfaz gráfica
        root.mainloop()
    else:
        print("Error al obtener información.")  # Muestra un mensaje de error si no se obtienen datos

if __name__ == "__main__":
    main()  # Ejecuta la función principal
