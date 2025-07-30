"""
Tests for model classes in the chunk_metadata_adapter.
"""
import uuid
import pytest
from datetime import datetime, timezone
from pydantic import ValidationError

from chunk_metadata_adapter import (
    SemanticChunk,
    FlatSemanticChunk,
    ChunkType,
    ChunkRole,
    ChunkStatus,
    ChunkMetrics,
    FeedbackMetrics
)


def test_chunk_status_enum():
    """Test ChunkStatus enum values and lifecycle stages."""
    # Test basic enum functionality
    assert ChunkStatus.RAW.value == "raw"
    assert ChunkStatus.CLEANED.value == "cleaned"
    assert ChunkStatus.VERIFIED.value == "verified"
    assert ChunkStatus.VALIDATED.value == "validated"
    assert ChunkStatus.RELIABLE.value == "reliable"
    
    # Test other operational statuses
    assert ChunkStatus.NEW.value == "new"
    assert ChunkStatus.INDEXED.value == "indexed"
    assert ChunkStatus.OBSOLETE.value == "obsolete"
    assert ChunkStatus.REJECTED.value == "rejected"
    assert ChunkStatus.IN_PROGRESS.value == "in_progress"
    assert ChunkStatus.NEEDS_REVIEW.value == "needs_review"
    assert ChunkStatus.ARCHIVED.value == "archived"
    
    # Test string to enum conversion
    assert ChunkStatus("raw") == ChunkStatus.RAW
    assert ChunkStatus("cleaned") == ChunkStatus.CLEANED
    assert ChunkStatus("verified") == ChunkStatus.VERIFIED
    assert ChunkStatus("validated") == ChunkStatus.VALIDATED
    assert ChunkStatus("reliable") == ChunkStatus.RELIABLE


def test_chunk_type_enum():
    """Test ChunkType enum values."""
    assert ChunkType.DOC_BLOCK.value == "DocBlock"
    assert ChunkType.CODE_BLOCK.value == "CodeBlock"
    assert ChunkType.MESSAGE.value == "Message"
    assert ChunkType("DocBlock") == ChunkType.DOC_BLOCK


def test_chunk_role_enum():
    """Test ChunkRole enum values."""
    assert ChunkRole.SYSTEM.value == "system"
    assert ChunkRole.USER.value == "user"
    assert ChunkRole.ASSISTANT.value == "assistant"
    assert ChunkRole.DEVELOPER.value == "developer"
    assert ChunkRole("developer") == ChunkRole.DEVELOPER


def test_feedback_metrics():
    """Test FeedbackMetrics model."""
    # Test default values
    metrics = FeedbackMetrics()
    assert metrics.accepted == 0
    assert metrics.rejected == 0
    assert metrics.modifications == 0
    
    # Test custom values
    metrics = FeedbackMetrics(accepted=5, rejected=2, modifications=3)
    assert metrics.accepted == 5
    assert metrics.rejected == 2
    assert metrics.modifications == 3
    
    # Test model dumping
    data = metrics.model_dump()
    assert data == {"accepted": 5, "rejected": 2, "modifications": 3}


def test_chunk_metrics():
    """Test ChunkMetrics model."""
    # Test default values
    metrics = ChunkMetrics()
    assert metrics.quality_score is None
    assert metrics.coverage is None
    assert metrics.matches is None
    assert metrics.used_in_generation is False
    assert metrics.used_as_input is False
    assert metrics.used_as_context is False
    assert isinstance(metrics.feedback, FeedbackMetrics)
    
    # Test custom values
    feedback = FeedbackMetrics(accepted=2, rejected=1)
    metrics = ChunkMetrics(
        quality_score=0.85,
        coverage=0.75,
        matches=10,
        used_in_generation=True,
        feedback=feedback
    )
    assert metrics.quality_score == 0.85
    assert metrics.coverage == 0.75
    assert metrics.matches == 10
    assert metrics.used_in_generation is True
    assert metrics.feedback.accepted == 2
    assert metrics.feedback.rejected == 1


