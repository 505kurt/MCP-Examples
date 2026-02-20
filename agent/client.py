import os
from typing import List, Optional

import requests
from dotenv import load_dotenv

from mcp_handler import mcp_handler

load_dotenv()

CF_ACCOUNT_ID = os.getenv("CF_ACCOUNT_ID")
CF_API_TOKEN = os.getenv("CF_API_TOKEN")

URL = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/ai/run/@cf/meta/llama-3.3-70b-instruct-fp8-fast"
headers = {
    "Authorization": f"Bearer {CF_API_TOKEN}",
    "Content-Type": "application/json"
}

TOOLS = requests.get("http://localhost:8000/")
TOOLS = TOOLS.json()

CONVERSATION_HISTORY = []


def llm_client(tools: List[dict] = TOOLS, prompt: Optional[str] = None, tool_response: Optional[List] = None):
    system_prompt = (
        "Você é um agente MCP.\n"
        "Responda sempre em português brasileiro.\n"
        "Nunca mostre diretamente para o usuário o json com parametros da ferramenta.\n"
        "Se detectar a intenção de usar uma ferramenta apenas use-a, sem responder nada ao usuário."
    )
    final_prompt = system_prompt

    final_prompt += prompt if prompt else final_prompt
    final_prompt += "\nRESPOSTA DA FERRAMENTA (JÁ CHAMADA): " + str(tool_response) if tool_response else final_prompt
    final_prompt += f"\nContexto (responda somente o ultimo contexto em memória, mas se baseando em toda a cadeia de contexto.): {CONVERSATION_HISTORY}" if len(CONVERSATION_HISTORY) > 0 else final_prompt

    payload = {
        "prompt": final_prompt,
        "tools": tools,
        "temperature": 0.15,
        "max_tokens": 512
    }

    response = requests.post(url=URL, headers=headers, json=payload)
    result = response.json()

    output = result.get("result", {}).get("response")
    if output is not None:
        CONVERSATION_HISTORY.append({
            "role": "assistant",
            "context": output,
        })
        return output

    tool_calls = result.get("result", {}).get("tool_calls")
    if tool_calls:
        return llm_client(tool_response=mcp_handler(tools=TOOLS, tool_calls=tool_calls))

print(llm_client(prompt="Faça uma saudação ao usuário e explique seu funcionamento."))
while True:
    prompt = input("\nUser: ")
    print("\n")
    CONVERSATION_HISTORY.append({
            "role": "user",
            "context": prompt
        })
    print("\nAssistant: " + llm_client(prompt=prompt) + "\n")