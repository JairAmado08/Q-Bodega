"""
Vista de Registro de Movimientos
"""
import streamlit as st
from data_manager import get_inventario, get_movimientos
from movimientos_crud import registrar_movimiento, movimiento_existe

def mostrar():
    """Muestra el formulario de registro de movimientos"""
    st.markdown("## ➕ Registrar Nuevo Movimiento")
    
    inventario = get_inventario()
    movimientos = get_movimientos()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📝 Información del Movimiento")

        col_form1, col_form2 = st.columns(2)
        with col_form1:
            id_movimiento = st.text_input("🆔 ID del movimiento", placeholder="Ej: M001")
            tipo_movimiento = st.selectbox(
                "🏷️ Tipo de movimiento", 
                options=["Entrada", "Salida", "Ajuste", "Devolución"]
            )
            
            # Productos disponibles
            productos_disponibles = inventario["ID"].tolist() if not inventario.empty else []
            if productos_disponibles:
                producto_seleccionado = st.selectbox("📦 Producto", productos_disponibles)
            else:
                st.error("❌ No hay productos disponibles. Primero registra algunos productos.")
                st.stop()

        with col_form2:
            if tipo_movimiento == "Ajuste":
                cantidad = st.number_input(
                    "📊 Cantidad (+ para agregar, - para quitar)", 
                    step=1, format="%d", help="Usa números negativos para ajustes de disminución"
                )
            else:
                cantidad = st.number_input("📊 Cantidad", min_value=1, step=1, value=1)

            observaciones = st.text_area("📝 Observaciones", placeholder="Comentarios adicionales...")

        # Mostrar stock actual fuera del form
        if 'producto_seleccionado' in locals():
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
        if id_movimiento and productos_disponibles:
            if movimiento_existe(id_movimiento):
                st.error("⚠️ Ya existe un movimiento con este ID.")
            else:
                exito = registrar_movimiento(
                    id_movimiento, tipo_movimiento, producto_seleccionado, cantidad, observaciones
                )
                if exito:
                    st.success("✅ Movimiento registrado correctamente.")
                    st.balloons()
        else:
            st.error("❌ Debes completar al menos ID y seleccionar un producto.")
