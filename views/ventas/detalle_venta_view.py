"""
Vista de Detalle de Venta
"""
import streamlit as st
import json
from ventas_crud import obtener_venta_por_id

def mostrar():
    """Muestra el detalle completo de una venta"""
    st.markdown("## 🧾 Detalle de Venta")
    
    # Verificar si hay ID de venta seleccionado
    if "venta_detalle_id" not in st.session_state:
        st.warning("⚠️ No se ha seleccionado ninguna venta.")
        if st.button("🔙 Volver al Dashboard"):
            st.session_state.menu_principal = "ventas_dashboard"
            st.rerun()
        return
    
    venta_id = st.session_state.venta_detalle_id
    venta = obtener_venta_por_id(venta_id)
    
    if not venta:
        st.error(f"❌ No se encontró la venta {venta_id}")
        if st.button("🔙 Volver al Dashboard"):
            st.session_state.menu_principal = "ventas_dashboard"
            st.rerun()
        return
    
    # Botón volver
    if st.button("🔙 Volver"):
        del st.session_state.venta_detalle_id
        st.session_state.menu_principal = "ventas_dashboard"
        st.rerun()
    
    st.markdown("---")
    
    # Información principal
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
        <div class="product-card" style="border-left: 4px solid #667eea; background: #f8f9ff;">
            <h3>🆔 {venta['ID']}</h3>
            <p><strong>📅 Fecha:</strong> {venta['Fecha']}</p>
            <p><strong>💳 Método de Pago:</strong> {venta['Metodo_Pago'].upper()}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🛒 Productos Vendidos")
        
        # Parsear items (simplificado, en producción usar json.loads)
        try:
            items_str = venta['Items']
            # Nota: En una implementación real, guardaríamos como JSON y haríamos json.loads
            st.info("💡 Los items se muestran en formato simplificado")
            st.code(items_str)
        except:
            st.warning("⚠️ No se pudieron cargar los items de la venta")
        
        st.markdown("### 💰 Totales")
        
        col_t1, col_t2, col_t3 = st.columns(3)
        
        with col_t1:
            st.metric("Subtotal", f"S/{venta['Total_Bruto']:.2f}")
        with col_t2:
            st.metric("Descuento", f"-S/{venta['Total_Descuento']:.2f}")
        with col_t3:
            st.metric("Total Final", f"S/{venta['Total_Final']:.2f}")
    
    with col2:
        st.markdown("### 🎁 Promociones Aplicadas")
        
        if venta['Promociones']:
            promociones = venta['Promociones'].split(',')
            for promo in promociones:
                if promo.strip():
                    st.success(f"✨ {promo.strip()}")
        else:
            st.info("Sin promociones aplicadas")
        
        st.markdown("---")
        
        st.markdown("### 🧾 Ticket")
        if st.button("🖨️ Generar Ticket", use_container_width=True):
            st.code(f"""
{'='*40}
          Q'BODEGA
{'='*40}
Venta: {venta['ID']}
Fecha: {venta['Fecha']}
{'='*40}

[Ver items en la sección principal]

{'='*40}
Subtotal:    S/{venta['Total_Bruto']:.2f}
Descuento:  -S/{venta['Total_Descuento']:.2f}
{'='*40}
TOTAL:       S/{venta['Total_Final']:.2f}
{'='*40}
Método: {venta['Metodo_Pago'].upper()}

¡Gracias por su compra!
{'='*40}
            """)
    
    st.markdown("---")
    
    # Información adicional
    st.markdown("### ℹ️ Información Adicional")
    st.info(f"""
    **Estado:** Venta completada  
    **Inventario:** Actualizado automáticamente  
    **Movimientos:** Registrados en el sistema  
    **Promociones:** {len(venta['Promociones'].split(',')) if venta['Promociones'] else 0} aplicadas
    """)
