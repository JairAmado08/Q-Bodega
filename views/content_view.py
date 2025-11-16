"""
Router de contenido principal
Decide qué vista mostrar según la opción seleccionada
"""
from views import inicio_view
from views.inventario import (
    dashboard_view, buscar_view, registrar_view, 
    actualizar_view, eliminar_view, reportes_view
)
from views.movimientos import (
    movimientos_dashboard_view, buscar_movimiento_view,
    registrar_movimiento_view, actualizar_movimiento_view,
    eliminar_movimiento_view
)
from views.promociones import (
    promociones_dashboard_view, registrar_promocion_view,
    buscar_promocion_view, actualizar_promocion_view,
    eliminar_promocion_view
)

def mostrar_contenido(opcion_key):
    """
    Muestra el contenido correspondiente a la opción seleccionada
    
    Args:
        opcion_key: Clave de la opción seleccionada
    """
    # Vista de inicio
    if opcion_key == "inicio":
        inicio_view.mostrar()
    
    # Vistas de inventario
    elif opcion_key == "dashboard":
        dashboard_view.mostrar()
    elif opcion_key == "buscar":
        buscar_view.mostrar()
    elif opcion_key == "registrar":
        registrar_view.mostrar()
    elif opcion_key == "actualizar":
        actualizar_view.mostrar()
    elif opcion_key == "eliminar":
        eliminar_view.mostrar()
    elif opcion_key == "reportes":
        reportes_view.mostrar()
    
    # Vistas de movimientos
    elif opcion_key == "movimientos_dashboard":
        movimientos_dashboard_view.mostrar()
    elif opcion_key == "buscar_movimiento":
        buscar_movimiento_view.mostrar()
    elif opcion_key == "registrar_movimiento":
        registrar_movimiento_view.mostrar()
    elif opcion_key == "actualizar_movimiento":
        actualizar_movimiento_view.mostrar()
    elif opcion_key == "eliminar_movimiento":
        eliminar_movimiento_view.mostrar()
    
    # Vistas de promociones
    elif opcion_key == "promociones_dashboard":
        promociones_dashboard_view.mostrar()
    elif opcion_key == "registrar_promocion":
        registrar_promocion_view.mostrar()
    elif opcion_key == "buscar_promocion":
        buscar_promocion_view.mostrar()
    elif opcion_key == "actualizar_promocion":
        actualizar_promocion_view.mostrar()
    elif opcion_key == "eliminar_promocion":
        eliminar_promocion_view.mostrar()
