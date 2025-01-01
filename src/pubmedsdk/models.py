"""
Pydantic models for the PubMed SDK

This code is mostly generated with Anthropic's Claude 3.5 sonnet based on the Entrez API detailed documentation.
see: https://www.ncbi.nlm.nih.gov/books/NBK25499/
"""


from enum import Enum
from typing import Literal, Optional

from pydantic import BaseModel, Field


class RetMode(str, Enum):
    """Valid return modes for EInfo"""

    XML = "xml"
    """ XML return mode """

    JSON = "json"
    """ JSON return mode """


class Db(str, Enum):
    """Valid databases for EInfo"""

    PUBMED = "pubmed"
    """ PubMed database """

    PROTEIN = "protein"
    """ Protein database """

    NUCCORE = "nuccore"
    """ Nucleotide database """

    IPG = "ipg"
    """ IPG database """

    NUCLEOTIDE = "nucleotide"
    """ Nucleotide database """

    STRUCTURE = "structure"
    """ Structure database """

    GENOME = "genome"
    """ Genome database """

    ANNOTINFO = "annotinfo"
    """ Annotation information database """

    ASSEMBLY = "assembly"
    """ Assembly database """

    BIOPROJECT = "bioproject"
    """ BioProject database """

    BIOSAMPLE = "biosample"
    """ BioSample database """

    BLASTDBINFO = "blastdbinfo"
    """ BLAST database information """

    BOOKS = "books"
    """ Books database """

    CDD = "cdd"
    """ Comparative Genomic Database """

    CLINVAR = "clinvar"
    """ ClinVar database """

    GAP = "gap"
    """ Genome Assembly database """

    GAPPLUS = "gapplus"
    """ Genome Assembly Plus database """

    GRASP = "grasp"
    """ Genome Assembly Plus database """

    DBVAR = "dbvar"
    """ Database of Variants """

    GENE = "gene"
    """ Gene database """

    GDS = "gds"
    """ Genome Data Structure database """

    GEOPROFILES = "geoprofiles"
    """ GeoProfiles database """

    MEDGEN = "medgen"
    """ Medical Genome database """

    MESH = "mesh"
    """ Medical Subject Headings database """

    NLMCATALOG = "nlmcatalog"
    """ NLM Catalog database """

    OMIM = "omim"
    """ OMIM database """

    ORGTRACK = "orgtrack"
    """ Organism Track database """

    PMC = "pmc"
    """ PubMed Central database """

    POPSET = "popset"
    """ Population Set database """

    PROTEINCLUSTERS = "proteinclusters"
    """ Protein Clusters database """

    PCASSAY = "pcassay"
    """ Protein Clusters Assay database """

    PROTFAM = "protfam"
    """ Protein Family database """

    PCCOMPOUND = "pccompound"
    """ Protein Clusters Compound database """

    PCSUBSTANCE = "pcsubstance"
    """ Protein Clusters Substance database """

    SEQANNOT = "seqannot"
    """ Sequence Annotation database """

    SNP = "snp"
    """ Single Nucleotide Polymorphism database """

    SRA = "sra"
    """ Sequence Read Archive database """

    TAXONOMY = "taxonomy"
    """ Taxonomy database """

    BIOCOLLECTIONS = "biocollections"
    """ BioCollections database """

    GTR = "gtr"
    """ Genome Translation Report database """


class EInfoRequest(BaseModel, use_enum_values=True, validate_default=True):
    """
    Request parameters for NCBI EInfo API

    Examples:
        >>> # Get list of all valid Entrez databases
        >>> EInfoRequest()

        >>> # Get statistics for Entrez Protein database with version 2.0 XML
        >>> EInfoRequest(db="protein", version="2.0")
    """

    db: Optional[str] = Field(
        None,
        description="Target database about which to gather statistics. If not provided, returns list of all valid Entrez databases",
    )
    version: Optional[Literal["2.0"]] = Field(
        None,
        description="Used to specify version 2.0 EInfo XML. Only supported value is '2.0'. When present, returns additional fields: IsTruncatable and IsRangeable",
    )
    retmode: RetMode = Field(
        RetMode.JSON, description="Retrieval type. Determines format of returned output"
    )


class DbInfo(BaseModel):
    """Database information returned by EInfo"""

    dbname: str = Field(..., description="Database name")
    menuname: str = Field(..., description="Display name")
    description: str = Field(..., description="Database description")
    dbbuild: str = Field(..., description="Database build number")
    count: int = Field(..., description="Number of records")
    lastupdate: str = Field(..., description="Last update timestamp")
    fieldlist: list[dict] = Field(..., description="List of indexing fields")
    linklist: list[dict] = Field(..., description="List of available links")


