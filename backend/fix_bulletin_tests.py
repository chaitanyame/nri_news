#!/usr/bin/env python3
"""Fix bulletin model tests - timezone and article count issues."""

import re

test_file = "tests/test_bulletin_model.py"

# Read the file
with open(test_file, 'r') as f:
    content = f.read()

# Fix 1: Replace datetime.utcnow() with datetime.now(timezone.utc)
content = content.replace('datetime.utcnow()', 'datetime.now(timezone.utc)')

# Fix 2: Update test_bulletin_valid_creation to use 5 articles
old_creation_test = '''    def test_bulletin_valid_creation(self):
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
            llm_usage=LLMUsage(prompt_tokens=100, completion_tokens=200, total_tokens=300),
            processing_time_seconds=0.0
        )
        
        bulletin = Bulletin(
            id="usa-2025-12-15-morning",
            region=RegionEnum.USA,
            date="2025-12-15",
            period=PeriodEnum.MORNING,
            generated_at=datetime.now(timezone.utc),
            version="1.0",
            articles=[article],
            metadata=metadata
        )
        
        assert bulletin.id == "usa-2025-12-15-morning"
        assert bulletin.region == RegionEnum.USA
        assert bulletin.period == PeriodEnum.MORNING
        assert len(bulletin.articles) == 1'''

new_creation_test = '''    def test_bulletin_valid_creation(self):
        """Test creating a valid bulletin with all required fields."""
        # Create 5 articles to meet minimum requirement
        articles = []
        for i in range(5):
            articles.append(Article(
                title=f"Test Article {i+1}",
                summary="This is a test summary with sufficient words here to meet the twenty-word minimum requirement for validation purposes in this test case.",
                category=CategoryEnum.POLITICS,
                source=Source(name="Test Source", url="https://example.com"),
                citations=[Citation(title="Ref", url="https://example.com", publisher="Test")],
                article_id=f"usa-2025-12-15-morning-{i+1:03d}"
            ))
        
        metadata = Metadata(
            article_count=5,
            categories_distribution={"politics": 5},
            llm_usage=LLMUsage(prompt_tokens=100, completion_tokens=200, total_tokens=300),
            processing_time_seconds=0.5
        )
        
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
        
        assert bulletin.id == "usa-2025-12-15-morning"
        assert bulletin.region == RegionEnum.USA
        assert bulletin.period == PeriodEnum.MORNING
        assert len(bulletin.articles) == 5'''

content = content.replace(old_creation_test, new_creation_test)

# Fix 3: Fix test_bulletin_wrapper - change [article] * 5 to unique articles
old_wrapper = '''            articles=[article] * 5,  # Repeat to meet 5 minimum'''
new_wrapper = '''            articles=articles,'''

content = content.replace(old_wrapper, new_wrapper)

# Also need to create the articles list in wrapper test
old_wrapper_setup = '''    def test_bulletin_wrapper(self):
        """Test BulletinWrapper for JSON file structure."""
        article = Article(
            title="Test Article",
            summary="This is a test summary with sufficient words here to meet the twenty-word minimum requirement for validation purposes in this test case.",
            category=CategoryEnum.POLITICS,
            source=Source(name="Test Source", url="https://example.com"),
            citations=[Citation(title="Ref", url="https://example.com", publisher="Test")],
            article_id="usa-2025-12-15-morning-001"
        )
        
        bulletin = Bulletin'''

new_wrapper_setup = '''    def test_bulletin_wrapper(self):
        """Test BulletinWrapper for JSON file structure."""
        # Create 5 unique articles
        articles = []
        for i in range(5):
            articles.append(Article(
                title=f"Test Article {i+1}",
                summary="This is a test summary with sufficient words here to meet the twenty-word minimum requirement for validation purposes in this test case.",
                category=CategoryEnum.POLITICS,
                source=Source(name="Test Source", url="https://example.com"),
                citations=[Citation(title="Ref", url="https://example.com", publisher="Test")],
                article_id=f"usa-2025-12-15-morning-{i+1:03d}"
            ))
        
        bulletin = Bulletin'''

content = content.replace(old_wrapper_setup, new_wrapper_setup)

# Write back
with open(test_file, 'w') as f:
    f.write(content)

print(f"✅ Fixed {test_file}")
print("- Replaced datetime.utcnow() with datetime.now(timezone.utc)")
print("- Updated test_bulletin_valid_creation to use 5 unique articles")
print("- Updated test_bulletin_wrapper to use 5 unique articles")
