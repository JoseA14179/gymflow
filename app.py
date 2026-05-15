import tkinter as tk
import json
###mirar como funciona flask 

Clientes = 'clientes.json'
Clientes_eliminados = 'clientes_eliminados.json'

try:
    with open(Clientes, "r", encoding='utf-8') as archivo:
        clientes = json.load(archivo)
except (FileNotFoundError, json.JSONDecodeError):
    clientes = {}

try:
    with open(Clientes_eliminados, "r", encoding='utf-8') as archivo:
        clientes_eliminados = json.load(archivo)
except (FileNotFoundError, json.JSONDecodeError):
    clientes_eliminados = {}

def guardar_en_json():
    with open(Clientes, "w", encoding='utf-8') as archivo:
        json.dump(clientes, archivo, indent=4, ensure_ascii=False)

def guardar_eliminados_en_json():
    with open(Clientes_eliminados, "w", encoding='utf-8') as archivo:
        json.dump(clientes_eliminados, archivo, indent=4, ensure_ascii=False)

def mostrar_clientes():
    campo.delete("1.0", tk.END)
    for cliente, datos in clientes.items():
        info = (f"{cliente.upper()}:\n"
                f"- Edad: {datos['edad']} años\n"
                f"- Sexo: {datos['sexo']}\n"
                f"- Objetivo: {datos['meta']}\n"
                f"{'-'*30}")
        campo.insert(tk.END, info +  "\n")
    
def agregar_cliente():
    nombre = entrada_cliente.get().strip().title()
    edad = entrada_edad.get().strip()
    sexo = entrada_sexo.get().strip()
    meta = entrada_meta.get().strip()
    if nombre:
        clientes[nombre] = {
            "edad": edad,
            "sexo": sexo,
            "meta": meta
        }
        guardar_en_json()
        entrada_cliente.delete(0, tk.END)
        entrada_edad.delete(0, tk.END)
        entrada_sexo.delete(0, tk.END)
        entrada_meta.delete(0, tk.END)
        mostrar_clientes()
    else:
        return None

def eliminar_cliente():
    nombre = entrada_cliente.get().strip().title()
    if nombre in clientes:
        datos_eliminados = clientes.pop(nombre)
        guardar_eliminados_en_json()
        clientes_eliminados[nombre] = datos_eliminados
        mostrar_clientes()
        campo.insert(tk.END, f"Se ha movido a la papelera a: {nombre}")
    else:
        campo.delete("1.0", tk.END)
        campo.insert(tk.END, "No hay clientes para eliminar")
    
def buscar_cliente():
    nombre = entrada_cliente.get().strip().title()
    campo.delete("1.0", tk.END)
    if nombre in clientes:
        campo.insert(tk.END, f"El usuario {nombre} está dado de alta")
    elif nombre in clientes_eliminados:
        campo.insert(tk.END, f"AVISO:\nEl usuario {nombre} se encuentra en la papelera")
    else:
        campo.insert(tk.END, f"ERROR:\nEl usuario {nombre} no existe")

ventana = tk.Tk()
ventana.title("App de entrenamiento personal - Python")
ventana.geometry("600x900")

boton_buscar = tk.Button(ventana, text="Buscar cliente", command=buscar_cliente, bg="orange", fg="white", width=20)
boton_buscar.grid(row=0, column=0, columnspan=2, pady=10)

label_nombre = tk.Label(ventana, text="Nombre:")
label_nombre.grid(row=1, column=0, sticky="w", padx=10, pady=5)
entrada_cliente = tk.Entry(ventana, width=40)
entrada_cliente.grid(row=1, column=1, padx=10, pady=5)

label_edad = tk.Label(ventana, text="Edad:")
label_edad.grid(row=2, column=0, sticky="w", padx=10, pady=5)
entrada_edad = tk.Entry(ventana, width=40)
entrada_edad.grid(row=2, column=1, padx=10, pady=5)

label_sexo = tk.Label(ventana, text="Sexo (M/F):")
label_sexo.grid(row=3, column=0, sticky="w", padx=10, pady=5)
entrada_sexo = tk.Entry(ventana, width=40)
entrada_sexo.grid(row=3, column=1, padx=10, pady=5)

label_meta = tk.Label(ventana, text="Objetivo:")
label_meta.grid(row=4, column=0, sticky="w", padx=10, pady=5)
entrada_meta = tk.Entry(ventana, width=40)
entrada_meta.grid(row=4, column=1, padx=10, pady=5)

boton_nuevo_cliente = tk.Button(ventana, text="Añadir nuevo cliente", command=agregar_cliente, bg="green", fg="white")
boton_nuevo_cliente.grid(row=5, column=0, columnspan=2, pady=20)

campo = tk.Text(ventana, width=60, height=15)
campo.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

boton_clientes = tk.Button(ventana, text="Mostrar clientes", command=mostrar_clientes, bg="blue", fg="white", width=30)
boton_clientes.grid(row=7, column=0, columnspan=2, pady=10)

boton_eliminar_cliente = tk.Button(ventana, text="Eliminar último cliente", command=eliminar_cliente, bg="red", fg="white", width=30)
boton_eliminar_cliente.grid(row=8, column=0, columnspan=2, pady=10)

ventana.mainloop()