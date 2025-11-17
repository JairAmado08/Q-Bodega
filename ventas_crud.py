"""
Módulo CRUD para gestión de ventas
"""
import streamlit as st
import pandas as pd
import json
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
    
    # Registrar la venta - GUARDAR ITEMS COMO JSON
    nueva_venta = pd.DataFrame(
        [[
            venta["id"],
            venta["fecha"],
            json.dumps(venta["items"]),  # Guardar como JSON válido
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

def obtener_items_venta(venta_id):
    """
    Obtiene los items de una venta específica parseados
    
    Args:
        venta_id: ID de la venta
    
    Returns:
        list: Lista de items o lista vacía si hay error
    """
    venta = obtener_venta_por_id(venta_id)
    if not venta:
        return []
    
    try:
        items = json.loads(venta['Items'])
        return items
    except:
        return []

def buscar_ventas(filtros):
    """
    Busca ventas según filtros
    
    Args:
        filtros: dict con criterios de búsqueda
    
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

def venta_existe(venta_id):
    """
    Verifica si una venta existe
    
    Args:
        venta_id: ID de la venta
    
    Returns:
        bool: True si la venta existe
    """
    return venta_id in st.session_state.ventas["ID"].values

def procesar_devolucion(venta_id, items_devolucion, motivo=""):
    """
    Procesa una devolución parcial o total de una venta
    
    Args:
        venta_id: ID de la venta a devolver
        items_devolucion: list de items a devolver
        motivo: Motivo general de la devolución
    
    Returns:
        bool: True si se procesó exitosamente
    """
    # Verificar que la venta existe
    venta = obtener_venta_por_id(venta_id)
    if not venta:
        st.error(f"❌ No existe la venta {venta_id}")
        return False
    
    # Obtener items originales de la venta
    items_venta = obtener_items_venta(venta_id)
    
    # Procesar cada item de devolución
    for item_dev in items_devolucion:
        producto = obtener_producto(item_dev["producto_id"])
        if producto is None:
            st.error(f"❌ Producto {item_dev['producto_id']} no encontrado")
            return False
        
        # Validar que el producto esté en la venta original
        item_encontrado = None
        for item_orig in items_venta:
            if item_orig["producto_id"] == item_dev["producto_id"]:
                item_encontrado = item_orig
                break
        
        if not item_encontrado:
            st.error(f"❌ El producto {producto['Nombre']} no está en esta venta")
            return False
        
        # Validar que la cantidad no exceda lo vendido
        if item_dev["cantidad"] > item_encontrado["cantidad"]:
            st.error(
                f"❌ No puedes devolver {item_dev['cantidad']} unidades de {producto['Nombre']}. "
                f"Solo se vendieron {item_encontrado['cantidad']} unidades."
            )
            return False
        
        # Devolver al inventario (SIN registrar movimiento aquí para evitar duplicación)
        actualizar_stock_producto(item_dev["producto_id"], item_dev["cantidad"])
        
        # Registrar movimiento de devolución (esto ya actualiza el inventario internamente)
        id_mov = generar_id_movimiento()
        # IMPORTANTE: NO llamar a registrar_movimiento porque ya actualizamos el stock arriba
        # Solo registrar en el DataFrame de movimientos SIN tocar el inventario de nuevo
        from datetime import datetime
        producto_info = obtener_producto(item_dev["producto_id"])
        
        nuevo_movimiento = pd.DataFrame(
            [[id_mov, "Devolución", item_dev["producto_id"], producto_info["Nombre"], 
              item_dev["cantidad"], datetime.now().strftime("%Y-%m-%d"), 
              st.session_state.username, 
              f"Devolución de venta {venta_id}. Motivo: {item_dev.get('motivo', motivo)}"]],
            columns=["ID_Movimiento", "Tipo", "Producto_ID", "Producto_Nombre", 
                    "Cantidad", "Fecha", "Usuario", "Observaciones"]
        )
        
        st.session_state.movimientos = pd.concat(
            [st.session_state.movimientos, nuevo_movimiento],
            ignore_index=True
        )
    
    # Registrar en historial de devoluciones
    if "devoluciones" not in st.session_state:
        st.session_state.devoluciones = pd.DataFrame(
            columns=["ID_Devolucion", "ID_Venta", "Fecha", "Items", "Motivo", "Estado"]
        )
    
    id_devolucion = f"DEV{len(st.session_state.devoluciones) + 1:03d}"
    
    nueva_devolucion = pd.DataFrame(
        [[id_devolucion, venta_id, datetime.now().strftime("%Y-%m-%d %H:%M"),
          json.dumps(items_devolucion), motivo, "procesada"]],
        columns=["ID_Devolucion", "ID_Venta", "Fecha", "Items", "Motivo", "Estado"]
    )
    
    st.session_state.devoluciones = pd.concat(
        [st.session_state.devoluciones, nueva_devolucion],
        ignore_index=True
    )
    
    return True

def obtener_devoluciones():
    """
    Obtiene todas las devoluciones registradas
    
    Returns:
        DataFrame: Todas las devoluciones
    """
    if "devoluciones" not in st.session_state:
        st.session_state.devoluciones = pd.DataFrame(
            columns=["ID_Devolucion", "ID_Venta", "Fecha", "Items", "Motivo", "Estado"]
        )
    
    return st.session_state.devoluciones
