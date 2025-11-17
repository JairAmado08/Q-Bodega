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

def inicializar_promociones():
    """Inicializa el DataFrame de promociones con datos de ejemplo"""
    if "promociones" not in st.session_state:
        st.session_state.promociones = pd.DataFrame(
            columns=["ID", "Nombre", "Tipo", "Valor", "Producto_ID", "Producto_Nombre",
                    "Fecha_Inicio", "Fecha_Fin", "Estado"]
        )
        
        # Datos de ejemplo de promociones
        promociones_ejemplo = [
            ["PR001", "2x1 en Gaseosas", "2x1", 0, "P001", "Inca Kola 1.5L", 
             "2025-11-01", "2025-11-30", "activa"],
            ["PR002", "20% OFF en Lácteos", "porcentaje", 20, "P003", "Leche Gloria tarro", 
             "2025-11-10", "2025-11-25", "activa"],
            ["PR003", "Descuento S/2 en Pan", "monto fijo", 0.20, "P004", "Pan francés (unidad)", 
             "2025-11-15", "2025-11-20", "activa"],
            ["PR004", "Combo Arroz", "porcentaje", 15, "P002", "Arroz Costeño 1kg", 
             "2025-10-01", "2025-10-31", "inactiva"]
        ]
        
        for promocion in promociones_ejemplo:
            nueva_promo = pd.DataFrame(
                [promocion], 
                columns=["ID", "Nombre", "Tipo", "Valor", "Producto_ID", "Producto_Nombre",
                        "Fecha_Inicio", "Fecha_Fin", "Estado"]
            )
            st.session_state.promociones = pd.concat(
                [st.session_state.promociones, nueva_promo], 
                ignore_index=True
            )

def inicializar_ventas():
    """Inicializa el DataFrame de ventas con datos de ejemplo"""
    if "ventas" not in st.session_state:
        st.session_state.ventas = pd.DataFrame(
            columns=["ID", "Fecha", "Items", "Total_Bruto", "Total_Descuento",
                    "Total_Final", "Metodo_Pago", "Promociones"]
        )
        
        # Datos de ejemplo de ventas
        ventas_ejemplo = [
            ["V001", "2025-11-16 10:30", "[{'producto_id':'P001','cantidad':2}]", 
             13.00, 6.50, 6.50, "efectivo", "PR001"],
            ["V002", "2025-11-16 14:15", "[{'producto_id':'P003','cantidad':1}]", 
             4.80, 0.96, 3.84, "tarjeta", "PR002"],
        ]
        
        for venta in ventas_ejemplo:
            nueva_venta = pd.DataFrame(
                [venta],
                columns=["ID", "Fecha", "Items", "Total_Bruto", "Total_Descuento",
                        "Total_Final", "Metodo_Pago", "Promociones"]
            )
            st.session_state.ventas = pd.concat(
                [st.session_state.ventas, nueva_venta],
                ignore_index=True
            )

def get_inventario():
    """Retorna el DataFrame de inventario"""
    return st.session_state.inventario

def get_movimientos():
    """Retorna el DataFrame de movimientos"""
    return st.session_state.movimientos

def get_promociones():
    """Retorna el DataFrame de promociones"""
    return st.session_state.promociones

def actualizar_inventario(df):
    """Actualiza el DataFrame de inventario"""
    st.session_state.inventario = df

def actualizar_movimientos(df):
    """Actualiza el DataFrame de movimientos"""
    st.session_state.movimientos = df

def actualizar_promociones(df):
    """Actualiza el DataFrame de promociones"""
    st.session_state.promociones = df
