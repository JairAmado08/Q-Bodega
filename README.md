# Sistema de Gestión de Bodega (Q'Bodega)
**Proyecto integrador – Grupo**

**INTEGRANTES:**
- Alfaro Salazar, Facundo Ismael
- Amado Diaz, Jair Renato
- Gonzales Pacheco, Felipe Andre
- Manrique Marcelo, Israel Gonzalo


Este proyecto es un prototipo de sistema de gestión de inventario para bodegas pequeñas y tradicionales, cuyo objetivo es digitalizar el control de productos, entradas y salidas, mejorando la eficiencia y la toma de decisiones.

---

## Problemática

Las bodegas han sido pilares de la economía local, ofreciendo cercanía y confianza. 
La gran mayoría de bodegas llevan sus procesos de forma manual, entre esos procesos se encuentra el control de inventario que se realiza manualmente controlando todo en un cuaderno.
Hoy enfrentan una brecha competitiva por el crecimiento de supermercados y minimarkets con gestión digital.  
Esto genera los siguientes problemas:

- Errores frecuentes y registros incompletos.  
- Falta de visibilidad en tiempo real sobre el stock.  
- Desabastecimiento de productos de alta rotación.  
- Sobrestock en otros casos.  
- Dificultad para identificar movimientos específicos.  
- Pérdida de tiempo al buscar información.  

Consecuencia: la toma de decisiones sobre compras y ventas se ve limitada, afectando la eficiencia operativa y la satisfacción del cliente.

---

## Objetivo del sistema

**Ejes Principales de Mejora**

  - Atención al cliente: Brindar un servicio ágil, cordial y personalizado.
  - Abastecimiento eficiente: Mantener un stock adecuado de los productos de mayor rotación.
  - Crecimiento sostenible: Ampliar progresivamente la variedad de productos según las necesidades del vecindario.
  - Digitalización básica: Implementar sistemas simples de gestión de inventario y ventas.
  - Relación comunitaria: Mantener precios competitivos, fomentando la confianza con los clientes.

**Objetivos**

- Accesibilidad: Diseñar un sistema económico y fácil de usar, que pueda ser implementado en bodegas sin la necesidad de grandes recursos tecnológicos
Calidad: Lograr que el software sea una herramienta accesible, sencilla y funcional
- Competitividad: Fortalecer la posición de las bodegas tradicionales frente a su competencia, impulsando su crecimiento y permanencia.
- Eficiencia: Reducir los tiempos y costos en la gestión de inventarios y ventas
Satisfacción del cliente: Lograr que el bodeguero perciba una mejora significativa al momento de realizar sus operaciones diarias.

---

## Actualizaciones del Prototipo

- **v1.0 (Septiembre 08 de 2025)**  
  - Se diseñaron y crearon las funciones para el CRUD del Inventario.
  - Se diseñó el Dashboard.
  - Diseño básico. 

- **v1.5 (Septiembre 13 de 2025)**  
  - Mejoras visuales en la interfaz con CSS.
  - Se añadió el Panel de Control.
  - Correción de errores por código de producto duplicado.
  - Se definieron de manera adecuada los datos.

- **v2.0 (Septiembre 14 de 2025)**  
  - Se añadió logo corporativo en el panel de Control.
  - Se integró módulo de Reportes (top productos, valor de inventario, etc.).
  - Se añadieron Alertas de Stock Bajo.
  - Refinamiento con CSS (logo, estilo de sidebar, tipografía más clara).

- **v2.5 (Septiembre 15 de 2025)**  
  - Se añadió un login y un cierre de sesión.
  - Se añadió el CRUD para los movimientos de inventario.
  - Se añadió un historial de movimientos junto a su respectivo dashboard.

- **v3.0 (Noviembre 14 de 2025)**  
  - Se reorganizó toda la estructura del proyecto para lograr una arquitectura más modular, escalable y mantenible.
  - Se separaron las vistas, componentes UI y operaciones CRUD en módulos independientes para mejorar la claridad del código.
  - Se optimizó el flujo de navegación entre módulos mediante un enrutador interno más ordenado.
  - Se estandarizaron nombres, rutas y archivos para una mejor consistencia en el desarrollo.
  - Se preparó la base del proyecto para futuras integraciones como reportes avanzados, nuevos módulos, etc.
    
 - **v3.5 (Noviembre 15 de 2025)**  
  - Sidebar rediseñado completamente para ofrecer una estética más moderna, con mejor organización visual.
  - Se incorporaron íconos más intuitivos, espaciado optimizado y secciones resaltadas con highlight para mejorar la experiencia de navegación.

--- 
## Estructura del Proyecto

```
qbodega/
│
├── app.py                          # Aplicación principal
│
├── config.py                       # Configuración y constantes
├── styles.py                       # Estilos CSS
│
├── auth.py                         # Módulo de autenticación
├── data_manager.py                 # Gestión e inicialización de datos
│
├── inventario_crud.py              # Operaciones CRUD de inventario
├── movimientos_crud.py             # Operaciones CRUD de movimientos
│
├── ui_components.py                # Componentes UI reutilizables
│
└── views/                          # Vistas de la aplicación
    ├── init.py
    ├── login_view.py               # Vista de login
    ├── sidebar_view.py             # Vista del sidebar
    ├── content_view.py             # Router de contenido
    │
    ├── inventario/                 # Vistas de inventario
    │   ├── init.py
    │   ├── dashboard_view.py       # Dashboard principal
    │   ├── buscar_view.py          # Búsqueda de productos
    │   ├── registrar_view.py       # Registro de productos
    │   ├── actualizar_view.py      # Actualización de productos
    │   ├── eliminar_view.py        # Eliminación de productos
    │   └── reportes_view.py        # Reportes y análisis
    │
    └── movimientos/                # Vistas de movimientos
        ├── __init__.py
        ├── movimientos_dashboard_view.py   # Dashboard principal
        ├── buscar_movimiento_view.py       # Búsqueda de movimientos
        ├── registrar_movimiento_view.py    # Registro de movimientos
        ├── actualizar_movimiento_view.py   # Actualización de movimientos
        └── eliminar_movimiento_view.py     # Eliminación de movimientos

```
