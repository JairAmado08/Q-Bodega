"""
Módulo CRUD para gestión de ventas
"""

import streamlit as st
import pandas as pd
import ast
from datetime import datetime

from inventario_crud import actualizar_stock_producto, obtener_producto
from movimientos_crud import registrar_movimiento
from promociones_crud import aplicar_promociones_a_carrito
from utils import generar_id_movimiento


# ------------------------------------------------------------------------------------
# REGISTRAR VENTA
# ------------------------------------------------------------------------------------
def registrar_venta(venta):
    """
    Registra una nueva venta en el sistema.

    Args:
        venta (dict): Contiene todos los datos de la venta:
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
    """

    # Validación de stock antes de procesar
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

    # Crear DataFrame para la venta
    nueva_venta = pd.DataFrame(
        [[
            venta["id"],
            venta["fecha"],
            str(venta["items"]),  # Se guarda como string (tu formato actual)
            venta["total_bruto"],
            venta["total_descuento"],
            venta["total_final"],
            venta["metodo_pago"],
            ",".join(venta["promociones_aplicadas"]) if venta["promociones_aplicadas"] else ""
        ]],
        columns=[
            "ID", "Fecha", "Items", "Total_Bruto",
            "Total_Descuento", "Total_Final",
            "Metodo_Pago", "Promociones"
        ]
    )

    st.session_state.ventas = pd.concat(
        [st.session_state.ventas, nueva_venta],
        ignore_index=True
    )

    # Actualizar inventario y registrar movimientos
    for item in venta["items"]:
        actualizar_stock_producto(item["producto_id"], -item["cantidad"])

        # Registrar movimiento tipo Salida
        registrar_movimiento(
            generar_id_movimiento(),
            "Salida",
            item["producto_id"],
            item["cantidad"],
            f"Venta {venta['id']}"
        )

    return True


# ------------------------------------------------------------------------------------
# OBTENER VENTA POR ID
# ------------------------------------------------------------------------------------
def obtener_venta_por_id(venta_id):
    ventas = st.session_state.ventas
    venta = ventas[ventas["ID"] == venta_id]

    if venta.empty:
        return None

    return venta.iloc[0].to_dict()


# ------------------------------------------------------------------------------------
# OBTENER ITEMS DE UNA VENTA — NECESARIO PARA DEVOLUCIONES
# ------------------------------------------------------------------------------------
def obtener_items_venta(venta_id):
    """
    Retorna la lista de items de la venta.

    Usa el formato EXACTO en el que tú ya guardas los items:
    str([{'producto_id':..., 'nombre':..., 'cantidad':..., 'precio_unitario':...}])
    """

    venta = obtener_venta_por_id(venta_id)
    if not venta:
        return []

    items_str = venta["Items"]

    try:
        items = ast.literal_eval(items_str)
        if isinstance(items, list):
            return items
    except:
        st.error("❌ Error al interpretar los items de la venta.")
        return []

    return []


# ------------------------------------------------------------------------------------
# BUSCAR VENTAS
# ------------------------------------------------------------------------------------
def buscar_ventas(filtros):
    ventas = st.session_state.ventas.copy()

    if ventas.empty:
        return ventas

    if filtros.get("id"):
        ventas = ventas[ventas["ID"].str.contains(filtros["id"], case=False, na=False)]

    if filtros.get("metodo_pago") and filtros["metodo_pago"] != "Todos":
        ventas = ventas[ventas["Metodo_Pago"] == filtros["metodo_pago"]]

    if filtros.get("fecha_inicio"):
        ventas = ventas[ventas["Fecha"] >= filtros["fecha_inicio"]]

    if filtros.get("fecha_fin"):
        ventas = ventas[ventas["Fecha"] <= filtros["fecha_fin"]]

    return ventas


# ------------------------------------------------------------------------------------
# OBTENER TODAS LAS VENTAS
# ------------------------------------------------------------------------------------
def obtener_todas_las_ventas():
    return st.session_state.ventas


# ------------------------------------------------------------------------------------
# CALCULAR TOTALES (usa promociones)
# ------------------------------------------------------------------------------------
def calcular_totales(carrito):
    if not carrito:
        return {
            "subtotal": 0,
            "descuento": 0,
            "total": 0,
            "promociones": []
        }

    resultado = aplicar_promociones_a_carrito(carrito)

    return {
        "subtotal": resultado["subtotal"],
        "descuento": resultado["descuento_total"],
        "total": resultado["total"],
        "promociones": resultado["promociones_aplicadas"]
    }


# ------------------------------------------------------------------------------------
# EXISTE VENTA
# ------------------------------------------------------------------------------------
def venta_existe(venta_id):
    return venta_id in st.session_state.ventas["ID"].values


# ------------------------------------------------------------------------------------
# PROCESAR DEVOLUCIÓN
# ------------------------------------------------------------------------------------
def procesar_devolucion(venta_id, items_devolucion, motivo=""):
    venta = obtener_venta_por_id(venta_id)
    if not venta:
        st.error(f"❌ No existe la venta {venta_id}")
        return False

    # Registrar movimientos de tipo Devolución
    for item in items_devolucion:
        if obtener_producto(item["producto_id"]) is None:
            st.error(f"❌ Producto {item['producto_id']} no encontrado")
            continue

        registrar_movimiento(
            generar_id_movimiento(),
            "Devolución",
            item["producto_id"],
            item["cantidad"],
            f"Devolución de venta {venta_id}. Motivo: {item.get('motivo', motivo)}"
        )

    # Crear historial de devoluciones si no existe
    if "devoluciones" not in st.session_state:
        st.session_state.devoluciones = pd.DataFrame(
            columns=["ID_Devolucion", "ID_Venta", "Fecha", "Items", "Motivo", "Estado"]
        )

    id_devolucion = f"DEV{len(st.session_state.devoluciones) + 1:03d}"

    nueva_devolucion = pd.DataFrame(
        [[
            id_devolucion,
            venta_id,
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            str(items_devolucion),
            motivo,
            "procesada"
        ]],
        columns=["ID_Devolucion", "ID_Venta", "Fecha", "Items", "Motivo", "Estado"]
    )

    st.session_state.devoluciones = pd.concat(
        [st.session_state.devoluciones, nueva_devolucion],
        ignore_index=True
    )

    return True


# ------------------------------------------------------------------------------------
# OBTENER DEVOLUCIONES
# ------------------------------------------------------------------------------------
def obtener_devoluciones():
    if "devoluciones" not in st.session_state:
        st.session_state.devoluciones = pd.DataFrame(
            columns=["ID_Devolucion", "ID_Venta", "Fecha", "Items", "Motivo", "Estado"]
        )

    return st.session_state.devoluciones
