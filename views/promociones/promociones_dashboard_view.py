"""
Vista del Dashboard de Promociones
"""
import streamlit as st
from data_manager import get_promociones
from promociones_crud import obtener_estadisticas_promociones, obtener_promociones_activas
from datetime import datetime

def mostrar():
    """Muestra el dashboard de promociones"""
    st.markdown("## 🎉 Dashboard de Promociones")
    
    # Estadísticas
    stats = obtener_estadisticas_promociones()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="stats-container">
            <h3>🎁</h3>
            <h2>{stats['total']}</h2>
            <p>Total Promociones</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stats-container" style="background: linear-gradient(135deg, #28a745 0%, #20c997 100%);">
            <h3>✅</h3>
            <h2>{stats['vigentes']}</h2>
            <p>Vigentes Hoy</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stats-container" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
            <h3>🟢</h3>
            <h2>{stats['activas']}</h2>
            <p>Activas</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stats-container" style="background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);">
            <h3>🔴</h3>
            <h2>{stats['inactivas']}</h2>
            <p>Inactivas</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Promociones vigentes
    promociones_vigentes = obtener_promociones_activas()
    
    if not promociones_vigentes.empty:
        st.markdown("### 🔥 Promociones Vigentes")
        
        for _, promo in promociones_vigentes.iterrows():
            mostrar_card_promocion(promo, vigente=True)
    else:
        st.info("💡 No hay promociones vigentes en este momento.")
    
    st.markdown("---")
    
    # Todas las promociones
    promociones = get_promociones()
    
    if not promociones.empty:
        # Filtros
        col1, col2, col3 = st.columns(3)
        
        with col1:
            tipos = ['Todos'] + sorted(promociones['Tipo'].unique().tolist())
            tipo_filtro = st.selectbox("🏷️ Filtrar por tipo:", tipos)
        
        with col2:
            estados = ['Todos', 'activa', 'inactiva']
            estado_filtro = st.selectbox("📊 Filtrar por estado:", estados)
        
        with col3:
            productos = ['Todos'] + sorted(promociones['Producto_ID'].unique().tolist())
            producto_filtro = st.selectbox("📦 Filtrar por producto:", productos)
        
        # Aplicar filtros
        df_filtrado = promociones.copy()
        
        if tipo_filtro != 'Todos':
            df_filtrado = df_filtrado[df_filtrado['Tipo'] == tipo_filtro]
        
        if estado_filtro != 'Todos':
            df_filtrado = df_filtrado[df_filtrado['Estado'] == estado_filtro]
        
        if producto_filtro != 'Todos':
            df_filtrado = df_filtrado[df_filtrado['Producto_ID'] == producto_filtro]
        
        # Mostrar promociones
        st.markdown("### 🎁 Todas las Promociones")
        
        if not df_filtrado.empty:
            for _, promo in df_filtrado.iterrows():
                mostrar_card_promocion(promo, vigente=False)
            
            # Vista detallada
            st.markdown("### 📋 Vista Detallada")
            st.dataframe(
                df_filtrado,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Valor": st.column_config.NumberColumn("Valor", format="%.2f"),
                    "Fecha_Inicio": st.column_config.DateColumn("Inicio"),
                    "Fecha_Fin": st.column_config.DateColumn("Fin")
                }
            )
        else:
            st.info("🔍 No se encontraron promociones con los filtros aplicados.")
    else:
        st.info("📭 No hay promociones registradas. ¡Crea la primera!")

def mostrar_card_promocion(promo, vigente=False):
    """
    Muestra una tarjeta con información de la promoción
    
    Args:
        promo: Serie con datos de la promoción
        vigente: bool indicando si es una promoción vigente
    """
    # Determinar estilo según estado y vigencia
    if vigente:
        card_style = "border-left: 4px solid #28a745; background: #f8fff8;"
        icon = "🔥"
    elif promo['Estado'] == 'activa':
        card_style = "border-left: 4px solid #667eea; background: #f8f9ff;"
        icon = "✅"
    else:
        card_style = "border-left: 4px solid #dc3545; background: #fff5f5;"
        icon = "❌"
    
    # Formatear valor según tipo
    if promo['Tipo'] == '2x1':
        valor_texto = "2x1"
    elif promo['Tipo'] == 'porcentaje':
        valor_texto = f"{promo['Valor']}% OFF"
    else:  # monto fijo
        valor_texto = f"S/ {promo['Valor']:.2f} OFF"
    
    # Verificar si está por vencer (menos de 3 días)
    fecha_fin = datetime.strptime(promo['Fecha_Fin'], "%Y-%m-%d")
    dias_restantes = (fecha_fin - date.now()).days
    
    alerta_vencimiento = ""
    if vigente and dias_restantes <= 3:
        alerta_vencimiento = f'<p style="color: #dc3545; font-weight: bold;">⏰ ¡Vence en {dias_restantes} días!</p>'
    
    st.markdown(f"""
    <div class="product-card" style="{card_style}">
        <h4>{icon} {promo['Nombre']} (ID: {promo['ID']})</h4>
        <p><strong>Tipo:</strong> {promo['Tipo']}</p>
        <p><strong>Descuento:</strong> {valor_texto}</p>
        <p><strong>Producto:</strong> {promo['Producto_Nombre']} ({promo['Producto_ID']})</p>
        <p><strong>Vigencia:</strong> {promo['Fecha_Inicio']} hasta {promo['Fecha_Fin']}</p>
        <p><strong>Estado:</strong> <span style="color: {'#28a745' if promo['Estado'] == 'activa' else '#dc3545'}; font-weight: bold;">{promo['Estado'].upper()}</span></p>
        {alerta_vencimiento}
    </div>
    """, unsafe_allow_html=True)
