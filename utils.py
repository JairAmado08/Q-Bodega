"""
Módulo de utilidades para el sistema Q'Bodega
"""
import streamlit as st

def generar_id_producto():
    """
    Genera un ID único para un nuevo producto
    Formato: P001, P002, P003, etc.
    
    Returns:
        str: ID del producto generado
    """
    inventario = st.session_state.inventario
    
    if inventario.empty:
        return "P001"
    
    # Obtener todos los IDs actuales que empiecen con P
    ids_productos = inventario[inventario["ID"].str.startswith("P", na=False)]["ID"].tolist()
    
    if not ids_productos:
        return "P001"
    
    # Extraer números de los IDs
    numeros = []
    for id_prod in ids_productos:
        try:
            # Extraer el número después de 'P'
            numero = int(id_prod[1:])
            numeros.append(numero)
        except (ValueError, IndexError):
            continue
    
    # Obtener el siguiente número
    if numeros:
        siguiente_numero = max(numeros) + 1
    else:
        siguiente_numero = 1
    
    # Formatear con ceros a la izquierda (3 dígitos)
    return f"P{siguiente_numero:03d}"

def generar_id_movimiento():
    """
    Genera un ID único para un nuevo movimiento
    Formato: M001, M002, M003, etc.
    
    Returns:
        str: ID del movimiento generado
    """
    movimientos = st.session_state.movimientos
    
    if movimientos.empty:
        return "M001"
    
    # Obtener todos los IDs actuales que empiecen con M
    ids_movimientos = movimientos[movimientos["ID_Movimiento"].str.startswith("M", na=False)]["ID_Movimiento"].tolist()
    
    if not ids_movimientos:
        return "M001"
    
    # Extraer números de los IDs
    numeros = []
    for id_mov in ids_movimientos:
        try:
            # Extraer el número después de 'M'
            numero = int(id_mov[1:])
            numeros.append(numero)
        except (ValueError, IndexError):
            continue
    
    # Obtener el siguiente número
    if numeros:
        siguiente_numero = max(numeros) + 1
    else:
        siguiente_numero = 1
    
    # Formatear con ceros a la izquierda (3 dígitos)
    return f"M{siguiente_numero:03d}"

def generar_id_promocion():
    """
    Genera un ID único para una nueva promoción
    Formato: PR001, PR002, PR003, etc.
    
    Returns:
        str: ID de la promoción generado
    """
    promociones = st.session_state.promociones
    
    if promociones.empty:
        return "PR001"
    
    # Obtener todos los IDs actuales que empiecen con PR
    ids_promociones = promociones[promociones["ID"].str.startswith("PR", na=False)]["ID"].tolist()
    
    if not ids_promociones:
        return "PR001"
    
    # Extraer números de los IDs
    numeros = []
    for id_promo in ids_promociones:
        try:
            # Extraer el número después de 'PR'
            numero = int(id_promo[2:])
            numeros.append(numero)
        except (ValueError, IndexError):
            continue
    
    # Obtener el siguiente número
    if numeros:
        siguiente_numero = max(numeros) + 1
    else:
        siguiente_numero = 1
    
    # Formatear con ceros a la izquierda (3 dígitos)
    return f"PR{siguiente_numero:03d}"

def generar_id_venta():
    """
    Genera un ID único para una nueva venta
    Formato: V001, V002, V003, etc.
    
    Returns:
        str: ID de la venta generado
    """
    ventas = st.session_state.ventas
    
    if ventas.empty:
        return "V001"
    
    # Obtener todos los IDs actuales que empiecen con V
    ids_ventas = ventas[ventas["ID"].str.startswith("V", na=False)]["ID"].tolist()
    
    if not ids_ventas:
        return "V001"
    
    # Extraer números de los IDs
    numeros = []
    for id_venta in ids_ventas:
        try:
            # Extraer el número después de 'V'
            numero = int(id_venta[1:])
            numeros.append(numero)
        except (ValueError, IndexError):
            continue
    
    # Obtener el siguiente número
    if numeros:
        siguiente_numero = max(numeros) + 1
    else:
        siguiente_numero = 1
    
    # Formatear con ceros a la izquierda (3 dígitos)
    return f"V{siguiente_numero:03d}"

def validar_id_unico(id_valor, tipo="producto"):
    """
    Valida si un ID es único en el sistema
    
    Args:
        id_valor: ID a validar
        tipo: Tipo de entidad ('producto', 'movimiento', 'promocion')
    
    Returns:
        bool: True si el ID es único, False si ya existe
    """
    if tipo == "producto":
        return id_valor not in st.session_state.inventario["ID"].values
    elif tipo == "movimiento":
        return id_valor not in st.session_state.movimientos["ID_Movimiento"].values
    elif tipo == "promocion":
        return id_valor not in st.session_state.promociones["ID"].values
    
    return False
