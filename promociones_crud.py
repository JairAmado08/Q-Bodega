"""
Módulo CRUD para gestión de promociones
"""
import streamlit as st
import pandas as pd
from datetime import datetime
from inventario_crud import obtener_producto

def crear_promocion(datos_promocion):
    """
    Crea una nueva promoción
    
    Args:
        datos_promocion: dict con los campos de la promoción
            {
                "id": "PR001",
                "nombre": "2x1 en Gaseosas",
                "tipo": "2x1 | porcentaje | monto fijo",
                "valor": 50,
                "producto_id": "P001",
                "fecha_inicio": "2025-11-15",
                "fecha_fin": "2025-11-30",
                "estado": "activa | inactiva"
            }
    
    Returns:
        bool: True si se creó exitosamente
    """
    # Validar que el producto existe
    producto = obtener_producto(datos_promocion["producto_id"])
    if producto is None:
        st.error(f"❌ El producto {datos_promocion['producto_id']} no existe.")
        return False
    
    # Validar fechas
    try:
        fecha_inicio = datetime.strptime(datos_promocion["fecha_inicio"], "%Y-%m-%d")
        fecha_fin = datetime.strptime(datos_promocion["fecha_fin"], "%Y-%m-%d")
        
        if fecha_fin < fecha_inicio:
            st.error("❌ La fecha de fin debe ser posterior a la fecha de inicio.")
            return False
    except ValueError:
        st.error("❌ Formato de fecha inválido. Use YYYY-MM-DD")
        return False
    
    # Validar valor según tipo
    if datos_promocion["tipo"] == "porcentaje" and (datos_promocion["valor"] < 0 or datos_promocion["valor"] > 100):
        st.error("❌ El porcentaje debe estar entre 0 y 100.")
        return False
    
    # Crear el registro
    nueva_promocion = pd.DataFrame(
        [[
            datos_promocion["id"],
            datos_promocion["nombre"],
            datos_promocion["tipo"],
            datos_promocion["valor"],
            datos_promocion["producto_id"],
            producto["Nombre"],  # Nombre del producto
            datos_promocion["fecha_inicio"],
            datos_promocion["fecha_fin"],
            datos_promocion["estado"]
        ]],
        columns=["ID", "Nombre", "Tipo", "Valor", "Producto_ID", "Producto_Nombre",
                "Fecha_Inicio", "Fecha_Fin", "Estado"]
    )
    
    st.session_state.promociones = pd.concat(
        [st.session_state.promociones, nueva_promocion],
        ignore_index=True
    )
    
    return True

def obtener_promocion_por_id(promocion_id):
    """
    Obtiene una promoción específica por su ID
    
    Args:
        promocion_id: ID de la promoción
    
    Returns:
        Series: Datos de la promoción o None si no existe
    """
    promociones = st.session_state.promociones
    promocion = promociones[promociones["ID"] == promocion_id]
    
    return promocion.iloc[0] if not promocion.empty else None

def buscar_promociones(filtros):
    """
    Busca promociones según filtros
    
    Args:
        filtros: dict con criterios de búsqueda
            {
                "nombre": str (opcional),
                "tipo": str (opcional),
                "estado": str (opcional),
                "fecha_inicio": str (opcional),
                "fecha_fin": str (opcional),
                "producto_id": str (opcional)
            }
    
    Returns:
        DataFrame: Promociones que cumplen los criterios
    """
    promociones = st.session_state.promociones.copy()
    
    if promociones.empty:
        return promociones
    
    # Filtrar por nombre
    if filtros.get("nombre"):
        promociones = promociones[
            promociones["Nombre"].str.contains(filtros["nombre"], case=False, na=False)
        ]
    
    # Filtrar por tipo
    if filtros.get("tipo") and filtros["tipo"] != "Todos":
        promociones = promociones[promociones["Tipo"] == filtros["tipo"]]
    
    # Filtrar por estado
    if filtros.get("estado") and filtros["estado"] != "Todos":
        promociones = promociones[promociones["Estado"] == filtros["estado"]]
    
    # Filtrar por producto
    if filtros.get("producto_id") and filtros["producto_id"] != "Todos":
        promociones = promociones[promociones["Producto_ID"] == filtros["producto_id"]]
    
    # Filtrar por rango de fechas
    if filtros.get("fecha_inicio"):
        promociones = promociones[promociones["Fecha_Inicio"] >= filtros["fecha_inicio"]]
    
    if filtros.get("fecha_fin"):
        promociones = promociones[promociones["Fecha_Fin"] <= filtros["fecha_fin"]]
    
    return promociones

