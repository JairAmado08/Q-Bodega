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
        
        # ----------------------------
        # Navegación con Secciones
        # ----------------------------
        st.markdown("### 🧭 Navegación")
        
        # Usar expanders para organizar por sección
        with st.expander("📦 **Inventario**", expanded=False):
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
        
        with st.expander("📦 **Movimientos**", expanded=False):
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
        
        with st.expander("🎉 **Promociones**", expanded=True):
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
        
        # Mapear las opciones a las claves
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
        
        # ======================================
        # SELECCIÓN CORRECTA DE MENÚ
        # ======================================
        
        # Inicializar opción actual si no existe
        if "opcion_actual" not in st.session_state:
            st.session_state["opcion_actual"] = "🎁 Dashboard de Promociones"
        
        # Leer los radios
        op_inv = st.session_state.get("radio_inventario")
        op_mov = st.session_state.get("radio_movimientos")
        op_pro = st.session_state.get("radio_promociones")
        
        # Si alguno cambió, actualizar la opción actual
        if op_inv and op_inv != st.session_state["opcion_actual"]:
            st.session_state["opcion_actual"] = op_inv
        
        elif op_mov and op_mov != st.session_state["opcion_actual"]:
            st.session_state["opcion_actual"] = op_mov
        
        elif op_pro and op_pro != st.session_state["opcion_actual"]:
            st.session_state["opcion_actual"] = op_pro
        
        # Determinar clave final
        opcion_seleccionada = st.session_state["opcion_actual"]
        opcion_key = menu_options.get(opcion_seleccionada, "promociones_dashboard")
        
        return opcion_key

