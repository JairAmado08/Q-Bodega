"""
Módulo de gestión de datos e inicialización
"""
import streamlit as st
import pandas as pd

def inicializar_inventario():
    """Inicializa el DataFrame de inventario con datos de ejemplo"""
    if "inventario" not in st.session_state:
        st.session_state.inventario = pd.DataFrame(
            columns=["ID", "Nombre", "Categoría", "Cantidad", "Precio", "Fecha_Agregado"]
        )
        
        # Datos de ejemplo
        ejemplos = [
            ["P001", "Inca Kola 1.5L", "Bebidas", 15, 6.50, "2024-01-15"],
            ["P002", "Arroz Costeño 1kg", "Abarrotes secos", 25, 5.00, "2024-01-16"],
            ["P003", "Leche Gloria tarro", "Lácteos y derivados", 18, 4.80, "2024-01-17"],
            ["P004", "Pan francés (unidad)", "Panadería y repostería", 50, 0.40, "2024-01-18"],
            ["P005", "Atún Florida 170g", "Enlatados y conservas", 2, 6.00, "2024-01-19"]
        ]
        
        for ejemplo in ejemplos:
            nuevo = pd.DataFrame(
                [ejemplo], 
                columns=["ID", "Nombre", "Categoría", "Cantidad", "Precio", "Fecha_Agregado"]
            )
            st.session_state.inventario = pd.concat(
                [st.session_state.inventario, nuevo], 
                ignore_index=True
            )

def inicializar_movimientos():
    """Inicializa el DataFrame de movimientos con datos de ejemplo"""
    if "movimientos" not in st.session_state:
        st.session_state.movimientos = pd.DataFrame(
            columns=["ID_Movimiento", "Tipo", "Producto_ID", "Producto_Nombre", 
                    "Cantidad", "Fecha", "Usuario", "Observaciones"]
        )
        
        # Datos de ejemplo de movimientos
        movimientos_ejemplo = [
            ["M001", "Entrada", "P001", "Inca Kola 1.5L", 20, "2024-01-15", "admin", "Compra inicial"],
            ["M002", "Salida", "P001", "Inca Kola 1.5L", 5, "2024-01-16", "carlos.rodriguez", "Venta"],
            ["M003", "Entrada", "P002", "Arroz Costeño 1kg", 30, "2024-01-16", "maria.gonzalez", "Reposición"],
            ["M004", "Salida", "P002", "Arroz Costeño 1kg", 5, "2024-01-17", "jose.martinez", "Venta"],
            ["M005", "Ajuste", "P005", "Atún Florida 170g", -3, "2024-01-19", "admin", "Producto vencido"]
        ]
        
        for movimiento in movimientos_ejemplo:
            nuevo_mov = pd.DataFrame(
                [movimiento], 
                columns=["ID_Movimiento", "Tipo", "Producto_ID", "Producto_Nombre", 
                        "Cantidad", "Fecha", "Usuario", "Observaciones"]
            )
            st.session_state.movimientos = pd.concat(
                [st.session_state.movimientos, nuevo_mov], 
                ignore_index=True
            )

def get_inventario():
    """Retorna el DataFrame de inventario"""
    return st.session_state.inventario

def get_movimientos():
    """Retorna el DataFrame de movimientos"""
    return st.session_state.movimientos

def actualizar_inventario(df):
    """Actualiza el DataFrame de inventario"""
    st.session_state.inventario = df

def actualizar_movimientos(df):
    """Actualiza el DataFrame de movimientos"""
    st.session_state.movimientos = df
