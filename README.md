¡Buenas! Bienvenidos a **GymFlow DB**. Este es un proyecto que estoy desarrollando para crear un "Sistema Operativo" (PT OS) enfocado en entrenadores personales (yo también soy uno 😜) y profesionales del fitness para gestionar clientes, objetivos y entrenamientos de forma eficiente. 

El proyecto está programado en **Python** usando **Flet** para la interfaz gráfica (que se ve en web y móvil) y **SQLite** para guardar toda la información.

Hace poco migré todo el sistema: antes funcionaba con archivos JSON locales, pero ahora usa una base de datos relacional de verdad (SQLite), lo que hace que todo sea mucho más rápido, limpio y profesional.

---

## 🚀 ¿Qué hace la app ahora mismo?
* **Añadir Clientes:** Un formulario donde guardamos el nombre, edad, peso, sexo y el objetivo principal del atleta.
* **Base de Datos Local:** Toda la info se guarda automáticamente en un archivo llamado `gymflow.db` dentro de la carpeta. No necesitas contraseñas ni servidores.
* **Fichas de Detalle:** Si pinchas en cualquier cliente de la lista, la app te lleva a una pantalla exclusiva con todos sus datos en tiempo real.
* **Papelera de Reciclaje (Borrado Lógico):** Cuando le das a "Eliminar Cliente", el usuario no se borra de la base de datos de forma destructiva. Solo se marca como inactivo (`activo = 0`), así no perdemos su historial ni descuadramos datos en el futuro.

PD: Cualquier ayuda o consulta siempre son bienvenidas. Un saludo!! 👋
