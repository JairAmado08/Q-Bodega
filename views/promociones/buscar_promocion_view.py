"""
Vista de Búsqueda de Promociones
"""
import streamlit as st
from datetime import datetime
from data_manager import get_promociones, get_inventario
from promociones_crud import buscar_promociones

def mostrar():
    """Muestra la interfaz de búsqueda de promociones"""
    st.markdown("## 🔍 Buscar Promoción")
    
    promociones = get_promociones()
    inventario = get_inventario()
    
    if promociones.empty:
        st.info("📭 No hay promociones registradas. ¡Crea la primera!")
        return
    
    # Formulario de búsqueda
    st.markdown("### 🔎 Filtros de Búsqueda")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        nombre_busqueda = st.text_input(
            "🏷️ Nombre de la promoción",
            placeholder="Buscar por nombre..."
        )
        
        tipo_busqueda = st.selectbox(
            "🎁 Tipo",
            options=["Todos", "2x1", "porcentaje", "monto fijo"]
        )
    
    with col2:
        estado_busqueda = st.selectbox(
            "🔘 Estado",
            options=["Todos", "activa", "inactiva"]
        )
        
        productos_disponibles = ["Todos"] + inventario["ID"].tolist()
        producto_busqueda = st.selectbox(
            "📦 Producto",
            options=productos_disponibles
        )
    
    with col3:
        usar_fechas = st.checkbox("📅 Filtrar por fechas")
        
        if usar_fechas:
            fecha_inicio_busqueda = st.date_input(
                "Desde",
                value=datetime.now()
            )
            fecha_fin_busqueda = st.date_input(
                "Hasta",
                value=datetime.now()
            )
        else:
            fecha_inicio_busqueda = None
            fecha_fin_busqueda = None
    
    # Botón de búsqueda
    if st.button("🔍 Buscar", use_container_width=True, type="primary"):
        # Preparar filtros
        filtros = {}
        
        if nombre_busqueda:
            filtros["nombre"] = nombre_busqueda
        
        if tipo_busqueda != "Todos":
            filtros["tipo"] = tipo_busqueda
        
        if estado_busqueda != "Todos":
            filtros["estado"] = estado_busqueda
        
        if producto_busqueda != "Todos":
            filtros["producto_id"] = producto_busqueda
        
        if usar_fechas and fecha_inicio_busqueda:
            filtros["fecha_inicio"] = fecha_inicio_busqueda.strftime("%Y-%m-%d")
        
        if usar_fechas and fecha_fin_busqueda:
            filtros["fecha_fin"] = fecha_fin_busqueda.strftime("%Y-%m-%d")
        
        # Buscar
        resultados = buscar_promociones(filtros)
        
        # Mostrar resultados
        st.markdown("---")
        st.markdown("### 📊 Resultados de Búsqueda")
        
        if not resultados.empty:
            st.success(f"✅ Se encontraron {len(resultados)} promociones.")
            
            # Mostrar cards
            for _, promo in resultados.iterrows():
                mostrar_card_resultado(promo)
            
            # Vista detallada
            st.markdown("### 📋 Vista Detallada")
            st.dataframe(
                resultados,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Valor": st.column_config.NumberColumn("Valor", format="%.2f"),
                    "Fecha_Inicio": st.column_config.DateColumn("Inicio"),
                    "Fecha_Fin": st.column_config.DateColumn("Fin")
                }
            )
        else:
            st.warning("⚠️ No se encontraron promociones con los criterios especificados.")
    
    # Tips de búsqueda
    st.markdown("---")
    st.markdown("### 💡 Tips de Búsqueda")
    st.info("""
    - **Sin filtros:** Muestra todas las promociones
    - **Por nombre:** Busca coincidencias parciales
    - **Por tipo:** Filtra por tipo de descuento
    - **Por estado:** Encuentra activas o inactivas
    - **Por producto:** Ve todas las promociones de un producto
    - **Por fechas:** Encuentra promociones en un rango específico
    """)

def mostrar_card_resultado(promo):
    """
    Muestra una tarjeta de resultado de búsqueda
    
    Args:
        promo: Serie con datos de la promoción
    """
    # Determinar estilo según estado
    if promo['Estado'] == 'activa':
        card_style = "border-left: 4px solid #28a745; background: #f8fff8;"
        icon = "✅"
    else:
        card_style = "border-left: 4px solid #dc3545; background: #fff5f5;"
        icon = "❌"
    
    # Formatear valor
    if promo['Tipo'] == '2x1':
        valor_texto = "2x1"
    elif promo['Tipo'] == 'porcentaje':
        valor_texto = f"{promo['Valor']}% OFF"
    else:
        valor_texto = f"S/ {promo['Valor']:.2f} OFF"
    
    st.markdown(f"""
    <div class="product-card" style="{card_style}">
        <h4>{icon} {promo['Nombre']} (ID: {promo['ID']})</h4>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
            <div>
                <p><strong>Tipo:</strong> {promo['Tipo']}</p>
                <p><strong>Descuento:</strong> {valor_texto}</p>
                <p><strong>Estado:</strong> {promo['Estado']}</p>
            </div>
            <div>
                <p><strong>Producto:</strong> {promo['Producto_Nombre']}</p>
                <p><strong>Inicio:</strong> {promo['Fecha_Inicio']}</p>
                <p><strong>Fin:</strong> {promo['Fecha_Fin']}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
