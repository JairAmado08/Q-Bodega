"""
Vista de Devoluciones - CORREGIDA
"""
import streamlit as st
from ventas_crud import (
    obtener_venta_por_id, procesar_devolucion, 
    obtener_devoluciones, obtener_items_venta
)
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
                items_venta = obtener_items_venta(venta_sel)
                
                if not items_venta:
                    st.error("❌ No se pudieron cargar los productos de esta venta.")
                    st.stop()
                
                st.markdown("---")
                st.markdown("### 📦 Detalles de la Venta")
                
                col_v1, col_v2, col_v3 = st.columns(3)
                with col_v1:
                    st.metric("Fecha", venta['Fecha'])
                with col_v2:
                    st.metric("Total", f"S/{venta['Total_Final']:.2f}")
                with col_v3:
                    st.metric("Método", venta['Metodo_Pago'].upper())
                
                # Mostrar productos de la venta
                st.markdown("---")
                st.markdown("### 🛍️ Productos en la Venta")
                
                for item in items_venta:
                    col_p1, col_p2, col_p3 = st.columns([2, 1, 1])
                    with col_p1:
                        st.markdown(f"**{item['nombre']}**")
                    with col_p2:
                        st.markdown(f"Cantidad: **{item['cantidad']}**")
                    with col_p3:
                        st.markdown(f"S/{item['precio_unitario']:.2f} c/u")
                
                st.markdown("---")
                st.markdown("### 🔄 Seleccionar Items a Devolver")
                
                # Inicializar carrito de devolución
                if "carrito_devolucion" not in st.session_state:
                    st.session_state.carrito_devolucion = []
                
                # Selector de producto SOLO de los que están en la venta
                col_prod, col_cant, col_btn = st.columns([3, 1, 1])
                
                with col_prod:
                    # Crear lista de productos disponibles en la venta
                    productos_venta = {item['producto_id']: item for item in items_venta}
                    productos_ids = list(productos_venta.keys())
                    
                    if not productos_ids:
                        st.error("❌ No hay productos disponibles para devolver")
                        st.stop()
                    
                    producto_dev = st.selectbox(
                        "📦 Producto a devolver",
                        productos_ids,
                        format_func=lambda x: f"{x} - {productos_venta[x]['nombre']} (Vendidos: {productos_venta[x]['cantidad']})"
                    )
                
                with col_cant:
                    # Límite de cantidad según lo vendido
                    max_cantidad = productos_venta[producto_dev]['cantidad']
                    
                    # Verificar si ya se agregó al carrito para restar
                    cantidad_ya_devuelta = 0
                    for item_carr in st.session_state.carrito_devolucion:
                        if item_carr['producto_id'] == producto_dev:
                            cantidad_ya_devuelta += item_carr['cantidad']
                    
                    cantidad_disponible = max_cantidad - cantidad_ya_devuelta
                    
                    if cantidad_disponible <= 0:
                        st.warning(f"Ya agregaste todas las unidades ({max_cantidad})")
                        cantidad_dev = 0
                    else:
                        cantidad_dev = st.number_input(
                            f"Cantidad (máx: {cantidad_disponible})",
                            min_value=1,
                            max_value=cantidad_disponible,
                            value=min(1, cantidad_disponible),
                            step=1
                        )
                
                with col_btn:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if cantidad_disponible > 0 and st.button("➕ Agregar"):
                        producto_info = productos_venta[producto_dev]
                        
                        st.session_state.carrito_devolucion.append({
                            "producto_id": producto_dev,
                            "nombre": producto_info['nombre'],
                            "cantidad": cantidad_dev,
                            "motivo": ""
                        })
                        st.success(f"✅ {producto_info['nombre']} agregado a devolución")
                        st.rerun()
                
                # Mostrar carrito de devolución
                if st.session_state.carrito_devolucion:
                    st.markdown("---")
                    st.markdown("### 🛒 Items a Devolver")
                    
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
                        "📝 Motivo General de Devolución (opcional)",
                        placeholder="Describe el motivo general de la devolución..."
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
                                - ✅ Productos devueltos al inventario
                                - ✅ Movimiento de devolución registrado
                                - ✅ Devolución documentada en el sistema
                                """)
                                
                                # Mostrar resumen
                                st.markdown("### 📊 Resumen de Devolución")
                                total_items = sum(item['cantidad'] for item in st.session_state.carrito_devolucion)
                                st.metric("Items devueltos", total_items)
                    
                    with col_canc:
                        if st.button("❌ Cancelar", use_container_width=True):
                            st.session_state.carrito_devolucion = []
                            st.rerun()
        
        with col2:
            st.markdown("### 💡 Información")
            st.info("""
            **Proceso de devolución:**
            1. ✅ Selecciona la venta
            2. ✅ Solo puedes devolver productos que están en esa venta
            3. ✅ Cantidad máxima = cantidad vendida
            4. ✅ Indica motivo de cada producto
            5. ✅ Confirma la devolución
            
            **Efectos automáticos:**
            - ✅ Productos vuelven al inventario
            - ✅ Se registra movimiento tipo "Devolución"
            - ✅ Se documenta en historial
            
            **Restricciones:**
            - ❌ No puedes devolver productos que NO están en la venta
            - ❌ No puedes devolver más unidades de las vendidas
            - ✅ El stock se actualiza UNA sola vez (sin duplicación)
            """)
            
            st.markdown("### ⚠️ Importante")
            st.warning("""
            Las devoluciones NO modifican la venta original, solo:
            - Registran el movimiento de devolución
            - Actualizan el inventario
            - Documentan el historial
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
