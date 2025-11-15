"""
Q'Bodega - Sistema de Gestión de Inventario
Aplicación principal
"""
from styles import get_custom_css

# Aplicar estilos
st.markdown(get_custom_css(), unsafe_allow_html=True)

import streamlit as st

# Importar módulos
from config import APP_CONFIG
from styles import get_custom_css
from auth import (
    inicializar_sesion, is_logged_in, get_display_name, 
    logout_user, get_current_user
)
from data_manager import inicializar_inventario, inicializar_movimientos
from ui_components import mostrar_header, mostrar_user_info, mostrar_logo, mostrar_footer

# Importar vistas
from views import login_view, sidebar_view, content_view

# ----------------------------
# Configuración de la App
# ----------------------------
st.set_page_config(**APP_CONFIG)

# Aplicar CSS personalizado
st.markdown(get_custom_css(), unsafe_allow_html=True)

# ----------------------------
# Inicialización
# ----------------------------
inicializar_sesion()
inicializar_inventario()
inicializar_movimientos()

# ----------------------------
# Sistema de Autenticación
# ----------------------------
if not is_logged_in():
    login_view.mostrar_login()
    st.stop()

# ----------------------------
# Sistema Principal
# ----------------------------

# Header principal
display_name = get_display_name(get_current_user())
mostrar_header(
    "📦 Sistema de Gestión de Inventario",
    "Q'Bodega: Control total, sin complicaciones.",
    display_name
)

# Sidebar
opcion_key = sidebar_view.mostrar_sidebar(display_name)

# Contenido principal según opción seleccionada
content_view.mostrar_contenido(opcion_key)

# Footer
mostrar_footer()
