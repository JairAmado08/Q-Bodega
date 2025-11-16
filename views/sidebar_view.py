"""
Vista del Sidebar con separadores de sección y highlight funcional
"""
import streamlit as st
from auth import logout_user
from ui_components import mostrar_user_info, mostrar_logo
from inventario_crud import obtener_estadisticas
from promociones_crud import obtener_estadisticas_promociones


def mostrar_sidebar(display_name):
    """
    Muestra el sidebar con información del usuario y navegación con highlight
    
    Args:
        display_name: Nombre del usuario para mostrar
    
    Returns:
        str: Clave de la opción seleccionada
    """
    
    # Inicializar estado del menú
    if "menu_principal" not in st.session_state:
        st.session_state.menu_principal = "inicio"  # Cambiado a "inicio"
    
    with st.sidebar:
        # Información del usuario logueado
        mostrar_user_info(display_name)
        
        # Botón de cerrar sesión
        if st.button("🚪 Cerrar Sesión", use_container_width=True):
            logout_user()
        
        # Logo
        mostrar_logo()
        
        # Encabezado principal
        st.markdown("## 🛠️ Panel de Control")
        
        # ----------------------------
        # Métricas
        # ----------------------------
        total_prod, total_cant, valor_total, bajo_stock = obtener_estadisticas()
        stats_promo = obtener_estadisticas_promociones()
        
        st.markdown("### 📊 Inventario")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("📦 Prod.", total_prod)
            st.metric("💰 Valor", f"S/{valor_total:,.2f}")
        with col2:
            st.metric("📈 Cant.", total_cant)
            st.metric("⚠️ Bajo Stock", bajo_stock, delta_color="inverse")
        
        st.markdown("### 🎉 Promociones")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("🎁 Total", stats_promo["total"])
        with col2:
            st.metric("🔥 Vigentes", stats_promo["vigentes"])
        
        st.markdown("---")
        st.markdown("### 🧭 Navegación")
        
        # CSS personalizado para los botones del menú
        st.markdown("""
            <style>
                /* Estilo para botones normales */
                div[data-testid="stSidebar"] button[kind="secondary"] {
                    background-color: transparent;
                    border: 1px solid rgba(120,120,120,0.25);
                    padding: 8px 12px;
                    border-radius: 8px;
                    width: 100%;
                    text-align: left;
                    font-size: 14px;
                    margin-top: 4px;
                    color: inherit;
                    transition: all 0.2s ease;
                }
                
                /* Hover en botones */
                div[data-testid="stSidebar"] button[kind="secondary"]:hover {
                    background-color: rgba(151, 166, 195, 0.15);
                    border-color: rgba(151, 166, 195, 0.5);
                }
                
                /* Estilo para botón primario (seleccionado) */
                div[data-testid="stSidebar"] button[kind="primary"] {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    border: none;
                    padding: 8px 12px;
                    border-radius: 8px;
                    font-weight: 600;
                    box-shadow: 0 2px 4px rgba(102, 126, 234, 0.3);
                }
                
                /* Expanders con estilo mejorado */
                div[data-testid="stSidebar"] .streamlit-expanderHeader {
                    background-color: rgba(151, 166, 195, 0.1);
                    border-radius: 8px;
                    font-weight: 600;
                    padding: 8px;
                }
            </style>
        """, unsafe_allow_html=True)
        
        # --------------------------------
        # Función helper para crear botones del menú
        # --------------------------------
        def crear_boton_menu(label, key_value):
            """Crea un botón de menú con highlight si está activo"""
            es_activo = (st.session_state.menu_principal == key_value)
            
            # Usar type="primary" para el botón activo
            if st.button(
                label, 
                key=f"btn_{key_value}",
                use_container_width=True,
                type="primary" if es_activo else "secondary"
            ):
                st.session_state.menu_principal = key_value
                st.rerun()
        
        # --------------------------------
        # Inventario
        # --------------------------------
        with st.expander("📦 **Inventario**", expanded=False):
            crear_boton_menu("📋 Dashboard", "dashboard")
            crear_boton_menu("🔎 Buscar Producto", "buscar")
            crear_boton_menu("➕ Registrar Producto", "registrar")
            crear_boton_menu("✏️ Actualizar Producto", "actualizar")
            crear_boton_menu("🗑️ Eliminar Producto", "eliminar")
            crear_boton_menu("📊 Reportes", "reportes")
        
        # --------------------------------
        # Movimientos
        # --------------------------------
        with st.expander("🔄 **Movimientos**", expanded=False):
            crear_boton_menu("📦 Dashboard", "movimientos_dashboard")
            crear_boton_menu("🔍 Buscar Movimiento", "buscar_movimiento")
            crear_boton_menu("➕ Registrar Movimiento", "registrar_movimiento")
            crear_boton_menu("✏️ Actualizar Movimiento", "actualizar_movimiento")
            crear_boton_menu("🗑️ Eliminar Movimiento", "eliminar_movimiento")
        
        # --------------------------------
        # Promociones
        # --------------------------------
        with st.expander("🎉 **Promociones**", expanded=True):
            crear_boton_menu("🎁 Dashboard", "promociones_dashboard")
            crear_boton_menu("➕ Registrar Promoción", "registrar_promocion")
            crear_boton_menu("🔍 Buscar Promoción", "buscar_promocion")
            crear_boton_menu("✏️ Actualizar Promoción", "actualizar_promocion")
            crear_boton_menu("🗑️ Eliminar Promoción", "eliminar_promocion")
    
    return st.session_state.menu_principal
