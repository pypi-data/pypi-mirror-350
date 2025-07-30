from typing import Literal, Optional

import llm
from exa_py import Exa


def web_search(
    query: str,
    num_results: int = 3,
    category: Optional[
        Literal[
            "company",
            "research paper",
            "news",
            "pdf",
            "github",
            "tweet",
            "personal site",
            "linkedin profile",
            "financial report",
        ]
    ] = None,
    include_domains: Optional[list[str]] = None,
):
    """Search the web using Exa API for high-quality, relevant results.

    Args:
        query: The search query string to find relevant content.
        num_results: Number of search results to return (default: 3).
        category: Optional content category to filter results by specific type.
        include_domains: Optional list of domains to limit search results to.
    """
    exa_key = llm.get_key(explicit_key="exa", key_alias="exa", env_var="EXA_API_KEY")
    exa = Exa(exa_key)
    results = exa.search_and_contents(
        query=query,
        num_results=num_results,
        category=category,
        type="auto",
        include_domains=include_domains,
        text=True,
        highlights=True,
    ).results
    output = []
    for result in results:
        output.append(f"Title: {result.title}")
        output.append(f"Author: {result.author}")
        output.append(f"URL: {result.url}")
        output.append(f"Published: {result.published_date}")
        output.append("Highlights:")
        for highlight in result.highlights:
            output.append(f"- {highlight}")
        output.append(f"Text: {result.text}")
        output.append("---------\n")
    return "\n".join(output)


@llm.hookimpl
def register_tools(register):
    register(web_search)
