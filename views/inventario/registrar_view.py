"""
Vista de Registro de Productos
"""
import streamlit as st
from inventario_crud import registrar_producto
from config import CATEGORIAS
from utils import generar_id_producto

def mostrar():
    """Muestra el formulario de registro de productos"""
    st.markdown("## ➕ Registrar Nuevo Producto")
    
    # Generar ID automáticamente
    id_producto_auto = generar_id_producto()
    
    with st.container():
        col1, col2 = st.columns([2, 1])
        
        with col1:
            with st.form("form_Registrar", clear_on_submit=True):
                st.markdown("### 📝 Información del Producto")
                
                # Mostrar ID que se asignará
                st.info(f"🆔 **ID automático asignado:** `{id_producto_auto}`")
                
                col_form1, col_form2 = st.columns(2)
                with col_form1:
                    nombre = st.text_input("🏷️ Nombre del producto", placeholder="Ej: Inca Kola 1.5L")
                    categoria = st.selectbox("📂 Categoría", options=CATEGORIAS, index=0)
                
                with col_form2:
                    cantidad = st.number_input("📦 Cantidad", min_value=0, step=1, value=1)
                    precio = st.number_input("💰 Precio unitario", min_value=0.0, step=0.01, format="%.2f", value=0.0)
                
                submit = st.form_submit_button("✅ Registrar Producto", use_container_width=True)
        
        with col2:
            st.markdown("### 💡 Consejos")
            st.info("""
            **Tips para Registrar productos:**
            - El ID se genera automáticamente
            - Categoriza correctamente para mejor organización
            - Revisa el stock mínimo recomendado
            - Verifica el precio antes de guardar
            """)
    
    if submit:
        if nombre:
            # Usar el ID generado automáticamente
            registrar_producto(id_producto_auto, nombre, categoria, cantidad, precio)
            st.markdown(
                '<div class="success-message">✅ Producto agregado correctamente con ID: <strong>' + id_producto_auto + '</strong></div>', 
                unsafe_allow_html=True
            )
            st.balloons()
            st.rerun()
        else:
            st.markdown(
                '<div class="error-message">❌ Debes completar el nombre del producto.</div>', 
                unsafe_allow_html=True
            )
