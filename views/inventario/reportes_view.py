"""
Vista de Reportes y Análisis
"""
import streamlit as st
import pandas as pd
from data_manager import get_inventario

def mostrar():
    """Muestra reportes y análisis del inventario"""
    st.markdown("## 📊 Reportes y Análisis")
    
    inventario = get_inventario()
    
    if not inventario.empty:
        # Resumen general
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_productos = len(inventario)
            st.markdown(f"""
            <div class="stats-container">
                <h3>📦</h3>
                <h2>{total_productos}</h2>
                <p>Productos Únicos</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            total_unidades = int(inventario['Cantidad'].sum())
            st.markdown(f"""
            <div class="stats-container">
                <h3>📈</h3>
                <h2>{total_unidades}</h2>
                <p>Unidades Totales</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            valor_total = (inventario['Cantidad'] * inventario['Precio']).sum()
            st.markdown(f"""
            <div class="stats-container">
                <h3>💰</h3>
                <h2>S/{valor_total:,.0f}</h2>
                <p>Valor Inventario</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            total_categorias = inventario['Categoría'].nunique()
            st.markdown(f"""
            <div class="stats-container">
                <h3>🏷️</h3>
                <h2>{total_categorias}</h2>
                <p>Categorías</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Distribución por categorías
        st.markdown("### 📊 Distribución por Categorías")
        categoria_counts = inventario['Categoría'].value_counts()
        max_count = categoria_counts.max()
        
        for categoria, count in categoria_counts.items():
            porcentaje = (count / len(inventario)) * 100
            width_percent = (count / max_count) * 100
            
            st.markdown(f"""
            <div class="category-bar">
                <div class="category-fill" style="width: {width_percent}%;">
                    {categoria}: {count} productos ({porcentaje:.1f}%)
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Top productos por valor
        st.markdown("### 💎 Top Productos por Valor")
        inventario_valor = inventario.copy()
        inventario_valor["Cantidad"] = pd.to_numeric(inventario_valor["Cantidad"], errors="coerce")
        inventario_valor["Precio"] = pd.to_numeric(inventario_valor["Precio"], errors="coerce")
        inventario_valor["Valor_Total"] = inventario_valor["Cantidad"] * inventario_valor["Precio"]
        
        top_productos = inventario_valor.nlargest(5, "Valor_Total")
        
        st.dataframe(
            top_productos[['Nombre', 'Categoría', 'Cantidad', 'Precio', 'Valor_Total']],
            use_container_width=True,
            hide_index=True,
            column_config={
                "Precio": st.column_config.NumberColumn("Precio", format="S/%.2f"),
                "Valor_Total": st.column_config.NumberColumn("Valor Total", format="S/%.2f")
            }
        )
        
        # Productos con stock bajo
        st.markdown("### ⚠️ Productos con Stock Bajo")
        productos_bajo_stock = inventario[inventario['Cantidad'] < 5]
        
        if not productos_bajo_stock.empty:
            st.dataframe(
                productos_bajo_stock,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Cantidad": st.column_config.NumberColumn(
                        "Cantidad",
                        help="⚠️ Stock bajo - requiere reabastecimiento",
                        format="%d unidades"
                    ),
                    "Precio": st.column_config.NumberColumn("Precio", format="S/%.2f")
                }
            )
        else:
            st.success("🎉 ¡Todos los productos tienen stock adecuado!")
        
        # Análisis por categoría
        st.markdown("### 📈 Análisis por Categoría")
        analisis_categoria = inventario.groupby('Categoría').agg({
            'Cantidad': 'sum',
            'Precio': 'mean'
        }).round(2)
        analisis_categoria['Valor_Categoria'] = inventario.groupby('Categoría').apply(
            lambda x: (x['Cantidad'] * x['Precio']).sum()
        ).round(2)
        
        st.dataframe(
            analisis_categoria,
            use_container_width=True,
            column_config={
                "Cantidad": st.column_config.NumberColumn("Total Unidades", format="%d"),
                "Precio": st.column_config.NumberColumn("Precio Promedio", format="S/%.2f"),
                "Valor_Categoria": st.column_config.NumberColumn("Valor Categoría", format="S/%.2f")
            }
        )
        
    else:
        st.info("📭 No hay datos suficientes para generar reportes.")
