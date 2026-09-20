"""Перевод: фразы жадно, затем пословно. Без сети."""

from __future__ import annotations

import re

from pydantic import BaseModel

from app.services.lexicon import LANGS, PHRASES, lookup

_WORD_RE = re.compile(r"[\w']+|[^\w\s]", re.UNICODE)


class Translation(BaseModel):
    translation: str
    coverage: float
    unknown: list[str]


def _restore_case(original: str, translated: str) -> str:
    if original.isupper():
        return translated.upper()
    if original[:1].isupper():
        return translated[:1].upper() + translated[1:]
    return translated


def translate(text: str, source: str, target: str) -> Translation:
    """Перевести текст. Детерминировано."""
    if not text or not text.strip():
        raise ValueError("text must not be empty")
    source, target = source.strip().lower(), target.strip().lower()
    if source not in LANGS:
        raise ValueError(f"unsupported source language: {source!r}")
    if target not in LANGS:
        raise ValueError(f"unsupported target language: {target!r}")
    if source == target:
        return Translation(translation=text.strip(), coverage=1.0, unknown=[])

    tokens = _WORD_RE.findall(text)
    phrases = PHRASES.get(source, {})
    out: list[str] = []
    unknown: list[str] = []
    translated_words = 0
    total_words = 0
    index = 0
    while index < len(tokens):
        token = tokens[index]
        if not re.fullmatch(r"[\w']+", token, re.UNICODE):
            out.append(token)
            index += 1
            continue
        total_words += 1
        matched = False
        for size in (3, 2):
            window = tokens[index : index + size]
            if len(window) < size or any(not re.fullmatch(r"[\w']+", part, re.UNICODE) for part in window):
                continue
            phrase = " ".join(window).lower()
            translation = phrases.get(phrase, {}).get(target)
            if translation is not None:
                out.append(_restore_case(window[0], translation))
                total_words += size - 1
                translated_words += size
                index += size
                matched = True
                break
        if matched:
            continue
        single = lookup(token, source, target)
        if single is None:
            out.append(f"[?{token}]")
            unknown.append(token)
        else:
            out.append(_restore_case(token, single))
            translated_words += 1
        index += 1
    # Простая склейка: пробел перед словами, кроме начала и после открывающих скобок.
    glued: list[str] = []
    for part in out:
        is_word = re.fullmatch(r"[\w']+|\[", part, re.UNICODE) is not None or part.startswith("[?")
        if glued and is_word and glued[-1] not in ("(", "«", "¿", "¡"):
            glued.append(" ")
        glued.append(part)
    coverage = round(translated_words / total_words, 2) if total_words else 1.0
    return Translation(translation="".join(glued).strip(), coverage=coverage, unknown=sorted(set(unknown)))
