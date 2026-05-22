import flet as ft
import json
from flet import Colors

Clientes = "clientes.json"
Clientes_Eliminados = "clientes_eliminados.json"

try:
    with open(Clientes, "r") as f:
        contenido_clientes = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    contenido_clientes = {}

try:
     with open(Clientes_Eliminados, "r") as f:
        contenido_eliminados = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    contenido_eliminados = {}

def guardar_en_json():
     with open(Clientes, "w", encoding="utf-8") as f:
          json.dump(contenido_clientes, f, indent=4, ensure_ascii=False)

def guardar_eliminados_en_json():
     with open(Clientes_Eliminados, "w", encoding="utf-8") as f:
          json.dump(contenido_eliminados, f, indent=4, ensure_ascii=False)

def main(page: ft.Page):
    page.title= "PT OS - Python - Flet"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    entrada_nombre = ft.TextField(label="Nombre", capitalization=ft.TextCapitalization.CAPITAL, width=250)
    entrada_edad = ft.TextField(label="Edad", keyboard_type=ft.keyboardType.NUMBER, width=250)
    entrada_peso = ft.TextField(label="Peso", keyboard_type=ft.keyboardType.NUMBER, width=250)
    entrada_sexo = ft.TextField(label="Sexo (M/F)", capitalization=ft.TextCapitalization.CAPITAL, width=250)
    entrada_meta = ft.Dropdown(label="Objetivo", width=250, options=[
        ft.dropdown.Option("perder_peso", "Perder peso"),
        ft.dropdown.Option("ganar_musculo", "Ganar masa muscular"),
        ft.dropdown.Option("ganar_fuerza", "Aumento de la fuerza"),
        ft.dropdown.Option("mejor_rend", "Mejorar rendimiento deportivo")
    ]
    )

    def mostrar_clientes(e):
        page.go("/clientes")

    def eliminar_cliente(e):
        if entrada_nombre in Clientes:
            page.dialog(ft.AlertDialog(content=ft.Text(f"El cliente {entrada_nombre} ha sido movido a la papelera")))
            eliminado = Clientes.pop(entrada_nombre)
            Clientes_Eliminados[entrada_nombre] = eliminado
            guardar_eliminados_en_json()
            guardar_en_json()
            entrada_nombre.value = ""
        elif entrada_nombre in Clientes_Eliminados:
            page.dialog(ft.AlertDialog(content=ft.Text(f"El cliente {entrada_nombre} ya se encuentra en la papelera")))
        elif entrada_nombre not in Clientes:
            page.dialog(ft.AlertDialog(content=ft.Text(f"El cliente {entrada_nombre} no existe")))

    def agregar_cliente(e):
        nombre = entrada_nombre.value().strip()
        edad = entrada_edad.value.strip()
        peso = entrada_peso.value.strip()
        sexo = entrada_sexo.value.strip().upper()
        meta = entrada_meta.value 
        if nombre and edad and peso and sexo and meta:
            contenido_clientes[nombre] = {
                  "Edad": edad,
                  "Peso": peso,
                  "Sexo": sexo,
                  "Meta": meta,
            }
            guardar_en_json()
            entrada_nombre.value = ""
            entrada_edad.value = ""
            entrada_peso.value = ""
            entrada_sexo.value = ""
            entrada_meta.value = ""
        elif nombre in contenido_clientes:
            page.dialog(ft.AlertDialog(content=ft.Text(f"Ya existe un usuario con el nombre {nombre}")))
        else:
            page.dialog(ft.AlertDialog(content=ft.Text(f"Necesita rellenar todos los campos para crear un nuevo usuario")))
        
    def vista_inicial(page):
            return ft.View("/", [
                ft.Text("Página principal", size=25, weight=ft.FontWeight.BOLD),
                ft.ElevatedButton("Mostrar Clientes", on_click=mostrar_clientes, bgcolor=Colors.BLUE_400, color="white"),
                ft.Divider(color=Colors.GREY_800),
                entrada_nombre,
                entrada_edad,
                entrada_peso,
                entrada_sexo,
                entrada_meta, 
                ft.ElevatedButton("Añadir Cliente", on_click=agregar_cliente, bgcolor=Colors.GREEN_300 , color="white"),
                ft.ElevatedButton("Eliminar Cliente", on_click=eliminar_cliente, bgcolor=Colors.RED_300, color="white")
            ])
        
    def vista_clientes(page):
            return ft.View("/clientes", [
                ft.Text("Clientes: ", size=25, weight=ft.FontWeight.BOLD), 
                *[ft.Container(content=ft.Column([
                        ft.Text(f"{cliente}", size=16, weight=ft.FontWeight.BOLD),
                        ft.Text(f"{cliente['Edad']} | {cliente['Peso']} | {cliente['Sexo']} | {cliente['Meta']}", size=16, color=Colors.GREY_500)
                    ]), 
                    bgcolor=Colors.SURFACE_VARIANT, 
                    border_radius=12, 
                    padding=16, 
                    margin=ft.margin.only(bottom=8),
                    ink=True,
                    on_click=lambda e, nombre=cliente: page.go(f"/cliente/{nombre}")
                    ) for cliente in contenido_clientes]
            ])
    
    def vista_detalle_cliente(page, nombre_cliente):
         datos = Clientes[nombre_cliente]
         return ft.View(route=f"/cliente/{nombre_cliente}", controls=[
              ft.AppBar(text=f"{nombre_cliente.title()}:", size=25, weight=ft.FontWeight.BOLD, bgcolor=Colors.BLACK_300, color="white"),
              ft.Divider(color=Colors.GREY_800),
              ft.Column([
                   ft.Text(text=f"{datos.get('Edad')}", size=16),
                   ft.Text(text=f"{datos.get('Peso')}", size=16),
                   ft.Text(text=f"{datos.get('Sexo')}", size=16),
                   ft.Text(text=f"{datos.get('Meta')}", size=16)
                ], spacing=10),
                ft.Divider(color=Colors.GREY_800),
                ft.ElevatedButton("Volver atrás", on_click=mostrar_clientes, bgcolor=Colors.ORANGE_300, color="white")
         ])
    
    def change_route(e):
            page.views.clear()
            if page.route == "/":
                page.views.append(vista_inicial(page))
            elif page.route == "/clientes":
                page.views.append(vista_clientes(page))
            elif page.route.startswith("/cliente"):
                nombre_seleccionado = page.route[9:]
                if nombre_seleccionado in Clientes:
                    page.views.append(vista_detalle_cliente(page, nombre_seleccionado))
                    page.update()

    page.on_route_change = change_route
    page.go(page.route or "/")

ft.run(main)