def actualizar_promocion(promocion_id, nuevos_datos):
    """
    Actualiza los datos de una promoción
    
    Args:
        promocion_id: ID de la promoción a actualizar
        nuevos_datos: dict con los nuevos valores
    
    Returns:
        bool: True si se actualizó exitosamente
    """
    idx = st.session_state.promociones[
        st.session_state.promociones["ID"] == promocion_id
    ].index
    
    if idx.empty:
        st.error(f"❌ No existe promoción con ID {promocion_id}")
        return False
    
    # Validar producto si cambió
    if "producto_id" in nuevos_datos:
        producto = obtener_producto(nuevos_datos["producto_id"])
        if producto is None:
            st.error(f"❌ El producto {nuevos_datos['producto_id']} no existe.")
            return False
        nuevos_datos["producto_nombre"] = producto["Nombre"]
    
    # Validar fechas si cambiaron
    if "fecha_inicio" in nuevos_datos and "fecha_fin" in nuevos_datos:
        try:
            fecha_inicio = datetime.strptime(nuevos_datos["fecha_inicio"], "%Y-%m-%d")
            fecha_fin = datetime.strptime(nuevos_datos["fecha_fin"], "%Y-%m-%d")
            
            if fecha_fin < fecha_inicio:
                st.error("❌ La fecha de fin debe ser posterior a la fecha de inicio.")
                return False
        except ValueError:
            st.error("❌ Formato de fecha inválido.")
            return False
    
    # Validar valor si cambió
    if "tipo" in nuevos_datos and "valor" in nuevos_datos:
        if nuevos_datos["tipo"] == "porcentaje" and (nuevos_datos["valor"] < 0 or nuevos_datos["valor"] > 100):
            st.error("❌ El porcentaje debe estar entre 0 y 100.")
            return False
    
    # Actualizar campos
    for campo, valor in nuevos_datos.items():
        columna_map = {
            "nombre": "Nombre",
            "tipo": "Tipo",
            "valor": "Valor",
            "producto_id": "Producto_ID",
            "producto_nombre": "Producto_Nombre",
            "fecha_inicio": "Fecha_Inicio",
            "fecha_fin": "Fecha_Fin",
            "estado": "Estado"
        }
        
        if campo in columna_map:
            st.session_state.promociones.loc[idx[0], columna_map[campo]] = valor
    
    return True

def eliminar_promocion(promocion_id):
    """
    Elimina una promoción
    
    Args:
        promocion_id: ID de la promoción a eliminar
    
    Returns:
        bool: True si se eliminó exitosamente
    """
    if not promocion_existe(promocion_id):
        st.error(f"❌ No existe promoción con ID {promocion_id}")
        return False
    
    st.session_state.promociones = st.session_state.promociones[
        st.session_state.promociones["ID"] != promocion_id
    ]
    
    return True

def obtener_promociones_activas():
    """
    Obtiene todas las promociones activas vigentes
    
    Returns:
        DataFrame: Promociones activas en el rango de fechas actual
    """
    promociones = st.session_state.promociones
    
    if promociones.empty:
        return promociones
    
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    
    # Filtrar por estado activo y fechas vigentes
    promociones_activas = promociones[
        (promociones["Estado"] == "activa") &
        (promociones["Fecha_Inicio"] <= fecha_actual) &
        (promociones["Fecha_Fin"] >= fecha_actual)
    ]
    
    return promociones_activas

