"""
Vista del Sidebar con separadores de sección
"""
import streamlit as st
from auth import logout_user
from ui_components import mostrar_user_info, mostrar_logo
from inventario_crud import obtener_estadisticas
from promociones_crud import obtener_estadisticas_promociones

def mostrar_sidebar(display_name):

    with st.sidebar:
        # Usuario
        mostrar_user_info(display_name)

        # Cerrar sesión
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
            st.metric("⚠️ Bajo Stock", bajo_stock, delta_color="inverse")

        st.markdown("### 🎉 Promociones")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("🎁 Total", stats_promo["total"])
        with col2:
            st.metric("🔥 Vigentes", stats_promo["vigentes"])

        st.markdown("---")
        st.markdown("### 🧭 Navegación")

        # ===========================
        # SISTEMA ESTABLE DE NAVEGACIÓN
        # ===========================

        # Si no existe, inicializar menú
        if "menu_principal" not in st.session_state:
            st.session_state.menu_principal = "promociones_dashboard"

        # --- Inventario ---
        with st.expander("📦 Inventario", expanded=False):
            if st.button("📋 Dashboard de Inventario"):
                st.session_state.menu_principal = "dashboard"
            if st.button("🔎 Buscar Producto"):
                st.session_state.menu_principal = "buscar"
            if st.button("➕ Registrar Producto"):
                st.session_state.menu_principal = "registrar"
            if st.button("✏️ Actualizar Producto"):
                st.session_state.menu_principal = "actualizar"
            if st.button("🗑️ Eliminar Producto"):
                st.session_state.menu_principal = "eliminar"
            if st.button("📊 Reportes"):
                st.session_state.menu_principal = "reportes"

        # --- Movimientos ---
        with st.expander("📦 Movimientos", expanded=False):
            if st.button("📦 Dashboard de Movimientos"):
                st.session_state.menu_principal = "movimientos_dashboard"
            if st.button("🔍 Buscar Movimiento"):
                st.session_state.menu_principal = "buscar_movimiento"
            if st.button("➕ Registrar Movimiento"):
                st.session_state.menu_principal = "registrar_movimiento"
            if st.button("✏️ Actualizar Movimiento"):
                st.session_state.menu_principal = "actualizar_movimiento"
            if st.button("🗑️ Eliminar Movimiento"):
                st.session_state.menu_principal = "eliminar_movimiento"

        # --- Promociones ---
        with st.expander("🎉 Promociones", expanded=True):
            if st.button("🎁 Dashboard de Promociones"):
                st.session_state.menu_principal = "promociones_dashboard"
            if st.button("➕ Registrar Promoción"):
                st.session_state.menu_principal = "registrar_promocion"
            if st.button("🔍 Buscar Promoción"):
                st.session_state.menu_principal = "buscar_promocion"
            if st.button("✏️ Actualizar Promoción"):
                st.session_state.menu_principal = "actualizar_promocion"
            if st.button("🗑️ Eliminar Promoción"):
                st.session_state.menu_principal = "eliminar_promocion"

        # Retornar la opción final seleccionada
        return st.session_state.menu_principal
