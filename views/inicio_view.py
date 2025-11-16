"""
Vista de Inicio/Bienvenida
"""
import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo
from config import SOFTSOLUTIONS_LOGO_URL, APP_INFO
from inventario_crud import obtener_estadisticas
from movimientos_crud import obtener_estadisticas_movimientos
from promociones_crud import obtener_estadisticas_promociones
from auth import get_display_name, get_current_user

def mostrar():
    """Muestra la página de inicio con el logo de SoftSolutions"""
    
    # Obtener información del usuario
    display_name = get_display_name(get_current_user())
    
    # Hora de Perú (UTC-5)
    try:
        zona_peru = ZoneInfo("America/Lima")
    except:
        # Fallback si ZoneInfo no está disponible
        from datetime import timezone, timedelta
        zona_peru = timezone(timedelta(hours=-5))
    
    ahora_peru = datetime.now(zona_peru)
    hora_actual = ahora_peru.strftime("%H:%M")
    
    # Nombres de meses en español
    meses_esp = {
        1: "enero", 2: "febrero", 3: "marzo", 4: "abril",
        5: "mayo", 6: "junio", 7: "julio", 8: "agosto",
        9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
    }
    
    # Nombres de días en español
    dias_esp = {
        0: "lunes", 1: "martes", 2: "miércoles", 3: "jueves",
        4: "viernes", 5: "sábado", 6: "domingo"
    }
    
    dia_nombre = dias_esp[ahora_peru.weekday()].capitalize()
    mes_nombre = meses_esp[ahora_peru.month]
    fecha_actual = f"{dia_nombre}, {ahora_peru.day} de {mes_nombre} de {ahora_peru.year}"
    
    # Determinar saludo según la hora (hora de Perú)
    hora = ahora_peru.hour
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
