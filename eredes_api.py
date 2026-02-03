"""Real E-REDES Open Data API client for scheduled interruptions."""

import httpx

from config import EREDES_API_BASE, EREDES_DATASET


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
    url = f"{EREDES_API_BASE}/{EREDES_DATASET}/records"

    where_clauses = []
    if municipality:
        where_clauses.append(f'search(municipality, "{municipality}")')
    if postal_code:
        clean = postal_code.strip().replace("-", "")
        where_clauses.append(f'search(zipcode, "{clean}")')

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
