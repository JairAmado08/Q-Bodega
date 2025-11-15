"""
Vista del Sidebar con separadores de sección
"""
import streamlit as st
from auth import logout_user
from ui_components import mostrar_user_info, mostrar_logo
from inventario_crud import obtener_estadisticas
from promociones_crud import obtener_estadisticas_promociones

# --- CLASE DE BOTÓN CON HIGHLIGHT ---
def nav_button(label, key_value):
    """Crea un botón de navegación con highlight automático"""
    
    is_active = st.session_state.menu_principal == key_value

    estilo = """
        background-color:#4CAF50; color:white; font-weight:bold;
        border-radius:8px; padding:8px; width:100%;
    """ if is_active else """
        width:100%; padding:8px; border-radius:8px;
    """

    if st.button(label, use_container_width=True, key=label, help=key_value, 
                 type="secondary" if not is_active else "primary"):
        st.session_state.menu_principal = key_value


def mostrar_sidebar(display_name):

    with st.sidebar:

        mostrar_user_info(display_name)

        # Logout
        if st.button("🚪 Cerrar Sesión", use_container_width=True):
            logout_user()

        mostrar_logo()

        st.markdown("## 🛠️ Panel de Control")

        # --- Métricas ---
        total_prod, total_cant, valor_total, bajo_stock = obtener_estadisticas()
        stats_promo = obtener_estadisticas_promociones()

        st.markdown("### 📊 Estadísticas")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("📦 Productos", total_prod)
            st.metric("💰 Valor Total", f"S/{valor_total:,.2f}")
        with col2:
            st.metric("📈 Stock Total", total_cant)
            st.metric("⚠️ Bajo Stock", bajo_stock)

        st.markdown("### 🎉 Promociones")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("🎁 Total", stats_promo["total"])
        with col2:
            st.metric("🔥 Vigentes", stats_promo["vigentes"])

        st.markdown("---")
        st.markdown("### 🧭 Navegación")

        # Init state
        if "menu_principal" not in st.session_state:
            st.session_state.menu_principal = "promociones_dashboard"

        # ===========================
        # INVENTARIO
        # ===========================
        with st.expander("📦 Inventario", expanded=False):
            colA, colB = st.columns(2)
            with colA:
                nav_button("📋 Dashboard", "dashboard")
                nav_button("➕ Registrar", "registrar")
                nav_button("✏️ Actualizar", "actualizar")
            with colB:
                nav_button("🔎 Buscar", "buscar")
                nav_button("🗑️ Eliminar", "eliminar")
                nav_button("📊 Reportes", "reportes")

        # ===========================
        # MOVIMIENTOS
        # ===========================
        with st.expander("🔄 Movimientos", expanded=False):
            colA, colB = st.columns(2)
            with colA:
                nav_button("📦 Dashboard", "movimientos_dashboard")
                nav_button("➕ Registrar", "registrar_movimiento")
                nav_button("✏️ Editar", "actualizar_movimiento")
            with colB:
                nav_button("🔍 Buscar", "buscar_movimiento")
                nav_button("🗑️ Eliminar", "eliminar_movimiento")

        # ===========================
        # PROMOCIONES
        # ===========================
        with st.expander("🎉 Promociones", expanded=True):
            colA, colB = st.columns(2)
            with colA:
                nav_button("🎁 Dashboard", "promociones_dashboard")
                nav_button("➕ Registrar", "registrar_promocion")
                nav_button("✏️ Editar", "actualizar_promocion")
            with colB:
                nav_button("🔍 Buscar", "buscar_promocion")
                nav_button("🗑️ Eliminar", "eliminar_promocion")

        return st.session_state.menu_principal
