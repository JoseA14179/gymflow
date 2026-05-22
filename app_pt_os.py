import flet as ft
import json
from flet import Colors

Ruta_Clientes = "clientes.json"
Ruta_Clientes_Eliminados = "clientes_eliminados.json"

try:
    with open("clientes.json", "r") as f:
        contenido_clientes = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    contenido_clientes = {
        "Juan": {"Edad": "30", "Peso": "80", "Sexo": "M", "Meta": "Ganar masa muscular"},
        "Maria": {"Edad": "25", "Peso": "60", "Sexo": "F", "Meta": "Perder peso"}
    }

try:
     with open("clientes_eliminados.json", "r") as f:
        contenido_eliminados = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    contenido_eliminados = {}

def guardar_en_json():
     with open("clientes.json", "w", encoding="utf-8") as f:
          json.dump(contenido_clientes, f, indent=4, ensure_ascii=False)

def guardar_eliminados_en_json():
     with open("clientes_eliminados.json", "w", encoding="utf-8") as f:
          json.dump(contenido_eliminados, f, indent=4, ensure_ascii=False)

async def main(page: ft.Page):
    page.title= "PT OS - Python - Flet"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    entrada_nombre = ft.TextField(label="Nombre", capitalization=ft.TextCapitalization.WORDS, width=250)
    entrada_edad = ft.TextField(label="Edad", keyboard_type=ft.KeyboardType.NUMBER, width=250)
    entrada_peso = ft.TextField(label="Peso", keyboard_type=ft.KeyboardType.NUMBER, width=250)
    entrada_sexo = ft.TextField(label="Sexo (M/F)", capitalization=ft.TextCapitalization.CHARACTERS, width=250)
    entrada_meta = ft.Dropdown(label="Objetivo", width=250, options=[
        ft.dropdown.Option("perder_peso", "Perder peso"),
        ft.dropdown.Option("ganar_musculo", "Ganar masa muscular"),
        ft.dropdown.Option("ganar_fuerza", "Aumento de la fuerza"),
        ft.dropdown.Option("mejor_rend", "Mejorar rendimiento deportivo")
    ]
    )

    async def mostrar_clientes(e):
        await page.push_route("/clientes")

    async def eliminar_cliente(e):
        if entrada_nombre in contenido_clientes:
            eliminado = contenido_clientes.pop(entrada_nombre)
            contenido_eliminados[entrada_nombre] = eliminado
            guardar_eliminados_en_json()
            guardar_en_json()
            entrada_nombre.value = ""
            page.dialog = ft.AlertDialog(content=ft.Text(f"El cliente {entrada_nombre} ha sido movido a la papelera"))
        elif entrada_nombre in contenido_eliminados:
            page.dialog = ft.AlertDialog(content=ft.Text(f"El cliente {entrada_nombre} ya se encuentra en la papelera"))
        elif entrada_nombre not in contenido_clientes:
            page.dialog = ft.AlertDialog(content=ft.Text(f"El cliente {entrada_nombre} no existe"))
        page.dialog.open = True
        await page.update()

    async def agregar_cliente(e):
        nombre = entrada_nombre.value.strip().title()
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
            page.dialog = ft.AlertDialog(content=ft.Text(f"Ya existe un usuario con el nombre {nombre}"))
            page.dialog.open = True
            await page.update()

        else:
            page.dialog = ft.AlertDialog(content=ft.Text(f"Necesita rellenar todos los campos para crear un nuevo usuario"))
            page.dialog.open = True
            await page.update()
    
    async def change_route(e):
            page.views.clear()
            if page.route == "/":
                page.views.append(vista_inicial(page))
            elif page.route == "/clientes":
                page.views.append(vista_clientes(page))
            elif page.route.startswith("/cliente"):
                nombre_seleccionado = page.route[9:]
                if nombre_seleccionado in contenido_clientes:
                    page.views.append(vista_detalle_cliente(page, nombre_seleccionado))
            page.update()
        
    def vista_inicial(page):
            return ft.View(route="/", controls=[
                ft.Text("Página principal", size=25, weight=ft.FontWeight.BOLD),
                ft.Button("Mostrar Clientes", on_click=mostrar_clientes, bgcolor=Colors.BLUE_400, color="white"),
                ft.Divider(color=Colors.GREY_800),
                entrada_nombre,
                entrada_edad,
                entrada_peso,
                entrada_sexo,
                entrada_meta, 
                ft.Button("Añadir Cliente", on_click=agregar_cliente, bgcolor=Colors.GREEN_300 , color="white"),
                ft.Button("Eliminar Cliente", on_click=eliminar_cliente, bgcolor=Colors.RED_300, color="white")
            ])
        
    def vista_clientes(page):
            return ft.View(route="/clientes", controls=[
                ft.Text("Clientes: ", size=25, weight=ft.FontWeight.BOLD), 
                *[ft.Container(content=ft.Column([
                        ft.Text(f"{cliente}", size=16, weight=ft.FontWeight.BOLD),
                    ]), 
                    bgcolor=Colors.BLUE_200, 
                    border_radius=12, 
                    padding=16, 
                    ink=True,
                    on_click=lambda e, nombre=cliente: page.go(f"/cliente/{nombre}")
                    ) for cliente in contenido_clientes],
                    ft.Divider(color=Colors.GREY_800),
                    ft.Button("Volver a Inicio", on_click=lambda e: page.go("/"))
            ])
    
    def vista_detalle_cliente(page, nombre_cliente):
         datos = contenido_clientes[nombre_cliente]
         return ft.View(route=f"/cliente/{nombre_cliente}", controls=[
              ft.AppBar(title=f"{nombre_cliente.title()}:", bgcolor=Colors.BLACK_87, color="white"),
              ft.Divider(color=Colors.GREY_800),
              ft.Column([
                   ft.Text(f"Edad: {datos.get('Edad')}", size=18),
                   ft.Text(f"Peso corporal actual: {datos.get('Peso')}", size=18),
                   ft.Text(f"Sexo: {datos.get('Sexo')}", size=18),
                   ft.Text(f"Objetivo: {datos.get('Meta')}", size=18)
                ], spacing=12),
                ft.Divider(color=Colors.GREY_800),
                ft.Button("Volver atrás", on_click=mostrar_clientes, bgcolor=Colors.ORANGE_300, color="white")
         ])

    page.on_route_change = change_route
    page.views.append(vista_inicial(page))
    page.update()
    await page.push_route(page.route)

ft.run(main, view=ft.AppView.WEB_BROWSER)