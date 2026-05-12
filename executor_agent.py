import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from schemas import A2AMessage, ExecutionResult
from legacy_api import check_order_status

def execute_task(message: A2AMessage) -> ExecutionResult:
    \"\"\"
    Agente Ejecutor que consume el protocolo A2A y decide si usar o no un LLM grande
    basado en la respuesta de los sistemas back-end (cost optimization).
    \"\"\"
    if message.intent == "CHECK_ORDER_STATUS":
        order_id = message.entities.order_id
        if not order_id:
            return ExecutionResult(
                status="FAILURE",
                user_message="No pude identificar el ID del pedido en tu solicitud. ¿Podrías proporcionarlo?"
            )
            
        # Llama a la API simulada (costo 0$)
        api_response = check_order_status(order_id)
        
        status = api_response.get("status")
        details = api_response.get("details", "")
        
        # Lógica de enrutamiento y optimización de costos
        if status in ["DELIVERED", "PROCESSING", "NOT_FOUND"]:
            # Casos simples: No se requiere LLM grande. Devolvemos respuesta directa.
            friendly_message = f"El estado de tu pedido {order_id} es: {status}. Detalles: {details}"
            if status == "NOT_FOUND":
                friendly_message = f"Lo siento, no encontré ningún pedido con el ID {order_id}."
                
            return ExecutionResult(
                status="SUCCESS",
                user_message=friendly_message,
                technical_details=api_response
            )
        else:
            # Caso complejo (ej. ERROR con XML stacktrace)
            # Aquí usamos el Modelo Grande (gpt-4o) para razonamiento complejo
            try:
                llm = ChatOpenAI(model="gpt-4o", temperature=0.2)
                prompt = ChatPromptTemplate.from_messages([
                    ("system", \"\"\"Eres un técnico de soporte Nivel 2. 
Se ha producido un error técnico al consultar el pedido del usuario. 
Analiza los siguientes detalles técnicos (pueden ser XML, JSON o StackTraces) y redacta un mensaje muy amable, 
sencillo y sin jerga técnica para el usuario final, explicándole que estamos experimentando problemas y que 
su caso ha sido escalado. No le muestres el error técnico crudo.\"\"\"),
                    ("human", "Detalles técnicos del error: {error_details}")
                ])
                
                chain = prompt | llm
                ai_message = chain.invoke({"error_details": details})
                
                return ExecutionResult(
                    status="ESCALATED",
                    user_message=ai_message.content,
                    technical_details=api_response
                )
            except Exception as e:
                # Fallback
                return ExecutionResult(
                    status="ESCALATED",
                    user_message="Actualmente estamos experimentando problemas técnicos para consultar tu pedido. Ha sido escalado a soporte avanzado.",
                    technical_details={"error": str(e), "original_backend_error": api_response}
                )
                
    elif message.intent == "CANCEL_ORDER":
        # Implementación de seguridad: No se permiten acciones destructivas automáticas
        return ExecutionResult(
            status="ESCALATED",
            user_message="Por razones de seguridad, las cancelaciones deben ser procesadas por un agente humano. He transferido tu solicitud."
        )
    else:
        return ExecutionResult(
            status="FAILURE",
            user_message="No pude entender completamente tu solicitud o no tengo los permisos para ejecutarla."
        )
