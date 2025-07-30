import json
import os
import sys
import httpx
from pydantic import Field
from typing import Annotated
from mcp.server.fastmcp import FastMCP


mcp = FastMCP("netmind-mcpserver-mcp")
NETMIND_API_TOKEN = os.environ.get("NETMIND_API_TOKEN")
HEADERS = {"Authorization": f"Bearer {NETMIND_API_TOKEN}"}
API_URL = os.environ.get("API_URL", "https://mcp.netmind.ai/servers")


async def _query_server(name_like: str = None, offset: int = 0, limit: int = 50):
    params = {
        "offset": offset,
        "limit": limit,
    }
    if name_like:
        params["name"] = name_like
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f'{API_URL}', headers=HEADERS, timeout=1 * 60,
            params=params
        )
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"query_server error, code: {response.status_code}, msg {response.text}")


@mcp.tool()
async def query_server(name: str = None, offset: int = 0, limit: int = 50):
    """
    Query the server list with optional fuzzy name matching and pagination.
    :param name: Optional name to filter servers by a fuzzy match.
    :param offset: The starting point for pagination.
    :param limit: The maximum number of servers to return.
    :return: A list of servers in JSON format.
    """
    res = await _query_server(name, offset=offset, limit=limit)
    return json.dumps(res)


@mcp.tool()
async def get_server(server_name: str):
    """
    Retrieves detailed information about a specific server by its name.
    :param server_name: The name of the server to retrieve information for.
    :return: A JSON object containing the server's details.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f'{API_URL}/{server_name}', headers=HEADERS, timeout=1 * 60)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"get server error, code: {response.status_code}, msg {response.text}")


@mcp.tool()
async def add_update_rating_review(
        server_name: str,
        rating: Annotated[float, Field(ge=1.0, le=5.0)] = 5.0,
        review: str = '',
):
    """
    Adds or updates a rating and review for a specific server.
    :param server_name: The name of the server to add or update the rating and review for.
    :param rating: The rating to give the server, between 1.0 and 5.0.
    :param review: The review text to add or update for the server.
    """
    servers = await _query_server(server_name)
    if isinstance(servers, list) and len(servers) > 1:
        names = [s['name'] for s in servers]
        raise Exception(
            f"Server {server_name} hosts multiple servers, "
            f"please specify one of the following names: {', '.join(names)}"
        )
    elif isinstance(servers, list) and len(servers) == 0:
        raise Exception(f"Server {server_name} not found")
    else:
        server_name = servers[0]['name']

    payload = {
        'server_name': server_name,
        'rating': rating,
        'review': review
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(f'{API_URL}/reviews', json=payload, headers=HEADERS, timeout=1 * 60)

    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"add_update_rating_review error, code: {response.status_code}, msg {response.text}")


@mcp.tool()
async def list_rating_review(server_name: str, offset: int = 0, limit: int = 50):
    """
    Lists reviews and ratings for a specific server.

    :param server_name: The name of the server to list reviews for.
    :param offset: The starting point for pagination.
    :param limit: The maximum number of reviews to return.
    :return: A JSON object containing the total number of reviews, average rating, and a list of reviews.
    """
    servers = await _query_server(server_name)
    if isinstance(servers, list) and len(servers) > 1:
        names = [s['name'] for s in servers]
        raise Exception(
            f"Server {server_name} hosts multiple servers, "
            f"please specify one of the following names: {', '.join(names)}"
        )
    elif isinstance(servers, list) and len(servers) == 0:
        raise Exception(f"Server {server_name} not found")
    else:
        server_name = servers[0]['name']

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f'{API_URL}/reviews',
            params={'server_name': server_name, 'offset': offset, 'limit': limit},
            headers=HEADERS,
            timeout=1 * 60
        )
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"list_rating_review error, code: {response.status_code}, msg {response.text}")


def main():
    if not NETMIND_API_TOKEN:
        print(
            "Error: NETMIND_API_TOKEN environment variable is required",
            file=sys.stderr,
        )
        sys.exit(1)
    mcp.run(transport='stdio')


if __name__ == "__main__":
    main()
