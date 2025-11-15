"""
Vista del Sidebar con separadores de sección
"""
import streamlit as st
from auth import logout_user
from ui_components import mostrar_user_info, mostrar_logo
from inventario_crud import obtener_estadisticas
from promociones_crud import obtener_estadisticas_promociones


# ============================================
#  ESTILO PERSONALIZADO PARA HIGHLIGHT
# ============================================
def button_style():
    st.markdown("""
        <style>
            .menu-btn {
                background-color: transparent;
                border: 1px solid rgba(120,120,120,0.25);
                padding: 6px 10px;
                border-radius: 8px;
                width: 100%;
                text-align: left;
                font-size: 15px;
                margin-top: 4px;
            }
            .menu-btn:hover {
                background-color: rgba(200,200,200,0.15);
            }
            .menu-btn-selected {
                background-color: #4A90E2 !important;
                color: white !important;
                border-color: #4A90E2 !important;
            }
        </style>
    """, unsafe_allow_html=True)


# ============================================
#  FUNCIÓN PARA CREAR BOTONES CON HIGHLIGHT
# ============================================
def menu_button(label, key_value):
    activo = (st.session_state.menu_principal == key_value)

    css_class = "menu-btn-selected" if activo else "menu-btn"

    clicked = st.button(
        label,
        key=f"btn_{key_value}",
        use_container_width=True
    )

    # Aplicar estilo visual
    st.markdown(f"""
        <script>
            var btn = window.parent.document.querySelector('button[key="btn_{key_value}"]');
            if (btn) {{
                btn.classList.add('{css_class}');
            }}
        </script>
    """, unsafe_allow_html=True)

    # Lógica del botón
    if clicked:
        st.session_state.menu_principal = key_value



# ============================================
#  SIDEBAR PRINCIPAL
# ============================================
def mostrar_sidebar(display_name):

    button_style()  # Aplicar CSS

    with st.sidebar:

        mostrar_user_info(display_name)

        if st.button("🚪 Cerrar Sesión", use_container_width=True):
            logout_user()

        mostrar_logo()

        st.markdown("## 🛠️ Panel de Control")

        # --- Métricas ---
        total_prod, total_cant, valor_total, bajo_stock = obtener_estadisticas()
        stats_promo = obtener_estadisticas_promociones()

        st.markdown("### 📊 Inventario")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("📦 Prod.", total_prod)
            st.metric("💰 Valor", f"S/{valor_total:,.2f}")
        with col2:
            st.metric("📈 Cant.", total_cant)
            st.metric("⚠️ Bajo Stock", bajo_stock)

        st.markdown("### 🎉 Promociones")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("🎁 Total", stats_promo["total"])
        with col2:
            st.metric("🔥 Vigentes", stats_promo["vigentes"])

        st.markdown("---")
        st.markdown("### 🧭 Navegación")

        # Estado inicial
        if "menu_principal" not in st.session_state:
            st.session_state.menu_principal = "promociones_dashboard"

        # --------------------------------
        # Inventario
        # --------------------------------
        with st.expander("📦 Inventario", expanded=False):
            menu_button("📋 Dashboard", "dashboard")
            menu_button("🔎 Buscar Producto", "buscar")
            menu_button("➕ Registrar Producto", "registrar")
            menu_button("✏️ Actualizar Producto", "actualizar")
            menu_button("🗑️ Eliminar Producto", "eliminar")
            menu_button("📊 Reportes", "reportes")

        # --------------------------------
        # Movimientos
        # --------------------------------
        with st.expander("🔄 Movimientos", expanded=False):
            menu_button("📦 Dashboard", "movimientos_dashboard")
            menu_button("🔍 Buscar Movimiento", "buscar_movimiento")
            menu_button("➕ Registrar Movimiento", "registrar_movimiento")
            menu_button("✏️ Actualizar Movimiento", "actualizar_movimiento")
            menu_button("🗑️ Eliminar Movimiento", "eliminar_movimiento")

        # --------------------------------
        # Promociones
        # --------------------------------
        with st.expander("🎉 Promociones", expanded=True):
            menu_button("🎁 Dashboard", "promociones_dashboard")
            menu_button("➕ Registrar Promoción", "registrar_promocion")
            menu_button("🔍 Buscar Promoción", "buscar_promocion")
            menu_button("✏️ Actualizar Promoción", "actualizar_promocion")
            menu_button("🗑️ Eliminar Promoción", "eliminar_promocion")

    return st.session_state.menu_principal
