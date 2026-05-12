import time
import random

def check_order_status(order_id: str) -> dict:
    \"\"\"
    Simula una llamada a una API Legacy (ej. un SOAP o REST viejo).
    \"\"\"
    time.sleep(0.5) # Simula latencia
    
    # Base de datos simulada
    mock_db = {
        "ORD-123": {
            "status": "DELIVERED",
            "details": "Entregado el 2023-10-01."
        },
        "ORD-404": {
            "status": "NOT_FOUND",
            "details": "El pedido no existe en el sistema."
        },
        "ORD-999": {
            "status": "ERROR",
            "details": "<XML><ErrorCode>ERR-552</ErrorCode><Trace>NullPointerException at com.legacy.fulfillment.Order.getTracker(Order.java:452)</Trace></XML>"
        }
    }
    
    # Comportamiento por defecto para pedidos no mapeados explícitamente
    if order_id not in mock_db:
        # Simulamos un fallo aleatorio 10% del tiempo para forzar uso del LLM
        if random.random() < 0.1:
             return {
                "status": "SYS_ERROR",
                "details": "Connection reset by peer at backend.db.oracle (timeout: 30000ms)"
             }
        return {
            "status": "PROCESSING",
            "details": "El pedido está en el centro de distribución."
        }
        
    return mock_db[order_id]
