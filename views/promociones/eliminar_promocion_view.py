"""
Vista de Eliminación de Promociones
"""
import streamlit as st
from data_manager import get_promociones
from promociones_crud import eliminar_promocion, obtener_promocion_por_id

def mostrar():
    """Muestra la interfaz de eliminación de promociones"""
    st.markdown("## 🗑️ Eliminar Promoción")
    
    promociones = get_promociones()
    
    if promociones.empty:
        st.info("📭 No hay promociones registradas para eliminar.")
        return
    
    ids_promociones = promociones["ID"].tolist()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        id_promo_sel = st.selectbox(
            "🔍 Selecciona una promoción por ID",
            ids_promociones
        )
        
        promo = obtener_promocion_por_id(id_promo_sel)
        
        if promo is not None:
            st.markdown("### ⚠️ Promoción a Eliminar")
            
            # Formatear valor
            if promo['Tipo'] == '2x1':
                valor_texto = "2x1"
            elif promo['Tipo'] == 'porcentaje':
                valor_texto = f"{promo['Valor']}% OFF"
            else:
                valor_texto = f"S/ {promo['Valor']:.2f} OFF"
            
            st.markdown(f"""
            <div class="product-card" style="border-left: 4px solid #dc3545; background: #fff5f5;">
                <h4>🎁 {promo['Nombre']} (ID: {promo['ID']})</h4>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                    <div>
                        <p><strong>Tipo:</strong> {promo['Tipo']}</p>
                        <p><strong>Descuento:</strong> {valor_texto}</p>
                        <p><strong>Estado:</strong> {promo['Estado']}</p>
                    </div>
                    <div>
                        <p><strong>Producto:</strong> {promo['Producto_Nombre']} ({promo['Producto_ID']})</p>
                        <p><strong>Inicio:</strong> {promo['Fecha_Inicio']}</p>
                        <p><strong>Fin:</strong> {promo['Fecha_Fin']}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Advertencia especial si está activa
            if promo['Estado'] == 'activa':
                st.error("""
                ⚠️ **ADVERTENCIA: Esta promoción está ACTIVA**
                
                Si la eliminas:
                - Se quitará del sistema inmediatamente
                - Ya no se aplicará en nuevas ventas
                - Las ventas anteriores con esta promoción permanecerán sin cambios
                """)
            
            # Confirmación
            confirmacion = st.checkbox(
                f"✅ Confirmo que deseo eliminar la promoción **{promo['Nombre']}**"
            )
            
            if confirmacion:
                if st.button("🗑️ ELIMINAR PROMOCIÓN", type="primary", use_container_width=True):
                    if eliminar_promocion(id_promo_sel):
                        st.markdown(
                            '<div class="success-message">✅ Promoción eliminada correctamente.</div>',
                            unsafe_allow_html=True
                        )
                        st.rerun()
    
    with col2:
        st.markdown("### ⚠️ Advertencia")
        st.warning("""
        **¡Atención!**
        
        Esta acción eliminará permanentemente la promoción del sistema.
        
        **Consecuencias:**
        
        - ❌ No se puede deshacer
        - 🛒 No se aplicará en futuras ventas
        - 📊 Se perderán las estadísticas asociadas
        - 💾 Las ventas anteriores no se verán afectadas
        
        Asegúrate de que realmente quieres eliminar esta promoción.
        """)
        
        st.markdown("### 💡 Alternativa")
        st.info("""
        Si solo quieres desactivar temporalmente la promoción, considera **actualizarla** y cambiar su estado a "inactiva" en lugar de eliminarla.
        """)
