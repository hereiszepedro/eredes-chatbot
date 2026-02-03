"""Mock Storm Kristin outage database by district."""

STORM_DATE = "2026-01-28"

OUTAGE_DATA = {
    "leiria": {
        "distrito": "Leiria",
        "clientes_afetados": 45200,
        "clientes_sem_luz": 8300,
        "equipas_no_terreno": 42,
        "geradores_instalados": 18,
        "postos_transformacao_afetados": 156,
        "linhas_media_tensao_afetadas": 23,
        "data_estimada_reposicao": "2026-02-05",
        "percentagem_reposta": 82,
        "concelhos_mais_afetados": [
            "Marinha Grande",
            "Leiria",
            "Pombal",
            "Figueira da Foz",
        ],
        "estado": "Em recuperação",
    },
    "coimbra": {
        "distrito": "Coimbra",
        "clientes_afetados": 32100,
        "clientes_sem_luz": 4500,
        "equipas_no_terreno": 35,
        "geradores_instalados": 12,
        "postos_transformacao_afetados": 98,
        "linhas_media_tensao_afetadas": 15,
        "data_estimada_reposicao": "2026-02-04",
        "percentagem_reposta": 86,
        "concelhos_mais_afetados": [
            "Coimbra",
            "Figueira da Foz",
            "Cantanhede",
            "Montemor-o-Velho",
        ],
        "estado": "Em recuperação",
    },
    "castelo branco": {
        "distrito": "Castelo Branco",
        "clientes_afetados": 18500,
        "clientes_sem_luz": 6200,
        "equipas_no_terreno": 28,
        "geradores_instalados": 10,
        "postos_transformacao_afetados": 72,
        "linhas_media_tensao_afetadas": 18,
        "data_estimada_reposicao": "2026-02-06",
        "percentagem_reposta": 67,
        "concelhos_mais_afetados": [
            "Castelo Branco",
            "Covilhã",
            "Fundão",
            "Sertã",
        ],
        "estado": "Em recuperação",
    },
    "portalegre": {
        "distrito": "Portalegre",
        "clientes_afetados": 12800,
        "clientes_sem_luz": 3100,
        "equipas_no_terreno": 18,
        "geradores_instalados": 7,
        "postos_transformacao_afetados": 45,
        "linhas_media_tensao_afetadas": 9,
        "data_estimada_reposicao": "2026-02-04",
        "percentagem_reposta": 76,
        "concelhos_mais_afetados": ["Portalegre", "Elvas", "Ponte de Sor"],
        "estado": "Em recuperação",
    },
    "santarem": {
        "distrito": "Santarém",
        "clientes_afetados": 28700,
        "clientes_sem_luz": 5400,
        "equipas_no_terreno": 32,
        "geradores_instalados": 14,
        "postos_transformacao_afetados": 110,
        "linhas_media_tensao_afetadas": 20,
        "data_estimada_reposicao": "2026-02-05",
        "percentagem_reposta": 81,
        "concelhos_mais_afetados": [
            "Santarém",
            "Tomar",
            "Abrantes",
            "Torres Novas",
        ],
        "estado": "Em recuperação",
    },
    "viseu": {
        "distrito": "Viseu",
        "clientes_afetados": 22400,
        "clientes_sem_luz": 7800,
        "equipas_no_terreno": 30,
        "geradores_instalados": 11,
        "postos_transformacao_afetados": 88,
        "linhas_media_tensao_afetadas": 16,
        "data_estimada_reposicao": "2026-02-06",
        "percentagem_reposta": 65,
        "concelhos_mais_afetados": ["Viseu", "Lamego", "Mangualde", "Tondela"],
        "estado": "Em recuperação",
    },
    "guarda": {
        "distrito": "Guarda",
        "clientes_afetados": 15300,
        "clientes_sem_luz": 5900,
        "equipas_no_terreno": 22,
        "geradores_instalados": 9,
        "postos_transformacao_afetados": 65,
        "linhas_media_tensao_afetadas": 14,
        "data_estimada_reposicao": "2026-02-07",
        "percentagem_reposta": 61,
        "concelhos_mais_afetados": [
            "Guarda",
            "Seia",
            "Gouveia",
            "Celorico da Beira",
        ],
        "estado": "Em recuperação",
    },
}

