"""
Vista de Devoluciones - Con validaciones completas
"""
import streamlit as st
from ventas_crud import obtener_venta_por_id, procesar_devolucion, obtener_devoluciones, parsear_items_venta
from data_manager import get_ventas

def mostrar():
    """Muestra la interfaz de devoluciones con validaciones"""
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
                
                # Parsear items de la venta
                items_venta = parsear_items_venta(venta['Items'])
                
                if items_venta:
                    st.markdown("---")
                    st.markdown("### 🛍️ Productos de la Venta")
                    
                    # Mostrar productos vendidos
                    for item in items_venta:
                        col_n, col_c, col_p = st.columns([3, 1, 1])
                        with col_n:
                            st.markdown(f"**{item['nombre']}** ({item['producto_id']})")
                        with col_c:
                            st.markdown(f"Cantidad: **{item['cantidad']}**")
                        with col_p:
                            st.markdown(f"S/{item['precio_unitario']:.2f}")
                    
                    st.markdown("---")
                    st.markdown("### 🔄 Seleccionar Items a Devolver")
                    
                    # Inicializar carrito de devolución
                    if "carrito_devolucion" not in st.session_state:
                        st.session_state.carrito_devolucion = []
                    
                    # Crear diccionario de cantidades vendidas
                    productos_vendidos = {item['producto_id']: item for item in items_venta}
                    
                    # Selector de productos SOLO de la venta
                    col_prod, col_cant, col_btn = st.columns([3, 1, 1])
                    
                    with col_prod:
                        productos_ids_venta = [item['producto_id'] for item in items_venta]
                        
                        producto_dev = st.selectbox(
                            "Producto a devolver",
                            productos_ids_venta,
                            format_func=lambda x: f"{x} - {productos_vendidos[x]['nombre']} (Vendidos: {productos_vendidos[x]['cantidad']})"
                        )
                    
                    with col_cant:
                        # Cantidad máxima = cantidad vendida
                        max_cant = productos_vendidos[producto_dev]['cantidad']
                        cantidad_dev = st.number_input(
                            "Cantidad", 
                            min_value=1, 
                            max_value=max_cant,
                            value=1, 
                            step=1,
                            help=f"Máximo: {max_cant} (cantidad vendida)"
                        )
                    
                    with col_btn:
                        st.markdown("<br>", unsafe_allow_html=True)
                        if st.button("➕ Agregar"):
                            # Verificar si ya está en el carrito
                            existe = False
                            for cart_item in st.session_state.carrito_devolucion:
                                if cart_item["producto_id"] == producto_dev:
                                    # Verificar que no exceda la cantidad vendida
                                    nueva_cant = cart_item["cantidad"] + cantidad_dev
                                    if nueva_cant <= max_cant:
                                        cart_item["cantidad"] = nueva_cant
                                        existe = True
                                        st.success(f"✅ Cantidad actualizada")
                                    else:
                                        st.error(f"❌ No puedes devolver más de {max_cant} unidades")
                                        existe = True
                                    break
                            
                            if not existe:
                                st.session_state.carrito_devolucion.append({
                                    "producto_id": producto_dev,
                                    "nombre": productos_vendidos[producto_dev]['nombre'],
                                    "cantidad": cantidad_dev,
                                    "cantidad_vendida": max_cant,
                                    "motivo": ""
                                })
                                st.success(f"✅ {productos_vendidos[producto_dev]['nombre']} agregado")
                            
                            st.rerun()
                    
                    # Mostrar carrito de devolución
                    if st.session_state.carrito_devolucion:
                        st.markdown("---")
                        st.markdown("#### 🛒 Items a Devolver")
                        
                        for i, item in enumerate(st.session_state.carrito_devolucion):
                            st.markdown(f"**{item['nombre']}** ({item['producto_id']})")
                            
                            col_c, col_m, col_d = st.columns([1, 3, 1])
                            
                            with col_c:
                                st.markdown(f"Cantidad: **{item['cantidad']}** / {item['cantidad_vendida']}")
                            
                            with col_m:
                                motivo = st.text_input(
                                    "Motivo de devolución",
                                    key=f"motivo_{i}",
                                    placeholder="Ej: Producto defectuoso, mal estado, etc."
                                )
                                st.session_state.carrito_devolucion[i]["motivo"] = motivo
                            
                            with col_d:
                                if st.button("🗑️", key=f"del_dev_{i}", help="Quitar"):
                                    st.session_state.carrito_devolucion.pop(i)
                                    st.rerun()
                        
                        st.markdown("---")
                        
                        # Motivo general
                        motivo_general = st.text_area(
                            "📝 Motivo General de Devolución",
                            placeholder="Describe el motivo general de la devolución...",
                            help="Este motivo se aplicará a todos los productos si no especificas uno individual"
                        )
                        
                        # Botones de acción
                        col_conf, col_canc = st.columns(2)
                        
                        with col_conf:
                            if st.button("✅ Procesar Devolución", type="primary", use_container_width=True):
                                # Validar que todos los items tengan motivo
                                items_sin_motivo = [item for item in st.session_state.carrito_devolucion 
                                                   if not item["motivo"] and not motivo_general]
                                
                                if items_sin_motivo and not motivo_general:
                                    st.warning("⚠️ Debes indicar un motivo para cada producto o un motivo general")
                                else:
                                    # Procesar devolución
                                    exito, mensaje = procesar_devolucion(
                                        venta_sel, 
                                        st.session_state.carrito_devolucion, 
                                        motivo_general
                                    )
                                    
                                    if exito:
                                        st.success(mensaje)
                                        st.balloons()
                                        
                                        # Limpiar carrito
                                        st.session_state.carrito_devolucion = []
                                        
                                        st.info("""
                                        ✅ **Acciones realizadas:**
                                        - ✓ Productos devueltos al inventario
                                        - ✓ Movimientos tipo "Devolución" registrados
                                        - ✓ Devolución documentada en el historial
                                        """)
                                        
                                        st.rerun()
                                    else:
                                        st.error(mensaje)
                        
                        with col_canc:
                            if st.button("❌ Cancelar y Limpiar", use_container_width=True):
                                st.session_state.carrito_devolucion = []
                                st.rerun()
                    else:
                        st.info("🛒 No has agregado productos para devolver. Selecciona productos de la venta.")
                
                else:
                    st.error("❌ No se pudieron cargar los productos de esta venta")
        
        with col2:
            st.markdown("### 💡 Información")
            st.info("""
            **Proceso de devolución:**
            1. ✅ Selecciona la venta
            2. ✅ Solo puedes devolver productos **de esa venta**
            3. ✅ Cantidad máxima = cantidad vendida
            4. ✅ Indica motivo de devolución
            5. ✅ Confirma la devolución
            
            **Efectos automáticos:**
            - ✓ Productos vuelven al inventario
            - ✓ Se registra movimiento "Devolución"
            - ✓ Se documenta en historial
            
            **Restricciones:**
            - ❌ No puedes devolver productos que no estén en la venta
            - ❌ No puedes devolver más cantidad de la vendida
            """)
            
            st.markdown("### ⚠️ Importante")
            st.warning("""
            Las devoluciones NO modifican el monto de la venta original.
            
            Solo registran el movimiento y devuelven el stock al inventario.
            """)
    
    with tab2:
        st.markdown("### 📋 Historial de Devoluciones")
        
        devoluciones = obtener_devoluciones()
        
        if not devoluciones.empty:
            # Ordenar por fecha descendente
            devoluciones_ordenadas = devoluciones.sort_values('Fecha', ascending=False)
            
            st.dataframe(
                devoluciones_ordenadas,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "ID_Devolucion": st.column_config.TextColumn("ID Devolución"),
                    "ID_Venta": st.column_config.TextColumn("Venta Original"),
                    "Fecha": st.column_config.DatetimeColumn("Fecha"),
                    "Motivo": st.column_config.TextColumn("Motivo"),
                    "Estado": st.column_config.TextColumn("Estado")
                }
            )
            
            # Estadísticas
            st.markdown("---")
            st.markdown("### 📊 Estadísticas de Devoluciones")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Devoluciones", len(devoluciones))
            with col2:
                procesadas = len(devoluciones[devoluciones["Estado"] == "procesada"])
                st.metric("Procesadas", procesadas)
            with col3:
                # Devoluciones del mes actual
                from datetime import datetime
                mes_actual = datetime.now().month
                devoluciones_ordenadas['Fecha_dt'] = pd.to_datetime(devoluciones_ordenadas['Fecha'])
                devs_mes = len(devoluciones_ordenadas[devoluciones_ordenadas['Fecha_dt'].dt.month == mes_actual])
                st.metric("Este Mes", devs_mes)
        else:
            st.info("📭 No hay devoluciones registradas.")
