from datetime import datetime

from fastapi import APIRouter

router = APIRouter(
    prefix="/timestamp"
)


@router.get("/")
def get_timestamp():
    return {"time" : f"{datetime.now()}"}