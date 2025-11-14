"""
Archivo de configuración para Q'Bodega
Contiene constantes y configuraciones globales
"""

# Configuración de la aplicación
APP_CONFIG = {
    "page_title": "Q'Bodega - Inventario",
    "page_icon": "📦",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Información de la aplicación
APP_INFO = {
    "name": "Q'Bodega",
    "subtitle": "Control total, sin complicaciones.",
    "version": "2.5",
    "developer": "Soft Solutions"
}

# Usuarios autorizados (en producción esto estaría en una base de datos)
EMPLEADOS_AUTORIZADOS = {
    "admin": "123456",
    "carlos.rodriguez": "empleado123",
    "maria.gonzalez": "empleado456",
    "jose.martinez": "empleado789",
    "ana.lopez": "empleado321",
    "luis.torres": "empleado654"
}

# Nombres para mostrar de usuarios
NOMBRES_DISPLAY = {
    "admin": "Administrador",
    "carlos.rodriguez": "Carlos Rodríguez",
    "maria.gonzalez": "María González", 
    "jose.martinez": "José Martínez",
    "ana.lopez": "Ana López",
    "luis.torres": "Luis Torres"
}

# Categorías de productos
CATEGORIAS = [
    "Abarrotes secos",
    "Bebidas",
    "Lácteos y derivados",
    "Snacks y golosinas",
    "Panadería y repostería",
    "Cárnicos y embutidos",
    "Frutas y verduras",
    "Productos de limpieza e higiene personal",
    "Enlatados y conservas",
    "Aceites y salsas"
]

# Tipos de movimientos
TIPOS_MOVIMIENTO = ["Entrada", "Salida", "Ajuste", "Devolución"]

# Umbrales de stock
STOCK_BAJO = 5
STOCK_MEDIO = 15

# Logo de la empresa
LOGO_URL = "https://raw.githubusercontent.com/JairAmado08/Q-Bodega/main/images/Q'Bodega.png"
