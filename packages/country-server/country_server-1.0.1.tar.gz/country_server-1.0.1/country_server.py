#!/usr/bin/env python3
"""
Basic MCP Server that returns countries starting with a given letter.
Uses stdio transport (JSON-RPC over stdin/stdout).
"""

import asyncio
import json
import sys
from typing import Any, Dict, List

# Sample country data
COUNTRIES = [
    "Afghanistan", "Albania", "Algeria", "Argentina", "Armenia", "Australia", "Austria",
    "Bahrain", "Bangladesh", "Belgium", "Brazil", "Bulgaria",
    "Cambodia", "Canada", "Chile", "China", "Colombia", "Croatia", "Cuba",
    "Denmark", "Dominican Republic",
    "Ecuador", "Egypt", "Estonia", "Ethiopia",
    "Finland", "France",
    "Germany", "Ghana", "Greece",
    "Haiti", "Hungary",
    "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy",
    "Jamaica", "Japan", "Jordan",
    "Kazakhstan", "Kenya", "Kuwait",
    "Latvia", "Lebanon", "Libya", "Lithuania", "Luxembourg",
    "Malaysia", "Mexico", "Morocco",
    "Nepal", "Netherlands", "New Zealand", "Nigeria", "Norway",
    "Pakistan", "Peru", "Philippines", "Poland", "Portugal",
    "Qatar",
    "Romania", "Russia",
    "Saudi Arabia", "Singapore", "South Africa", "South Korea", "Spain", "Sri Lanka", "Sudan", "Sweden", "Switzerland", "Sitil",
    "Thailand", "Turkey",
    "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uruguay",
    "Venezuela", "Vietnam",
    "Yemen",
    "Zimbabwe"
]

class MCPServer:
    def __init__(self):
        self.tools = {
            "get_countries": {
                "name": "get_countries",
                "description": "Get countries that start with a specific letter",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "letter": {
                            "type": "string",
                            "description": "The letter to filter countries by (case insensitive)"
                        }
                    },
                    "required": ["letter"]
                }
            }
        }

    async def handle_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        method = message.get("method")
        params = message.get("params", {})
        message_id = message.get("id")

        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": message_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": { "tools": {} },
                    "serverInfo": { "name": "country-server", "version": "1.0.0" }
                }
            }

        elif method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": message_id,
                "result": { "tools": list(self.tools.values()) }
            }

        elif method == "tools/call":
            tool_name = params.get("name")
            args = params.get("arguments", {})

            if tool_name == "get_countries":
                letter = args.get("letter", "").strip().upper()
                if not letter:
                    return {"jsonrpc": "2.0", "id": message_id,
                            "error": {"code": -32602, "message": "Letter parameter is required"}}
                matches = [c for c in COUNTRIES if c.upper().startswith(letter)]
                text = (f"Countries starting with '{letter}':\n" +
                        "\n".join(f"• {c}" for c in matches)) if matches else f"No countries found starting with '{letter}'"
                return {"jsonrpc": "2.0", "id": message_id,
                        "result": {"content": [{"type": "text", "text": text}]}}

            return {"jsonrpc": "2.0", "id": message_id,
                    "error": {"code": -32601, "message": f"Unknown tool: {tool_name}"}}

        else:
            return {"jsonrpc": "2.0", "id": message_id,
                    "error": {"code": -32601, "message": f"Unknown method: {method}"}}

    async def run(self):
        while True:
            line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
            if not line:
                break
            try:
                msg = json.loads(line.strip())
                resp = await self.handle_message(msg)
            except json.JSONDecodeError:
                resp = {"jsonrpc": "2.0", "id": None,
                        "error": {"code": -32700, "message": "Parse error"}}
            except Exception as e:
                resp = {"jsonrpc": "2.0", "id": None,
                        "error": {"code": -32603, "message": f"Internal error: {e}"}}
            print(json.dumps(resp), flush=True)

async def main():
    server = MCPServer()
    await server.run()


def cli() -> None:
    """Sync entry-point for pipx / console_scripts"""
    asyncio.run(main())

if __name__ == "__main__":
    cli()
