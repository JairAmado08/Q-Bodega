"""
Vista de Registro de Productos
"""
import streamlit as st
from inventario_crud import registrar_producto, producto_existe
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
                    categoria = st.selectbox("📂 Categoría", options=CATEGORIAS, index=5)
                
                with col_form2:
                    cantidad = st.number_input("📦 Cantidad", min_value=0, step=1, value=1)
                    precio = st.number_input("💰 Precio unitario", min_value=0.0, step=0.01, format="%.2f")
                
                submit = st.form_submit_button("✅ Registrar Producto", use_container_width=True)
        
        with col2:
            st.markdown("### 💡 Consejos")
            st.info("""
            **Tips para Registrar productos:**
            - Usa IDs únicos y descriptivos
            - Categoriza correctamente para mejor organización
            - Revisa el stock mínimo recomendado
            - Verifica el precio antes de guardar
            """)
    
    if submit:
        if id_ and nombre:
            if producto_existe(id_):
                st.markdown('<div class="warning-message">⚠️ Ya existe un producto con este ID.</div>', 
                          unsafe_allow_html=True)
            else:
                registrar_producto(id_, nombre, categoria, cantidad, precio)
                st.markdown('<div class="success-message">✅ Producto agregado correctamente.</div>', 
                          unsafe_allow_html=True)
                st.balloons()
        else:
            st.markdown('<div class="error-message">❌ Debes completar al menos ID y Nombre.</div>', 
                       unsafe_allow_html=True)