class EInfoHeader(BaseModel):
    """Header information from NCBI EInfo API response"""

    type: str = Field(..., description="Response type (einfo)")
    version: str = Field(..., description="API version")


class EInfoResult(BaseModel):
    """Wrapper for database information"""

    dbinfo: list[DbInfo] = Field(..., description="List of database information")
    dblist: Optional[list[str]] = Field(
        None, description="List of valid Entrez database names"
    )


class EInfoResponse(BaseModel):
    """
    Response from NCBI EInfo API

    Contains either:
    1. List of valid database names (if no db parameter provided)
    2. Detailed statistics about a specific database

    Wrapped in a header and result structure
    """

    header: EInfoHeader = Field(..., description="Response header information")
    einforesult: EInfoResult = Field(..., description="Response content")


class ESearchRequest(BaseModel, use_enum_values=True, validate_default=True):
    """
    Request parameters for NCBI ESearch API

    Functions:
        - Provides a list of UIDs matching a text query
        - Posts the results of a search on the History server
        - Downloads all UIDs from a dataset stored on the History server
        - Combines or limits UID datasets stored on the History server
        - Sorts sets of UIDs

    Note:
        API users should be aware that some NCBI products contain search tools that
        generate content from searches on the web interface that are not available
        to ESearch. For example, the PubMed web interface contains citation matching
        and spelling correction tools that are only available through that interface.

    Examples:
        >>> # Basic search in PubMed for asthma articles
        >>> ESearchRequest(db="pubmed", term="asthma")

        >>> # Search with publication date range
        >>> ESearchRequest(
        ...     db="pubmed",
        ...     term="asthma",
        ...     mindate="2020/01/01",
        ...     maxdate="2020/12/31",
        ...     datetype="pdat"
        ... )

        >>> # Search with history server and get 100 results
        >>> ESearchRequest(
        ...     db="pubmed",
        ...     term="asthma",
        ...     usehistory="y",
        ...     retmax=100
        ... )

        >>> # Search with field restriction
        >>> ESearchRequest(db="pubmed", term="asthma[title]")
        >>> # Or equivalently:
        >>> ESearchRequest(db="pubmed", term="asthma", field="title")

        >>> # Search with proximity operator (PubMed only)
        >>> ESearchRequest(db="pubmed", term='"asthma treatment"[Title:~3]')

        >>> # Combine previous results using history
        >>> ESearchRequest(
        ...     db="pubmed",
        ...     term="#1 AND asthma",
        ...     WebEnv="<webenv string>",
        ...     usehistory="y"
        ... )

        >>> # Sort results by publication date
        >>> ESearchRequest(
        ...     db="pubmed",
        ...     term="asthma",
        ...     sort="pub_date"
        ... )

        >>> # Get only the count of results
        >>> ESearchRequest(
        ...     db="pubmed",
        ...     term="asthma",
        ...     rettype="count"
        ... )
    """

    db: Db = Field(
        Db.PUBMED,
        description="Database to search. Value must be a valid Entrez database name",
    )
    term: str = Field(
        ...,
        description="""Entrez text query. All special characters must be URL encoded. 
        Spaces may be replaced by '+' signs. For very long queries (more than several 
        hundred characters), consider using an HTTP POST call. See PubMed or Entrez 
        help for information about search field descriptions and tags. Search fields 
        and tags are database specific.""",
    )
    usehistory: Optional[Literal["y"]] = Field(
        None,
        description="""When set to 'y', ESearch will post UIDs to the History server 
        for use in subsequent E-utility calls. Required for interpreting query keys 
        in term or accepting a WebEnv as input.""",
    )
    WebEnv: Optional[str] = Field(
        None,
        description="""Web environment string from previous E-utility call. When provided, 
        ESearch will post results to this pre-existing WebEnv. Allows query keys to be 
        used in term parameter. Must be used with usehistory='y'.""",
    )
    query_key: Optional[int] = Field(
        None,
        description="""Query key from previous E-utility call. When provided with WebEnv, 
        finds intersection of this set and current search (combines with AND).""",
    )
    retstart: Optional[int] = Field(
        0,
        description="""Sequential index of first UID to be shown (default=0). Can be used 
        with retmax to download arbitrary subset of UIDs.""",
    )
    retmax: Optional[int] = Field(
        20,
        description="""Number of UIDs to return (default=20, max=10000). If usehistory='y', 
        remaining UIDs are stored on History server. For >10000 UIDs from non-PubMed 
        databases, use multiple requests with retstart.""",
    )
    rettype: Optional[Literal["uilist", "count"]] = Field(
        None,
        description="""'uilist' (default) for standard XML output, 'count' displays 
        only the Count tag.""",
    )
    retmode: RetMode = Field(
        RetMode.JSON, description="Retrieval type. Determines format of returned output"
    )
    sort: Optional[str] = Field(
        None,
        description="""Sort method for results. Values vary by database. PubMed values:
        - pub_date: descending sort by publication date
        - Author: ascending sort by first author
        - JournalName: ascending sort by journal name
        - relevance: default sort order ("Best Match")""",
    )
    field: Optional[str] = Field(
        None,
        description="""Search field to limit entire search. Equivalent to adding [field] 
        to term.""",
    )
    datetype: Optional[Literal["mdat", "pdat", "edat"]] = Field(
        None,
        description="""Type of date used to limit search:
        - mdat: modification date
        - pdat: publication date
        - edat: Entrez date
        Generally databases have only two allowed values.""",
    )
    reldate: Optional[int] = Field(
        None,
        description="""When set to n, returns items with datetype within the last n 
        days.""",
    )
    mindate: Optional[str] = Field(
        None,
        description="""Start date for date range. Format: YYYY/MM/DD, YYYY/MM, or YYYY. 
        Must be used with maxdate.""",
    )
    maxdate: Optional[str] = Field(
        None,
        description="""End date for date range. Format: YYYY/MM/DD, YYYY/MM, or YYYY. 
        Must be used with mindate.""",
    )


