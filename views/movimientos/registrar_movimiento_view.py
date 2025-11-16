"""
Vista de Registro de Movimientos
"""
import streamlit as st
from data_manager import get_inventario
from movimientos_crud import registrar_movimiento
from utils import generar_id_movimiento

def mostrar():
    """Muestra el formulario de registro de movimientos"""
    st.markdown("## ➕ Registrar Nuevo Movimiento")
    
    inventario = get_inventario()
    
    if inventario.empty:
        st.error("❌ No hay productos disponibles. Primero registra algunos productos.")
        st.stop()
    
    # Generar ID automáticamente
    id_movimiento_auto = generar_id_movimiento()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📝 Información del Movimiento")
        
        # Mostrar ID que se asignará
        st.info(f"🆔 **ID automático asignado:** `{id_movimiento_auto}`")

        col_form1, col_form2 = st.columns(2)
        
        with col_form1:
            tipo_movimiento = st.selectbox(
                "🏷️ Tipo de movimiento", 
                options=["Entrada", "Salida", "Ajuste", "Devolución"]
            )
            
            # Productos disponibles
            productos_disponibles = inventario["ID"].tolist()
            producto_seleccionado = st.selectbox("📦 Producto", productos_disponibles)

        with col_form2:
            if tipo_movimiento == "Ajuste":
                cantidad = st.number_input(
                    "📊 Cantidad (+ para agregar, - para quitar)", 
                    step=1, format="%d", help="Usa números negativos para ajustes de disminución",
                    value=0
                )
            else:
                cantidad = st.number_input("📊 Cantidad", min_value=1, step=1, value=1)

            observaciones = st.text_area("📝 Observaciones", placeholder="Comentarios adicionales...")

        # Mostrar stock actual fuera del form
        stock_actual = inventario[inventario["ID"] == producto_seleccionado]["Cantidad"].iloc[0]
        st.metric("📦 Stock Actual", int(stock_actual))

        # Botón de registro
        submit = st.button("✅ Registrar Movimiento", use_container_width=True)
    
    with col2:
        st.markdown("### 💡 Tipos de Movimiento")
        st.info("""
        **📥 Entrada:** Compras, recepciones  
        **📤 Salida:** Ventas, entregas  
        **⚖️ Ajuste:** Correcciones de inventario  
        **🔄 Devolución:** Returns de clientes
        """)

    if submit:
        # Usar el ID generado automáticamente
        exito = registrar_movimiento(
            id_movimiento_auto, tipo_movimiento, producto_seleccionado, cantidad, observaciones
        )
        if exito:
            st.success(f"✅ Movimiento registrado correctamente con ID: **{id_movimiento_auto}**")
            st.balloons()
            st.rerun()
