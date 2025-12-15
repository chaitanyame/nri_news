"""
Unit tests for Article and related Pydantic models.

Tests validation rules for Article, Source, Citation, Metadata, and LLMUsage.
"""

import pytest
from pydantic import ValidationError, HttpUrl
from src.models.article import (
    Article, Source, Citation, Metadata, LLMUsage,
    CategoryEnum
)


class TestArticleModel:
    """Test Article model validation and constraints."""
    
    def test_article_valid_creation(self):
        """Test creating a valid article with all required fields."""
        article = Article(
            title="Test News Title",
            summary="This is a test summary with sufficient words here to meet the twenty word minimum requirement for validation purposes in this comprehensive test case for our article model validation.",
            category=CategoryEnum.POLITICS,
            source=Source(name="Test Source", url="https://example.com"),
            citations=[Citation(title="Reference", url="https://example.com", publisher="Test Pub")],
            article_id="usa-2025-12-15-morning-001"
        )
        
        assert article.title == "Test News Title"
        assert article.category == CategoryEnum.POLITICS
        assert len(article.citations) == 1
    
    def test_article_title_length_min(self):
        """Test article title must be at least 10 characters."""
        with pytest.raises(ValidationError) as exc_info:
            Article(
                title="Short",  # Too short
                summary="This is a test summary with at least twenty words to meet the minimum requirement for validation purposes.",
                category=CategoryEnum.POLITICS,
                source=Source(name="Test Source", url="https://example.com"),
                citations=[Citation(title="Ref", url="https://example.com", publisher="Test")],
                article_id="usa-2025-12-15-morning-001"
            )
        
        errors = exc_info.value.errors()
        assert any("title" in str(error).lower() for error in errors)
    
    def test_article_title_length_max(self):
        """Test article title must not exceed 120 characters."""
        long_title = "A" * 121
        
        with pytest.raises(ValidationError) as exc_info:
            Article(
                title=long_title,  # Too long
                summary="This is a test summary with at least twenty words to meet the minimum requirement for validation purposes.",
                category=CategoryEnum.POLITICS,
                source=Source(name="Test Source", url="https://example.com"),
                citations=[Citation(title="Ref", url="https://example.com", publisher="Test")],
                article_id="usa-2025-12-15-morning-001"
            )
        
        errors = exc_info.value.errors()
        assert any("title" in str(error).lower() for error in errors)
    
    def test_article_summary_length_min(self):
        """Test article summary must be at least 40 characters."""
        with pytest.raises(ValidationError) as exc_info:
            Article(
                title="Test Article Title",
                summary="Too short",  # Too short
                category=CategoryEnum.POLITICS,
                source=Source(name="Test Source", url="https://example.com"),
                citations=[Citation(title="Ref", url="https://example.com", publisher="Test")],
                article_id="usa-2025-12-15-morning-001"
            )
        
        errors = exc_info.value.errors()
        assert any("summary" in str(error).lower() for error in errors)
    
    def test_article_summary_length_max(self):
        """Test article summary must not exceed 500 characters."""
        long_summary = "A" * 501
        
        with pytest.raises(ValidationError) as exc_info:
            Article(
                title="Test Article Title",
                summary=long_summary,  # Too long
                category=CategoryEnum.POLITICS,
                source=Source(name="Test Source", url="https://example.com"),
                citations=[Citation(title="Ref", url="https://example.com", publisher="Test")],
                article_id="usa-2025-12-15-morning-001"
            )
        
        errors = exc_info.value.errors()
        assert any("summary" in str(error).lower() for error in errors)
    
    def test_article_summary_word_count(self):
        """Test article summary must have 20-100 words."""
        # Too few words (less than 20)
        with pytest.raises(ValidationError):
            Article(
                title="Test Article Title",
                summary="This summary has only ten words total here.",
                category=CategoryEnum.POLITICS,
                source=Source(name="Test Source", url="https://example.com"),
                citations=[Citation(title="Ref", url="https://example.com", publisher="Test")],
                article_id="usa-2025-12-15-morning-001"
            )
    
    def test_article_category_enum(self):
        """Test article category must be valid enum value."""
        with pytest.raises(ValidationError):
            Article(
                title="Test Article Title",
                summary="This is a test summary with at least twenty words to meet the minimum requirement for validation purposes.",
                category="invalid_category",  # Invalid enum
                source=Source(name="Test Source", url="https://example.com"),
                citations=[Citation(title="Ref", url="https://example.com", publisher="Test")],
                article_id="usa-2025-12-15-morning-001"
            )
    
    def test_article_citations_min(self):
        """Test article must have at least 1 citation."""
        with pytest.raises(ValidationError) as exc_info:
            Article(
                title="Test Article Title",
                summary="This is a test summary with at least twenty words to meet the minimum requirement for validation purposes.",
                category=CategoryEnum.POLITICS,
                source=Source(name="Test Source", url="https://example.com"),
                citations=[],  # Empty citations
                article_id="usa-2025-12-15-morning-001"
            )
        
        errors = exc_info.value.errors()
        assert any("citation" in str(error).lower() for error in errors)
    
    def test_article_citations_max(self):
        """Test article must have at most 3 citations."""
        citations = [
            Citation(title=f"Ref {i}", url="https://example.com", publisher="Test")
            for i in range(4)  # 4 citations (exceeds max of 3)
        ]
        
        with pytest.raises(ValidationError) as exc_info:
            Article(
                title="Test Article Title",
                summary="This is a test summary with at least twenty words to meet the minimum requirement for validation purposes.",
                category=CategoryEnum.POLITICS,
                source=Source(name="Test Source", url="https://example.com"),
                citations=citations,
                article_id="usa-2025-12-15-morning-001"
            )
        
        errors = exc_info.value.errors()
        assert any("citation" in str(error).lower() for error in errors)


