import logging
from contextlib import asynccontextmanager

import httpx

from pubmedmcp.models import (
    EInfoRequest,
    EInfoResponse,
    ESearchRequest,
    ESearchResponse,
    RetMode,
)

log = logging.getLogger(__file__)

# Constants
BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"


@asynccontextmanager
async def pubmedsdk_client() -> httpx.AsyncClient:
    """
    Context manager to create an async client with default headers for NCBI Entrez API.
    """
    headers = {
        "tool": "PubMedSDK",
        "email": "guillaume.raille@gmail.com",
    }
    async with httpx.AsyncClient(headers=headers) as client:
        yield client


async def einfo(client: httpx.AsyncClient, params: EInfoRequest) -> EInfoResponse:
    """
    Query NCBI EInfo API to get information about Entrez databases.

    Provides the number of records indexed in each field of a given database, the date
    of the last update of the database, and the available links from the database to
    other Entrez databases.

    Args:
        client: an httpx.AsyncClient used to make the request
        params: EInfoRequest model containing query parameters

    Returns:
        EInfoResponse containing database information

    Examples:
        >>> # Get list of all databases
        >>> response = await einfo(EInfoRequest())

        >>> # Get details about protein database
        >>> response = await einfo(EInfoRequest(db="protein", version="2.0"))

    Notes:
        - Base URL: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/einfo.fcgi
        - No required parameters if getting list of all databases
        - Version 2.0 adds IsTruncatable and IsRangeable fields
    """
    if params.retmode != RetMode.JSON:
        raise ValueError(
            f"We only support {RetMode.JSON} return mode for EInfo at this time. You provided {params.retmode}."
        )

    base_url = f"{BASE_URL}/einfo.fcgi"

    # Build query parameters
    query_params = params.model_dump(exclude_none=True)

    response = await client.get(base_url, params=query_params)
    response.raise_for_status()

    return EInfoResponse.model_validate_json(response.text)


async def esearch(client: httpx.AsyncClient, params: ESearchRequest) -> ESearchResponse:
    """
    Query NCBI ESearch API to search and retrieve UIDs matching a text query.

    Provides a list of UIDs matching a text query, optionally using the Entrez History
    server to store results for use in subsequent E-utility calls.

    Args:
        client: an httpx.AsyncClient used to make the request
        params: ESearchRequest model containing query parameters

    Returns:
        ESearchResponse containing search results, translations and any errors

    Examples:
        >>> # Basic search for asthma articles
        >>> response = await esearch(client, ESearchRequest(term="asthma"))

        >>> # Search with date range
        >>> response = await esearch(client,
        ...     ESearchRequest(
        ...         term="asthma",
        ...         mindate="2020/01/01",
        ...         maxdate="2020/12/31",
        ...         datetype="pdat"
        ...     )
        ... )

        >>> # Search using history server
        >>> response = await esearch(client,
        ...     ESearchRequest(
        ...         term="asthma",
        ...         usehistory="y",
        ...         retmax=100
        ...     )
        ... )

        >>> # Search with field restriction
        >>> response = await esearch(client,
        ...     ESearchRequest(term="asthma[title]")
        ... )

    Notes:
        - Base URL: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi
        - For PubMed, ESearch can only retrieve the first 10,000 records matching a query
        - For other databases, use retstart to iterate through results beyond 10,000
        - Some PubMed web interface features (citation matching, spelling correction)
          are not available through ESearch
    """
    if params.retmode != RetMode.JSON:
        raise ValueError(
            f"We only support {RetMode.JSON} return mode for ESearch at this time. You provided {params.retmode}."
        )

    base_url = f"{BASE_URL}/esearch.fcgi"

    # Build query parameters
    query_params = params.model_dump(exclude_none=True)

    response = await client.get(base_url, params=query_params)
    response.raise_for_status()

    return ESearchResponse.model_validate_json(response.text)


if __name__ == "__main__":
    import asyncio

    logging.basicConfig(level=logging.INFO)

    async def main():
        async with pubmedsdk_client() as client:
            # Get info about pubmed database
            params = EInfoRequest(db="pubmed", version="2.0")
            response = await einfo(client, params)
            print(response)

    asyncio.run(main())
