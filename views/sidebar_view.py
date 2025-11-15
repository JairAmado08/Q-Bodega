"""
Vista del Sidebar
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
        # Navegación
        # ----------------------------
        st.markdown("### 🧭 Navegación")
        
        # Crear el diccionario de opciones completo
        menu_options = {}
        
        # INVENTARIO
        menu_options.update({
            "📋 Dashboard de Inventario": "dashboard",
            "🔎 Buscar Producto": "buscar",
            "➕ Registrar Producto": "registrar",
            "✏️ Actualizar Producto": "actualizar", 
            "🗑️ Eliminar Producto": "eliminar",
            "📊 Reportes": "reportes",
        })
        
        # MOVIMIENTOS
        menu_options.update({
            "📦 Dashboard de Movimientos": "movimientos_dashboard",
            "🔍 Buscar Movimiento": "buscar_movimiento",
            "➕ Registrar Movimiento": "registrar_movimiento",
            "✏️ Actualizar Movimiento": "actualizar_movimiento",
            "🗑️ Eliminar Movimiento": "eliminar_movimiento"
        })
        
        # PROMOCIONES
        menu_options.update({
            "🎁 Dashboard de Promociones": "promociones_dashboard",
            "➕ Registrar Promoción": "registrar_promocion",
            "🔍 Buscar Promoción": "buscar_promocion",
            "✏️ Actualizar Promoción": "actualizar_promocion",
            "🗑️ Eliminar Promoción": "eliminar_promocion"
        })
        
        # Radio button sin separadores visuales
        opcion = st.radio("", list(menu_options.keys()), key="menu_radio")
        opcion_key = menu_options[opcion]
        
        return opcion_key
