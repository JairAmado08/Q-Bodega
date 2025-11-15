"""
Módulo CRUD para gestión de inventario
"""
import streamlit as st
import pandas as pd
from datetime import datetime
from config import STOCK_BAJO

def registrar_producto(id_, nombre, categoria, cantidad, precio):
    """
    Registra un nuevo producto en el inventario
    
    Args:
        id_: ID único del producto
        nombre: Nombre del producto
        categoria: Categoría del producto
        cantidad: Cantidad inicial en stock
        precio: Precio unitario
    """
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    nuevo = pd.DataFrame(
        [[id_, nombre, categoria, cantidad, precio, fecha_actual]], 
        columns=["ID", "Nombre", "Categoría", "Cantidad", "Precio", "Fecha_Agregado"]
    )
    st.session_state.inventario = pd.concat(
        [st.session_state.inventario, nuevo], 
        ignore_index=True
    )

def eliminar_producto(id_):
    """
    Elimina un producto del inventario
    
    Args:
        id_: ID del producto a eliminar
    """
    st.session_state.inventario = st.session_state.inventario[
        st.session_state.inventario["ID"] != id_
    ]

def actualizar_producto(id_, nombre, categoria, cantidad, precio):
    """
    Actualiza la información de un producto existente
    
    Args:
        id_: ID del producto a actualizar
        nombre: Nuevo nombre
        categoria: Nueva categoría
        cantidad: Nueva cantidad
        precio: Nuevo precio
    """
    idx = st.session_state.inventario[st.session_state.inventario["ID"] == id_].index
    if not idx.empty:
        st.session_state.inventario.loc[
            idx[0], 
            ["Nombre", "Categoría", "Cantidad", "Precio"]
        ] = [nombre, categoria, cantidad, precio]

def actualizar_stock_producto(producto_id, cantidad_cambio):
    """
    Actualiza el stock de un producto
    
    Args:
        producto_id: ID del producto
        cantidad_cambio: Cantidad a agregar o quitar (puede ser negativa)
    """
    idx = st.session_state.inventario[
        st.session_state.inventario["ID"] == producto_id
    ].index
    
    if not idx.empty:
        nueva_cantidad = max(
            0, 
            st.session_state.inventario.loc[idx[0], "Cantidad"] + cantidad_cambio
        )
        st.session_state.inventario.loc[idx[0], "Cantidad"] = nueva_cantidad

def obtener_estadisticas_movimientos():
    """
    Obtiene estadísticas generales del inventario
    
    Returns:
        tuple: (total_productos, total_cantidad, valor_total, productos_bajo_stock)
    """
    inventario = st.session_state.inventario
    
    if inventario.empty:
        return 0, 0, 0, 0
    
    total_productos = len(inventario)
    total_cantidad = inventario["Cantidad"].sum()
    valor_total = (inventario["Cantidad"] * inventario["Precio"]).sum()
    productos_bajo_stock = len(inventario[inventario["Cantidad"] < STOCK_BAJO])
    
    return total_productos, total_cantidad, valor_total, productos_bajo_stock

def obtener_producto(producto_id):
    """
    Obtiene la información de un producto específico
    
    Args:
        producto_id: ID del producto
    
    Returns:
        Series: Información del producto o None si no existe
    """
    inventario = st.session_state.inventario
    producto = inventario[inventario["ID"] == producto_id]
    
    return producto.iloc[0] if not producto.empty else None

def producto_existe(producto_id):
    """
    Verifica si un producto existe en el inventario
    
    Args:
        producto_id: ID del producto
    
    Returns:
        bool: True si el producto existe
    """
    return producto_id in st.session_state.inventario["ID"].values
