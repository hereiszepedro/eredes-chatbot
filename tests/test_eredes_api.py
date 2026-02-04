"""Unit tests for E-REDES API sanitization."""

from eredes_api import _sanitize_search_term


def test_sanitize_plain_text():
    assert _sanitize_search_term("Leiria") == "Leiria"


def test_sanitize_accented_text():
    assert _sanitize_search_term("São João") == "São João"


def test_sanitize_strips_special_chars():
    result = _sanitize_search_term('Leiria"; DROP TABLE--')
    assert '"' not in result
    assert ";" not in result


def test_sanitize_truncates_to_100():
    long_input = "a" * 200
    assert len(_sanitize_search_term(long_input)) == 100


def test_sanitize_allows_hyphens():
    assert _sanitize_search_term("Montemor-o-Velho") == "Montemor-o-Velho"


def test_sanitize_strips_whitespace():
    assert _sanitize_search_term("  Coimbra  ") == "Coimbra"
