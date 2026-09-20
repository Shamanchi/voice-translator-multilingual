"""Словари: разговорник фраз и пословный глоссарий. Без сети."""

from __future__ import annotations

LANGS = ["en", "ru", "es", "de", "fr"]

# Фразы: исходный язык -> фраза -> переводы.
PHRASES: dict[str, dict[str, dict[str, str]]] = {
    "en": {
        "thank you": {"ru": "спасибо", "es": "gracias", "de": "danke", "fr": "merci"},
        "good morning": {"ru": "доброе утро", "es": "buenos días", "de": "guten Morgen", "fr": "bonjour"},
        "good evening": {"ru": "добрый вечер", "es": "buenas noches", "de": "guten Abend", "fr": "bonsoir"},
        "see you later": {"ru": "увидимся", "es": "hasta luego", "de": "bis später", "fr": "à bientôt"},
    },
    "ru": {
        "спасибо большое": {"en": "thank you very much", "es": "muchas gracias", "de": "vielen Dank", "fr": "merci beaucoup"},
        "доброе утро": {"en": "good morning", "es": "buenos días", "de": "guten Morgen", "fr": "bonjour"},
    },
    "es": {
        "muchas gracias": {"en": "thank you very much", "ru": "большое спасибо", "de": "vielen Dank", "fr": "merci beaucoup"},
    },
    "de": {
        "vielen dank": {"en": "thank you very much", "ru": "большое спасибо", "es": "muchas gracias", "fr": "merci beaucoup"},
    },
    "fr": {
        "merci beaucoup": {"en": "thank you very much", "ru": "большое спасибо", "es": "muchas gracias", "de": "vielen Dank"},
    },
}

# Однословный глоссарий: формы по языкам.
WORDS: list[dict[str, str]] = [
    {"en": "hello", "ru": "привет", "es": "hola", "de": "hallo", "fr": "bonjour"},
    {"en": "goodbye", "ru": "пока", "es": "adiós", "de": "tschüss", "fr": "au revoir"},
    {"en": "please", "ru": "пожалуйста", "es": "por favor", "de": "bitte", "fr": "s'il vous plaît"},
    {"en": "yes", "ru": "да", "es": "sí", "de": "ja", "fr": "oui"},
    {"en": "no", "ru": "нет", "es": "no", "de": "nein", "fr": "non"},
    {"en": "good", "ru": "хороший", "es": "bueno", "de": "gut", "fr": "bon"},
    {"en": "morning", "ru": "утро", "es": "mañana", "de": "morgen", "fr": "matin"},
    {"en": "evening", "ru": "вечер", "es": "noche", "de": "abend", "fr": "soir"},
    {"en": "water", "ru": "вода", "es": "agua", "de": "wasser", "fr": "eau"},
    {"en": "coffee", "ru": "кофе", "es": "café", "de": "kaffee", "fr": "café"},
    {"en": "bill", "ru": "счёт", "es": "cuenta", "de": "rechnung", "fr": "addition"},
    {"en": "help", "ru": "помощь", "es": "ayuda", "de": "hilfe", "fr": "aide"},
    {"en": "sorry", "ru": "извините", "es": "lo siento", "de": "entschuldigung", "fr": "désolé"},
    {"en": "price", "ru": "цена", "es": "precio", "de": "preis", "fr": "prix"},
    {"en": "hotel", "ru": "отель", "es": "hotel", "de": "hotel", "fr": "hôtel"},
    {"en": "train", "ru": "поезд", "es": "tren", "de": "zug", "fr": "train"},
    {"en": "airport", "ru": "аэропорт", "es": "aeropuerto", "de": "flughafen", "fr": "aéroport"},
    {"en": "food", "ru": "еда", "es": "comida", "de": "essen", "fr": "nourriture"},
    {"en": "day", "ru": "день", "es": "día", "de": "tag", "fr": "jour"},
    {"en": "night", "ru": "ночь", "es": "noche", "de": "nacht", "fr": "nuit"},
    {"en": "friend", "ru": "друг", "es": "amigo", "de": "freund", "fr": "ami"},
    {"en": "time", "ru": "время", "es": "tiempo", "de": "zeit", "fr": "temps"},
    {"en": "today", "ru": "сегодня", "es": "hoy", "de": "heute", "fr": "aujourd'hui"},
    {"en": "love", "ru": "люблю", "es": "amo", "de": "liebe", "fr": "aime"},
]

# Обратный индекс: язык -> форма -> запись.
_INDEX: dict[str, dict[str, dict[str, str]]] = {}
for _entry in WORDS:
    for _lang in LANGS:
        _INDEX.setdefault(_lang, {})[_entry[_lang].lower()] = _entry


def lookup(word: str, source: str, target: str) -> str | None:
    """Перевести одно слово. None, если нет в словаре."""
    entry = _INDEX.get(source, {}).get(word.lower())
    if entry is None:
        return None
    return entry.get(target)
