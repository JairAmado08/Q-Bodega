"""
Vista de Registro de Ventas
"""
import streamlit as st
from datetime import datetime
from data_manager import get_inventario
from ventas_crud import registrar_venta, calcular_totales
from inventario_crud import obtener_producto
from utils import generar_id_venta

def mostrar():
    """Muestra el formulario de registro de ventas"""
    st.markdown("## 🛒 Registrar Nueva Venta")
    
    inventario = get_inventario()
    
    if inventario.empty:
        st.error("❌ No hay productos disponibles. Primero registra algunos productos.")
        st.stop()
    
    # Inicializar carrito en session_state
    if "carrito" not in st.session_state:
        st.session_state.carrito = []
    
    # Generar ID de venta
    id_venta = generar_id_venta()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🛍️ Agregar Productos al Carrito")
        st.info(f"🆔 **ID de venta:** `{id_venta}`")
        
        # Selector de productos
        col_prod, col_cant, col_btn = st.columns([3, 1, 1])
        
        with col_prod:
            productos_disponibles = inventario[inventario["Cantidad"] > 0]["ID"].tolist()
            
            if not productos_disponibles:
                st.warning("⚠️ No hay productos con stock disponible.")
                st.stop()
            
            producto_sel = st.selectbox(
                "📦 Producto",
                productos_disponibles,
                format_func=lambda x: f"{x} - {inventario[inventario['ID'] == x]['Nombre'].iloc[0]} (Stock: {int(inventario[inventario['ID'] == x]['Cantidad'].iloc[0])})"
            )
        
        with col_cant:
            producto_info = obtener_producto(producto_sel)
            max_cantidad = int(producto_info["Cantidad"])
            
            cantidad = st.number_input(
                "Cantidad",
                min_value=1,
                max_value=max_cantidad,
                value=1,
                step=1
            )
        
        with col_btn:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("➕ Agregar", use_container_width=True):
                # Agregar al carrito
                producto_info = obtener_producto(producto_sel)
                
                # Verificar si ya está en el carrito
                existe = False
                for item in st.session_state.carrito:
                    if item["producto_id"] == producto_sel:
                        item["cantidad"] += cantidad
                        existe = True
                        break
                
                if not existe:
                    st.session_state.carrito.append({
                        "producto_id": producto_sel,
                        "nombre": producto_info["Nombre"],
                        "cantidad": cantidad,
                        "precio_unitario": float(producto_info["Precio"])
                    })
                
                st.success(f"✅ {producto_info['Nombre']} agregado al carrito")
                st.rerun()
        
        # Mostrar carrito
        st.markdown("---")
        st.markdown("### 🛒 Carrito de Compras")
        
        if st.session_state.carrito:
            # Calcular totales con promociones
            totales = calcular_totales(st.session_state.carrito)
            
            # Tabla del carrito
            for i, item in enumerate(st.session_state.carrito):
                col_nom, col_cant, col_prec, col_sub, col_del = st.columns([3, 1, 1, 1, 1])
                
                with col_nom:
                    st.markdown(f"**{item['nombre']}**")
                with col_cant:
                    st.markdown(f"x{item['cantidad']}")
                with col_prec:
                    st.markdown(f"S/{item['precio_unitario']:.2f}")
                with col_sub:
                    subtotal_item = item['cantidad'] * item['precio_unitario']
                    st.markdown(f"S/{subtotal_item:.2f}")
                with col_del:
                    if st.button("🗑️", key=f"del_{i}", help="Eliminar"):
                        st.session_state.carrito.pop(i)
                        st.rerun()
            
            st.markdown("---")
            
            # Totales
            col_label, col_valor = st.columns([3, 1])
            
            with col_label:
                st.markdown("**Subtotal:**")
                st.markdown("**Descuento:**")
                if totales["promociones"]:
                    for promo in totales["promociones"]:
                        st.markdown(f"  - _{promo['nombre']}_")
                st.markdown("### **TOTAL:**")
            
            with col_valor:
                st.markdown(f"S/{totales['subtotal']:.2f}")
                st.markdown(f"-S/{totales['descuento']:.2f}")
                if totales["promociones"]:
                    for promo in totales["promociones"]:
                        st.markdown(f"-S/{promo['descuento']:.2f}")
                st.markdown(f"### **S/{totales['total']:.2f}**")
            
            st.markdown("---")
            
            # Método de pago
            metodo_pago = st.selectbox(
                "💳 Método de Pago",
                ["efectivo", "tarjeta", "yape", "plin"]
            )
            
            # Botones de acción
            col_conf, col_canc = st.columns(2)
            
            with col_conf:
                if st.button("✅ Confirmar Venta", type="primary", use_container_width=True):
                    # Preparar venta
                    venta = {
                        "id": id_venta,
                        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "items": st.session_state.carrito,
                        "total_bruto": totales["subtotal"],
                        "total_descuento": totales["descuento"],
                        "total_final": totales["total"],
                        "metodo_pago": metodo_pago,
                        "promociones_aplicadas": [p["nombre"] for p in totales["promociones"]]
                    }
                    
                    # Registrar venta
                    if registrar_venta(venta):
                        st.success(f"✅ Venta {id_venta} registrada exitosamente!")
                        st.balloons()
                        
                        # Limpiar carrito
                        st.session_state.carrito = []
                        
                        # Mostrar ticket
                        st.markdown("---")
                        st.markdown("### 🧾 Ticket de Venta")
                        st.code(f"""
{'='*40}
          Q'BODEGA
{'='*40}
Venta: {id_venta}
Fecha: {venta['fecha']}
{'='*40}

PRODUCTOS:
{chr(10).join([f"{item['nombre']} x{item['cantidad']} ... S/{item['cantidad'] * item['precio_unitario']:.2f}" for item in st.session_state.carrito])}

{'='*40}
Subtotal:    S/{totales['subtotal']:.2f}
Descuento:  -S/{totales['descuento']:.2f}
{'='*40}
TOTAL:       S/{totales['total']:.2f}
{'='*40}
Método: {metodo_pago.upper()}

¡Gracias por su compra!
{'='*40}
                        """)
                        
                        st.info("💡 Usa el botón del sidebar para ver el dashboard de ventas")
            
            with col_canc:
                if st.button("❌ Cancelar y Limpiar", use_container_width=True):
                    st.session_state.carrito = []
                    st.rerun()
        
        else:
            st.info("🛒 El carrito está vacío. Agrega productos para continuar.")
    
    with col2:
        st.markdown("### 💡 Información")
        st.info("""
        **Proceso de venta:**
        1. Selecciona un producto
        2. Indica la cantidad
        3. Agrega al carrito
        4. Repite para más productos
        5. Selecciona método de pago
        6. Confirma la venta
        
        **Promociones:**
        Se aplican automáticamente según las promociones activas.
        """)
        
        if st.session_state.carrito:
            st.markdown("### 🎁 Promociones Aplicadas")
            totales = calcular_totales(st.session_state.carrito)
            
            if totales["promociones"]:
                for promo in totales["promociones"]:
                    st.success(f"✨ {promo['nombre']}")
            else:
                st.warning("Sin promociones aplicables")
