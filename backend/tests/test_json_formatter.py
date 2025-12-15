"""
Unit tests for JSON formatter.

Tests conversion of API responses to Bulletin objects, validation,
and error handling for malformed data.
"""

import pytest
import json
from pydantic import ValidationError
from src.fetchers.json_formatter import JSONFormatter
from src.models.article import CategoryEnum
from src.models.bulletin import BulletinWrapper


class TestJSONFormatter:
    """Test JSON formatter functionality."""
    
    def test_format_valid_response(self):
        """Test formatting a valid API response to Bulletin."""
        response_data = {
            "content": json.dumps({
                "articles": [
                    {
                        "title": "Test Article One for Valid Response",
                        "summary": "This is a test summary with at least twenty words to meet the minimum requirement for validation purposes and testing.",
                        "category": "politics"
                    },
                    {
                        "title": "Test Article Two for Valid Response",
                        "summary": "Another test summary text with sufficient words here to meet the twenty word minimum requirement for validation purposes in this comprehensive test case.",
                        "category": "economy"
                    },
                    {
                        "title": "Test Article Three for Valid Response",
                        "summary": "Third test summary text with sufficient words here to meet the twenty word minimum requirement for validation purposes in this comprehensive test case.",
                        "category": "technology"
                    },
                    {
                        "title": "Test Article Four for Valid Response",
                        "summary": "Fourth test summary text with sufficient words here to meet the twenty word minimum requirement for validation purposes in this comprehensive test case.",
                        "category": "sports"
                    },
                    {
                        "title": "Test Article Five for Valid Response",
                        "summary": "Fifth test summary text with sufficient words here to meet the twenty word minimum requirement for validation purposes in this comprehensive test case.",
                        "category": "health"
                    }
                ]
            }),
            "citations": [
                {"title": "Ref 1", "url": "https://example.com/1", "publisher": "Publisher 1"},
                {"title": "Ref 2", "url": "https://example.com/2", "publisher": "Publisher 2"},
                {"title": "Ref 3", "url": "https://example.com/3", "publisher": "Publisher 3"},
                {"title": "Ref 4", "url": "https://example.com/4", "publisher": "Publisher 4"},
                {"title": "Ref 5", "url": "https://example.com/5", "publisher": "Publisher 5"}
            ],
            "usage": {
                "prompt_tokens": 500,
                "completion_tokens": 800,
                "total_tokens": 1300
            }
        }
        
        formatter = JSONFormatter()
        result = formatter.format(
            response_data=response_data,
            region="usa",
            period="morning",
            date="2025-12-15"
        )
        
        assert isinstance(result, BulletinWrapper)
        assert result.bulletin.id == "usa-2025-12-15-morning"
        assert result.bulletin.region.value == "usa"
        assert result.bulletin.period.value == "morning"
        assert len(result.bulletin.articles) == 5
        assert result.bulletin.metadata.article_count == 5
        assert result.bulletin.metadata.llm_usage.total_tokens == 1300
    
    def test_format_extracts_articles_from_json(self):
        """Test extracting articles array from JSON content."""
        formatter = JSONFormatter()
        
        # Test with "articles" key
        content1 = '{"articles": [{"title": "Test", "summary": "Summary text", "category": "politics"}]}'
        articles1 = formatter._extract_articles_from_content(content1)
        assert len(articles1) == 1
        assert articles1[0]["title"] == "Test"
        
        # Test with array directly
        content2 = '[{"title": "Test", "summary": "Summary text", "category": "politics"}]'
        articles2 = formatter._extract_articles_from_content(content2)
        assert len(articles2) == 1
    
    def test_format_handles_markdown_code_blocks(self):
        """Test extracting JSON from markdown code blocks."""
        formatter = JSONFormatter()
        
        content = '''Here is the response:
```json
{"articles": [{"title": "Test", "summary": "Summary", "category": "politics"}]}
```
'''
        
        articles = formatter._extract_articles_from_content(content)
        assert len(articles) == 1
        assert articles[0]["title"] == "Test"
    
    def test_format_raises_on_empty_content(self):
        """Test formatter raises ValueError on empty content."""
        response_data = {
            "content": "",
            "citations": [],
            "usage": {}
        }
        
        formatter = JSONFormatter()
        
        with pytest.raises(ValueError) as exc_info:
            formatter.format(
                response_data=response_data,
                region="usa",
                period="morning"
            )
        
        assert "Empty content" in str(exc_info.value)
    
    def test_format_raises_on_malformed_json(self):
        """Test formatter raises ValueError on malformed JSON."""
        response_data = {
            "content": "This is not JSON",
            "citations": [],
            "usage": {}
        }
        
        formatter = JSONFormatter()
        
        with pytest.raises(ValueError) as exc_info:
            formatter.format(
                response_data=response_data,
                region="usa",
                period="morning"
            )
        
        assert "JSON" in str(exc_info.value)
    
    def test_format_validates_article_count(self):
        """Test formatter warns on fewer than 5 articles."""
        response_data = {
            "content": json.dumps({
                "articles": [
                    {
                        "title": "Only Article One",
                        "summary": "This is a test summary with at least twenty words to meet the minimum requirement for validation purposes.",
                        "category": "politics"
                    }
                ]
            }),
            "citations": [],
            "usage": {"prompt_tokens": 100, "completion_tokens": 200, "total_tokens": 300}
        }
        
        formatter = JSONFormatter()
        
        # Should create bulletin but with validation warning/error
        with pytest.raises(ValidationError):  # Pydantic will reject <5 articles
            formatter.format(
                response_data=response_data,
                region="usa",
                period="morning"
            )
    
    def test_format_creates_article_ids(self):
        """Test formatter generates correct article IDs."""
        response_data = {
            "content": json.dumps({
                "articles": [
                    {
                        "title": f"Test Article {i}",
                        "summary": "This is a test summary with at least twenty words to meet the minimum requirement for validation purposes and testing.",
                        "category": "politics"
                    }
                    for i in range(1, 6)
                ]
            }),
            "citations": [],
            "usage": {"prompt_tokens": 100, "completion_tokens": 200, "total_tokens": 300}
        }
        
        formatter = JSONFormatter()
        result = formatter.format(
            response_data=response_data,
            region="usa",
            period="morning",
            date="2025-12-15"
        )
        
        # Check article IDs
        for idx, article in enumerate(result.bulletin.articles, start=1):
            expected_id = f"usa-2025-12-15-morning-{idx:03d}"
            assert article.article_id == expected_id
    
    def test_format_handles_invalid_category(self):
        """Test formatter defaults to 'world' for invalid categories."""
        response_data = {
            "content": json.dumps({
                "articles": [
                    {
                        "title": f"Test Article {i}",
                        "summary": "This is a test summary with at least twenty words to meet the minimum requirement for validation purposes and testing.",
                        "category": "invalid_category"  # Invalid
                    }
                    for i in range(1, 6)
                ]
            }),
            "citations": [],
            "usage": {"prompt_tokens": 100, "completion_tokens": 200, "total_tokens": 300}
        }
        
        formatter = JSONFormatter()
        result = formatter.format(
            response_data=response_data,
            region="usa",
            period="morning",
            date="2025-12-15"
        )
        
        # All articles should have "world" category (default fallback)
        for article in result.bulletin.articles:
            assert article.category == CategoryEnum.WORLD
    
    def test_format_creates_citations(self):
        """Test formatter creates 1-3 citations per article."""
        response_data = {
            "content": json.dumps({
                "articles": [
                    {
                        "title": f"Test Article {i}",
                        "summary": "This is a test summary with at least twenty words to meet the minimum requirement for validation purposes and testing.",
                        "category": "politics"
                    }
                    for i in range(1, 6)
                ]
            }),
            "citations": [
                {"title": f"Citation {i}", "url": f"https://example.com/{i}", "publisher": f"Pub {i}"}
                for i in range(1, 16)  # 15 citations (3 per article)
            ],
            "usage": {"prompt_tokens": 100, "completion_tokens": 200, "total_tokens": 300}
        }
        
        formatter = JSONFormatter()
        result = formatter.format(
            response_data=response_data,
            region="usa",
            period="morning",
            date="2025-12-15"
        )
        
        # Check citations
        for article in result.bulletin.articles:
            assert 1 <= len(article.citations) <= 3
    
    def test_format_creates_default_citation(self):
        """Test formatter creates default citation if none provided."""
        response_data = {
            "content": json.dumps({
                "articles": [
                    {
                        "title": f"Test Article {i}",
                        "summary": "This is a test summary with at least twenty words to meet the minimum requirement for validation purposes and testing.",
                        "category": "politics"
                    }
                    for i in range(1, 6)
                ]
            }),
            "citations": [],  # No citations
            "usage": {"prompt_tokens": 100, "completion_tokens": 200, "total_tokens": 300}
        }
        
        formatter = JSONFormatter()
        result = formatter.format(
            response_data=response_data,
            region="usa",
            period="morning",
            date="2025-12-15"
        )
        
        # Each article should have at least 1 default citation
        for article in result.bulletin.articles:
            assert len(article.citations) >= 1
            assert article.citations[0].title == "Original Source"
    
    def test_format_calculates_metadata(self):
        """Test formatter calculates correct metadata."""
        response_data = {
            "content": json.dumps({
                "articles": [
                    {"title": "Article One Title", "summary": "This is a test summary with at least twenty words to meet the minimum requirement for validation purposes and testing.", "category": "politics"},
                    {"title": "Article Two Title", "summary": "This is a test summary with at least twenty words to meet the minimum requirement for validation purposes and testing.", "category": "politics"},
                    {"title": "Article Three Title", "summary": "This is a test summary with at least twenty words to meet the minimum requirement for validation purposes and testing.", "category": "economy"},
                    {"title": "Article Four Title", "summary": "This is a test summary with at least twenty words to meet the minimum requirement for validation purposes and testing.", "category": "technology"},
                    {"title": "Article Five Title", "summary": "This is a test summary with at least twenty words to meet the minimum requirement for validation purposes and testing.", "category": "technology"}
                ]
            }),
            "citations": [],
            "usage": {"prompt_tokens": 500, "completion_tokens": 800, "total_tokens": 1300}
        }
        
        formatter = JSONFormatter()
        result = formatter.format(
            response_data=response_data,
            region="usa",
            period="morning",
            date="2025-12-15"
        )
        
        metadata = result.bulletin.metadata
        assert metadata.article_count == 5
        assert metadata.categories_distribution["politics"] == 2
        assert metadata.categories_distribution["economy"] == 1
        assert metadata.categories_distribution["technology"] == 2
        assert metadata.llm_usage.prompt_tokens == 500
        assert metadata.llm_usage.completion_tokens == 800
        assert metadata.llm_usage.total_tokens == 1300
    
    def test_format_with_workflow_run_id(self):
        """Test formatter includes workflow_run_id in metadata."""
        response_data = {
            "content": json.dumps({
                "articles": [
                    {
                        "title": f"Test Article {i}",
                        "summary": "This is a test summary with at least twenty words to meet the minimum requirement for validation purposes and testing.",
                        "category": "politics"
                    }
                    for i in range(1, 6)
                ]
            }),
            "citations": [],
            "usage": {"prompt_tokens": 100, "completion_tokens": 200, "total_tokens": 300}
        }
        
        formatter = JSONFormatter()
        result = formatter.format(
            response_data=response_data,
            region="usa",
            period="morning",
            date="2025-12-15",
            workflow_run_id="12345678"
        )
        
        assert result.bulletin.metadata.workflow_run_id == "12345678"
