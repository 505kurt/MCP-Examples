import json

from fastapi import APIRouter

router = APIRouter(
    prefix="/counter"
)

COUNTER = 0
    

@router.post("/")
def add_in_counter(number: int) -> dict:
    try:
        with open("api/counter.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {"count": 0}

    data["count"] += number

    with open("api/counter.json", "w") as f:
        json.dump(data, f)

    return {"count": data["count"]}