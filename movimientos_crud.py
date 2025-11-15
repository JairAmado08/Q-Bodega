"""
Módulo CRUD para gestión de movimientos de inventario
"""
import streamlit as st
import pandas as pd
from datetime import datetime
from inventario_crud import actualizar_stock_producto, obtener_producto

def registrar_movimiento(id_mov, tipo, producto_id, cantidad, observaciones=""):
    """
    Registra un nuevo movimiento de inventario
    
    Args:
        id_mov: ID único del movimiento
        tipo: Tipo de movimiento (Entrada, Salida, Ajuste, Devolución)
        producto_id: ID del producto
        cantidad: Cantidad del movimiento
        observaciones: Observaciones adicionales
    
    Returns:
        bool: True si el movimiento se registró exitosamente
    """
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    
    # Obtener información del producto
    producto_info = obtener_producto(producto_id)
    
    if producto_info is None:
        st.error("❌ Producto no encontrado.")
        return False
    
    producto_nombre = producto_info["Nombre"]
    stock_actual = int(producto_info["Cantidad"])
    
    # Validar stock suficiente para salidas
    if tipo == "Salida" and cantidad > stock_actual:
        st.error(
            f"❌ No hay suficiente stock. Stock actual: {stock_actual}, "
            f"intentaste sacar: {cantidad}."
        )
        return False
    
    # Crear movimiento
    nuevo_movimiento = pd.DataFrame(
        [[id_mov, tipo, producto_id, producto_nombre, cantidad, fecha_actual, 
          st.session_state.username, observaciones]],
        columns=["ID_Movimiento", "Tipo", "Producto_ID", "Producto_Nombre", 
                "Cantidad", "Fecha", "Usuario", "Observaciones"]
    )
    
    st.session_state.movimientos = pd.concat(
        [st.session_state.movimientos, nuevo_movimiento], 
        ignore_index=True
    )
    
    # Actualizar inventario según el tipo de movimiento
    if tipo in ["Entrada", "Devolución"]:
        actualizar_stock_producto(producto_id, cantidad)
    elif tipo in ["Salida", "Ajuste"] and cantidad < 0:
        actualizar_stock_producto(producto_id, cantidad)
    elif tipo == "Salida":
        actualizar_stock_producto(producto_id, -cantidad)
    
    return True

def eliminar_movimiento(id_movimiento):
    """
    Elimina un movimiento (sin revertir cambios de stock)
    
    Args:
        id_movimiento: ID del movimiento a eliminar
    """
    st.session_state.movimientos = st.session_state.movimientos[
        st.session_state.movimientos["ID_Movimiento"] != id_movimiento
    ]

def actualizar_movimiento(id_mov, tipo, producto_id, cantidad, fecha, observaciones):
    """
    Actualiza los datos de un movimiento
    
    Args:
        id_mov: ID del movimiento
        tipo: Nuevo tipo de movimiento
        producto_id: Nuevo ID de producto
        cantidad: Nueva cantidad
        fecha: Nueva fecha
        observaciones: Nuevas observaciones
    """
    idx = st.session_state.movimientos[
        st.session_state.movimientos["ID_Movimiento"] == id_mov
    ].index
    
    if not idx.empty:
        # Obtener nombre del producto
        producto_info = obtener_producto(producto_id)
        producto_nombre = producto_info["Nombre"] if producto_info is not None else "Producto no encontrado"
        
        st.session_state.movimientos.loc[
            idx[0], 
            ["Tipo", "Producto_ID", "Producto_Nombre", "Cantidad", "Fecha", "Observaciones"]
        ] = [tipo, producto_id, producto_nombre, cantidad, fecha, observaciones]

def obtener_estadisticas_movimientos():
    """
    Obtiene estadísticas de movimientos
    
    Returns:
        tuple: (total_movimientos, entradas, salidas, ajustes)
    """
    movimientos = st.session_state.movimientos
    
    if movimientos.empty:
        return 0, 0, 0, 0
    
    total_movimientos = len(movimientos)
    entradas = len(movimientos[movimientos["Tipo"] == "Entrada"])
    salidas = len(movimientos[movimientos["Tipo"] == "Salida"])
    ajustes = len(movimientos[movimientos["Tipo"].isin(["Ajuste", "Devolución"])])
    
    return total_movimientos, entradas, salidas, ajustes

def movimiento_existe(id_movimiento):
    """
    Verifica si un movimiento existe
    
    Args:
        id_movimiento: ID del movimiento
    
    Returns:
        bool: True si el movimiento existe
    """
    return id_movimiento in st.session_state.movimientos["ID_Movimiento"].values
