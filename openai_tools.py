"""OpenAI tool definitions and handler for the E-REDES chatbot."""

import json

from eredes_api import query_scheduled_interruptions
from outage_data import get_national_summary, get_outage_by_location

# ── Tool definitions for the OpenAI API ─────────────────────────────────────

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "consultar_interrupcoes_programadas",
            "description": (
                "Consulta interrupções programadas (trabalhos de manutenção) "
                "na rede E-REDES, usando a API oficial de dados abertos. "
                "Pode filtrar por concelho ou código postal."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "concelho": {
                        "type": "string",
                        "description": "Nome do concelho (ex: 'Leiria', 'Coimbra')",
                    },
                    "codigo_postal": {
                        "type": "string",
                        "description": "Código postal completo ou parcial (ex: '2400-001' ou '2400')",
                    },
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "consultar_estado_tempestade_kristin",
            "description": (
                "Consulta o estado atual das avarias causadas pela Tempestade "
                "Kristin numa determinada localização. Aceita código postal, "
                "nome de distrito ou nome de concelho."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "localizacao": {
                        "type": "string",
                        "description": (
                            "Código postal (ex: '2400-001'), distrito (ex: 'Leiria') "
                            "ou concelho (ex: 'Pombal')"
                        ),
                    },
                },
                "required": ["localizacao"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "resumo_nacional_tempestade",
            "description": (
                "Obtém o resumo nacional do impacto da Tempestade Kristin "
                "na rede elétrica, incluindo totais de clientes afetados, "
                "equipas no terreno e progresso de recuperação."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
]


async def handle_tool_call(name: str, arguments: dict) -> str:
    """Execute a tool call and return the JSON result as a string."""
    if name == "consultar_interrupcoes_programadas":
        result = await query_scheduled_interruptions(
            municipality=arguments.get("concelho"),
            postal_code=arguments.get("codigo_postal"),
        )
    elif name == "consultar_estado_tempestade_kristin":
        location = arguments.get("localizacao", "")
        data = get_outage_by_location(location)
        if data:
            result = data
        else:
            result = {
                "info": (
                    f"Não foram encontrados dados de avarias da Tempestade "
                    f"Kristin para a localização '{location}'. Esta zona pode "
                    f"não ter sido afetada ou não está na nossa base de dados. "
                    f"Para informações atualizadas, contacte a Linha de "
                    f"Avarias: 800 506 506."
                )
            }
    elif name == "resumo_nacional_tempestade":
        result = get_national_summary()
    else:
        result = {"erro": f"Ferramenta desconhecida: {name}"}

    return json.dumps(result, ensure_ascii=False)
