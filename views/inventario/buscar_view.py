"""
Vista de Búsqueda de Productos
"""
import streamlit as st
from data_manager import get_inventario

def mostrar():
    """Muestra la interfaz de búsqueda de productos"""
    st.markdown("## 🔎 Buscar Producto en Inventario")
    
    inventario = get_inventario()
    busqueda = st.text_input("Ingrese nombre, ID o categoría del producto:")

    if busqueda:
        resultados = inventario[
            inventario["Nombre"].str.contains(busqueda, case=False, na=False) |
            inventario["ID"].astype(str).str.contains(busqueda, case=False, na=False) |
            inventario["Categoría"].str.contains(busqueda, case=False, na=False)
        ]
        
        if not resultados.empty:
            st.success(f"✅ Se encontraron {len(resultados)} productos que coinciden con '{busqueda}'.")
            
            st.dataframe(
                resultados,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Cantidad": st.column_config.NumberColumn("Cantidad", format="%d unidades"),
                    "Precio": st.column_config.NumberColumn("Precio", format="S/%.2f")
                }
            )
        else:
            st.error(f"⚠️ No se encontraron productos que coincidan con '{busqueda}'.")
    else:
        st.info("✍️ Escriba el nombre, ID o categoría para buscar un producto.")