# Map postal code prefixes to districts
POSTAL_CODE_DISTRICT_MAP = {
    "2400": "leiria",
    "2401": "leiria",
    "2410": "leiria",
    "2415": "leiria",
    "2420": "leiria",
    "2425": "leiria",
    "2430": "leiria",
    "2440": "leiria",
    "2445": "leiria",
    "2450": "leiria",
    "2460": "leiria",
    "3000": "coimbra",
    "3001": "coimbra",
    "3004": "coimbra",
    "3020": "coimbra",
    "3030": "coimbra",
    "3040": "coimbra",
    "3050": "coimbra",
    "3060": "coimbra",
    "3080": "coimbra",
    "3100": "coimbra",
    "3150": "coimbra",
    "6000": "castelo branco",
    "6001": "castelo branco",
    "6005": "castelo branco",
    "6200": "castelo branco",
    "6215": "castelo branco",
    "6230": "castelo branco",
    "6300": "castelo branco",
    "7300": "portalegre",
    "7301": "portalegre",
    "7350": "portalegre",
    "7400": "portalegre",
    "2000": "santarem",
    "2001": "santarem",
    "2005": "santarem",
    "2040": "santarem",
    "2050": "santarem",
    "2100": "santarem",
    "2200": "santarem",
    "2300": "santarem",
    "2305": "santarem",
    "2350": "santarem",
    "3500": "viseu",
    "3501": "viseu",
    "3504": "viseu",
    "3510": "viseu",
    "3515": "viseu",
    "3520": "viseu",
    "5100": "viseu",
    "6290": "guarda",
    "6260": "guarda",
    "6270": "guarda",
    "6320": "guarda",
    "6360": "guarda",
}


def get_district_from_postal(postal_code: str) -> str | None:
    """Map a postal code to a district. Returns district key or None."""
    prefix = postal_code.strip().split("-")[0]
    return POSTAL_CODE_DISTRICT_MAP.get(prefix)


def get_outage_by_district(district_name: str) -> dict | None:
    """Look up outage data by district name (case-insensitive)."""
    key = district_name.strip().lower()
    return OUTAGE_DATA.get(key)


def get_outage_by_location(location: str) -> dict | None:
    """Try to find outage data by postal code or district/municipality name."""
    # Try postal code first
    if any(c.isdigit() for c in location):
        district_key = get_district_from_postal(location)
        if district_key:
            return OUTAGE_DATA.get(district_key)

    # Try direct district match
    key = location.strip().lower()
    if key in OUTAGE_DATA:
        return OUTAGE_DATA[key]

    # Try matching against concelhos_mais_afetados
    for data in OUTAGE_DATA.values():
        for concelho in data["concelhos_mais_afetados"]:
            if key == concelho.lower():
                return data

    return None


def get_national_summary() -> dict:
    """Return aggregated national summary of storm impact."""
    total_afetados = sum(d["clientes_afetados"] for d in OUTAGE_DATA.values())
    total_sem_luz = sum(d["clientes_sem_luz"] for d in OUTAGE_DATA.values())
    total_equipas = sum(d["equipas_no_terreno"] for d in OUTAGE_DATA.values())
    total_geradores = sum(d["geradores_instalados"] for d in OUTAGE_DATA.values())
    total_pt = sum(
        d["postos_transformacao_afetados"] for d in OUTAGE_DATA.values()
    )

    percentagem_global = (
        round((1 - total_sem_luz / total_afetados) * 100, 1)
        if total_afetados
        else 0
    )

    return {
        "evento": "Tempestade Kristin",
        "data_evento": STORM_DATE,
        "distritos_afetados": [d["distrito"] for d in OUTAGE_DATA.values()],
        "total_clientes_afetados": total_afetados,
        "total_clientes_sem_luz": total_sem_luz,
        "percentagem_global_reposta": percentagem_global,
        "total_equipas_no_terreno": total_equipas,
        "total_geradores_instalados": total_geradores,
        "total_postos_transformacao_afetados": total_pt,
        "estado_geral": "Operação de recuperação em curso",
    }
