import requests  # Importa la biblioteca requests para realizar solicitudes HTTP
import tkinter as tk  # Importa tkinter para crear la interfaz gráfica
from tkinter import messagebox, simpledialog  # Importa messagebox y simpledialog para mostrar diálogos y mensajes de error

def obtener_datos(api_url: str) -> dict:
    """Obtiene datos JSON desde una API."""
    try:
        respuesta = requests.get(api_url)  # Realiza una solicitud GET a la API con la URL proporcionada
        respuesta.raise_for_status()  # Lanza una excepción si la respuesta HTTP contiene un error
        return respuesta.json()  # Retorna la respuesta en formato JSON si es exitosa
    except requests.exceptions.RequestException as e:  # Captura excepciones relacionadas con la solicitud
        messagebox.showerror("Error", f"No se pudo conectar: {e}")  # Muestra un mensaje de error en la interfaz gráfica
        return None  # Retorna None si ocurre una excepción para indicar que la solicitud falló

def buscar_personaje():
    """Busca un personaje por nombre y muestra los resultados."""
    nombre = simpledialog.askstring("Buscar Personaje", "Nombre del personaje:")  # Muestra un cuadro de diálogo para ingresar el nombre
    if nombre:  # Verifica que el usuario haya ingresado un nombre
        # Filtra los personajes que contienen el nombre ingresado (ignorando mayúsculas y minúsculas)
        resultados = [p for p in lista_personajes if nombre.lower() in p['name'].lower()]
        mostrar_resultados(resultados, f"Resultados para '{nombre}'")  # Muestra los resultados en la interfaz

def filtrar_por_habilidad():
    """Filtra personajes por habilidad y muestra los resultados."""
    habilidad = simpledialog.askstring("Filtrar por Habilidad", "Habilidad:")  # Muestra un cuadro de diálogo para ingresar una habilidad
    if habilidad:  # Verifica que el usuario haya ingresado una habilidad
        # Filtra los personajes que tienen la habilidad ingresada (ignorando mayúsculas y minúsculas)
        resultados = [p for p in lista_personajes if habilidad.lower() in (h.lower() for h in p.get('abilities', []))]
        mostrar_resultados(resultados, f"Resultados para habilidad '{habilidad}'")  # Muestra los resultados en la interfaz

def mostrar_resultados(resultados, titulo):
    """Muestra resultados en el área de texto."""
    text_area.delete("1.0", tk.END)  # Limpia el área de texto, eliminando el contenido actual
    text_area.insert(tk.END, f"{titulo}:\n\n")  # Inserta el título de la búsqueda en el área de texto
    
    for p in resultados:  # Itera sobre los resultados encontrados
        alias = p.get('aliases', 'Sin alias')  # Obtiene el alias del personaje, o indica "Sin alias" si no tiene
        habilidades = p.get('abilities', [])  # Obtiene las habilidades del personaje, o devuelve una lista vacía
        # Inserta en el área de texto el nombre, alias y habilidades del personaje
        text_area.insert(tk.END, f"Nombre: {p['name']}\nAlias: {alias}\nHabilidades: {', '.join(habilidades) or 'Sin habilidades'}\n\n")
    
    if not resultados:  # Si no se encuentran resultados en la búsqueda
        text_area.insert(tk.END, "No se encontraron resultados.")  # Muestra un mensaje indicando que no hubo coincidencias

def main():
    """Inicializa la GUI y obtiene los datos de la API."""
    global lista_personajes, text_area  # Declara variables globales para usarlas en otras funciones
    
    api_url = "https://api.batmanapi.com/v1/characters"  # Define la URL de la API para obtener personajes
    response_json = obtener_datos(api_url)  # Llama a la función para obtener datos de la API y almacena la respuesta

    if response_json and 'data' in response_json:  # Verifica que la respuesta tenga datos válidos
        # Extrae la lista de personajes del campo 'data' en la respuesta
        lista_personajes = [item['attributes'] for item in response_json['data']]
        
        root = tk.Tk()  # Crea la ventana principal de la interfaz gráfica
        root.title("Aplicación de Personajes")  # Establece el título de la ventana
        
        text_area = tk.Text(root, wrap="word", width=60, height=20)  # Crea un área de texto para mostrar los resultados
        text_area.pack(padx=10, pady=10)  # Coloca el área de texto en la ventana con un pequeño margen
        
        # Crea y coloca un botón para buscar personajes por nombre
        tk.Button(root, text="Buscar Personaje", command=buscar_personaje).pack(pady=5)
        
        # Crea y coloca un botón para filtrar personajes por habilidad
        tk.Button(root, text="Filtrar por Habilidad", command=filtrar_por_habilidad).pack(pady=5)
        
        # Crea y coloca un botón para salir de la aplicación
        tk.Button(root, text="Salir", command=root.quit).pack(pady=5)

        root.mainloop()  # Inicia el bucle principal de la interfaz gráfica para que permanezca abierta
    else:  # Si no se obtienen datos válidos de la API
        print("Error al obtener información.")  # Imprime un mensaje de error en la consola

if __name__ == "__main__":
    main()  # Ejecuta la función principal al iniciar el script
