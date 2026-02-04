"""Unit tests for outage data lookups."""

from outage_data import get_national_summary, get_outage_by_location


def test_lookup_by_postal_code():
    result = get_outage_by_location("2400-001")
    assert result is not None
    assert result["distrito"] == "Leiria"


def test_lookup_by_district():
    result = get_outage_by_location("Coimbra")
    assert result is not None
    assert result["distrito"] == "Coimbra"


def test_lookup_by_concelho():
    result = get_outage_by_location("Pombal")
    assert result is not None
    assert result["distrito"] == "Leiria"


def test_lookup_not_found():
    result = get_outage_by_location("Lisboa")
    assert result is None


def test_national_summary():
    summary = get_national_summary()
    assert summary["evento"] == "Tempestade Kristin"
    assert summary["total_clientes_afetados"] == 175000
    assert summary["total_clientes_sem_luz"] == 41200
    assert len(summary["distritos_afetados"]) == 7
    assert 0 < summary["percentagem_global_reposta"] < 100
