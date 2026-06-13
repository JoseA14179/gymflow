import flet as ft
import sqlite3
from flet import Colors
from flet import Icon

#CONFIGURACIÓN Y GESTIÓN DE SQLITE
def conectar_db():
    conexion = sqlite3.connect("gymflow.db")
    conexion.row_factory = sqlite3.Row
    return conexion

def inicializar_db():
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            edad INTEGER,
            peso REAL,
            sexo TEXT,
            objetivo_patologias TEXT,
            activo BOOLEAN DEFAULT 1
        );
    """)
    conexion.commit()
    cursor.close()
    conexion.close()

#FUNCIÓN PARA LA BARRA DE NAVEGACIÓN
def crear_barra_nav(page, indice_activo):
    return ft.NavigationRail(
        selected_index=indice_activo,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=400,
        extended=False,
        destinations=[
            ft.NavigationRailDestination(icon=ft.Icons.HOME, label="Inicio"),
            ft.NavigationRailDestination(icon=ft.Icons.PEOPLE, label="Clientes")
        ],
        on_change=lambda e: al_cambiar_pestaña(e, page)
    )

#FUNCIÓN PARA GESTIONAR ACCIONES DE LA BARRA DE NAVEGACIÓN
def al_cambiar_pestaña(e, page):
    if e.control.selected_index == 0:
        page.go("/")
    elif e.control.selected_index == 1:
        page.go("/clientes")

#INTERFAZ DE FLET
async def main(page: ft.Page):
#INICIALIZAMOS DB
    inicializar_db()

#AJUSTE DE VENTANA
    page.title= "PT OS - Python - Flet"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
#INPUTS PARA DATOS NECESARIOS
    entrada_nombre = ft.TextField(label="Nombre", capitalization=ft.TextCapitalization.WORDS, width=250)
    entrada_edad = ft.TextField(label="Edad", keyboard_type=ft.KeyboardType.NUMBER, width=250)
    entrada_peso = ft.TextField(label="Peso", keyboard_type=ft.KeyboardType.NUMBER, width=250)
    entrada_sexo = ft.TextField(label="Sexo (M/F)", capitalization=ft.TextCapitalization.CHARACTERS, width=250)
    entrada_meta = ft.Dropdown(label="Objetivo", width=250, options=[
        ft.dropdown.Option("Perder peso", "Perder peso"),
        ft.dropdown.Option("Ganar masa muscular", "Ganar masa muscular"),
        ft.dropdown.Option("Aumento de la fuerza", "Aumento de la fuerza"),
        ft.dropdown.Option("Mejorar rendimiento deportivo", "Mejorar rendimiento deportivo")
    ]
    )
#DEFINICIÓN DE LAS DISTINTAS FUNCIONES QUE SE PUEDEN REALIZAR

#FUNCIÓN PARA IR A LA PÁGINA DONDE SE ENCUENTRAN TODOS LOS CLIENTES
    async def mostrar_clientes(e):
        await page.push_route("/clientes")

#FUNCIÓN PARA ELIMINAR CLIENTES(ARCHIVADO)
    async def eliminar_cliente(e):
        nombre = entrada_nombre.value.strip().title()
        if nombre:
            try:
                conexion = conectar_db()
                cursor = conexion.cursor()
                cursor.execute("SELECT id, activo FROM Usuarios WHERE nombre = ?;", (nombre,))
                resultado = cursor.fetchone()
                if resultado:
                    usuario_id = resultado["id"]
                    activo = resultado["activo"]
                    if activo == 0:
                        page.dialog = ft.AlertDialog(content=ft.Text(f"El cliente {nombre} ya se encuentra en la papelera"))
                    else:
                        cursor.execute("UPDATE Usuarios SET activo = FALSE WHERE id = ?;", (usuario_id,))
                        conexion.commit()
                        entrada_nombre.value = ""
                        page.dialog = ft.AlertDialog(content=ft.Text(f"El cliente {nombre} se ha movido a la papelera"))
                else:
                    page.dialog = ft.AlertDialog(content=ft.Text(f"El cliente {nombre} no existe"))
            except sqlite3.Error as err:
                page.dialog = ft.AlertDialog(content=ft.Text(f"Error: {err}"))
            finally:
                if 'conexion' in locals():
                    cursor.close()
                    conexion.close()
        else:
            page.dialog = ft.AlertDialog(content=ft.Text(f"Por favor, escriba el nombre del usuario que quiera eliminar"))
        page.dialog.open = True
        page.update()

#FUNCIÓN PARA AGREGAR CLIENTES
    async def agregar_cliente(e):
        nombre = entrada_nombre.value.strip().title()
        edad = entrada_edad.value.strip()
        peso = entrada_peso.value.strip()
        sexo = entrada_sexo.value.strip().upper()
        meta = entrada_meta.value 
        #DEBE RELLENAR TODOS LOS CAMPOS
        if nombre and edad and peso and sexo and meta:
            try:
                conexion = conectar_db()
                cursor = conexion.cursor()
                consulta = """
                        INSERT INTO Usuarios (nombre, edad, peso, sexo, objetivo_patologias)
                        VALUES (?, ?, ?, ?, ?)
                    """
                valores = (nombre, int(edad), float(peso), sexo, meta)
                cursor.execute(consulta, valores)
                conexion.commit()

                entrada_nombre.value = ""
                entrada_edad.value = ""
                entrada_peso.value = ""
                entrada_sexo.value = ""
                entrada_meta.value = ""
                page.dialog = ft.AlertDialog(content=ft.Text(f"Cliente {nombre} guardado en la base de datos con éxito."))
            except sqlite3.Error as err:
                page.dialog = ft.AlertDialog(content=ft.Text(f"Error de conexión con la base de datos"))
            finally:
                if 'conexion' in locals():
                    cursor.close()
                    conexion.close()
        else:
            page.dialog = ft.AlertDialog(content=ft.Text(f"Necesita rellenar todos los campos para crear un nuevo usuario"))
        page.dialog.open = True
        page.update()

#FUNCIÓN PARA CAMBIAR DE PÁGINA
    async def change_route(e):
            page.views.clear()
            if page.route == "/":
                page.views.append(vista_inicial(page))
            elif page.route == "/clientes":
                page.views.append(vista_clientes(page))
            elif page.route.startswith("/cliente"):
                cliente_id = page.route[9:]
                page.views.append(vista_detalle_cliente(page, cliente_id))
            page.update()

#VISTA PRINCIPAL     
    def vista_inicial(page):
            sidebar = crear_barra_nav(page, 0)
            return ft.View(route="/", controls=[
                ft.Row([
                    ft.Text("Página principal", size=35, weight=ft.FontWeight.BOLD)
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([
                    sidebar,
                    ft.VerticalDivider(width=1, color=Colors.GREY_300)
                ], 
                expand=True,
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.STRETCH
                ),
                ft.Column([
                    entrada_nombre,
                    entrada_edad,
                    entrada_peso,
                    entrada_sexo,
                    entrada_meta,
                    ft.Button("Añadir Cliente", on_click=agregar_cliente, bgcolor=Colors.GREEN_300 , color="white"),
                    #ft.Button("Eliminar Cliente", on_click=eliminar_cliente, bgcolor=Colors.RED_300, color="white")
                ], 
                spacing=15,
                horizontal_alignment=ft.MainAxisAlignment.CENTER)
            ])

#VISTA DE LISTADO DE CLIENTES       
    def vista_clientes(page):
        sidebar = crear_barra_nav(page, 1)
        lista_contenedores_clientes = []
        try:
            conexion = conectar_db()
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM Usuarios ORDER BY nombre ASC;")
            usuarios = cursor.fetchall()

            for usuario in usuarios:
                uid, unombre = usuario["id"], usuario["nombre"]
                uedad = usuario["edad"]
                usexo = usuario["sexo"]
                upeso = usuario["peso"]
                umeta = usuario["objetivo_patologias"]
                lista_contenedores_clientes.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(ft.Icons.PERSON_OUTLINE, color=ft.Colors.GREY_700, size=25),
                            ft.Text(f"{unombre} | {uid}", size=16, weight=ft.FontWeight.BOLD),
                            ft.Text(f"{uedad} años | {usexo} | {upeso} kg | {umeta}")
                        ]),
                        bgcolor=Colors.BLUE_200, 
                        border_radius=12, 
                        padding=16, 
                        ink=True,
                        #REDIRIGIR SEGÚN ID DEL CLIENTE
                        on_click=lambda e, id_atleta=uid: page.go(f"/cliente/{id_atleta}")
                    )
                )
        except sqlite3.Error as err:
            lista_contenedores_clientes.append(ft.Text(f"Error al cargar usuarios: {err}", color="red"))
        finally:
            if 'conexion' in locals():
                cursor.close()
                conexion.close()

        return ft.View(route="/clientes", controls=[
            ft.Row([ft.Text("Clientes en el Sistema: ", size=25, weight=ft.FontWeight.BOLD)], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([
                    sidebar,
                    ft.VerticalDivider(width=1, color=Colors.GREY_300)
                ], 
                expand=True,
                vertical_alignment=ft.CrossAxisAlignment.STRETCH
            ),
            ft.Column([ 
                *lista_contenedores_clientes,
                ft.Divider(color=Colors.GREY_800)
            ], horizontal_alignment=ft.MainAxisAlignment.CENTER)
        ],
    )
    
    #CREACIÓN DE TABLAS PARA LOS ENTRENAMIENTOS DE LOS CLIENTES
    def crear_tabla(nombre_cliente):
        columnas = [
            ft.DataColumn(ft.Text("Ejercicio")),
            ft.DataColumn(ft.Text("Series")),
            ft.DataColumn(ft.Text("Repeticiones")),
            ft.DataColumn(ft.Text("Peso(kg)"))
        ]

        filas = [
            ft.DataRow(cells=[
                ft.DataCell(ft.Text("Banca")),
                ft.DataCell(ft.Text("4")),
                ft.DataCell(ft.Text("8")),
                ft.DataCell(ft.Text("75"))
            ]),
            ft.DataRow(cells=[
                ft.DataCell(ft.Text("Dominadas")),
                ft.DataCell(ft.Text("3")),
                ft.DataCell(ft.Text("2")),
                ft.DataCell(ft.Text("40"))
            ])
        ]

        tabla = ft.DataTable(columns=columnas, rows=filas)

        return ft.Column([ft.Text("Tu Rutina", size=24, weight="bold"),
        tabla
        ], scroll=ft.ScrollMode.AUTO)

#VISTA TÉCINICA DE CADA CLIENTE Y SUS DATOS       
    def vista_detalle_cliente(page, id_cliente):
        try:
            conexion = conectar_db()
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM Usuarios WHERE id = ?;", (id_cliente,))
            datos = cursor.fetchone()
        except sqlite3.Error:
            datos = None
        finally:
            if 'conexion' in locals():
                cursor.close()
                conexion.close()
        if datos:
            return ft.View(route=f"/cliente/{id_cliente}", controls=[
                ft.AppBar(title=f"Ficha de {datos['nombre']}", bgcolor=Colors.BLACK_87, color="white"),
                ft.Divider(color=Colors.GREY_800),
                ft.Column([
                    ft.Text(f"Edad: {datos['edad']} años", size=18),
                    ft.Text(f"Peso corporal actual: {datos['peso']} kg", size=18),
                    ft.Text(f"Sexo: {datos['sexo']}", size=18),
                    ft.Text(f"Objetivo principal: {datos['objetivo_patologias']}", size=18)
                ], spacing=12),
                ft.Divider(color=Colors.GREY_800),
                crear_tabla(datos['nombre']),
                ft.Divider(color=Colors.GREY_800),
                ft.Button("Volver atrás", on_click=lambda e: page.go("/clientes"), bgcolor=Colors.ORANGE_300, color="white")
            ])
        else:
            return ft.View(route=f"/cliente/{id_cliente}", controls=[ft.Text("Cliente no encontrado.")])

#DEFINIR NAVEGACIÓN CON FLET
    page.on_route_change = change_route
    page.views.append(vista_inicial(page))
    page.update()
    await page.push_route(page.route)

#INICIALIZAR APP EN MODO WEB LOCAL
ft.run(main, view=ft.AppView.WEB_BROWSER)