class TestSourceModel:
    """Test Source model validation."""
    
    def test_source_valid_creation(self):
        """Test creating a valid source."""
        source = Source(
            name="Test News Outlet",
            url="https://example.com/article"
        )
        
        assert source.name == "Test News Outlet"
        assert str(source.url) == "https://example.com/article"
    
    def test_source_url_validation(self):
        """Test source URL must be valid HTTPS URL."""
        with pytest.raises(ValidationError) as exc_info:
            Source(
                name="Test Source",
                url="not-a-valid-url"  # Invalid URL
            )
        
        errors = exc_info.value.errors()
        assert any("url" in str(error).lower() for error in errors)
    
    def test_source_published_at_optional(self):
        """Test published_at is optional."""
        # Without published_at
        source1 = Source(name="Test", url="https://example.com")
        assert source1.published_at is None
        
        # With published_at (parsed as datetime, not string)
        from datetime import datetime
        source2 = Source(name="Test", url="https://example.com", published_at="2025-12-15T08:30:00Z")
        assert isinstance(source2.published_at, datetime)


class TestCitationModel:
    """Test Citation model validation."""
    
    def test_citation_valid_creation(self):
        """Test creating a valid citation."""
        citation = Citation(
            title="Reference Article",
            url="https://example.com/ref",
            publisher="Test Publisher"
        )
        
        assert citation.title == "Reference Article"
        assert citation.publisher == "Test Publisher"
    
    def test_citation_title_max_length(self):
        """Test citation title must not exceed 150 characters."""
        long_title = "A" * 151
        
        with pytest.raises(ValidationError) as exc_info:
            Citation(
                title=long_title,  # Too long
                url="https://example.com",
                publisher="Test"
            )
        
        errors = exc_info.value.errors()
        assert any("title" in str(error).lower() for error in errors)
    
    def test_citation_publisher_max_length(self):
        """Test citation publisher must not exceed 100 characters."""
        long_publisher = "A" * 101
        
        with pytest.raises(ValidationError) as exc_info:
            Citation(
                title="Reference",
                url="https://example.com",
                publisher=long_publisher  # Too long
            )
        
        errors = exc_info.value.errors()
        assert any("publisher" in str(error).lower() for error in errors)


class TestLLMUsageModel:
    """Test LLMUsage model validation."""
    
    def test_llm_usage_valid_creation(self):
        """Test creating valid LLM usage."""
        usage = LLMUsage(
            prompt_tokens=100,
            completion_tokens=200,
            total_tokens=300
        )
        
        assert usage.prompt_tokens == 100
        assert usage.completion_tokens == 200
        assert usage.total_tokens == 300
    
    def test_llm_usage_total_tokens_validation(self):
        """Test total_tokens must equal sum of prompt and completion tokens."""
        with pytest.raises(ValidationError) as exc_info:
            LLMUsage(
                prompt_tokens=100,
                completion_tokens=200,
                total_tokens=250  # Wrong total (should be 300)
            )
        
        errors = exc_info.value.errors()
        assert any("total_tokens" in str(error).lower() for error in errors)


class TestMetadataModel:
    """Test Metadata model validation."""
    
    def test_metadata_valid_creation(self):
        """Test creating valid metadata."""
        metadata = Metadata(
            article_count=8,
            categories_distribution={"politics": 3, "economy": 2, "technology": 3},
            llm_usage=LLMUsage(prompt_tokens=500, completion_tokens=800, total_tokens=1300),
            processing_time_seconds=0.0
        )
        
        assert metadata.article_count == 8
        assert metadata.llm_model == "sonar"  # Default value
    
    def test_metadata_article_count_min(self):
        """Test article_count must be at least 1."""
        with pytest.raises(ValidationError) as exc_info:
            Metadata(
                article_count=0,  # Too low
                categories_distribution={},
                llm_usage=LLMUsage(prompt_tokens=0, completion_tokens=0, total_tokens=0),
                processing_time_seconds=0.0
            )
        
        errors = exc_info.value.errors()
        assert any("article_count" in str(error).lower() for error in errors)
    
    def test_metadata_article_count_max(self):
        """Test article_count must not exceed 10."""
        with pytest.raises(ValidationError) as exc_info:
            Metadata(
                article_count=11,  # Too high
                categories_distribution={},
                llm_usage=LLMUsage(prompt_tokens=0, completion_tokens=0, total_tokens=0),
                processing_time_seconds=0.0
            )
        
        errors = exc_info.value.errors()
        assert any("article_count" in str(error).lower() for error in errors)
    
    def test_metadata_workflow_run_id_optional(self):
        """Test workflow_run_id is optional."""
        # Without workflow_run_id
        metadata1 = Metadata(
            article_count=5,
            categories_distribution={"politics": 5},
            llm_usage=LLMUsage(prompt_tokens=100, completion_tokens=200, total_tokens=300),
            processing_time_seconds=0.0
        )
        assert metadata1.workflow_run_id is None
        
        # With workflow_run_id
        metadata2 = Metadata(
            article_count=5,
            categories_distribution={"politics": 5},
            llm_usage=LLMUsage(prompt_tokens=100, completion_tokens=200, total_tokens=300),
            workflow_run_id="12345678",
            processing_time_seconds=0.0
        )
        assert metadata2.workflow_run_id == "12345678"
