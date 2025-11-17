import sys
print("Python path:", sys.path)

try:
    print("\n1. Importando views.ventas...")
    from views import ventas
    print("✅ views.ventas OK")
    
    print("\n2. Importando ventas_dashboard_view...")
    from views.ventas import ventas_dashboard_view
    print("✅ ventas_dashboard_view OK")
    
    print("\n3. Verificando función mostrar()...")
    print(f"   Tiene función mostrar: {hasattr(ventas_dashboard_view, 'mostrar')}")
    
    print("\n4. Importando registrar_venta_view...")
    from views.ventas import registrar_venta_view
    print("✅ registrar_venta_view OK")
    
    print("\n5. Importando buscar_venta_view...")
    from views.ventas import buscar_venta_view
    print("✅ buscar_venta_view OK")
    
    print("\n6. Importando detalle_venta_view...")
    from views.ventas import detalle_venta_view
    print("✅ detalle_venta_view OK")
    
    print("\n🎉 ¡TODO ESTÁ BIEN!")
    
except ImportError as e:
    print(f"\n❌ ERROR DE IMPORTACIÓN: {e}")
    import traceback
    traceback.print_exc()
    
except Exception as e:
    print(f"\n❌ ERROR GENERAL: {e}")
    import traceback
    traceback.print_exc()
