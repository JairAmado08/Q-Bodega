"""
Vista de Eliminación de Productos
"""
import streamlit as st
from data_manager import get_inventario
from inventario_crud import eliminar_producto

def mostrar():
    """Muestra la interfaz de eliminación de productos"""
    st.markdown("## 🗑️ Eliminar Producto")
    
    inventario = get_inventario()
    ids = inventario["ID"].tolist()
    
    if ids:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            id_sel = st.selectbox("🔍 Selecciona un producto por ID", ids)
            producto = inventario[inventario["ID"] == id_sel].iloc[0]
            
            # Mostrar información del producto a eliminar
            st.markdown(f"### ⚠️ Producto a Eliminar")
            
            st.markdown(f"""
            <div class="product-card" style="border-left: 4px solid #dc3545; background: #fff5f5;">
                <h4>🏷️ {producto['Nombre']} (ID: {producto['ID']})</h4>
                <p><strong>Categoría:</strong> {producto['Categoría']}</p>
                <p><strong>Cantidad:</strong> {int(producto['Cantidad'])} unidades</p>
                <p><strong>Precio:</strong> S/{float(producto['Precio']):.2f}</p>
                <p><strong>Valor Total:</strong> S/{float(producto['Precio']) * int(producto['Cantidad']):.2f}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Confirmación con checkbox
            confirmacion = st.checkbox(f"✅ Confirmo que deseo eliminar el producto **{producto['Nombre']}**")
            
            if confirmacion:
                if st.button("🗑️ ELIMINAR PRODUCTO", type="primary", use_container_width=True):
                    eliminar_producto(id_sel)
                    st.markdown('<div class="success-message">✅ Producto eliminado correctamente.</div>', 
                               unsafe_allow_html=True)
                    st.rerun()
        
        with col2:
            st.markdown("### ⚠️ Advertencia")
            st.warning("""
            **¡Atención!**
            
            Esta acción eliminará permanentemente el producto del inventario.
            
            **No se puede deshacer.**
            
            Asegúrate de que realmente quieres eliminar este producto.
            """)
            
    else:
        st.info("📭 No hay productos en el inventario para eliminar.")
