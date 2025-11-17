"""
Vista de Búsqueda de Ventas
"""
import streamlit as st
from datetime import datetime, timedelta
from ventas_crud import buscar_ventas
from data_manager import get_ventas

def mostrar():
    """Muestra la interfaz de búsqueda de ventas"""
    st.markdown("## 🔍 Buscar Venta")
    
    ventas = get_ventas()
    
    if ventas.empty:
        st.info("📭 No hay ventas registradas.")
        return
    
    st.markdown("### 🔎 Filtros de Búsqueda")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        id_busqueda = st.text_input("🆔 ID de Venta", placeholder="Ej: V001")
        
        metodo_busqueda = st.selectbox(
            "💳 Método de Pago",
            ["Todos", "efectivo", "tarjeta", "yape", "plin"]
        )
    
    with col2:
        usar_fechas = st.checkbox("📅 Filtrar por fechas", value=True)
        
        if usar_fechas:
            fecha_inicio = st.date_input(
                "Desde",
                value=datetime.now() - timedelta(days=30)
            )
    
    with col3:
        if usar_fechas:
            st.markdown("<br>", unsafe_allow_html=True)
            fecha_fin = st.date_input(
                "Hasta",
                value=datetime.now()
            )
    
    # Botón de búsqueda
    if st.button("🔍 Buscar", use_container_width=True, type="primary"):
        # Preparar filtros
        filtros = {}
        
        if id_busqueda:
            filtros["id"] = id_busqueda
        
        if metodo_busqueda != "Todos":
            filtros["metodo_pago"] = metodo_busqueda
        
        if usar_fechas:
            filtros["fecha_inicio"] = fecha_inicio.strftime("%Y-%m-%d")
            filtros["fecha_fin"] = (fecha_fin + timedelta(days=1)).strftime("%Y-%m-%d")
        
        # Buscar
        resultados = buscar_ventas(filtros)
        
        # Mostrar resultados
        st.markdown("---")
        st.markdown("### 📊 Resultados de Búsqueda")
        
        if not resultados.empty:
            st.success(f"✅ Se encontraron {len(resultados)} ventas.")
            
            # Cards de resultados
            for _, venta in resultados.iterrows():
                col1, col2, col3, col4, col5 = st.columns([2, 2, 1, 1, 1])
                
                with col1:
                    st.markdown(f"**🆔 {venta['ID']}**")
                with col2:
                    st.markdown(f"📅 {venta['Fecha']}")
                with col3:
                    st.markdown(f"💵 S/{venta['Total_Final']:.2f}")
                with col4:
                    st.markdown(f"💳 {venta['Metodo_Pago']}")
                with col5:
                    if st.button("👁️ Ver", key=f"ver_{venta['ID']}"):
                        st.session_state.venta_detalle_id = venta['ID']
                        st.session_state.menu_principal = "detalle_venta"
                        st.rerun()
            
            # Vista detallada
            st.markdown("### 📋 Vista Detallada")
            st.dataframe(
                resultados,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Total_Bruto": st.column_config.NumberColumn("Subtotal", format="S/%.2f"),
                    "Total_Descuento": st.column_config.NumberColumn("Descuento", format="S/%.2f"),
                    "Total_Final": st.column_config.NumberColumn("Total", format="S/%.2f"),
                }
            )
            
            # Resumen
            st.markdown("### 📊 Resumen")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total de Ventas", len(resultados))
            with col2:
                st.metric("Ingresos Totales", f"S/{resultados['Total_Final'].sum():,.2f}")
            with col3:
                st.metric("Descuentos Aplicados", f"S/{resultados['Total_Descuento'].sum():,.2f}")
        
        else:
            st.warning("⚠️ No se encontraron ventas con los criterios especificados.")
    
    # Tips
    st.markdown("---")
    st.markdown("### 💡 Tips de Búsqueda")
    st.info("""
    - **Sin filtros:** Muestra todas las ventas
    - **Por ID:** Busca una venta específica
    - **Por método de pago:** Filtra por forma de pago
    - **Por fechas:** Encuentra ventas en un rango específico
    - **Combinar filtros:** Usa múltiples criterios para búsquedas precisas
    """)