def aplicar_promociones_a_carrito(carrito):
    """
    Aplica promociones a un carrito de compras
    
    Args:
        carrito: list de dicts con productos del carrito
            [
                {
                    "producto_id": "P001",
                    "nombre": "Inca Kola 1.5L",
                    "cantidad": 2,
                    "precio_unitario": 6.50
                },
                ...
            ]
    
    Returns:
        dict: Información del carrito con descuentos aplicados
            {
                "subtotal": 100.00,
                "descuento_total": 15.00,
                "total": 85.00,
                "promociones_aplicadas": [
                    {
                        "nombre": "2x1 en Gaseosas",
                        "descuento": 15.00
                    }
                ],
                "items": [...]  # Carrito con descuentos aplicados
            }
    """
    if not carrito:
        return {
            "subtotal": 0,
            "descuento_total": 0,
            "total": 0,
            "promociones_aplicadas": [],
            "items": []
        }
    
    promociones_activas = obtener_promociones_activas()
    
    subtotal = sum(item["cantidad"] * item["precio_unitario"] for item in carrito)
    descuento_total = 0
    promociones_aplicadas = []
    
    # Aplicar promociones
    for _, promocion in promociones_activas.iterrows():
        for item in carrito:
            if item["producto_id"] == promocion["Producto_ID"]:
                descuento_item = 0
                
                # Aplicar según tipo de promoción
                if promocion["Tipo"] == "2x1":
                    # Por cada 2 unidades, descuenta 1
                    pares = item["cantidad"] // 2
                    descuento_item = pares * item["precio_unitario"]
                
                elif promocion["Tipo"] == "porcentaje":
                    # Descuento porcentual sobre el subtotal del item
                    subtotal_item = item["cantidad"] * item["precio_unitario"]
                    descuento_item = subtotal_item * (promocion["Valor"] / 100)
                
                elif promocion["Tipo"] == "monto fijo":
                    # Descuento fijo por unidad
                    descuento_item = min(
                        promocion["Valor"] * item["cantidad"],
                        item["cantidad"] * item["precio_unitario"]
                    )
                
                if descuento_item > 0:
                    descuento_total += descuento_item
                    promociones_aplicadas.append({
                        "nombre": promocion["Nombre"],
                        "producto": item["nombre"],
                        "descuento": descuento_item
                    })
    
    total = max(0, subtotal - descuento_total)
    
    return {
        "subtotal": round(subtotal, 2),
        "descuento_total": round(descuento_total, 2),
        "total": round(total, 2),
        "promociones_aplicadas": promociones_aplicadas,
        "items": carrito
    }

def obtener_estadisticas_promociones():
    """
    Obtiene estadísticas de promociones
    
    Returns:
        dict: Estadísticas generales
    """
    promociones = st.session_state.promociones
    
    if promociones.empty:
        return {
            "total": 0,
            "activas": 0,
            "inactivas": 0,
            "vigentes": 0
        }
    
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    
    total = len(promociones)
    activas = len(promociones[promociones["Estado"] == "activa"])
    inactivas = len(promociones[promociones["Estado"] == "inactiva"])
    
    vigentes = len(promociones[
        (promociones["Estado"] == "activa") &
        (promociones["Fecha_Inicio"] <= fecha_actual) &
        (promociones["Fecha_Fin"] >= fecha_actual)
    ])
    
    return {
        "total": total,
        "activas": activas,
        "inactivas": inactivas,
        "vigentes": vigentes
    }

def promocion_existe(promocion_id):
    """
    Verifica si una promoción existe
    
    Args:
        promocion_id: ID de la promoción
    
    Returns:
        bool: True si la promoción existe
    """
    return promocion_id in st.session_state.promociones["ID"].values
