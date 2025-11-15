"""
Vista de Actualización de Promociones
"""
import streamlit as st
import pandas as pd
from datetime import datetime
from data_manager import get_promociones, get_inventario
from promociones_crud import actualizar_promocion, obtener_promocion_por_id

def mostrar():
    """Muestra el formulario de actualización de promociones"""
    st.markdown("## ✏️ Actualizar Promoción")
    
    promociones = get_promociones()
    inventario = get_inventario()
    
    if promociones.empty:
        st.info("📭 No hay promociones registradas para actualizar.")
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
            st.markdown(f"### 📋 Promoción Actual: **{promo['Nombre']}**")
            
            with st.form("form_actualizar_promocion"):
                st.markdown("#### 📝 Nuevos Datos")
                
                col_form1, col_form2 = st.columns(2)
                
                with col_form1:
                    nombre = st.text_input("🏷️ Nombre", value=promo["Nombre"])
                    
                    tipo = st.selectbox(
                        "🎁 Tipo",
                        options=["2x1", "porcentaje", "monto fijo"],
                        index=["2x1", "porcentaje", "monto fijo"].index(promo["Tipo"])
                    )
                    
                    # Valor según tipo
                    if tipo == "2x1":
                        valor = 0
                        st.info("💡 El descuento se calcula automáticamente")
                    elif tipo == "porcentaje":
                        valor = st.number_input(
                            "📊 Porcentaje (%)",
                            min_value=0.0,
                            max_value=100.0,
                            value=float(promo["Valor"]) if promo["Tipo"] == "porcentaje" else 10.0,
                            step=5.0
                        )
                    else:  # monto fijo
                        valor = st.number_input(
                            "💰 Monto (S/)",
                            min_value=0.0,
                            value=float(promo["Valor"]) if promo["Tipo"] == "monto fijo" else 1.0,
                            step=0.50,
                            format="%.2f"
                        )
                
                with col_form2:
                    # Producto
                    productos_disponibles = inventario["ID"].tolist()
                    if promo["Producto_ID"] in productos_disponibles:
                        producto_idx = productos_disponibles.index(promo["Producto_ID"])
                    else:
                        producto_idx = 0
                    
                    producto_id = st.selectbox(
                        "📦 Producto",
                        options=productos_disponibles,
                        index=producto_idx,
                        format_func=lambda x: f"{x} - {inventario[inventario['ID'] == x]['Nombre'].iloc[0]}"
                    )
                    
                    # Fechas
                    fecha_inicio = st.date_input(
                        "📅 Fecha de inicio",
                        value=pd.to_datetime(promo["Fecha_Inicio"]).date()
                    )
                    
                    fecha_fin = st.date_input(
                        "📅 Fecha de fin",
                        value=pd.to_datetime(promo["Fecha_Fin"]).date()
                    )
                    
                    # Estado
                    estado = st.selectbox(
                        "🔘 Estado",
                        options=["activa", "inactiva"],
                        index=0 if promo["Estado"] == "activa" else 1
                    )
                
                submit = st.form_submit_button("🔄 Actualizar Promoción", use_container_width=True)
    
    with col2:
        st.markdown("### 📊 Información Actual")
        st.info(f"""
        **Nombre:** {promo['Nombre']}
        
        **Tipo:** {promo['Tipo']}
        
        **Valor:** {promo['Valor']}
        
        **Producto:** {promo['Producto_Nombre']}
        
        **Vigencia:** {promo['Fecha_Inicio']} - {promo['Fecha_Fin']}
        
        **Estado:** {promo['Estado']}
        """)
        
        # Verificar si está vigente
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        if (promo['Estado'] == 'activa' and 
            promo['Fecha_Inicio'] <= fecha_actual <= promo['Fecha_Fin']):
            st.success("✅ Esta promoción está vigente")
        else:
            st.warning("⚠️ Esta promoción no está vigente")
    
    if submit:
        # Preparar datos actualizados
        nuevos_datos = {
            "nombre": nombre,
            "tipo": tipo,
            "valor": valor,
            "producto_id": producto_id,
            "fecha_inicio": fecha_inicio.strftime("%Y-%m-%d"),
            "fecha_fin": fecha_fin.strftime("%Y-%m-%d"),
            "estado": estado
        }
        
        if actualizar_promocion(id_promo_sel, nuevos_datos):
            st.markdown(
                '<div class="success-message">✅ Promoción actualizada correctamente.</div>',
                unsafe_allow_html=True
            )
            st.rerun()
