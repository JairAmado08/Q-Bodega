"""
Vista de Eliminación de Movimientos
"""
import streamlit as st
from data_manager import get_movimientos
from movimientos_crud import eliminar_movimiento

def mostrar():
    """Muestra la interfaz de eliminación de movimientos"""
    st.markdown("## 🗑️ Eliminar Movimiento")
    
    movimientos = get_movimientos()
    ids_movimientos = movimientos["ID_Movimiento"].tolist()
    
    if ids_movimientos:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            id_mov_sel = st.selectbox("🔍 Selecciona un movimiento por ID", ids_movimientos)
            movimiento = movimientos[movimientos["ID_Movimiento"] == id_mov_sel].iloc[0]
            
            st.markdown("### ⚠️ Movimiento a Eliminar")
            
            st.markdown(f"""
            <div class="product-card" style="border-left: 4px solid #dc3545; background: #fff5f5;">
                <h4>🏷️ {movimiento['ID_Movimiento']} - {movimiento['Tipo']}</h4>
                <p><strong>Producto:</strong> {movimiento['Producto_Nombre']} ({movimiento['Producto_ID']})</p>
                <p><strong>Cantidad:</strong> {movimiento['Cantidad']} unidades</p>
                <p><strong>Fecha:</strong> {movimiento['Fecha']}</p>
                <p><strong>Usuario:</strong> {movimiento['Usuario']}</p>
                <p><strong>Observaciones:</strong> {movimiento['Observaciones'] if movimiento['Observaciones'] else 'Sin observaciones'}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            confirmacion = st.checkbox(f"✅ Confirmo que deseo eliminar el movimiento **{movimiento['ID_Movimiento']}**")
            
            if confirmacion:
                if st.button("🗑️ ELIMINAR MOVIMIENTO", type="primary", use_container_width=True):
                    eliminar_movimiento(id_mov_sel)
                    st.success("✅ Movimiento eliminado correctamente.")
                    st.rerun()
        
        with col2:
            st.markdown("### ⚠️ Advertencia")
            st.warning("""
            **¡Atención!**
            
            Esta acción eliminará permanentemente el movimiento del historial.
            
            **El stock del producto NO se revertirá automáticamente.**
            
            Si necesitas revertir el stock, hazlo manualmente mediante un ajuste.
            """)
    else:
        st.info("📭 No hay movimientos registrados para eliminar.")
