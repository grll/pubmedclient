# PubMed SDK

[PubMed](https://pubmed.ncbi.nlm.nih.gov/) is a database of over 37 million citations for biomedical literature from MEDLINE, life science journals, and online books. Citations may include links to full text content from PubMed Central and publisher web sites.

PubMed SDK is a simple open-source Python SDK for calling the NCBI PubMed API.

At the moment, the SDK mostly wraps around Entrez 'E-Utilities' API.

See for more details on the E-Utilities API from PubMed: 

* [A General Introduction to the E-utilities](https://www.ncbi.nlm.nih.gov/books/NBK25497/)
* [The E-utilities In-Depth: Parameters, Syntax and More](https://www.ncbi.nlm.nih.gov/books/NBK25499/)

## Installation

```bash
# recommended uv, will add pubmesdk to your uv project
uv add pubmedsdk

# or pip
pip install pubmedsdk
```

## Usage

warning: without api key, you can only make 3 requests per second per IP.

```python
from pubmedsdk import pubmedsdk_client

# this is a thin wrapper around httpx
# with a few headers set for Entrez API
async with pubmedsdk_client() as client:

    # get the name of all available databases via EInfo
    params = EInfoRequest()
    response = await einfo(client, params)
    print(response)

    # get info about pubmed database
    params = EInfoRequest(db="pubmed")
    response = await einfo(client, params)
    print(response)

    # search for articles about asthma in the pubmed database
    params = ESearchRequest(db="pubmed", term="asthma")
    response = await esearch(client, params)
    print(response)

    # fetch the abstract for one of the returned id
    params = EFetchRequest(db="pubmed", id="39737528", rettype="abstract", retmode="text")
    response = await efetch(client, params)
    print(response)
```

## Contributing

The API coverage is far from complete.

We welcome contributions. Please feel free to open an issue or a PR.
