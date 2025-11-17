"""
Vista del Dashboard de Ventas
"""
import streamlit as st
from data_manager import get_ventas
from ventas_crud import obtener_estadisticas_ventas

def mostrar():
    """Muestra el dashboard de ventas con estadísticas"""
    st.markdown("## 💰 Dashboard de Ventas")
    
    # Obtener estadísticas
    stats = obtener_estadisticas_ventas()
    
    # Fila de estadísticas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stats-container" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
            <h3>📊</h3>
            <h2>{stats['total_ventas']}</h2>
            <p>Ventas Totales</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stats-container" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
            <h3>📅</h3>
            <h2>{stats['ventas_hoy']}</h2>
            <p>Ventas Hoy</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stats-container" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
            <h3>📆</h3>
            <h2>{stats['ventas_mes']}</h2>
            <p>Ventas del Mes</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stats-container" style="background: linear-gradient(135deg, #28a745 0%, #20c997 100%);">
            <h3>💵</h3>
            <h2>S/{stats['ingresos_totales']:,.0f}</h2>
            <p>Ingresos Totales</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Ingresos detallados
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 💰 Ingresos del Día")
        st.metric("Total Hoy", f"S/{stats['ingresos_hoy']:,.2f}", 
                 delta=f"{stats['ventas_hoy']} ventas")
    
    with col2:
        st.markdown("### 📊 Ingresos del Mes")
        st.metric("Total del Mes", f"S/{stats['ingresos_mes']:,.2f}",
                 delta=f"{stats['ventas_mes']} ventas")
    
    st.markdown("---")
    
    # Botón para nueva venta
    if st.button("➕ Registrar Nueva Venta", use_container_width=True, type="primary"):
        st.session_state.menu_principal = "registrar_venta"
        st.rerun()
    
    st.markdown("---")
    
    # Últimas ventas
    ventas = get_ventas()
    
    if not ventas.empty:
        st.markdown("### 📋 Últimas Ventas")
        
        # Ordenar por fecha descendente
        ventas_ordenadas = ventas.sort_values('Fecha', ascending=False).head(10)
        
        for _, venta in ventas_ordenadas.iterrows():
            col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
            
            with col1:
                st.markdown(f"**🆔 {venta['ID']}**")
            with col2:
                st.markdown(f"📅 {venta['Fecha']}")
            with col3:
                st.markdown(f"💵 S/{venta['Total_Final']:.2f}")
            with col4:
                if st.button("👁️", key=f"ver_{venta['ID']}", help="Ver detalles"):
                    st.session_state.venta_detalle_id = venta['ID']
                    st.session_state.menu_principal = "detalle_venta"
                    st.rerun()
        
        # Tabla completa
        st.markdown("### 📊 Vista Detallada")
        st.dataframe(
            ventas_ordenadas[['ID', 'Fecha', 'Total_Final', 'Metodo_Pago']],
            use_container_width=True,
            hide_index=True,
            column_config={
                "Total_Final": st.column_config.NumberColumn("Total", format="S/%.2f"),
                "Metodo_Pago": st.column_config.TextColumn("Método de Pago")
            }
        )
    else:
        st.info("📭 No hay ventas registradas. ¡Registra la primera venta!")
