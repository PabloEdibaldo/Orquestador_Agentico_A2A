from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from schemas import UserRequest, ExecutionResult
from triage_agent import run_triage
from executor_agent import execute_task
import uvicorn
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Orquestador de Agentes - Soporte Nivel 1",
    description="Implementación del patrón A2A para automatización de soporte técnico.",
    version="1.0.0"
)

class SupportResponse(BaseModel):
    trace_id: str
    response_message: str
    status: str

@app.post("/api/v1/support", response_model=SupportResponse)
async def handle_support_request(request: UserRequest):
    try:
        # 1. Agente de Triaje (Cost optimization: GPT-4o-mini)
        a2a_message = run_triage(request)
        
        # 2. Agente Ejecutor (Cost optimization: Deterministic + GPT-4o fallback)
        execution_result = execute_task(a2a_message)
        
        return SupportResponse(
            trace_id=a2a_message.trace_id,
            response_message=execution_result.user_message,
            status=execution_result.status
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
