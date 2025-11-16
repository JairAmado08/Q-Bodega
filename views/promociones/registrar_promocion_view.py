"""
Vista de Registro de Promociones
"""
import streamlit as st
from datetime import datetime, timedelta
from data_manager import get_inventario
from promociones_crud import crear_promocion, promocion_existe
from utils import generar_id_promocion

def mostrar():
    """Muestra el formulario de registro de promociones"""
    st.markdown("## ➕ Registrar Nueva Promoción")
    
    inventario = get_inventario()
    
    if inventario.empty:
        st.error("❌ No hay productos disponibles. Primero registra algunos productos.")
        st.stop()
    
    # Generar ID automáticamente
    id_promocion_auto = generar_id_promocion()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.form("form_registrar_promocion", clear_on_submit=True):
            st.markdown("### 📝 Información de la Promoción")
            
            # Mostrar ID que se asignará
            st.info(f"🆔 **ID automático asignado:** `{id_promocion_auto}`")
            
            col_form1, col_form2 = st.columns(2)
            
            with col_form1:
                nombre = st.text_input("🏷️ Nombre de la promoción", placeholder="Ej: 2x1 en Gaseosas")
                
                tipo = st.selectbox(
                    "🎁 Tipo de promoción",
                    options=["2x1", "porcentaje", "monto fijo"],
                    help="2x1: Por cada 2 unidades, 1 gratis\nPorcentaje: % de descuento\nMonto fijo: Descuento en S/"
                )
                
                # Valor según tipo
                if tipo == "2x1":
                    valor = 0
                    st.info("💡 El descuento se calcula automáticamente (50% en grupos de 2)")
                elif tipo == "porcentaje":
                    valor = st.number_input(
                        "📊 Porcentaje de descuento (%)",
                        min_value=0.0,
                        max_value=100.0,
                        step=5.0,
                        value=10.0
                    )
                else:  # monto fijo
                    valor = st.number_input(
                        "💰 Monto de descuento (S/)",
                        min_value=0.0,
                        step=0.50,
                        value=1.0,
                        format="%.2f"
                    )
            
            with col_form2:
                # Producto asociado
                productos_disponibles = inventario["ID"].tolist()
                producto_id = st.selectbox(
                    "📦 Producto asociado",
                    options=productos_disponibles,
                    format_func=lambda x: f"{x} - {inventario[inventario['ID'] == x]['Nombre'].iloc[0]}"
                )
                
                # Fechas
                fecha_inicio = st.date_input(
                    "📅 Fecha de inicio",
                    value=datetime.now(),
                    min_value=datetime.now()
                )
                
                fecha_fin = st.date_input(
                    "📅 Fecha de fin",
                    value=datetime.now() + timedelta(days=7),
                    min_value=datetime.now()
                )
                
                # Estado
                estado = st.selectbox(
                    "🔘 Estado",
                    options=["activa", "inactiva"],
                    index=0
                )
            
            submit = st.form_submit_button("✅ Crear Promoción", use_container_width=True)
    
    with col2:
        st.markdown("### 💡 Tipos de Promoción")
        st.info("""
        **🎁 2x1**  
        Por cada 2 unidades, el cliente paga solo 1.
        
        **📊 Porcentaje**  
        Descuento del X% sobre el precio del producto.
        
        **💰 Monto Fijo**  
        Descuento de S/ X por cada unidad.
        """)
        
        st.markdown("### 📋 Consejos")
        st.warning("""
        - Usa IDs únicos (PR001, PR002...)
        - Verifica que las fechas sean correctas
        - Las promociones activas se aplican automáticamente en ventas
        - Puedes tener múltiples promociones por producto
        """)
    
    if submit:
        if id_promocion and nombre:
            if promocion_existe(id_promocion):
                st.markdown(
                    '<div class="warning-message">⚠️ Ya existe una promoción con este ID.</div>',
                    unsafe_allow_html=True
                )
            else:
                # Preparar datos
                datos_promocion = {
                    "id": id_promocion,
                    "nombre": nombre,
                    "tipo": tipo,
                    "valor": valor,
                    "producto_id": producto_id,
                    "fecha_inicio": fecha_inicio.strftime("%Y-%m-%d"),
                    "fecha_fin": fecha_fin.strftime("%Y-%m-%d"),
                    "estado": estado
                }
                
                # Crear promoción
                if crear_promocion(datos_promocion):
                    st.markdown(
                        '<div class="success-message">✅ Promoción creada correctamente.</div>',
                        unsafe_allow_html=True
                    )
                    st.balloons()
        else:
            st.markdown(
                '<div class="error-message">❌ Debes completar al menos ID y Nombre.</div>',
                unsafe_allow_html=True
            )
