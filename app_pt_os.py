import flet as ft
import json
from flet import Colors

Clientes = "clientes.json"
Clientes_Eliminados = "clientes_eliminados.json"

try:
    with open(Clientes, "r", encoding="utf-8") as f:
        contenido_clientes = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    contenido_clientes = {}

try:
    with open(Clientes_Eliminados, "r", encoding="utf-8") as f:
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
    page.title = "PT OS - Python"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    entrada_nombre = ft.TextField(label="Nombre", width=350, capitalization=ft.TextCapitalization.WORDS)
    entrada_edad = ft.TextField(label="Edad", width=350, keyboard_type=ft.KeyboardType.NUMBER)
    entrada_peso = ft.TextField(label="Peso", width=350, keyboard_type=ft.KeyboardType.NUMBER)
    entrada_sexo = ft.TextField(label="Sexo (M/F)", width=350, capitalization=ft.TextCapitalization.CHARACTERS)
    entrada_meta = ft.Dropdown(
        label="Objetivo",
        width=350,
        options=[
            ft.dropdown.Option("perder_peso", "Perder peso"),
            ft.dropdown.Option("ganar_musculo", "Ganar masa muscular"),
            ft.dropdown.Option("ganar_fuerza", "Aumento de la fuerza"),
            ft.dropdown.Option("mejor_rend", "Mejorar rendimiento deportivo")
        ]
    )

    mensaje_estado = ft.Text(value="", color=Colors.ORANGE_400, weight=ft.FontWeight.BOLD)

    def mostrar_clientes(e):
        if contenido_clientes:
            page.go("/clientes")
        else:
            page.dialog = ft.AlertDialog(content=ft.Text("No hay clientes"))
            page.dialog.open = True
            page.update()

    def agregar_cliente(e):
        nombre = entrada_nombre.value.strip().title()
        edad = entrada_edad.value.strip()
        peso = entrada_peso.value.strip()
        sexo = entrada_sexo.value.strip().upper()
        meta = entrada_meta.value

        if not nombre:
            mensaje_estado.value = "Debe rellenar el nombre"
            mensaje_estado.color = Colors.RED_400
            page.update()

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
        entrada_meta.value = None

        mensaje_estado.value = f"Cliente {nombre} añadido con éxito"
        mensaje_estado.color = Colors.GREEN_400
        page.update()

    def eliminar_cliente(e):
        nombre = entrada_nombre.value.strip().title()
        if not nombre:
            mensaje_estado.value = "Introduce un nombre para eliminar"
            mensaje_estado.color = Colors.RED_400
            page.update()

        if nombre in contenido_clientes:
            eliminado = contenido_clientes.pop(nombre)
            contenido_eliminados[nombre] = eliminado
            guardar_eliminados_en_json()
            guardar_en_json()
            entrada_nombre.value = ""
            mensaje_estado.value = f"El cliente {nombre} ha sido movido a la papelera"
            mensaje_estado.color = Colors.ORANGE_400
            page.go("/clientes")
        elif nombre in contenido_eliminados:
            mensaje_estado.value = f"El cliente {nombre} ya está en la papelera"
            mensaje_estado.color = Colors.YELLOW_600
            page.update()
        else:
            mensaje_estado.value = f"El cliente {nombre} no existe"
            mensaje_estado.color = Colors.RED_400
            page.update()

    def change_route(e):
        current_route = page.route
        if not current_route:
            page.go("/")
            return
        page.views.clear()

        if current_route == "/":
            page.views.append(
                ft.View(
                    route="/",
                    controls=[
                        ft.Text("Página principal", size=25, weight=ft.FontWeight.BOLD),
                        ft.Button("Mostrar Clientes", on_click=mostrar_clientes, bgcolor=Colors.BLUE_400, color="white"),
                        ft.Divider(color=Colors.GREY_800),
                        entrada_nombre,
                        entrada_edad,
                        entrada_peso,
                        entrada_sexo,
                        entrada_meta,
                        ft.Button("Añadir Cliente", on_click=agregar_cliente, bgcolor=Colors.GREEN_300, color="white"),
                        ft.Button("Eliminar Cliente", on_click=eliminar_cliente, bgcolor=Colors.RED_300, color="white"),
                        mensaje_estado,
                    ],
                )
            )
        elif current_route == "/clientes":
            controls = [
                ft.Button("Volver a inicio", on_click=lambda e: page.go("/"), bgcolor=Colors.BLACK_300, color="white"),
                ft.Divider(color=Colors.GREY_800),
                ft.Text("Clientes:", size=25, weight=ft.FontWeight.BOLD),
            ]
            if contenido_clientes:
                for nombre, datos in contenido_clientes.items():
                    controls.append(
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text(nombre, size=16, weight=ft.FontWeight.BOLD),
                                    ft.Text(
                                        f"{datos.get('Edad')} | {datos.get('Peso')} | {datos.get('Sexo')} | {datos.get('Meta')}",
                                        size=16,
                                        color=Colors.GREY_500,
                                    ),
                                ],
                                spacing=4,
                            ),
                            bgcolor=Colors.SURFACE_VARIANT,
                            border_radius=12,
                            padding=16,
                            margin=ft.margin.only(bottom=8),
                            ink=True,
                            on_click=lambda e, nombre=nombre: page.go(f"/cliente/{nombre}"),
                        )
                    )
            else:
                controls.append(ft.Text("No hay clientes activos"))

            page.views.append(
                ft.View(
                    route="/clientes",
                    controls=[
                        ft.AppBar(title=ft.Text("Lista de Clientes"), bgcolor=Colors.ON_SURFACE_VARIANT, color="white"),
                        ft.Column(controls, spacing=10),
                    ],
                )
            )
        elif current_route.startswith("/cliente/"):
            nombre_seleccionado = current_route[9:]
            datos = contenido_clientes.get(nombre_seleccionado, {})
            page.views.append(
                ft.View(
                    route=current_route,
                    controls=[
                        ft.AppBar(title=ft.Text(f"Ficha de: {nombre_seleccionado}"), bgcolor=Colors.ON_SURFACE_VARIANT),
                        ft.Column(
                            [
                                ft.Text(nombre_seleccionado, size=24, weight=ft.FontWeight.BOLD, color=Colors.BLUE_400),
                                ft.Divider(),
                                ft.Text(f"Edad: {datos.get('Edad')}", size=16),
                                ft.Text(f"Peso: {datos.get('Peso')}", size=16),
                                ft.Text(f"Sexo: {datos.get('Sexo')}", size=16),
                                ft.Text(f"Meta: {datos.get('Meta')}", size=16),
                                ft.Divider(height=20),
                                ft.ElevatedButton("Volver a la lista", on_click=lambda e: page.go("/clientes"), bgcolor=Colors.ORANGE_300, color="white"),
                                ft.ElevatedButton("Volver al inicio", on_click=lambda e: page.go("/"), bgcolor=Colors.GREY_800, color="white"),
                            ],
                            spacing=10,
                        ),
                    ],
                )
            )

        page.update()

    def view_pop(e):
        if page.views:
            page.views.pop()
            if page.views:
                page.go(page.views[-1].route)

    page.on_route_change = change_route
    page.on_view_pop = view_pop

    if not page.route:
        page.go("/")
    else:
        change_route(None)

ft.run(main)