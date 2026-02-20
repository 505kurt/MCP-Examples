from typing import List

from fastapi import FastAPI

from api.routes.timestamp import router as timestamp_router
from api.routes.counter import router as counter_router

app = FastAPI()


@app.get("/")
def root() -> List[dict]:
    return [
        {
            "type": "function",
            "function": {
                "name": "timestamp",
                "description": "Consulta o horário atual do sistema.",
                "parameters": {
                    "type": "object",
                    "required": [],
                    "properties": {
                    },
                    "additionalProperties": False
                },
                "url": "http://localhost:8000/timestamp",
                "method": "GET"
            }
        },
        {
            "type": "function",
            "function": {
                "name": "counter",
                "description": "Soma um valor ao contador e retorna o valor atual do contador.",
                "parameters": {
                    "type": "object",
                    "required": ["number"],
                    "properties": {
                        "number": {
                            "type": "number",
                            "description": "Valor a ser somado."
                        }
                    },
                    "additionalProperties": False
                },
                "url": "http://localhost:8000/counter",
                "method": "POST"
            }
        },
        
    ]


app.include_router(timestamp_router)
app.include_router(counter_router)
