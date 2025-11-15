"""
Vista del Dashboard de Inventario
"""
import streamlit as st
from data_manager import get_inventario
from ui_components import mostrar_alerta_stock_bajo, mostrar_producto_card
from config import STOCK_BAJO

def mostrar():
    """Muestra el dashboard principal de inventario"""
    st.markdown("## 📋 Dashboard de Inventario")
    
    inventario = get_inventario()
    
    if not inventario.empty:
        # ----------------------------
        # Alertas de Stock Bajo
        # ----------------------------
        bajo_stock = inventario[inventario["Cantidad"] < STOCK_BAJO]
        if not bajo_stock.empty:
            st.markdown("### 🔔 Alertas de Stock Bajo")
            for _, row in bajo_stock.iterrows():
                mostrar_alerta_stock_bajo(row)
        else:
            st.markdown(
                '<div style="background-color: #4CAF50; color: white; padding: 10px; '
                'border-radius: 8px; font-weight: bold;">✅ No hay alertas de stock bajo.</div>',
                unsafe_allow_html=True
            )
        
        # ----------------------------
        # Filtros
        # ----------------------------
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            categorias = ['Todas'] + sorted(inventario['Categoría'].unique().tolist())
            categoria_filtro = st.selectbox("🏷️ Filtrar por categoría:", categorias)
        
        with col2:
            stock_filtro = st.selectbox(
                "📊 Filtrar por stock:", 
                ['Todos', 'Stock bajo (<5)', 'Stock medio (5-15)', 'Stock alto (>15)']
            )
        
        with col3:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔄 Actualizar", use_container_width=True):
                st.rerun()
        
        # ----------------------------
        # Aplicar filtros
        # ----------------------------
        df_filtrado = inventario.copy()
        
        if categoria_filtro != 'Todas':
            df_filtrado = df_filtrado[df_filtrado['Categoría'] == categoria_filtro]
        
        if stock_filtro == 'Stock bajo (<5)':
            df_filtrado = df_filtrado[df_filtrado['Cantidad'] < 5]
        elif stock_filtro == 'Stock medio (5-15)':
            df_filtrado = df_filtrado[
                (df_filtrado['Cantidad'] >= 5) & (df_filtrado['Cantidad'] <= 15)
            ]
        elif stock_filtro == 'Stock alto (>15)':
            df_filtrado = df_filtrado[df_filtrado['Cantidad'] > 15]
        
        # ----------------------------
        # Mostrar productos como cards
        # ----------------------------
        st.markdown("### 🏪 Productos en Inventario")
        
        for idx, producto in df_filtrado.iterrows():
            mostrar_producto_card(producto)
        
        # ----------------------------
        # Tabla detallada
        # ----------------------------
        st.markdown("### 📋 Vista Detallada")
        st.dataframe(
            df_filtrado,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Cantidad": st.column_config.NumberColumn(
                    "Cantidad",
                    help="Cantidad en stock",
                    format="%d unidades"
                ),
                "Precio": st.column_config.NumberColumn(
                    "Precio",
                    help="Precio por unidad",
                    format="S/%.2f"
                )
            }
        )
        
    else:
        st.info("📭 No hay productos en el inventario. ¡Comienza agregando algunos!")
