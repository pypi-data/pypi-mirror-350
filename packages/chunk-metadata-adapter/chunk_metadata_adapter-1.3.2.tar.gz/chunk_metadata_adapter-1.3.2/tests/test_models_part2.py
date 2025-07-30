"""
Tests for the data models (part 2).
"""
import re
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


class TestSemanticChunk:
    """Tests for SemanticChunk model"""
    
    def test_uuid_validation(self):
        """Test UUID validation"""
        # Valid UUID should pass
        valid_uuid = str(uuid.uuid4())
        chunk = SemanticChunk(
            uuid=valid_uuid,
            type=ChunkType.DOC_BLOCK,
            text="Test content",
            language="markdown",
            sha256="a" * 64,
            start=0,
            end=1
        )
        assert chunk.uuid == valid_uuid
        
        # Invalid UUIDs should fail
        with pytest.raises(ValidationError):
            SemanticChunk(
                uuid="invalid-uuid",
                type=ChunkType.DOC_BLOCK,
                text="Test content",
                language="markdown",
                sha256="a" * 64,
                start=0,
                end=1
            )
            
        # Non-version 4 UUIDs should fail
        non_v4_uuid = str(uuid.uuid1())
        with pytest.raises(ValidationError):
            SemanticChunk(
                uuid=non_v4_uuid.replace("-4", "-1"),  # Force version 1
                type=ChunkType.DOC_BLOCK,
                text="Test content",
                language="markdown",
                sha256="a" * 64,
                start=0,
                end=1
            )
            
    def test_timestamp_validation(self):
        """Test timestamp validation"""
        # Valid ISO timestamp with timezone should pass
        valid_timestamp = datetime.now(timezone.utc).isoformat()
        chunk = SemanticChunk(
            uuid=str(uuid.uuid4()),
            type=ChunkType.DOC_BLOCK,
            text="Test content",
            language="markdown",
            sha256="a" * 64,
            created_at=valid_timestamp,
            start=0,
            end=1
        )
        assert chunk.created_at == valid_timestamp
        
        # ISO timestamp without timezone should fail
        with pytest.raises(ValidationError):
            SemanticChunk(
                uuid=str(uuid.uuid4()),
                type=ChunkType.DOC_BLOCK,
                text="Test content",
                language="markdown",
                sha256="a" * 64,
                created_at="2023-01-01T12:00:00",  # No timezone
                start=0,
                end=1
            )
            
        # Invalid format should fail
        with pytest.raises(ValidationError):
            SemanticChunk(
                uuid=str(uuid.uuid4()),
                type=ChunkType.DOC_BLOCK,
                text="Test content",
                language="markdown",
                sha256="a" * 64,
                created_at="01/01/2023 12:00:00",  # Invalid format
                start=0,
                end=1
            )
            
    def test_links_validation(self):
        """Test links validation"""
        # Valid link should pass
        valid_link = f"parent:{str(uuid.uuid4())}"
        chunk = SemanticChunk(
            uuid=str(uuid.uuid4()),
            type=ChunkType.DOC_BLOCK,
            text="Test content",
            language="markdown",
            sha256="a" * 64,
            links=[valid_link],
            start=0,
            end=1
        )
        assert chunk.links[0] == valid_link
        
        # Invalid link format should fail
        with pytest.raises(ValidationError):
            SemanticChunk(
                uuid=str(uuid.uuid4()),
                type=ChunkType.DOC_BLOCK,
                text="Test content",
                language="markdown",
                sha256="a" * 64,
                links=["invalid-link-format"],
                start=0,
                end=1
            )
            
        # Link with invalid UUID should fail
        with pytest.raises(ValidationError):
            SemanticChunk(
                uuid=str(uuid.uuid4()),
                type=ChunkType.DOC_BLOCK,
                text="Test content",
                language="markdown",
                sha256="a" * 64,
                links=[f"parent:invalid-uuid"],
                start=0,
                end=1
            )


