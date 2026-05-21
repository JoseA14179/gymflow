import flet as ft
from flet import Colors
import json

# Ruta JSON
Clientes = 'clientes.json'
Clientes_eliminados = 'clientes_eliminados.json'

# Carga inicial de archivos JSON
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

# Ficheros  JSON de clientes activos y eliminados
def guardar_en_json():
    with open(Clientes, "w", encoding='utf-8') as archivo:
        json.dump(clientes, archivo, indent=4, ensure_ascii=False)

def guardar_eliminados_en_json():
    with open(Clientes_eliminados, "w", encoding='utf-8') as archivo:
        json.dump(clientes_eliminados, archivo, indent=4, ensure_ascii=False)


def main(page: ft.Page):
    # Configuración de la ventana principal
    page.title = "App de entrenamiento personal - Flet - Python"
    page.window_width = 600
    page.window_height = 850
    page.theme_mode = ft.ThemeMode.LIGHT

    # --- Inputs ---
    entrada_cliente = ft.TextField(label="Nombre del Cliente", width=400, capitalization=ft.TextCapitalization.WORDS)
    entrada_edad = ft.TextField(label="Edad", width=400, keyboard_type=ft.KeyboardType.NUMBER)
    entrada_sexo = ft.TextField(label="Sexo (M/F)", width=400, capitalization=ft.TextCapitalization.CHARACTERS)
    entrada_meta = ft.TextField(label="Objetivo / Meta", width=400, capitalization=ft.TextCapitalization.SENTENCES)
    
    # Texto auxiliar para mensajes del sistema
    texto_consola = ft.Text(value="", color=Colors.ORANGE_400, weight=ft.FontWeight.BOLD)

    # --- FUNCIONES DE LA INTERFAZ ---
    
    def mostrar_clientes(e=None):
        # Esta función ahora solo navega a la lista
        page.go("/clientes")

    def agregar_cliente(e):
        nombre = entrada_cliente.value.strip().title()
        edad = entrada_edad.value.strip()
        sexo = entrada_sexo.value.strip()
        meta = entrada_meta.value.strip()
        
        if nombre:
            clientes[nombre] = {
                "edad": edad,
                "sexo": sexo,
                "meta": meta
            }
            guardar_en_json()
            
            # Limpiamos los cuadros de texto
            entrada_cliente.value = ""
            entrada_edad.value = ""
            entrada_sexo.value = ""
            entrada_meta.value = ""
            
            texto_consola.value = f"¡Cliente {nombre} añadido con éxito!"
            texto_consola.color = Colors.GREEN_400
            
            page.update()
        else:
            texto_consola.value = "Error: El campo de nombre es obligatorio."
            texto_consola.color = Colors.RED_400
            page.update()

    def eliminar_cliente(e):
        nombre = entrada_cliente.value.strip().title()
        if nombre in clientes:
            datos_eliminados = clientes.pop(nombre)
            clientes_eliminados[nombre] = datos_eliminados
            guardar_eliminados_en_json()
            guardar_en_json()
            entrada_cliente.value = ""
            texto_consola.value = f"Se ha movido a la papelera a: {nombre}"
            texto_consola.color = Colors.RED_300
            page.go("/clientes")
        else:
            texto_consola.value = "Introduce un nombre válido en el campo superior para eliminar"
            texto_consola.color = Colors.RED_400
            page.update()
        
    def buscar_cliente(e):
        nombre = entrada_cliente.value.strip().title()
        if not nombre:
            texto_consola.value = "Por favor, escribe un nombre para buscar."
            texto_consola.color = Colors.AMBER_400
        elif nombre in clientes:
            texto_consola.value = f"El usuario {nombre} está dado de alta en el sistema."
            texto_consola.color = Colors.GREEN_400
        elif nombre in clientes_eliminados:
            texto_consola.value = f"AVISO: El usuario {nombre} se encuentra en la papelera."
            texto_consola.color = Colors.YELLOW_600
        else:
            texto_consola.value = f"ERROR: El usuario {nombre} no existe."
            texto_consola.color = Colors.RED_400
        page.update()

    def route_change(e):
        # Use the page route directly, que es lo que Flet actualiza cuando cambia la ruta.
        current_route = page.route

        if not current_route:
            page.go("/")
            return
        page.views.clear()
        
        # Home View
        if current_route == "/":
            page.views.append(
                ft.View(
                    route="/",
                    controls=[
                        ft.AppBar(title=ft.Text("Panel de Control", color=Colors.WHITE), bgcolor=Colors.ON_SURFACE_VARIANT),
                        ft.Column([
                            ft.Text("Registrar Nuevo Cliente", size=20, weight=ft.FontWeight.BOLD),
                            entrada_cliente, entrada_edad, entrada_sexo, entrada_meta,
                            ft.ElevatedButton("Guardar Cliente", on_click=agregar_cliente, bgcolor=Colors.GREEN_700, color="white", width=250),
                            ft.ElevatedButton("Buscar por nombre", on_click=buscar_cliente, bgcolor=Colors.ORANGE_700, color="white", width=250),
                            ft.ElevatedButton("Eliminar por nombre", on_click=eliminar_cliente, bgcolor=Colors.RED_700, color="white", width=250),
                            texto_consola,
                            ft.Divider(height=20),
                            ft.ElevatedButton("Ver Lista de Clientes", on_click=mostrar_clientes, bgcolor=Colors.BLUE_700, color="white", width=250),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15)
                    ],
                    scroll=ft.ScrollMode.ADAPTIVE,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            )
        elif current_route == "/clientes":
            lista_tarjetas = ft.Column(spacing=10, scroll="adaptive")
            if not clientes:
                lista_tarjetas.controls.append(ft.Text("No hay clientes activos"))
            else:
                for nombre_cliente in clientes.keys():
                    tarjeta_interactiva = ft.ListTile(
                        title=ft.Text(nombre_cliente.upper(), weight=ft.FontWeight.BOLD, color=Colors.WHITE),
                        subtitle=ft.Text("Ver ficha técnica y entrenamientos -->", color=Colors.WHITE70),
                        trailing=ft.Icon(ft.icons.Icons.ARROW_FORWARD, size=14, color=Colors.WHITE),
                        bgcolor=Colors.ON_SURFACE_VARIANT,
                        on_click=lambda e, name=nombre_cliente: page.go(f"/cliente/{name}")
                    )
                    lista_tarjetas.controls.append(tarjeta_interactiva)
            page.views.append(
                ft.View(
                    route="/clientes",
                    controls=[
                        ft.AppBar(title=ft.Text("Lista de Clientes"), bgcolor=Colors.ON_SURFACE_VARIANT, color="white"),
                        ft.Container(content=lista_tarjetas, padding=15),
                        ft.ElevatedButton("Volver a Inicio", on_click=lambda _: page.go("/"), bgcolor=Colors.GREY_800, color="white")
                    ],
                    scroll=ft.ScrollMode.ADAPTIVE
                )
            )
        elif current_route.startswith("/cliente/"):
            nombre_seleccionado = current_route[9:]
            datos_cliente = clientes.get(nombre_seleccionado, {})
            page.views.append(
                ft.View(
                    route=current_route,
                    controls=[
                        ft.AppBar(title=ft.Text(f"{nombre_seleccionado}"), bgcolor=Colors.ON_SURFACE_VARIANT),
                        ft.Container(
                            content=ft.Column([
                                ft.Text(nombre_seleccionado.upper(), size=24, weight=ft.FontWeight.BOLD, color=Colors.BLUE_400),
                                ft.Divider(),
                                ft.Text(f"Edad: {datos_cliente.get('edad')} años", size=16),
                                ft.Text(f"Sexo: {datos_cliente.get('sexo')}", size=16),
                                ft.Text(f"Objetivo: {datos_cliente.get('meta')}", size=16),
                                ft.Divider(height=30),
                                ft.Container(
                                    content=ft.Text("Próximas Rutinas (Conectar con SQL)", color=Colors.BLACK_87),
                                    bgcolor=Colors.BLACK26,
                                    padding=20,
                                    border_radius=10
                                ),
                                ft.ElevatedButton("Volver a la lista", on_click=lambda _: page.go("/clientes"), bgcolor=Colors.GREY_400, color="white")
                            ], spacing=15),
                            padding=20
                        ),
                        ft.ElevatedButton("Volver al Inicio", on_click=lambda _: page.go("/"), bgcolor=Colors.GREY_800, color="white")
                    ]
                )
            )
        page.update()
    
    def view_pop(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    
    # Inicializamos la navegación
    if not page.route:
        page.push_route("/")
    else:
        route_change(None)
ft.run(main)