def test_semantic_chunk_validation():
    """Test SemanticChunk validation."""
    # Valid minimal chunk
    valid_chunk = {
        "uuid": str(uuid.uuid4()),
        "type": "DocBlock",
        "text": "Test content",
        "language": "text",
        "sha256": "abcdef1234567890abcdef1234567890",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "start": 0,
        "end": 1
    }
    chunk = SemanticChunk(**valid_chunk)
    assert chunk.uuid == valid_chunk["uuid"]
    assert chunk.type == ChunkType.DOC_BLOCK
    assert chunk.text == "Test content"
    
    # Test default values
    assert chunk.status == ChunkStatus.NEW  # Default is still NEW for direct creation
    assert isinstance(chunk.metrics, ChunkMetrics)
    assert len(chunk.links) == 0
    assert len(chunk.tags) == 0
    
    # Test invalid UUID
    invalid_uuid = valid_chunk.copy()
    invalid_uuid["uuid"] = "not-a-uuid"
    with pytest.raises(ValidationError):
        SemanticChunk(**invalid_uuid)
        
    # Test invalid created_at
    invalid_date = valid_chunk.copy()
    invalid_date["created_at"] = "2023-01-01"  # Missing time and timezone
    with pytest.raises(ValidationError):
        SemanticChunk(**invalid_date)


def test_semantic_chunk_lifecycle():
    """Test SemanticChunk lifecycle status handling."""
    chunk = SemanticChunk(
        uuid=str(uuid.uuid4()),
        type=ChunkType.DOC_BLOCK,
        text="Test lifecycle",
        language="text",
        sha256="abcdef1234567890abcdef1234567890",
        created_at=datetime.now(timezone.utc).isoformat(),
        status=ChunkStatus.RAW,  # Start with RAW status
        start=0,
        end=1
    )
    
    # Verify initial status
    assert chunk.status == ChunkStatus.RAW
    
    # Test status transitions
    chunk.status = ChunkStatus.CLEANED
    assert chunk.status == ChunkStatus.CLEANED
    
    chunk.status = ChunkStatus.VERIFIED
    assert chunk.status == ChunkStatus.VERIFIED
    
    chunk.status = ChunkStatus.VALIDATED
    assert chunk.status == ChunkStatus.VALIDATED
    
    chunk.status = ChunkStatus.RELIABLE
    assert chunk.status == ChunkStatus.RELIABLE
    
    # Test string assignment
    chunk.status = "archived"
    assert chunk.status == ChunkStatus.ARCHIVED


def test_flat_semantic_chunk():
    """Test FlatSemanticChunk model."""
    # Create a flat chunk
    flat = FlatSemanticChunk(
        uuid=str(uuid.uuid4()),
        type="DocBlock",
        text="Test flat chunk",
        language="text",
        sha256="abcdef1234567890abcdef1234567890",
        created_at=datetime.now(timezone.utc).isoformat(),
        status="raw",  # Use RAW status
        start=0,
        end=1
    )
    
    # Test basic properties
    assert flat.type == "DocBlock"
    assert flat.text == "Test flat chunk"
    assert flat.status == "raw"
    
    # Convert to semantic chunk
    semantic = flat.to_semantic_chunk()
    
    # Verify conversion
    assert semantic.uuid == flat.uuid
    assert semantic.type == ChunkType.DOC_BLOCK
    assert semantic.text == flat.text
    assert semantic.status == ChunkStatus.RAW
    
    # Convert back to flat
    restored = FlatSemanticChunk.from_semantic_chunk(semantic)
    
    # Verify round-trip conversion
    assert restored.uuid == flat.uuid
    assert restored.type == flat.type
    assert restored.text == flat.text
    assert restored.status == flat.status


def test_semantic_chunk_with_links_and_tags():
    """Test SemanticChunk with links and tags."""
    parent_id = str(uuid.uuid4())
    related_id = str(uuid.uuid4())
    
    chunk = SemanticChunk(
        uuid=str(uuid.uuid4()),
        type=ChunkType.DOC_BLOCK,
        text="Test with links and tags",
        language="text",
        sha256="abcdef1234567890abcdef1234567890",
        created_at=datetime.now(timezone.utc).isoformat(),
        links=[f"parent:{parent_id}", f"related:{related_id}"],
        tags=["tag1", "tag2", "tag3"],
        start=0,
        end=1
    )
    
    # Test links
    assert len(chunk.links) == 2
    assert f"parent:{parent_id}" in chunk.links
    assert f"related:{related_id}" in chunk.links
    
    # Test tags
    assert len(chunk.tags) == 3
    assert "tag1" in chunk.tags
    assert "tag2" in chunk.tags
    assert "tag3" in chunk.tags
    
    # Test conversion to flat
    flat = FlatSemanticChunk.from_semantic_chunk(chunk)
    assert flat.tags == "tag1,tag2,tag3"
    assert flat.link_parent == parent_id
    assert flat.link_related == related_id
    
    # Test conversion back to semantic
    restored = flat.to_semantic_chunk()
    assert len(restored.links) == 2
    assert f"parent:{parent_id}" in restored.links
    assert f"related:{related_id}" in restored.links
    assert len(restored.tags) == 3 