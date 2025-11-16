"""
Vista de Inicio/Bienvenida
"""
import streamlit as st
from datetime import datetime
from config import SOFTSOLUTIONS_LOGO_URL, APP_INFO
from inventario_crud import obtener_estadisticas
from movimientos_crud import obtener_estadisticas_movimientos
from promociones_crud import obtener_estadisticas_promociones
from auth import get_display_name, get_current_user

def mostrar():
    """Muestra la página de inicio con el logo de SoftSolutions"""
    
    # Obtener información del usuario
    display_name = get_display_name(get_current_user())
    hora_actual = datetime.now().strftime("%H:%M")
    fecha_actual = datetime.now().strftime("%A, %d de %B de %Y")
    
    # Determinar saludo según la hora
    hora = datetime.now().hour
    if hora < 12:
        saludo = "Buenos días"
        emoji = "🌅"
    elif hora < 18:
        saludo = "Buenas tardes"
        emoji = "☀️"
    else:
        saludo = "Buenas noches"
        emoji = "🌙"
    
    # Logo de SoftSolutions y bienvenida
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Logo centrado (más pequeño)
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem 0;">
            <img src="{SOFTSOLUTIONS_LOGO_URL}" 
                 style="max-width: 250px; width: 100%; height: auto; margin-bottom: 1.5rem;"
                 alt="SoftSolutions Logo">
        </div>
        """, unsafe_allow_html=True)
        
        # Mensaje de bienvenida
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    border-radius: 15px; color: white; margin-bottom: 2rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h1>{emoji} {saludo}, {display_name}</h1>
            <p style="font-size: 1.2rem; margin: 0;">Bienvenido al Sistema de Gestión de Inventario</p>
            <p style="font-size: 0.9rem; opacity: 0.9; margin-top: 0.5rem;">{fecha_actual} | {hora_actual}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # ----------------------------
    # Dashboard de Resumen
    # ----------------------------
    st.markdown("## 📊 Resumen General del Sistema")
    
    # Obtener estadísticas
    total_prod, total_cant, valor_total, bajo_stock = obtener_estadisticas()
    total_mov, entradas, salidas, ajustes = obtener_estadisticas_movimientos()
    stats_promo = obtener_estadisticas_promociones()
    
    # Fila 1: Inventario
    st.markdown("### 📦 Inventario")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stats-container" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
            <h3>📦</h3>
            <h2>{total_prod}</h2>
            <p>Productos Únicos</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stats-container" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
            <h3>📈</h3>
            <h2>{total_cant}</h2>
            <p>Unidades Totales</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stats-container" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
            <h3>💰</h3>
            <h2>S/{valor_total:,.0f}</h2>
            <p>Valor Total</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        color_alerta = "#dc3545" if bajo_stock > 0 else "#28a745"
        st.markdown(f"""
        <div class="stats-container" style="background: linear-gradient(135deg, {color_alerta} 0%, {'#c82333' if bajo_stock > 0 else '#20c997'} 100%);">
            <h3>⚠️</h3>
            <h2>{bajo_stock}</h2>
            <p>{"Alertas Stock Bajo" if bajo_stock > 0 else "Stock Óptimo"}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Fila 2: Movimientos y Promociones
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📦 Movimientos de Inventario")
        
        subcol1, subcol2 = st.columns(2)
        with subcol1:
            st.metric("📊 Total Movimientos", total_mov)
            st.metric("⬆️ Entradas", entradas)
        with subcol2:
            st.metric("⬇️ Salidas", salidas)
            st.metric("🔄 Ajustes", ajustes)
    
    with col2:
        st.markdown("### 🎉 Promociones Activas")
        
        subcol1, subcol2 = st.columns(2)
        with subcol1:
            st.metric("🎁 Total Promociones", stats_promo['total'])
            st.metric("✅ Activas", stats_promo['activas'])
        with subcol2:
            st.metric("🔥 Vigentes Hoy", stats_promo['vigentes'])
            st.metric("❌ Inactivas", stats_promo['inactivas'])
    
    st.markdown("---")
    
    # ----------------------------
    # Accesos Rápidos
    # ----------------------------
    st.markdown("## 🚀 Accesos Rápidos")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📋 Ver Inventario", use_container_width=True, type="primary"):
            st.session_state.menu_principal = "dashboard"
            st.rerun()
    
    with col2:
        if st.button("➕ Registrar Producto", use_container_width=True):
            st.session_state.menu_principal = "registrar"
            st.rerun()
    
    with col3:
        if st.button("📦 Registrar Movimiento", use_container_width=True):
            st.session_state.menu_principal = "registrar_movimiento"
            st.rerun()
    
    with col4:
        if st.button("🎁 Ver Promociones", use_container_width=True):
            st.session_state.menu_principal = "promociones_dashboard"
            st.rerun()
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # ----------------------------
    # Footer con información del sistema
    # ----------------------------
    st.markdown(f"""
    <div style="text-align: center; color: #666; padding: 2rem; border-top: 1px solid #e0e0e0; margin-top: 2rem;">
        <p style="font-size: 1.1rem; margin-bottom: 0.5rem;">
            <strong>📦 {APP_INFO['name']}</strong> | {APP_INFO['subtitle']}
        </p>
        <p style="font-size: 0.9rem; color: #888;">
            Versión {APP_INFO['version']} | Desarrollado por {APP_INFO['developer']}
        </p>
        <p style="font-size: 0.85rem; color: #aaa; margin-top: 1rem;">
            © 2025 SoftSolutions. Todos los derechos reservados.
        </p>
    </div>
    """, unsafe_allow_html=True)
