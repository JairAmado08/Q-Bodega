"""
Vista de Actualización de Movimientos
"""
import streamlit as st
import pandas as pd
from data_manager import get_movimientos, get_inventario
from movimientos_crud import actualizar_movimiento

def mostrar():
    """Muestra el formulario de actualización de movimientos"""
    st.markdown("## ✏️ Actualizar Movimiento")
    
    movimientos = get_movimientos()
    inventario = get_inventario()
    ids_movimientos = movimientos["ID_Movimiento"].tolist()
    
    if ids_movimientos:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            id_mov_sel = st.selectbox("🔍 Selecciona un movimiento por ID", ids_movimientos)
            movimiento = movimientos[movimientos["ID_Movimiento"] == id_mov_sel].iloc[0]
            
            st.markdown(f"### 📋 Movimiento Actual: **{movimiento['ID_Movimiento']}**")
            
            with st.form("form_actualizar_movimiento"):
                st.markdown("#### 📝 Nuevos Datos")
                
                col_form1, col_form2 = st.columns(2)
                with col_form1:
                    tipo_movimiento = st.selectbox("🏷️ Tipo de movimiento", 
                                                 options=["Entrada", "Salida", "Ajuste", "Devolución"],
                                                 index=["Entrada", "Salida", "Ajuste", "Devolución"].index(movimiento["Tipo"]))
                    
                    productos_disponibles = inventario["ID"].tolist()
                    if movimiento["Producto_ID"] in productos_disponibles:
                        producto_idx = productos_disponibles.index(movimiento["Producto_ID"])
                    else:
                        producto_idx = 0
                    
                    producto_seleccionado = st.selectbox("📦 Producto", productos_disponibles, index=producto_idx)
                
                with col_form2:
                    cantidad = st.number_input("📊 Cantidad", value=int(movimiento["Cantidad"]), step=1)
                    fecha = st.date_input("📅 Fecha", value=pd.to_datetime(movimiento["Fecha"]).date())
                
                observaciones = st.text_area("📝 Observaciones", value=movimiento["Observaciones"])
                
                submit = st.form_submit_button("🔄 Actualizar Movimiento", use_container_width=True)
        
        with col2:
            st.markdown("### 📊 Información Actual")
            st.info(f"""
            **Tipo:** {movimiento['Tipo']}
            
            **Producto:** {movimiento['Producto_Nombre']}
            
            **Cantidad:** {movimiento['Cantidad']}
            
            **Fecha:** {movimiento['Fecha']}
            
            **Usuario:** {movimiento['Usuario']}
            """)
        
        if submit:
            fecha_str = fecha.strftime("%Y-%m-%d")
            actualizar_movimiento(id_mov_sel, tipo_movimiento, producto_seleccionado, cantidad, fecha_str, observaciones)
            st.success("✅ Movimiento actualizado correctamente.")
            st.rerun()
    else:
        st.info("📭 No hay movimientos registrados para actualizar.")
