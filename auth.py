"""
Módulo de autenticación y gestión de sesiones
"""
import streamlit as st
from config import EMPLEADOS_AUTORIZADOS, NOMBRES_DISPLAY

def inicializar_sesion():
    """Inicializa las variables de sesión para autenticación"""
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = ""

def login_user(username, password):
    """
    Autenticar usuario
    
    Args:
        username: nombre de usuario
        password: contraseña
    
    Returns:
        bool: True si autenticación exitosa, False en caso contrario
    """
    if username in EMPLEADOS_AUTORIZADOS and EMPLEADOS_AUTORIZADOS[username] == password:
        st.session_state.logged_in = True
        st.session_state.username = username
        return True
    return False

def logout_user():
    """Cerrar sesión del usuario actual"""
    st.session_state.logged_in = False
    st.session_state.username = ""
    # Resetear el menú al inicio
    st.session_state.menu_principal = "inicio"
    st.rerun()

def get_display_name(username):
    """
    Obtener nombre para mostrar del usuario
    
    Args:
        username: nombre de usuario
    
    Returns:
        str: nombre formateado para mostrar
    """
    return NOMBRES_DISPLAY.get(username, username.replace(".", " ").title())

def is_logged_in():
    """
    Verificar si hay un usuario autenticado
    
    Returns:
        bool: True si hay sesión activa
    """
    return st.session_state.get("logged_in", False)

def get_current_user():
    """
    Obtener el usuario actual
    
    Returns:
        str: username del usuario actual o None
    """
    return st.session_state.get("username", None) if is_logged_in() else None
