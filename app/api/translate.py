"""Эндпоинты перевода."""

from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.lexicon import LANGS
from app.services.translator import Translation, translate

router = APIRouter()

Language = Literal["en", "ru", "es", "de", "fr"]


class TranslateRequest(BaseModel):
    text: str = Field(min_length=1, max_length=2000)
    source: Language = "en"
    target: Language = "es"


@router.get("/languages")
async def languages() -> dict:
    return {"languages": LANGS}


@router.post("/translate", response_model=Translation)
async def translate_endpoint(request: TranslateRequest) -> Translation:
    try:
        return translate(request.text, request.source, request.target)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
