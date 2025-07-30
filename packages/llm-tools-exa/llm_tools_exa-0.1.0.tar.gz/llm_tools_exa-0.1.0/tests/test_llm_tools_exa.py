from unittest.mock import Mock, patch

import pytest

from llm_tools_exa import web_search


@pytest.fixture
def mock_exa_result():
    """Mock Exa search result object."""
    result = Mock()
    result.title = "Test Title"
    result.author = "Test Author"
    result.url = "https://example.com"
    result.published_date = "2024-01-01"
    result.highlights = ["Important highlight 1", "Important highlight 2"]
    result.text = "This is the full text content of the result."
    return result


@pytest.fixture
def mock_exa_response(mock_exa_result):
    """Mock Exa API response."""
    response = Mock()
    response.results = [mock_exa_result]
    return response


@patch("llm_tools_exa.Exa")
@patch("llm_tools_exa.llm.get_key")
def test_web_search_basic(mock_get_key, mock_exa_class, mock_exa_response):
    """Test basic web search functionality."""
    # Setup mocks
    mock_get_key.return_value = "test_api_key"
    mock_exa_instance = Mock()
    mock_exa_instance.search_and_contents.return_value = mock_exa_response
    mock_exa_class.return_value = mock_exa_instance

    # Call function
    result = web_search("test query")

    # Verify API calls
    mock_get_key.assert_called_once_with(
        explicit_key="exa", key_alias="exa", env_var="EXA_API_KEY"
    )
    mock_exa_class.assert_called_once_with("test_api_key")
    mock_exa_instance.search_and_contents.assert_called_once_with(
        query="test query",
        num_results=3,
        category=None,
        type="auto",
        include_domains=None,
        text=True,
        highlights=True,
    )

    # Verify output format
    assert "Title: Test Title" in result
    assert "Author: Test Author" in result
    assert "URL: https://example.com" in result
    assert "Published: 2024-01-01" in result
    assert "- Important highlight 1" in result
    assert "- Important highlight 2" in result
    assert "Text: This is the full text content of the result." in result
    assert "---------" in result


@patch("llm_tools_exa.Exa")
@patch("llm_tools_exa.llm.get_key")
def test_web_search_with_parameters(mock_get_key, mock_exa_class, mock_exa_response):
    """Test web search with custom parameters."""
    mock_get_key.return_value = "test_api_key"
    mock_exa_instance = Mock()
    mock_exa_instance.search_and_contents.return_value = mock_exa_response
    mock_exa_class.return_value = mock_exa_instance

    # Call with custom parameters
    web_search(
        query="python tutorials",
        num_results=5,
        category="research paper",
        include_domains=["github.com", "stackoverflow.com"],
    )

    # Verify parameters passed correctly
    mock_exa_instance.search_and_contents.assert_called_once_with(
        query="python tutorials",
        num_results=5,
        category="research paper",
        type="auto",
        include_domains=["github.com", "stackoverflow.com"],
        text=True,
        highlights=True,
    )


@patch("llm_tools_exa.Exa")
@patch("llm_tools_exa.llm.get_key")
def test_web_search_multiple_results(mock_get_key, mock_exa_class):
    """Test web search with multiple results."""
    mock_get_key.return_value = "test_api_key"
    mock_exa_instance = Mock()

    # Create multiple mock results
    result1 = Mock()
    result1.title = "First Result"
    result1.author = "Author 1"
    result1.url = "https://example1.com"
    result1.published_date = "2024-01-01"
    result1.highlights = ["Highlight 1"]
    result1.text = "Text 1"

    result2 = Mock()
    result2.title = "Second Result"
    result2.author = "Author 2"
    result2.url = "https://example2.com"
    result2.published_date = "2024-01-02"
    result2.highlights = ["Highlight 2", "Another highlight"]
    result2.text = "Text 2"

    mock_response = Mock()
    mock_response.results = [result1, result2]
    mock_exa_instance.search_and_contents.return_value = mock_response
    mock_exa_class.return_value = mock_exa_instance

    result = web_search("test query")

    # Verify both results are in output
    assert "First Result" in result
    assert "Second Result" in result
    assert "https://example1.com" in result
    assert "https://example2.com" in result
    assert result.count("---------") == 2  # Separator appears for each result


@patch("llm_tools_exa.Exa")
@patch("llm_tools_exa.llm.get_key")
def test_web_search_empty_results(mock_get_key, mock_exa_class):
    """Test web search with no results."""
    mock_get_key.return_value = "test_api_key"
    mock_exa_instance = Mock()

    mock_response = Mock()
    mock_response.results = []
    mock_exa_instance.search_and_contents.return_value = mock_response
    mock_exa_class.return_value = mock_exa_instance

    result = web_search("nonexistent query")

    # Should return empty string when no results
    assert result == ""


@pytest.mark.parametrize(
    "category",
    [
        "company",
        "research paper",
        "news",
        "pdf",
        "github",
        "tweet",
        "personal site",
        "linkedin profile",
        "financial report",
    ],
)
@patch("llm_tools_exa.Exa")
@patch("llm_tools_exa.llm.get_key")
def test_web_search_valid_categories(
    mock_get_key, mock_exa_class, mock_exa_response, category
):
    """Test web search with all valid category values."""
    mock_get_key.return_value = "test_api_key"
    mock_exa_instance = Mock()
    mock_exa_instance.search_and_contents.return_value = mock_exa_response
    mock_exa_class.return_value = mock_exa_instance

    web_search("test", category=category)

    mock_exa_instance.search_and_contents.assert_called_once_with(
        query="test",
        num_results=3,
        category=category,
        type="auto",
        include_domains=None,
        text=True,
        highlights=True,
    )