class TestFlatSemanticChunk:
    """Tests for FlatSemanticChunk model"""
    
    def test_minimal_initialization(self):
        """Test initialization with minimal required fields"""
        uuid_val = str(uuid.uuid4())
        chunk = FlatSemanticChunk(
            uuid=uuid_val,
            type="DocBlock",
            text="Test content",
            language="markdown",
            sha256="a" * 64,
            created_at=datetime.now(timezone.utc).isoformat(),
            start=0,
            end=1
        )
        
        assert chunk.uuid == uuid_val
        assert chunk.type == "DocBlock"
        assert chunk.text == "Test content"
        assert chunk.language == "markdown"
        assert chunk.sha256 == "a" * 64
        
        # Check defaults
        assert chunk.source_id is None
        assert chunk.project is None
        assert chunk.task_id is None
        assert chunk.subtask_id is None
        assert chunk.unit_id is None
        assert chunk.role is None
        assert chunk.summary is None
        assert chunk.ordinal is None
        assert chunk.status == "new"
        assert chunk.source_path is None
        assert chunk.source_lines_start is None
        assert chunk.source_lines_end is None
        assert chunk.tags is None
        assert chunk.link_related is None
        assert chunk.link_parent is None
        assert chunk.quality_score is None
        assert chunk.used_in_generation is False
        assert chunk.feedback_accepted == 0
        assert chunk.feedback_rejected == 0
        
    def test_full_initialization(self):
        """Test initialization with all fields"""
        uuid_val = str(uuid.uuid4())
        source_id = str(uuid.uuid4())
        parent_id = str(uuid.uuid4())
        related_id = str(uuid.uuid4())
        timestamp = datetime.now(timezone.utc).isoformat()
        
        chunk = FlatSemanticChunk(
            uuid=uuid_val,
            source_id=source_id,
            project="TestProject",
            task_id="T-001",
            subtask_id="T-001-A",
            unit_id="test-unit",
            type="CodeBlock",
            role="developer",
            language="python",
            text="def test():\n    pass",
            summary="Test function",
            ordinal=5,
            sha256="b" * 64,
            created_at=timestamp,
            status="verified",
            source_path="src/test.py",
            source_lines_start=10,
            source_lines_end=11,
            tags="test,example",
            link_parent=parent_id,
            link_related=related_id,
            quality_score=0.9,
            used_in_generation=True,
            feedback_accepted=3,
            feedback_rejected=1,
            start=0,
            end=1
        )
        
        assert chunk.uuid == uuid_val
        assert chunk.source_id == source_id
        assert chunk.project == "TestProject"
        assert chunk.task_id == "T-001"
        assert chunk.subtask_id == "T-001-A"
        assert chunk.unit_id == "test-unit"
        assert chunk.type == "CodeBlock"
        assert chunk.role == "developer"
        assert chunk.language == "python"
        assert chunk.text == "def test():\n    pass"
        assert chunk.summary == "Test function"
        assert chunk.ordinal == 5
        assert chunk.sha256 == "b" * 64
        assert chunk.created_at == timestamp
        assert chunk.status == "verified"
        assert chunk.source_path == "src/test.py"
        assert chunk.source_lines_start == 10
        assert chunk.source_lines_end == 11
        assert chunk.tags == "test,example"
        assert chunk.link_parent == parent_id
        assert chunk.link_related == related_id
        assert chunk.quality_score == 0.9
        assert chunk.used_in_generation is True
        assert chunk.feedback_accepted == 3
        assert chunk.feedback_rejected == 1
        
    def test_conversion_to_semantic(self):
        """Test conversion from flat to semantic format"""
        uuid_val = str(uuid.uuid4())
        source_id = str(uuid.uuid4())
        parent_id = str(uuid.uuid4())
        timestamp = datetime.now(timezone.utc).isoformat()
        
        flat_chunk = FlatSemanticChunk(
            uuid=uuid_val,
            source_id=source_id,
            project="TestProject",
            type="DocBlock",
            language="markdown",
            text="Test content",
            summary="Test summary",
            sha256="c" * 64,
            created_at=timestamp,
            link_parent=parent_id,
            tags="tag1,tag2",
            start=7,
            end=42
        )
        
        # Convert to semantic format
        semantic_chunk = flat_chunk.to_semantic_chunk()
        
        assert isinstance(semantic_chunk, SemanticChunk)
        assert semantic_chunk.uuid == uuid_val
        assert semantic_chunk.source_id == source_id
        assert semantic_chunk.project == "TestProject"
        assert semantic_chunk.type == ChunkType.DOC_BLOCK
        assert semantic_chunk.language == "markdown"
        assert semantic_chunk.text == "Test content"
        assert semantic_chunk.summary == "Test summary"
        assert semantic_chunk.sha256 == "c" * 64
        assert semantic_chunk.created_at == timestamp
        assert len(semantic_chunk.links) == 1
        assert semantic_chunk.links[0] == f"parent:{parent_id}"
        assert len(semantic_chunk.tags) == 2
        assert "tag1" in semantic_chunk.tags
        assert "tag2" in semantic_chunk.tags
        assert semantic_chunk.start == 7
        assert semantic_chunk.end == 42
        
    def test_conversion_from_semantic(self):
        """Test conversion from semantic to flat format"""
        uuid_val = str(uuid.uuid4())
        source_id = str(uuid.uuid4())
        related_id = str(uuid.uuid4())
        timestamp = datetime.now(timezone.utc).isoformat()
        
        semantic_chunk = SemanticChunk(
            uuid=uuid_val,
            source_id=source_id,
            project="TestProject",
            type=ChunkType.CODE_BLOCK,
            language="python",
            text="def convert():\n    pass",
            summary="Conversion function",
            sha256="d" * 64,
            created_at=timestamp,
            links=[f"related:{related_id}"],
            tags=["python", "code"],
            start=0,
            end=1
        )
        
        # Convert to flat format
        flat_chunk = FlatSemanticChunk.from_semantic_chunk(semantic_chunk)
        
        assert isinstance(flat_chunk, FlatSemanticChunk)
        assert flat_chunk.uuid == uuid_val
        assert flat_chunk.source_id == source_id
        assert flat_chunk.project == "TestProject"
        assert flat_chunk.type == "CodeBlock"
        assert flat_chunk.language == "python"
        assert flat_chunk.text == "def convert():\n    pass"
        assert flat_chunk.summary == "Conversion function"
        assert flat_chunk.sha256 == "d" * 64
        assert flat_chunk.created_at == timestamp
        assert flat_chunk.link_related == related_id
        assert flat_chunk.link_parent is None
        assert flat_chunk.tags == "python,code"
        
    def test_uuid_validation(self):
        """Test UUID validation"""
        # Valid UUID should pass
        valid_uuid = str(uuid.uuid4())
        chunk = FlatSemanticChunk(
            uuid=valid_uuid,
            type="DocBlock",
            text="Test content",
            language="markdown",
            sha256="a" * 64,
            created_at=datetime.now(timezone.utc).isoformat(),
            start=0,
            end=1
        )
        assert chunk.uuid == valid_uuid
        
        # Invalid UUIDs should fail
        with pytest.raises(ValidationError):
            FlatSemanticChunk(
                uuid="invalid-uuid",
                type="DocBlock",
                text="Test content",
                language="markdown",
                sha256="a" * 64,
                created_at=datetime.now(timezone.utc).isoformat(),
                start=0,
                end=1
            )
            
    def test_timestamp_validation(self):
        """Test timestamp validation"""
        # Valid ISO timestamp with timezone should pass
        valid_timestamp = datetime.now(timezone.utc).isoformat()
        chunk = FlatSemanticChunk(
            uuid=str(uuid.uuid4()),
            type="DocBlock",
            text="Test content",
            language="markdown",
            sha256="a" * 64,
            created_at=valid_timestamp,
            start=0,
            end=1
        )
        assert chunk.created_at == valid_timestamp
        
        # ISO timestamp without timezone should fail
        with pytest.raises(ValidationError):
            FlatSemanticChunk(
                uuid=str(uuid.uuid4()),
                type="DocBlock",
                text="Test content",
                language="markdown",
                sha256="a" * 64,
                created_at="2023-01-01T12:00:00",  # No timezone
                start=0,
                end=1
            )
            
    def test_link_uuid_validation(self):
        """Test link UUID validation"""
        # Valid UUIDs should pass
        valid_uuid = str(uuid.uuid4())
        chunk = FlatSemanticChunk(
            uuid=str(uuid.uuid4()),
            type="DocBlock",
            text="Test content",
            language="markdown",
            sha256="a" * 64,
            created_at=datetime.now(timezone.utc).isoformat(),
            link_parent=valid_uuid,
            start=0,
            end=1
        )
        assert chunk.link_parent == valid_uuid
        
        # Invalid UUIDs should fail
        with pytest.raises(ValidationError):
            FlatSemanticChunk(
                uuid=str(uuid.uuid4()),
                type="DocBlock",
                text="Test content",
                language="markdown",
                sha256="a" * 64,
                created_at=datetime.now(timezone.utc).isoformat(),
                link_related="invalid-uuid",
                start=0,
                end=1
            ) 