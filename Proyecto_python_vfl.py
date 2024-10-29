import requests
import tkinter as tk
from tkinter import messagebox

def obtener_datos(api_url: str) -> dict:
    try:
        respuesta = requests.get(api_url)
        respuesta.raise_for_status()
        return respuesta.json()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Error: {e}")
        return None

def buscar_personaje():
    nombre = nombre_entry.get().lower()
    resultados = [p for p in lista_personajes if nombre in p['name'].lower()]
    mostrar_resultados(resultados)

def filtrar_habilidad():
    habilidad = habilidad_entry.get().lower()
    resultados = [p for p in lista_personajes if habilidad in (h.lower() for h in p.get('abilities', []))]
    mostrar_resultados(resultados)

def mostrar_resultados(resultados):
    text_area.delete("1.0", tk.END)
    if resultados:
        for p in resultados:
            alias = ', '.join(p.get('aliases', [])) or 'Sin alias'
            habilidades = ', '.join(p.get('abilities', [])) or 'Sin habilidades'
            text_area.insert(tk.END, f"Nombre: {p['name']}\nAlias: {alias}\nHabilidades: {habilidades}\n\n")
    else:
        text_area.insert(tk.END, "No encontrado.\n")

def salir_aplicacion():
    root.quit()

def main():
    global lista_personajes, nombre_entry, habilidad_entry, text_area, root
    api_url = "https://api.batmanapi.com/v1/characters"
    response_json = obtener_datos(api_url)

    if response_json and 'data' in response_json:
        lista_personajes = [item['attributes'] for item in response_json['data']]
        root = tk.Tk()
        root.title("Batman API - Búsqueda de Personajes")

        tk.Label(root, text="Nombre del personaje:").pack()
        nombre_entry = tk.Entry(root, width=30)
        nombre_entry.pack()
        tk.Button(root, text="Buscar Personaje", command=buscar_personaje).pack()

        tk.Label(root, text="Habilidad:").pack()
        habilidad_entry = tk.Entry(root, width=30)
        habilidad_entry.pack()
        tk.Button(root, text="Buscar por Habilidad", command=filtrar_habilidad).pack()

        text_area = tk.Text(root, wrap="word", height=10, width=40)
        text_area.pack()
        tk.Button(root, text="Salir", command=salir_aplicacion).pack()

        root.mainloop()
    else:
        messagebox.showerror("Error", "Error al obtener información.")

if __name__ == "__main__":
    main()