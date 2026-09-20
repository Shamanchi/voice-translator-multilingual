"""Unit-тесты переводчика: без сети, детерминированы."""

import pytest

from app.services.lexicon import LANGS
from app.services.translator import translate


def test_phrase_and_word() -> None:
    result = translate("hello, thank you", "en", "es")
    assert result.translation == "hola, gracias"
    assert result.coverage == 1.0
    assert result.unknown == []


def test_single_word_ru() -> None:
    result = translate("hello", "en", "ru")
    assert result.translation == "привет"
    assert result.coverage == 1.0


def test_unknown_marked() -> None:
    result = translate("hello xyzzy", "en", "es")
    assert result.translation == "hola [?xyzzy]"
    assert result.coverage == 0.5
    assert result.unknown == ["xyzzy"]


def test_same_language() -> None:
    result = translate("hello", "en", "en")
    assert result.translation == "hello"
    assert result.coverage == 1.0


def test_bad_input_rejected() -> None:
    with pytest.raises(ValueError):
        translate("   ", "en", "es")
    with pytest.raises(ValueError):
        translate("hello", "xx", "es")
    with pytest.raises(ValueError):
        translate("hello", "en", "xx")


def test_languages() -> None:
    assert LANGS == ["en", "ru", "es", "de", "fr"]
