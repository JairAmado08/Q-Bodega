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
        # Info usuario
        mostrar_user_info(display_name)

        # Botón cerrar sesión
        if st.button("🚪 Cerrar Sesión", use_container_width=True):
            logout_user()

        mostrar_logo()

        st.markdown("## 🛠️ Panel de Control")

        # MÉTRICAS
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

        # MÉTRICAS PROMOCIONES
        st.markdown("### 🎉 Promociones")
        col1, col2 = st.columns(2)

        with col1:
            st.metric("🎁 Total", stats_promo["total"])
        with col2:
            st.metric("🔥 Vigentes", stats_promo["vigentes"])

        st.markdown("---")
        st.markdown("### 🧭 Navegación")

        # 🚨 MENÚ ÚNICO (la clave de toda la solución)
        opcion = st.radio(
            "",
            [
                "📋 Dashboard de Inventario",
                "🔎 Buscar Producto",
                "➕ Registrar Producto",
                "✏️ Actualizar Producto",
                "🗑️ Eliminar Producto",
                "📊 Reportes",

                "📦 Dashboard de Movimientos",
                "🔍 Buscar Movimiento",
                "➕ Registrar Movimiento",
                "✏️ Actualizar Movimiento",
                "🗑️ Eliminar Movimiento",

                "🎁 Dashboard de Promociones",
                "➕ Registrar Promoción",
                "🔍 Buscar Promoción",
                "✏️ Actualizar Promoción",
                "🗑️ Eliminar Promoción",
            ],
            key="menu_principal"
        )

        # Mapeo
        menu_map = {
            "📋 Dashboard de Inventario": "dashboard",
            "🔎 Buscar Producto": "buscar",
            "➕ Registrar Producto": "registrar",
            "✏️ Actualizar Producto": "actualizar",
            "🗑️ Eliminar Producto": "eliminar",
            "📊 Reportes": "reportes",

            "📦 Dashboard de Movimientos": "movimientos_dashboard",
            "🔍 Buscar Movimiento": "buscar_movimiento",
            "➕ Registrar Movimiento": "registrar_movimiento",
            "✏️ Actualizar Movimiento": "actualizar_movimiento",
            "🗑️ Eliminar Movimiento": "eliminar_movimiento",

            "🎁 Dashboard de Promociones": "promociones_dashboard",
            "➕ Registrar Promoción": "registrar_promocion",
            "🔍 Buscar Promoción": "buscar_promocion",
            "✏️ Actualizar Promoción": "actualizar_promocion",
            "🗑️ Eliminar Promoción": "eliminar_promocion",
        }

        return menu_map[opcion]
