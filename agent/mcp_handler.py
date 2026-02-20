from typing import List

import requests
from urllib.parse import quote_plus

def mcp_handler(tools: List[dict], tool_calls:List[dict]):
    responses = []
    for call in tool_calls:
        args = list(call["arguments"].keys())
        params = "?"
        for item in args:
            params += "&" + item + "=" + quote_plus(call["arguments"][item])

        for tool in tools:
            if tool["function"]["name"] == call["name"]:
                response = requests.request(
                    url=f"{tool["function"]["url"] + params}",
                    method=f"{tool["function"]["method"]}"
                )
                responses.append(response.json())

    return responses
