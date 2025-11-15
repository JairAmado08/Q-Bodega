"""
Vista del Sidebar con separadores de sección
"""
import streamlit as st
from auth import logout_user
from ui_components import mostrar_user_info, mostrar_logo
from inventario_crud import obtener_estadisticas
from promociones_crud import obtener_estadisticas_promociones


def mostrar_sidebar(display_name):
    """
    Muestra el sidebar con información del usuario y navegación
    
    Args:
        display_name: Nombre del usuario para mostrar
    
    Returns:
        str: Clave de la opción seleccionada
    """
    with st.sidebar:
        # Información del usuario logueado
        mostrar_user_info(display_name)
        
        # Botón de cerrar sesión
        if st.button("🚪 Cerrar Sesión", use_container_width=True):
            logout_user()
        
        # Logo
        mostrar_logo()
        
        # Encabezado principal
        st.markdown("## 🛠️ Panel de Control")
        
        # ----------------------------
        # Métricas
        # ----------------------------
        total_productos, total_cantidad, valor_total, productos_bajo_stock = obtener_estadisticas()
        stats_promociones = obtener_estadisticas_promociones()
        
        st.markdown("### 📊 Estadísticas")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("📦 Productos", total_productos)
            st.metric("💰 Valor Total", f"S/{valor_total:,.2f}")
        with col2:
            st.metric("📈 Stock Total", total_cantidad)
            st.metric("⚠️ Bajo Stock", productos_bajo_stock, delta_color="inverse")
        
        # Métricas de promociones
        st.markdown("### 🎉 Promociones")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("🎁 Total", stats_promociones['total'])
        with col2:
            st.metric("🔥 Vigentes", stats_promociones['vigentes'])
        
        st.markdown("---")
        
        # ============================
        # Manejo de expanders dinámicos
        # ============================
        opcion_actual = st.session_state.get("opcion_key", None)

        exp_inventario = opcion_actual in [
            "dashboard", "buscar", "registrar", "actualizar", "eliminar", "reportes"
        ]
        exp_movimientos = opcion_actual in [
            "movimientos_dashboard", "buscar_movimiento", "registrar_movimiento",
            "actualizar_movimiento", "eliminar_movimiento"
        ]
        exp_promociones = opcion_actual in [
            "promociones_dashboard", "registrar_promocion", "buscar_promocion",
            "actualizar_promocion", "eliminar_promocion"
        ]
        
        # ============================
        # Navegación
        # ============================
        st.markdown("### 🧭 Navegación")
        
        # -------- Inventario --------
        with st.expander("📦 **Inventario**", expanded=exp_inventario):
            opcion_inventario = st.radio(
                "Opciones de Inventario",
                [
                    "📋 Dashboard de Inventario",
                    "🔎 Buscar Producto",
                    "➕ Registrar Producto",
                    "✏️ Actualizar Producto",
                    "🗑️ Eliminar Producto",
                    "📊 Reportes"
                ],
                key="radio_inventario",
                label_visibility="collapsed"
            )
        
        # -------- Movimientos --------
        with st.expander("📦 **Movimientos**", expanded=exp_movimientos):
            opcion_movimientos = st.radio(
                "Opciones de Movimientos",
                [
                    "📦 Dashboard de Movimientos",
                    "🔍 Buscar Movimiento",
                    "➕ Registrar Movimiento",
                    "✏️ Actualizar Movimiento",
                    "🗑️ Eliminar Movimiento"
                ],
                key="radio_movimientos",
                label_visibility="collapsed"
            )
        
        # -------- Promociones --------
        with st.expander("🎉 **Promociones**", expanded=exp_promociones):
            opcion_promociones = st.radio(
                "Opciones de Promociones",
                [
                    "🎁 Dashboard de Promociones",
                    "➕ Registrar Promoción",
                    "🔍 Buscar Promoción",
                    "✏️ Actualizar Promoción",
                    "🗑️ Eliminar Promoción"
                ],
                key="radio_promociones",
                label_visibility="collapsed"
            )
        
        # Mapeo de opciones → claves internas
        menu_options = {
            # Inventario
            "📋 Dashboard de Inventario": "dashboard",
            "🔎 Buscar Producto": "buscar",
            "➕ Registrar Producto": "registrar",
            "✏️ Actualizar Producto": "actualizar",
            "🗑️ Eliminar Producto": "eliminar",
            "📊 Reportes": "reportes",

            # Movimientos
            "📦 Dashboard de Movimientos": "movimientos_dashboard",
            "🔍 Buscar Movimiento": "buscar_movimiento",
            "➕ Registrar Movimiento": "registrar_movimiento",
            "✏️ Actualizar Movimiento": "actualizar_movimiento",
            "🗑️ Eliminar Movimiento": "eliminar_movimiento",

            # Promociones
            "🎁 Dashboard de Promociones": "promociones_dashboard",
            "➕ Registrar Promoción": "registrar_promocion",
            "🔍 Buscar Promoción": "buscar_promocion",
            "✏️ Actualizar Promoción": "actualizar_promocion",
            "🗑️ Eliminar Promoción": "eliminar_promocion"
        }

        # ============================
        # Determinar opción seleccionada
        ============================
        opcion_seleccionada = None

        if st.session_state.get("radio_inventario"):
            opcion_seleccionada = st.session_state.radio_inventario

        if st.session_state.get("radio_movimientos"):
            opcion_seleccionada = st.session_state.radio_movimientos

        if st.session_state.get("radio_promociones"):
            opcion_seleccionada = st.session_state.radio_promociones

        # Si ninguna seleccionada, default = dashboard inventario
        if opcion_seleccionada is None:
            opcion_seleccionada = "📋 Dashboard de Inventario"

        opcion_key = menu_options.get(opcion_seleccionada, "dashboard")

        # Guardar en session_state para expanders inteligentes
        st.session_state.opcion_key = opcion_key
        
        return opcion_key