class Translation(BaseModel):
    """
    Translation of search terms to database-specific syntax

    Contains translations of search terms into the database's search syntax,
    including MeSH term mappings, journal abbreviation expansions, etc.
    """

    from_: str = Field(..., alias="from", description="Original search term")
    to: str = Field(..., description="Translated search term")


class ErrorList(BaseModel):
    """
    List of errors in search

    Contains phrases and fields that could not be found or processed
    in the database.
    """

    phrasesnotfound: Optional[list[str]] = Field(
        None, description="Search phrases that returned no results"
    )
    fieldsnotfound: Optional[list[str]] = Field(
        None, description="Invalid search field tags"
    )


class ESearchResult(BaseModel):
    """
    Results from NCBI ESearch query

    Contains:
    - Total result count
    - Retrieved UIDs
    - Term translations
    - History server information (if requested)
    - Error messages (if any)

    Examples:
        >>> # Basic search result
        >>> ESearchResult(
        ...     count=42,
        ...     retmax=20,
        ...     retstart=0,
        ...     idlist=["12345", "67890"],
        ...     querytranslation="asthma[All Fields]"
        ... )

        >>> # Result with history server
        >>> ESearchResult(
        ...     count=42,
        ...     retmax=20,
        ...     retstart=0,
        ...     idlist=["12345", "67890"],
        ...     querykey=1,
        ...     webenv="MCID_12345...",
        ...     querytranslation="asthma[All Fields]"
        ... )
    """

    count: int = Field(..., description="Total number of UIDs matching query")
    retmax: int = Field(..., description="Number of UIDs returned in this response")
    retstart: int = Field(..., description="Index of first returned UID")
    querykey: Optional[int] = Field(None, description="Query key on history server")
    webenv: Optional[str] = Field(None, description="Web environment on history server")
    idlist: list[str] = Field(..., description="List of UIDs matching query")
    translationset: Optional[list[Translation]] = Field(
        None, description="Term translations including MeSH mappings"
    )
    translationstack: Optional[list[dict]] = Field(
        None,
        description="Boolean expression showing how translated terms were combined",
    )
    querytranslation: Optional[str] = Field(
        None, description="Complete translation of search expression"
    )
    errorlist: Optional[ErrorList] = Field(
        None, description="List of phrases and fields that produced errors"
    )
    warninglist: Optional[dict] = Field(
        None, description="List of warnings about query processing"
    )


class ESearchResponse(BaseModel):
    """
    Response from NCBI ESearch API

    Contains search results including:
    - Total result count
    - List of matching UIDs
    - Query translations
    - History server info if requested
    - Any errors or warnings

    Examples:
        >>> # Basic search response
        >>> ESearchResponse(
        ...     header=EInfoHeader(type="esearch", version="0.3"),
        ...     esearchresult=ESearchResult(
        ...         count=42,
        ...         retmax=20,
        ...         retstart=0,
        ...         idlist=["12345", "67890"],
        ...         querytranslation="asthma[All Fields]"
        ...     )
        ... )
    """

    header: EInfoHeader = Field(..., description="Response header information")
    esearchresult: ESearchResult = Field(..., description="Search results")


