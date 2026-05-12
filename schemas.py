from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class UserRequest(BaseModel):
    user_id: str = Field(..., description="ID del usuario")
    message: str = Field(..., description="Mensaje original del usuario")

class Entities(BaseModel):
    order_id: Optional[str] = Field(None, description="ID del pedido (ej. ORD-123, 123456)")
    rfc: Optional[str] = Field(None, description="RFC del usuario si aplica")
    error_reported: Optional[str] = Field(None, description="Descripción del error si el usuario reporta alguno")

class TriageOutput(BaseModel):
    intent: str = Field(..., description="Intención clasificada: CHECK_ORDER_STATUS, CANCEL_ORDER, UNKNOWN, etc.")
    entities: Entities
    classification_confidence: float = Field(..., description="Nivel de confianza de la clasificación de 0.0 a 1.0")

class A2AMessage(BaseModel):
    trace_id: str
    source_agent: str
    target_agent: str
    intent: str
    entities: Entities
    metadata: Dict[str, Any]

class ExecutionResult(BaseModel):
    status: str = Field(..., description="Estado de la ejecución (SUCCESS, FAILURE, ESCALATED)")
    user_message: str = Field(..., description="Mensaje amigable para el usuario final")
    technical_details: Optional[Dict[str, Any]] = Field(None, description="Detalles técnicos para debugging interno")
