"""Real E-REDES Open Data API client for scheduled interruptions."""

import re

import httpx

from config import settings


def _sanitize_search_term(term: str) -> str:
    """Strip non-alphanumeric/accent characters and truncate to 100 chars."""
    # Allow letters (including accented), digits, spaces, and hyphens
    cleaned = re.sub(r"[^\w\s\-]", "", term, flags=re.UNICODE)
    return cleaned.strip()[:100]


async def query_scheduled_interruptions(
    municipality: str | None = None,
    postal_code: str | None = None,
    limit: int = 10,
) -> dict:
    """Query the E-REDES API for scheduled network interruptions.

    Args:
        municipality: Filter by municipality name.
        postal_code: Filter by postal code (or prefix).
        limit: Max number of records to return.

    Returns:
        dict with results or error information.
    """
    url = f"{settings.eredes_api_base}/{settings.eredes_dataset}/records"

    where_clauses = []
    if municipality:
        safe_municipality = _sanitize_search_term(municipality)
        where_clauses.append(f'search(municipality, "{safe_municipality}")')
    if postal_code:
        clean = postal_code.strip().replace("-", "")
        safe_postal = _sanitize_search_term(clean)
        where_clauses.append(f'search(zipcode, "{safe_postal}")')

    params = {
        "limit": limit,
        "order_by": "startdatetime DESC",
    }
    if where_clauses:
        params["where"] = " AND ".join(where_clauses)

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(url, params=params)
            resp.raise_for_status()
            data = resp.json()

        records = data.get("records", [])
        results = []
        for rec in records:
            fields = rec.get("record", {}).get("fields", {})
            results.append(
                {
                    "codigo_postal": fields.get("zipcode", ""),
                    "concelho": fields.get("municipality", ""),
                    "freguesia": fields.get("parish", ""),
                    "inicio": fields.get("startdatetime", ""),
                    "fim": fields.get("enddatetime", ""),
                    "duracao": fields.get("durationallocation", ""),
                }
            )

        return {
            "total_encontrados": data.get("total_count", 0),
            "resultados": results,
        }

    except httpx.HTTPStatusError as e:
        return {"erro": f"Erro na API E-REDES: {e.response.status_code}"}
    except httpx.RequestError as e:
        return {"erro": f"Não foi possível contactar a API E-REDES: {str(e)}"}
