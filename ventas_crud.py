"""
Módulo CRUD para gestión de ventas
"""
import streamlit as st
import pandas as pd
from datetime import datetime
from inventario_crud import actualizar_stock_producto, obtener_producto
from movimientos_crud import registrar_movimiento
from promociones_crud import aplicar_promociones_a_carrito
from utils import generar_id_movimiento

def registrar_venta(venta):
    """
    Registra una nueva venta
    
    Args:
        venta: dict con los datos de la venta
        {
            "id": "V001",
            "fecha": "2025-11-16 15:30",
            "items": [...],
            "total_bruto": 100.00,
            "total_descuento": 10.00,
            "total_final": 90.00,
            "metodo_pago": "efectivo",
            "promociones_aplicadas": ["PR001"]
        }
    
    Returns:
        bool: True si se registró exitosamente
    """
    # Validar stock de todos los productos antes de procesar
    for item in venta["items"]:
        producto = obtener_producto(item["producto_id"])
        if producto is None:
            st.error(f"❌ Producto {item['producto_id']} no existe.")
            return False
        
        if producto["Cantidad"] < item["cantidad"]:
            st.error(
                f"❌ Stock insuficiente para {producto['Nombre']}. "
                f"Stock: {producto['Cantidad']}, Solicitado: {item['cantidad']}"
            )
            return False
    
    # Registrar la venta
    nueva_venta = pd.DataFrame(
        [[
            venta["id"],
            venta["fecha"],
            str(venta["items"]),  # Guardar como string JSON
            venta["total_bruto"],
            venta["total_descuento"],
            venta["total_final"],
            venta["metodo_pago"],
            ",".join(venta["promociones_aplicadas"]) if venta["promociones_aplicadas"] else ""
        ]],
        columns=["ID", "Fecha", "Items", "Total_Bruto", "Total_Descuento", 
                "Total_Final", "Metodo_Pago", "Promociones"]
    )
    
    st.session_state.ventas = pd.concat(
        [st.session_state.ventas, nueva_venta],
        ignore_index=True
    )
    
    # Actualizar inventario y registrar movimientos
    for item in venta["items"]:
        # Restar del inventario
        actualizar_stock_producto(item["producto_id"], -item["cantidad"])
        
        # Registrar movimiento de salida
        id_mov = generar_id_movimiento()
        producto = obtener_producto(item["producto_id"])
        
        registrar_movimiento(
            id_mov,
            "Salida",
            item["producto_id"],
            item["cantidad"],
            f"Venta {venta['id']}"
        )
    
    return True

def obtener_venta_por_id(venta_id):
    """
    Obtiene una venta específica por su ID
    
    Args:
        venta_id: ID de la venta
    
    Returns:
        dict: Datos de la venta o None si no existe
    """
    ventas = st.session_state.ventas
    venta = ventas[ventas["ID"] == venta_id]
    
    if venta.empty:
        return None
    
    return venta.iloc[0].to_dict()

def buscar_ventas(filtros):
    """
    Busca ventas según filtros
    
    Args:
        filtros: dict con criterios de búsqueda
        {
            "fecha_inicio": "2025-11-01",
            "fecha_fin": "2025-11-30",
            "metodo_pago": "efectivo",
            "id": "V001"
        }
    
    Returns:
        DataFrame: Ventas que cumplen los criterios
    """
    ventas = st.session_state.ventas.copy()
    
    if ventas.empty:
        return ventas
    
    # Filtrar por ID
    if filtros.get("id"):
        ventas = ventas[ventas["ID"].str.contains(filtros["id"], case=False, na=False)]
    
    # Filtrar por método de pago
    if filtros.get("metodo_pago") and filtros["metodo_pago"] != "Todos":
        ventas = ventas[ventas["Metodo_Pago"] == filtros["metodo_pago"]]
    
    # Filtrar por rango de fechas
    if filtros.get("fecha_inicio"):
        ventas = ventas[ventas["Fecha"] >= filtros["fecha_inicio"]]
    
    if filtros.get("fecha_fin"):
        ventas = ventas[ventas["Fecha"] <= filtros["fecha_fin"]]
    
    return ventas

def obtener_todas_las_ventas():
    """
    Obtiene todas las ventas registradas
    
    Returns:
        DataFrame: Todas las ventas
    """
    return st.session_state.ventas

def calcular_totales(carrito):
    """
    Calcula los totales del carrito aplicando promociones
    
    Args:
        carrito: list de items del carrito
        [
            {
                "producto_id": "P001",
                "nombre": "Coca Cola",
                "cantidad": 2,
                "precio_unitario": 3.50
            }
        ]
    
    Returns:
        dict: Totales calculados con promociones aplicadas
    """
    if not carrito:
        return {
            "subtotal": 0,
            "descuento": 0,
            "total": 0,
            "promociones": []
        }
    
    # Aplicar promociones usando la función del módulo promociones
    resultado = aplicar_promociones_a_carrito(carrito)
    
    return {
        "subtotal": resultado["subtotal"],
        "descuento": resultado["descuento_total"],
        "total": resultado["total"],
        "promociones": resultado["promociones_aplicadas"]
    }

def obtener_estadisticas_ventas():
    """
    Obtiene estadísticas de ventas
    
    Returns:
        dict: Estadísticas generales
    """
    ventas = st.session_state.ventas
    
    if ventas.empty:
        return {
            "total_ventas": 0,
            "ventas_hoy": 0,
            "ventas_mes": 0,
            "ingresos_totales": 0,
            "ingresos_hoy": 0,
            "ingresos_mes": 0
        }
    
    # Convertir fechas
    ventas["Fecha_dt"] = pd.to_datetime(ventas["Fecha"])
    hoy = datetime.now().date()
    mes_actual = datetime.now().month
    anio_actual = datetime.now().year
    
    # Filtros
    ventas_hoy = ventas[ventas["Fecha_dt"].dt.date == hoy]
    ventas_mes = ventas[
        (ventas["Fecha_dt"].dt.month == mes_actual) &
        (ventas["Fecha_dt"].dt.year == anio_actual)
    ]
    
    return {
        "total_ventas": len(ventas),
        "ventas_hoy": len(ventas_hoy),
        "ventas_mes": len(ventas_mes),
        "ingresos_totales": ventas["Total_Final"].sum(),
        "ingresos_hoy": ventas_hoy["Total_Final"].sum() if not ventas_hoy.empty else 0,
        "ingresos_mes": ventas_mes["Total_Final"].sum() if not ventas_mes.empty else 0
    }

def obtener_productos_mas_vendidos(limite=5):
    """
    Obtiene los productos más vendidos
    
    Args:
        limite: Número de productos a retornar
    
    Returns:
        list: Lista de productos más vendidos
    """
    ventas = st.session_state.ventas
    
    if ventas.empty:
        return []
    
    # Contar productos vendidos
    productos_count = {}
    
    for _, venta in ventas.iterrows():
        items_str = venta["Items"]
        # Parsear items (esto es simplificado, en producción usar json.loads)
        # Por ahora retornamos lista vacía si no hay datos
        pass
    
    return []

def venta_existe(venta_id):
    """
    Verifica si una venta existe
    
    Args:
        venta_id: ID de la venta
    
    Returns:
        bool: True si la venta existe
    """
    return venta_id in st.session_state.ventas["ID"].values
