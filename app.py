"""
Q'Bodega - Sistema de Gestión de Inventario
Aplicación principal
"""
import streamlit as st

# Verificar que los módulos existan
try:
    from config import APP_CONFIG
    from styles import get_custom_css
    from auth import (
        inicializar_sesion, is_logged_in, get_display_name, 
        logout_user, get_current_user
    )
    from data_manager import (
        inicializar_inventario, inicializar_movimientos, inicializar_promociones, inicializar_ventas
    )
    from ui_components import mostrar_header, mostrar_user_info, mostrar_logo, mostrar_footer
except ImportError as e:
    st.error(f"❌ Error al importar módulos: {e}")
    st.info("""
    Asegúrate de tener todos los archivos necesarios:
    - config.py
    - styles.py
    - auth.py
    - data_manager.py
    - ui_components.py
    - inventario_crud.py
    - movimientos_crud.py
    - promociones_crud.py
    """)
    st.stop()

# Importar vistas
try:
    from views import login_view, sidebar_view, content_view
except ImportError as e:
    st.error(f"❌ Error al importar vistas: {e}")
    st.info("Asegúrate de tener el directorio 'views' con todos sus archivos")
    st.stop()

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
inicializar_promociones()

# Inicializar menú principal si no existe
if "menu_principal" not in st.session_state:
    st.session_state.menu_principal = "inicio"

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
