"""
Vista de Actualización de Productos
"""
import streamlit as st
from data_manager import get_inventario
from inventario_crud import actualizar_producto
from config import CATEGORIAS

def mostrar():
    """Muestra el formulario de actualización de productos"""
    st.markdown("## ✏️ Actualizar Producto")
    
    inventario = get_inventario()
    ids = inventario["ID"].tolist()
    
    if ids:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            id_sel = st.selectbox("🔍 Selecciona un producto por ID", ids)
            producto = inventario[inventario["ID"] == id_sel].iloc[0]
            
            # Mostrar información actual
            st.markdown(f"### 📋 Producto Actual: **{producto['Nombre']}**")
            
            with st.form("form_actualizar"):
                st.markdown("#### 📝 Nuevos Datos")
                
                col_form1, col_form2 = st.columns(2)
                with col_form1:
                    nombre = st.text_input("🏷️ Nombre", value=producto["Nombre"])
                    
                    # Determinar índice de la categoría actual
                    if producto["Categoría"] in CATEGORIAS:
                        categoria_idx = CATEGORIAS.index(producto["Categoría"])
                    else:
                        categoria_idx = 0
                    
                    categoria = st.selectbox("📂 Categoría", options=CATEGORIAS, index=categoria_idx)
                
                with col_form2:
                    cantidad = st.number_input("📦 Cantidad", min_value=0, value=int(producto["Cantidad"]), step=1)
                    precio = st.number_input("💰 Precio", min_value=0.0, value=float(producto["Precio"]), step=0.01, format="%.2f")
                
                submit = st.form_submit_button("🔄 Actualizar Producto", use_container_width=True)
        
        with col2:
            st.markdown("### 📊 Información Actual")
            st.metric("📦 Cantidad Actual", int(producto["Cantidad"]))
            st.metric("💰 Precio Actual", f"S/{float(producto['Precio']):.2f}")
            st.metric("💎 Valor Total", f"S/{float(producto['Precio']) * int(producto['Cantidad']):.2f}")
        
        if submit:
            actualizar_producto(id_sel, nombre, categoria, cantidad, precio)
            st.markdown('<div class="success-message">✅ Producto actualizado correctamente.</div>', 
                       unsafe_allow_html=True)
            st.rerun()
    else:
        st.info("📭 No hay productos en el inventario para actualizar.")
