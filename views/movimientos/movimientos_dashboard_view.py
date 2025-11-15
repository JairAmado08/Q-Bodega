"""
Vista del Dashboard de Movimientos
"""
import streamlit as st
from data_manager import get_movimientos
from movimientos_crud import obtener_estadisticas_movimientos
from ui_components import mostrar_movimiento_card

def mostrar():
    """Muestra el dashboard de movimientos"""
    st.markdown("## 📦 Dashboard de Movimientos")
    
    movimientos = get_movimientos()
    
    # Estadísticas de movimientos
    total_movimientos, entradas, salidas, ajustes = obtener_estadisticas_movimientos()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📊 Total Movimientos", total_movimientos)
    with col2:
        st.metric("⬆️ Entradas", entradas)
    with col3:
        st.metric("⬇️ Salidas", salidas)
    with col4:
        st.metric("🔄 Ajustes/Devoluciones", ajustes)
    
    if not movimientos.empty:
        # Filtros
        col1, col2, col3 = st.columns(3)
        with col1:
            tipos = ['Todos'] + sorted(movimientos['Tipo'].unique().tolist())
            tipo_filtro = st.selectbox("🏷️ Filtrar por tipo:", tipos)
        
        with col2:
            productos_mov = ['Todos'] + sorted(movimientos['Producto_ID'].unique().tolist())
            producto_filtro = st.selectbox("📦 Filtrar por producto:", productos_mov)
        
        with col3:
            usuarios = ['Todos'] + sorted(movimientos['Usuario'].unique().tolist())
            usuario_filtro = st.selectbox("👤 Filtrar por usuario:", usuarios)
        
        # Aplicar filtros
        df_filtrado = movimientos.copy()
        if tipo_filtro != 'Todos':
            df_filtrado = df_filtrado[df_filtrado['Tipo'] == tipo_filtro]
        if producto_filtro != 'Todos':
            df_filtrado = df_filtrado[df_filtrado['Producto_ID'] == producto_filtro]
        if usuario_filtro != 'Todos':
            df_filtrado = df_filtrado[df_filtrado['Usuario'] == usuario_filtro]
        
        # Mostrar movimientos
        st.markdown("### 📋 Historial de Movimientos")
        
        # Ordenar por fecha descendente
        df_filtrado = df_filtrado.sort_values('Fecha', ascending=False)
        
        for _, movimiento in df_filtrado.iterrows():
            mostrar_movimiento_card(movimiento)
        
        # Vista detallada
        st.markdown("### 📋 Vista Detallada")
        st.dataframe(
            df_filtrado,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Cantidad": st.column_config.NumberColumn("Cantidad", format="%d"),
                "Fecha": st.column_config.DateColumn("Fecha")
            }
        )
    else:
        st.info("📭 No hay movimientos registrados.")
