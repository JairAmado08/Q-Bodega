"""
Vista de Devoluciones
"""
import streamlit as st
import ast
from ventas_crud import obtener_venta_por_id, procesar_devolucion, obtener_devoluciones
from data_manager import get_ventas
from inventario_crud import obtener_producto

def mostrar():
    """Muestra la interfaz de devoluciones"""
    st.markdown("## 🔄 Procesar Devolución")
    
    ventas = get_ventas()
    
    if ventas.empty:
        st.info("📭 No hay ventas registradas para procesar devoluciones.")
        return
    
    tab1, tab2 = st.tabs(["📝 Nueva Devolución", "📋 Historial de Devoluciones"])
    
    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 🔍 Seleccionar Venta")
            
            # Selector de venta
            ventas_ids = ventas["ID"].tolist()
            venta_sel = st.selectbox(
                "🆔 ID de Venta",
                ventas_ids,
                format_func=lambda x: f"{x} - {ventas[ventas['ID']==x]['Fecha'].iloc[0]} (S/{ventas[ventas['ID']==x]['Total_Final'].iloc[0]:.2f})"
            )
            
            if venta_sel:
                venta = obtener_venta_por_id(venta_sel)
                
                st.markdown("---")
                st.markdown("### 📦 Detalles de la Venta")
                
                col_v1, col_v2, col_v3 = st.columns(3)
                with col_v1:
                    st.metric("Fecha", venta['Fecha'])
                with col_v2:
                    st.metric("Total", f"S/{venta['Total_Final']:.2f}")
                with col_v3:
                    st.metric("Método", venta['Metodo_Pago'].upper())
                
                st.markdown("---")
                st.markdown("### 🔄 Items a Devolver")
                
                # Parsear items de la venta (simplificado)
                try:
                    items_str = venta['Items']
                    # En producción, usar json.loads
                    st.info("💡 Selecciona los productos a devolver")
                    
                    # Simulación de items (en producción, parsear correctamente)
                    # Por ahora, permitir selección manual
                    
                    st.markdown("#### Seleccionar productos")
                    
                    # Inicializar carrito de devolución
                    if "carrito_devolucion" not in st.session_state:
                        st.session_state.carrito_devolucion = []
                    
                    # Agregar producto al carrito de devolución
                    col_prod, col_cant, col_btn = st.columns([3, 1, 1])
                    
                    with col_prod:
                        # Nota: En producción, obtener productos de la venta original
                        from data_manager import get_inventario
                        inventario = get_inventario()
                        productos_disp = inventario["ID"].tolist()
                        
                        producto_dev = st.selectbox(
                            "Producto",
                            productos_disp,
                            format_func=lambda x: f"{x} - {inventario[inventario['ID']==x]['Nombre'].iloc[0]}"
                        )
                    
                    with col_cant:
                        cantidad_dev = st.number_input("Cantidad", min_value=1, value=1, step=1)
                    
                    with col_btn:
                        st.markdown("<br>", unsafe_allow_html=True)
                        if st.button("➕ Agregar"):
                            producto_info = obtener_producto(producto_dev)
                            
                            st.session_state.carrito_devolucion.append({
                                "producto_id": producto_dev,
                                "nombre": producto_info["Nombre"],
                                "cantidad": cantidad_dev,
                                "motivo": ""
                            })
                            st.success(f"✅ {producto_info['Nombre']} agregado a devolución")
                            st.rerun()
                    
                    # Mostrar carrito de devolución
                    if st.session_state.carrito_devolucion:
                        st.markdown("---")
                        st.markdown("#### 🛒 Items a Devolver")
                        
                        for i, item in enumerate(st.session_state.carrito_devolucion):
                            col_n, col_c, col_m, col_d = st.columns([2, 1, 2, 1])
                            
                            with col_n:
                                st.markdown(f"**{item['nombre']}**")
                            with col_c:
                                st.markdown(f"x{item['cantidad']}")
                            with col_m:
                                motivo = st.text_input(
                                    "Motivo",
                                    key=f"motivo_{i}",
                                    placeholder="Ej: Producto defectuoso"
                                )
                                st.session_state.carrito_devolucion[i]["motivo"] = motivo
                            with col_d:
                                if st.button("🗑️", key=f"del_dev_{i}"):
                                    st.session_state.carrito_devolucion.pop(i)
                                    st.rerun()
                        
                        st.markdown("---")
                        
                        # Motivo general
                        motivo_general = st.text_area(
                            "📝 Motivo General de Devolución",
                            placeholder="Describe el motivo de la devolución..."
                        )
                        
                        # Botones de acción
                        col_conf, col_canc = st.columns(2)
                        
                        with col_conf:
                            if st.button("✅ Procesar Devolución", type="primary", use_container_width=True):
                                # Procesar devolución
                                if procesar_devolucion(venta_sel, st.session_state.carrito_devolucion, motivo_general):
                                    st.success("✅ Devolución procesada correctamente!")
                                    st.balloons()
                                    
                                    # Limpiar carrito
                                    st.session_state.carrito_devolucion = []
                                    
                                    st.info("""
                                    ✅ **Acciones realizadas:**
                                    - Productos devueltos al inventario
                                    - Movimientos registrados
                                    - Devolución documentada
                                    """)
                        
                        with col_canc:
                            if st.button("❌ Cancelar", use_container_width=True):
                                st.session_state.carrito_devolucion = []
                                st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Error al procesar items: {e}")
                    st.info("💡 Usa el selector manual de productos arriba")
        
        with col2:
            st.markdown("### 💡 Información")
            st.info("""
            **Proceso de devolución:**
            1. Selecciona la venta
            2. Agrega productos a devolver
            3. Indica cantidad y motivo
            4. Confirma la devolución
            
            **Efectos:**
            - ✅ Productos vuelven al inventario
            - ✅ Se registra movimiento
            - ✅ Se documenta la devolución
            
            **Nota:** Las devoluciones no modifican la venta original, solo registran el movimiento.
            """)
    
    with tab2:
        st.markdown("### 📋 Historial de Devoluciones")
        
        devoluciones = obtener_devoluciones()
        
        if not devoluciones.empty:
            st.dataframe(
                devoluciones,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "ID_Devolucion": st.column_config.TextColumn("ID"),
                    "ID_Venta": st.column_config.TextColumn("Venta"),
                    "Fecha": st.column_config.DatetimeColumn("Fecha"),
                    "Estado": st.column_config.TextColumn("Estado")
                }
            )
            
            # Estadísticas
            st.markdown("---")
            st.markdown("### 📊 Estadísticas")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Devoluciones", len(devoluciones))
            with col2:
                procesadas = len(devoluciones[devoluciones["Estado"] == "procesada"])
                st.metric("Procesadas", procesadas)
        else:
            st.info("📭 No hay devoluciones registradas.")
