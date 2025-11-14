"""
Vista de Login
"""
import streamlit as st
from auth import login_user
from ui_components import mostrar_login_container, mostrar_usuarios_prueba

def mostrar_login():
    """Muestra la pantalla de login"""
    # Centrar el contenido de login
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        mostrar_login_container()
        
        with st.form("login_form"):
            st.markdown("### 🔐 Iniciar Sesión")
            
            username = st.text_input("👤 Usuario", placeholder="nombre.apellido")
            password = st.text_input("🔑 Contraseña", type="password", placeholder="Su contraseña")
            
            col_login1, col_login2 = st.columns(2)
            with col_login1:
                login_button = st.form_submit_button("🚀 Ingresar", use_container_width=True)
            
            if login_button:
                if username and password:
                    if login_user(username, password):
                        st.success("✅ ¡Bienvenido! Accediendo al sistema...")
                        st.rerun()
                    else:
                        st.error("❌ Usuario o contraseña incorrectos.")
                else:
                    st.warning("⚠️ Por favor, complete todos los campos.")
        
        # Información de usuarios de prueba
        mostrar_usuarios_prueba()