class EFetchRequest(BaseModel, use_enum_values=True, validate_default=True):
    """
    Request parameters for NCBI EFetch API

    Functions:
    - Returns formatted data records for a list of input UIDs
    - Returns formatted data records for a set of UIDs stored on the Entrez History server

    Examples:
        >>> # Fetch PMIDs 17284678 and 9997 as text abstracts
        >>> EFetchRequest(
        ...     db="pubmed",
        ...     id="17284678,9997",
        ...     retmode="text",
        ...     rettype="abstract"
        ... )

        >>> # Fetch PMIDs in XML
        >>> EFetchRequest(
        ...     db="pubmed",
        ...     id="11748933,11700088",
        ...     retmode="xml"
        ... )

        >>> # Fetch XML for PubMed Central ID
        >>> EFetchRequest(db="pmc", id="212403")

        >>> # Fetch first 100 bases of plus strand in FASTA format
        >>> EFetchRequest(
        ...     db="nuccore",
        ...     id="21614549",
        ...     strand="1",
        ...     seq_start=1,
        ...     seq_stop=100,
        ...     rettype="fasta",
        ...     retmode="text"
        ... )

        >>> # Fetch GenPept flat file for protein
        >>> EFetchRequest(
        ...     db="protein",
        ...     id="8",
        ...     rettype="gp"
        ... )

        >>> # Fetch using history server
        >>> EFetchRequest(
        ...     db="pubmed",
        ...     query_key=1,
        ...     WebEnv="MCID_123..."
        ... )
    """

    db: Db = Field(
        Db.PUBMED,
        description="Database from which to retrieve records. Value must be a valid Entrez database name",
    )
    id: Optional[str] = Field(
        None,
        description="""UID list. Either a single UID or a comma-delimited list of UIDs. 
        All UIDs must be from the specified database. For sequence databases (nuccore, 
        popset, protein), the UID list may be a mixed list of GI numbers and 
        accession.version identifiers.""",
    )
    query_key: Optional[int] = Field(
        None,
        description="""Query key specifying which UID list attached to the Web Environment 
        will be used as input. Must be used with WebEnv.""",
    )
    WebEnv: Optional[str] = Field(
        None,
        description="""Web Environment containing the UID list to use as input. Usually 
        obtained from previous ESearch, EPost or ELink call. Must be used with query_key.""",
    )
    retmode: Optional[str] = Field(
        None,
        description="""Retrieval mode specifying the data format of returned records 
        (e.g., text, XML, JSON). Valid values vary by database.""",
    )
    rettype: Optional[str] = Field(
        None,
        description="""Retrieval type specifying the record view (e.g., abstract, MEDLINE, 
        FASTA). Valid values vary by database.""",
    )
    retstart: Optional[int] = Field(
        0,
        description="""Sequential index of first record to retrieve (default=0). Can be 
        used with retmax to download an arbitrary subset of records.""",
    )
    retmax: Optional[int] = Field(
        20,
        description="""Total number of records to retrieve, up to maximum of 10,000. For 
        large sets, retstart can be iterated while holding retmax constant.""",
    )
    strand: Optional[Literal["1", "2"]] = Field(
        None,
        description="""Strand of DNA to retrieve. Available values are "1" for plus strand 
        and "2" for minus strand. For sequence databases only.""",
    )
    seq_start: Optional[int] = Field(
        None,
        description="""First sequence base to retrieve. Integer coordinate of first desired 
        base, with "1" representing the first base. For sequence databases only.""",
    )
    seq_stop: Optional[int] = Field(
        None,
        description="""Last sequence base to retrieve. Integer coordinate of last desired 
        base. For sequence databases only.""",
    )
    complexity: Optional[int] = Field(
        None,
        description="""Data content to return. Controls how much of the record "blob" to 
        return. Values:
        0: entire blob
        1: bioseq
        2: minimal bioseq-set  
        3: minimal nuc-prot
        4: minimal pub-set
        For sequence databases only.""",
    )


class EFetchResponse(BaseModel):
    """
    Response from NCBI EFetch API

    The response format varies significantly based on:
    - Database being queried (db parameter)
    - Retrieval mode (retmode parameter) 
    - Retrieval type (rettype parameter)

    Common formats include:
    - XML (retmode=xml)
    - Text (retmode=text)
    - JSON (retmode=json)
    - FASTA (rettype=fasta)
    - GenBank/GenPept flat files (rettype=gb/gp)

    Due to the variable response format, this base model should be extended
    for specific database/format combinations.
    """

    pass  # Specific response formats should extend this base class

