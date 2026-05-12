# Orquestador de Agentes A2A - Soporte Técnico Nivel 1

Este proyecto implementa una arquitectura de **Orquestador de Agentes** utilizando el patrón **A2A (Agent-to-Agent)** para automatizar la atención al cliente en escenarios de Soporte Técnico de Nivel 1. 

Construido sobre **FastAPI**, **LangChain**, y **Pydantic**, el sistema prioriza la **optimización de costos de inferencia** mediante el enrutamiento inteligente de LLMs y proporciona un marco robusto de **seguridad** contra acciones destructivas (Prompt Injections y escalación).

## 🚀 Arquitectura

El orquestador está compuesto por dos agentes principales:

1. **Agente de Triaje (Cerebro Frontal)**
   - **Modelo:** `gpt-4o-mini` (Bajo costo, respuesta rápida).
   - **Responsabilidad:** Procesamiento de lenguaje natural, clasificación de intenciones y extracción estructurada de entidades (NLU).
   
2. **Agente Ejecutor (Músculo/Especialista)**
   - **Lógica:** Determinista (Llamadas API) + `gpt-4o` (Razonamiento complejo bajo demanda).
   - **Responsabilidad:** Consultar sistemas Legacy. Si el backend responde sin errores (ej. "Entregado"), la respuesta se devuelve mediante código estándar. Si el backend devuelve logs técnicos o trazas XML, el Agente utiliza un LLM grande para sintetizar y explicar el error amigablemente al cliente final.

> **Ahorro de Costos:** Al usar `gpt-4o-mini` para el 100% de la clasificación inicial y reservar `gpt-4o` solo para casos de borde (ej. fallos de la API Legacy), el costo total de inferencia se reduce drásticamente (hasta un 80%).

## 📦 Estructura del Proyecto

```text
├── executor_agent.py    # Lógica del Agente Ejecutor
├── legacy_api.py        # API Legacy simulada (base de datos de órdenes y errores)
├── main.py              # Endpoints principales en FastAPI
├── requirements.txt     # Dependencias de Python
├── schemas.py           # Modelos de Pydantic para el protocolo A2A
├── triage_agent.py      # Lógica del Agente de Triaje
└── tests/
    └── test_security.py # Pruebas de seguridad (Prompt Injection, Tool Scoping)
```

## 🛠️ Requisitos Previos

- Python 3.10 o superior.
- Clave de API de OpenAI (`OPENAI_API_KEY`).

## ⚙️ Instalación y Uso

1. **Clonar el repositorio y configurar el entorno:**
   ```bash
   git clone <tu-repositorio>
   cd Orquestador_Agentico_A2A
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configurar las variables de entorno:**
   Crea un archivo `.env` en la raíz del proyecto y añade tu clave de OpenAI:
   ```env
   OPENAI_API_KEY=tu_clave_api_aqui
   ```

3. **Ejecutar el servidor local:**
   ```bash
   uvicorn main:app --reload
   ```
   La API estará disponible en: [http://localhost:8000/docs](http://localhost:8000/docs) (Interfaz interactiva de Swagger).

## 🧪 Pruebas de Seguridad (Testing Framework)

El proyecto incluye pruebas diseñadas para garantizar que los agentes no tomen acciones indeseadas:

* **Tool Scoping:** Validar que intenciones como `CANCEL_ORDER` sean siempre escaladas a un humano (Human-in-the-Loop).
* **Adversarial Testing:** Pruebas contra Inyección de Prompts para asegurar que el Agente de Triaje no omite sus instrucciones centrales.
* **Strict Mocking:** Se aseguran las llamadas mediante librerías de Mocking para evitar que el Ejecutor realice peticiones no autorizadas a Internet.

Ejecutar las pruebas con:
```bash
pytest tests/
```
