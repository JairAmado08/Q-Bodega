"""
Módulo de componentes de interfaz de usuario reutilizables
"""
import streamlit as st
from config import LOGO_URL, EMPLEADOS_AUTORIZADOS

def mostrar_header(titulo, subtitulo, usuario):
    """
    Muestra el header principal de la aplicación
    
    Args:
        titulo: Título principal
        subtitulo: Subtítulo
        usuario: Nombre del usuario actual
    """
    st.markdown(f"""
    <div class="main-header">
        <h1>{titulo}</h1>
        <h3>{subtitulo}</h3>
        <p>¡Bienvenido/a, <strong>{usuario}</strong>! | Prototipo CRUD de gestión | Versión 3.5</p>
    </div>
    """, unsafe_allow_html=True)

def mostrar_login_container():
    """Muestra el contenedor de login"""
    st.markdown("""
    <div class="login-container">
        <h1>🏪 Q'Bodega</h1>
        <h3>Sistema de Inventario</h3>
        <p>Ingrese sus credenciales de empleado</p>
    </div>
    """, unsafe_allow_html=True)

def mostrar_user_info(usuario):
    """
    Muestra la información del usuario en el sidebar
    
    Args:
        usuario: Nombre del usuario para mostrar
    """
    st.markdown(f"""
    <div class="user-info">
        <h4>👤 Usuario Activo</h4>
        <p><strong>{usuario}</strong></p>
        <p><small>Empleado de Bodega XYZ</small></p>
    </div>
    """, unsafe_allow_html=True)

def mostrar_logo():
    """Muestra el logo de la empresa en el sidebar"""
    st.markdown(
        f"""
        <div class="sidebar-logo">
            <img src="{LOGO_URL}">
        </div>
        """,
        unsafe_allow_html=True
    )

def mostrar_usuarios_prueba():
    """Muestra el expander con usuarios de prueba"""
    with st.expander("👥 Usuarios de Prueba"):
        st.markdown("**Empleados autorizados:**")
        for username, password in EMPLEADOS_AUTORIZADOS.items():
            st.markdown(f"- `{username}` / `{password}`")

def mostrar_alerta_stock_bajo(producto):
    """
    Muestra una alerta de stock bajo para un producto
    
    Args:
        producto: Serie de pandas con información del producto
    """
    st.markdown(
        f"""
        <div style="
            background-color: #ff4d4d;
            color: white;
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 8px;
            font-weight: bold;">
            🚨 <strong>{producto['Nombre']}</strong> (ID: {producto['ID']}) 
            tiene solo <strong>{int(producto['Cantidad'])}</strong> unidades en stock.
        </div>
        """,
        unsafe_allow_html=True
    )

def mostrar_producto_card(producto):
    """
    Muestra una tarjeta con información del producto
    
    Args:
        producto: Serie de pandas con información del producto
    """
    cantidad = producto['Cantidad']
    
    # Determinar el estado del stock
    if cantidad < 5:
        card_class = "product-card low-stock"
        stock_icon = "🔴"
        stock_text = "Stock Bajo"
    elif cantidad <= 15:
        card_class = "product-card medium-stock" 
        stock_icon = "🟡"
        stock_text = "Stock Medio"
    else:
        card_class = "product-card good-stock"
        stock_icon = "🟢"
        stock_text = "Stock Bueno"
    
    precio_total = cantidad * producto['Precio']
    
    st.markdown(f"""
    <div class="{card_class}">
        <div style="display: flex; justify-content: between; align-items: center;">
            <div style="flex: 1;">
                <h4>🏷️ {producto['Nombre']} (ID: {producto['ID']})</h4>
                <p><strong>Categoría:</strong> {producto['Categoría']}</p>
                <p><strong>Cantidad:</strong> {cantidad} unidades {stock_icon} <em>{stock_text}</em></p>
                <p><strong>Precio unitario:</strong> S/{producto['Precio']:.2f}</p>
                <p><strong>Valor total:</strong> S/{precio_total:.2f}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def mostrar_movimiento_card(movimiento):
    """
    Muestra una tarjeta con información del movimiento
    
    Args:
        movimiento: Serie de pandas con información del movimiento
    """
    # Determinar estilo según tipo de movimiento
    if movimiento['Tipo'] == 'Entrada':
        card_style = "border-left: 4px solid #28a745; background: #f8fff8;"
        icon = "⬆️"
    elif movimiento['Tipo'] == 'Salida':
        card_style = "border-left: 4px solid #dc3545; background: #fff5f5;"
        icon = "⬇️"
    elif movimiento['Tipo'] == 'Devolución':
        card_style = "border-left: 4px solid #17a2b8; background: #f0f8ff;"
        icon = "🔄"
    else:  # Ajuste
        card_style = "border-left: 4px solid #ffc107; background: #fffbf0;"
        icon = "⚖️"
    
    cantidad_text = f"+{movimiento['Cantidad']}" if movimiento['Cantidad'] > 0 else str(movimiento['Cantidad'])
    observaciones = movimiento['Observaciones'] if movimiento['Observaciones'] else 'Sin observaciones'
    
    st.markdown(f"""
    <div class="product-card" style="{card_style}">
        <h4>{icon} {movimiento['Tipo']} - ID: {movimiento['ID_Movimiento']}</h4>
        <p><strong>Producto:</strong> {movimiento['Producto_Nombre']} ({movimiento['Producto_ID']})</p>
        <p><strong>Cantidad:</strong> {cantidad_text} unidades</p>
        <p><strong>Fecha:</strong> {movimiento['Fecha']}</p>
        <p><strong>Usuario:</strong> {movimiento['Usuario']}</p>
        <p><strong>Observaciones:</strong> {observaciones}</p>
    </div>
    """, unsafe_allow_html=True)

def mostrar_stats_container(titulo, valor, icono):
    """
    Muestra un contenedor de estadística
    
    Args:
        titulo: Título de la estadística
        valor: Valor a mostrar
        icono: Emoji o icono
    """
    st.markdown(f"""
    <div class="stats-container">
        <h3>{icono}</h3>
        <h2>{valor}</h2>
        <p>{titulo}</p>
    </div>
    """, unsafe_allow_html=True)

def mostrar_footer():
    """Muestra el footer de la aplicación"""
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>📦 <strong>Sistema de Inventario Q'Bodega</strong> | Desarrollado por Soft Solutions</p>
        <p><small>Versión 3.5 - Sin Dependencias Externas</small></p>
    </div>
    """, unsafe_allow_html=True)
