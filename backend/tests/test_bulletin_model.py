"""
Unit tests for Bulletin and Article Pydantic models.

Tests validation rules, enum constraints, and data integrity checks.
"""

import pytest
from datetime import datetime, timezone
from pydantic import ValidationError
from src.models.bulletin import Bulletin, BulletinWrapper
from src.models.article import (
    Article, Source, Citation, Metadata, LLMUsage,
    RegionEnum, PeriodEnum, CategoryEnum
)


class TestBulletinModel:
    """Test Bulletin model validation and constraints."""
    
    def test_bulletin_valid_creation(self):
        """Test creating a valid bulletin with all required fields."""
        article = Article(
            title="Test Article",
            summary="This is a test summary with sufficient words here to meet the twenty-word minimum requirement for validation purposes in this test case.",
            category=CategoryEnum.POLITICS,
            source=Source(name="Test Source", url="https://example.com"),
            citations=[Citation(title="Ref", url="https://example.com", publisher="Test")],
            article_id="usa-2025-12-15-morning-001"
        )
        
        metadata = Metadata(
            article_count=1,
            categories_distribution={"politics": 1},
            llm_usage=LLMUsage(prompt_tokens=100, completion_tokens=200, total_tokens=300)
        )
        
        bulletin = Bulletin(
            id="usa-2025-12-15-morning",
            region=RegionEnum.usa,
            date="2025-12-15",
            period=PeriodEnum.morning,
            generated_at=datetime.utcnow(),
            version="1.0",
            articles=[article],
            metadata=metadata
        )
        
        assert bulletin.id == "usa-2025-12-15-morning"
        assert bulletin.region == RegionEnum.USA
        assert bulletin.period == PeriodEnum.MORNING
        assert len(bulletin.articles) == 1
    
    def test_bulletin_id_format_validation(self):
        """Test bulletin ID must match region-date-period format."""
        article = Article(
            title="Test Article",
            summary="This is a test summary with sufficient words here to meet the twenty-word minimum requirement for validation purposes in this test case.",
            category=CategoryEnum.POLITICS,
            source=Source(name="Test Source", url="https://example.com"),
            citations=[Citation(title="Ref", url="https://example.com", publisher="Test")],
            article_id="usa-2025-12-15-morning-001"
        )
        
        metadata = Metadata(
            article_count=1,
            categories_distribution={"politics": 1},
            llm_usage=LLMUsage(prompt_tokens=100, completion_tokens=200, total_tokens=300)
        )
        
        with pytest.raises(ValidationError) as exc_info:
            Bulletin(
                id="invalid-id-format",  # Wrong format
                region=RegionEnum.USA,
                date="2025-12-15",
                period=PeriodEnum.MORNING,
                generated_at=datetime.now(timezone.utc),
                version="1.0",
                articles=[article],
                metadata=metadata
            )
        
        errors = exc_info.value.errors()
        assert any("id" in str(error).lower() for error in errors)
    
    def test_bulletin_region_enum(self):
        """Test region must be valid enum value."""
        with pytest.raises(ValidationError):
            Bulletin(
                id="invalid-2025-12-15-morning",
                region="invalid_region",  # Invalid enum
                date="2025-12-15",
                period=PeriodEnum.MORNING,
                generated_at=datetime.now(timezone.utc),
                version="1.0",
                articles=[],
                metadata=Metadata(
                    article_count=0,
                    categories_distribution={},
                    llm_usage=LLMUsage(prompt_tokens=0, completion_tokens=0, total_tokens=0)
                )
            )
    
    def test_bulletin_period_enum(self):
        """Test period must be valid enum value."""
        with pytest.raises(ValidationError):
            Bulletin(
                id="usa-2025-12-15-invalid",
                region=RegionEnum.USA,
                date="2025-12-15",
                period="invalid_period",  # Invalid enum
                generated_at=datetime.now(timezone.utc),
                version="1.0",
                articles=[],
                metadata=Metadata(
                    article_count=0,
                    categories_distribution={},
                    llm_usage=LLMUsage(prompt_tokens=0, completion_tokens=0, total_tokens=0)
                )
            )
    
    def test_bulletin_date_format(self):
        """Test date must be valid YYYY-MM-DD format."""
        articles = [
            Article(
                title=f"Test Article {i}",
                summary="This is a test summary with sufficient words here to meet the twenty-word minimum requirement for validation purposes in this test case.",
                category=CategoryEnum.POLITICS,
                source=Source(name="Test Source", url="https://example.com"),
                citations=[Citation(title="Ref", url="https://example.com", publisher="Test")],
                article_id=f"usa-2025-12-15-morning-{i:03d}"
            )
            for i in range(1, 6)  # Create 5 articles
        ]
        
        metadata = Metadata(
            article_count=5,
            categories_distribution={"politics": 5},
            llm_usage=LLMUsage(prompt_tokens=100, completion_tokens=200, total_tokens=300),
            processing_time_seconds=0.0
        )
        
        # Valid date
        bulletin = Bulletin(
            id="usa-2025-12-15-morning",
            region=RegionEnum.USA,
            date="2025-12-15",
            period=PeriodEnum.MORNING,
            generated_at=datetime.now(timezone.utc),
            version="1.0",
            articles=articles,
            metadata=metadata
        )
        assert bulletin.date == "2025-12-15"
        
        # Invalid date format
        with pytest.raises(ValidationError):
            Bulletin(
                id="usa-12/15/2025-morning",
                region=RegionEnum.USA,
                date="12/15/2025",  # Wrong format
                period=PeriodEnum.MORNING,
                generated_at=datetime.now(timezone.utc),
                version="1.0",
                articles=articles,
                metadata=metadata
            )
    
    def test_bulletin_article_count_range(self):
        """Test bulletin must have 5-10 articles."""
        # Less than 5 articles
        with pytest.raises(ValidationError) as exc_info:
            Bulletin(
                id="usa-2025-12-15-morning",
                region=RegionEnum.USA,
                date="2025-12-15",
                period=PeriodEnum.MORNING,
                generated_at=datetime.now(timezone.utc),
                version="1.0",
                articles=[],  # Too few
                metadata=Metadata(
                    article_count=0,
                    categories_distribution={},
                    llm_usage=LLMUsage(prompt_tokens=0, completion_tokens=0, total_tokens=0),
                    processing_time_seconds=0.0
                )
            )
        
        errors = exc_info.value.errors()
        # The error should be about articles length
        assert len(errors) > 0
    
    def test_bulletin_article_ids_unique(self):
        """Test all article IDs must be unique."""
        articles = [
            Article(
                title="Article One",
                summary="This is a test summary with sufficient words here to meet the twenty-word minimum requirement for validation purposes in this test case.",
                category=CategoryEnum.POLITICS,
                source=Source(name="Test Source", url="https://example.com"),
                citations=[Citation(title="Ref", url="https://example.com", publisher="Test")],
                article_id="usa-2025-12-15-morning-001"
            ),
            Article(
                title="Article Two",
                summary="This is a test summary with sufficient words here to meet the twenty-word minimum requirement for validation purposes in this test case.",
                category=CategoryEnum.ECONOMY,
                source=Source(name="Test Source", url="https://example.com"),
                citations=[Citation(title="Ref", url="https://example.com", publisher="Test")],
                article_id="usa-2025-12-15-morning-001"  # Duplicate ID
            )
        ]
        
        # Need to create 5 articles minimum
        for i in range(3, 6):
            articles.append(
                Article(
                    title=f"Article {i} Title",
                    summary="This is a test summary with sufficient words here to meet the twenty-word minimum requirement for validation purposes in this test case.",
                    category=CategoryEnum.TECHNOLOGY,
                    source=Source(name="Test Source", url="https://example.com"),
                    citations=[Citation(title="Ref", url="https://example.com", publisher="Test")],
                    article_id=f"usa-2025-12-15-morning-{i:03d}"
                )
            )
        
        with pytest.raises(ValidationError) as exc_info:
            Bulletin(
                id="usa-2025-12-15-morning",
                region=RegionEnum.USA,
                date="2025-12-15",
                period=PeriodEnum.MORNING,
                generated_at=datetime.now(timezone.utc),
                version="1.0",
                articles=articles,
                metadata=Metadata(
                    article_count=5,
                    categories_distribution={"politics": 2, "technology": 3},
                    llm_usage=LLMUsage(prompt_tokens=100, completion_tokens=200, total_tokens=300),
                    processing_time_seconds=0.0
                )
            )
        
        errors = exc_info.value.errors()
        assert any("unique" in str(error).lower() or "article" in str(error).lower() for error in errors)
    
    def test_bulletin_wrapper(self):
        """Test BulletinWrapper for JSON file structure."""
        article = Article(
            title="Test Article",
            summary="This is a test summary with sufficient words here to meet the twenty-word minimum requirement for validation purposes in this test case.",
            category=CategoryEnum.POLITICS,
            source=Source(name="Test Source", url="https://example.com"),
            citations=[Citation(title="Ref", url="https://example.com", publisher="Test")],
            article_id="usa-2025-12-15-morning-001"
        )
        
        bulletin = Bulletin(
            id="usa-2025-12-15-morning",
            region=RegionEnum.USA,
            date="2025-12-15",
            period=PeriodEnum.MORNING,
            generated_at=datetime.now(timezone.utc),
            version="1.0",
            articles=[article] * 5,  # Repeat to meet 5 minimum
            metadata=Metadata(
                article_count=5,
                categories_distribution={"politics": 5},
                llm_usage=LLMUsage(prompt_tokens=100, completion_tokens=200, total_tokens=300),
                processing_time_seconds=0.0
            )
        )
        
        wrapper = BulletinWrapper(bulletin=bulletin)
        assert wrapper.bulletin.id == "usa-2025-12-15-morning"
        
        # Test JSON serialization
        json_data = wrapper.model_dump()
        assert "bulletin" in json_data
        assert json_data["bulletin"]["id"] == "usa-2025-12-15-morning"
