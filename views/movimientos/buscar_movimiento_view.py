"""
Vista de Búsqueda de Movimientos
"""
import streamlit as st
from data_manager import get_movimientos

def mostrar():
    """Muestra la interfaz de búsqueda de movimientos"""
    st.markdown("## 🔍 Buscar Movimiento")
    
    movimientos = get_movimientos()
    col1, col2 = st.columns([2, 1])
    
    with col1:
        busqueda = st.text_input("🔎 Ingrese ID de movimiento, tipo, producto o fecha:")
        
        if busqueda:
            resultados = movimientos[
                movimientos["ID_Movimiento"].str.contains(busqueda, case=False, na=False) |
                movimientos["Tipo"].str.contains(busqueda, case=False, na=False) |
                movimientos["Producto_ID"].str.contains(busqueda, case=False, na=False) |
                movimientos["Producto_Nombre"].str.contains(busqueda, case=False, na=False) |
                movimientos["Fecha"].str.contains(busqueda, case=False, na=False) |
                movimientos["Usuario"].str.contains(busqueda, case=False, na=False)
            ]
            
            if not resultados.empty:
                st.success(f"✅ Se encontraron {len(resultados)} movimientos que coinciden con '{busqueda}'.")
                
                st.dataframe(
                    resultados.sort_values('Fecha', ascending=False),
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Cantidad": st.column_config.NumberColumn("Cantidad", format="%d"),
                        "Fecha": st.column_config.DateColumn("Fecha")
                    }
                )
            else:
                st.error(f"⚠️ No se encontraron movimientos que coincidan con '{busqueda}'.")
        else:
            st.info("✍️ Escriba el ID, tipo, producto, fecha o usuario para buscar un movimiento de inventario.")
    
    with col2:
        st.markdown("### 💡 Tips de Búsqueda")
        st.info("""
        Puedes buscar por:
        - **ID:** M001, M002...
        - **Tipo:** Entrada, Salida, Ajuste, Devolución
        - **Producto:** P001, Inca Kola...
        - **Fecha:** 2024-01-15
        - **Usuario:** admin, carlos...
        """)
