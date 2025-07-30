"""
Tests for ChunkMetadataBuilder functionality.
"""
import uuid
import pytest
from datetime import datetime
import re
from chunk_metadata_adapter import (
    ChunkMetadataBuilder,
    ChunkType,
    ChunkRole,
    ChunkStatus,
    SemanticChunk,
    FlatSemanticChunk
)


def test_metadata_builder_initialization():
    """Test the initialization of the ChunkMetadataBuilder."""
    # Test default initialization
    builder = ChunkMetadataBuilder()
    assert builder.project is None
    assert builder.unit_id == "chunker"
    assert builder.chunking_version == "1.0"
    
    # Test with custom parameters
    builder = ChunkMetadataBuilder(
        project="TestProject",
        unit_id="custom-chunker",
        chunking_version="2.0"
    )
    assert builder.project == "TestProject"
    assert builder.unit_id == "custom-chunker"
    assert builder.chunking_version == "2.0"


def test_generate_uuid():
    """Test UUID generation."""
    builder = ChunkMetadataBuilder()
    uuid_str = builder.generate_uuid()
    
    # Check UUID format
    uuid_pattern = re.compile(
        r'^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$',
        re.IGNORECASE
    )
    assert uuid_pattern.match(uuid_str)
    
    # Ensure UUIDs are unique
    assert builder.generate_uuid() != builder.generate_uuid()


def test_compute_sha256():
    """Test SHA256 computation."""
    builder = ChunkMetadataBuilder()
    
    # Test with empty string
    assert builder.compute_sha256("") == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    
    # Test with sample text
    assert builder.compute_sha256("test") == "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"
    
    # Test consistency
    assert builder.compute_sha256("hello world") == builder.compute_sha256("hello world")


def test_get_iso_timestamp():
    """Test ISO8601 timestamp generation."""
    builder = ChunkMetadataBuilder()
    timestamp = builder._get_iso_timestamp()
    
    # Check ISO8601 format with timezone
    iso_pattern = re.compile(
        r'^([0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T([2][0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-][0-9]{2}:[0-9]{2})$'
    )
    assert iso_pattern.match(timestamp)
    
    # Ensure timestamp has timezone
    assert timestamp.endswith('Z') or '+' in timestamp or '-' in timestamp


def test_build_flat_metadata():
    """Test building flat metadata."""
    builder = ChunkMetadataBuilder(project="TestProject")
    source_id = str(uuid.uuid4())
    
    # Test basic flat metadata creation
    metadata = builder.build_flat_metadata(
        text="Test content",
        source_id=source_id,
        ordinal=1,
        type=ChunkType.DOC_BLOCK,
        language="text"
    )
    
    # Check required fields
    assert isinstance(metadata["uuid"], str)
    assert metadata["source_id"] == source_id
    assert metadata["ordinal"] == 1
    assert metadata["type"] == "DocBlock"
    assert metadata["language"] == "text"
    assert metadata["text"] == "Test content"
    assert metadata["project"] == "TestProject"
    assert metadata["status"] == "raw"  # Default is now RAW
    assert isinstance(metadata["created_at"], str)
    assert isinstance(metadata["sha256"], str)
    
    # Test with optional parameters
    metadata = builder.build_flat_metadata(
        text="Test with options",
        source_id=source_id,
        ordinal=2,
        type=ChunkType.CODE_BLOCK,
        language="python",
        source_path="test.py",
        source_lines_start=10,
        source_lines_end=20,
        summary="Test summary",
        tags="tag1,tag2",
        role=ChunkRole.DEVELOPER,
        task_id="TASK-123",
        subtask_id="TASK-123-A",
        status=ChunkStatus.VERIFIED
    )
    
    # Check optional fields
    assert metadata["source_path"] == "test.py"
    assert metadata["source_lines_start"] == 10
    assert metadata["source_lines_end"] == 20
    assert metadata["summary"] == "Test summary"
    assert metadata["tags"] == "tag1,tag2"
    assert metadata["role"] == "developer"
    assert metadata["task_id"] == "TASK-123"
    assert metadata["subtask_id"] == "TASK-123-A"
    assert metadata["status"] == "verified"


def test_build_semantic_chunk():
    """Test building semantic chunk."""
    builder = ChunkMetadataBuilder(project="TestProject")
    source_id = str(uuid.uuid4())
    
    # Test basic semantic chunk creation
    chunk = builder.build_semantic_chunk(
        text="Test content",
        language="text",
        type=ChunkType.DOC_BLOCK,
        source_id=source_id,
        start=0,
        end=1
    )
    
    # Check that the result is a SemanticChunk
    assert isinstance(chunk, SemanticChunk)
    
    # Check required fields
    assert isinstance(chunk.uuid, str)
    assert chunk.source_id == source_id
    assert chunk.type == ChunkType.DOC_BLOCK
    assert chunk.language == "text"
    assert chunk.text == "Test content"
    assert chunk.project == "TestProject"
    assert chunk.status == ChunkStatus.RAW  # Default is now RAW
    assert isinstance(chunk.created_at, str)
    assert isinstance(chunk.sha256, str)
    
    # Test with options and string enum values
    chunk = builder.build_semantic_chunk(
        text="Test with options",
        language="python",
        type="CodeBlock",  # String instead of enum
        source_id=source_id,
        summary="Test summary",
        role="developer",  # String instead of enum
        source_path="test.py",
        source_lines=[10, 20],
        ordinal=3,
        task_id="TASK-123",
        subtask_id="TASK-123-A",
        tags=["tag1", "tag2"],
        links=[f"parent:{str(uuid.uuid4())}"],
        status="verified",  # String instead of enum
        start=2,
        end=8
    )
    
    # Check enum conversions
    assert chunk.type == ChunkType.CODE_BLOCK
    assert chunk.role == ChunkRole.DEVELOPER
    assert chunk.status == ChunkStatus.VERIFIED
    
    # Check other optional fields
    assert chunk.summary == "Test summary"
    assert chunk.source_path == "test.py"
    assert chunk.source_lines == [10, 20]
    assert chunk.ordinal == 3
    assert chunk.task_id == "TASK-123"
    assert chunk.subtask_id == "TASK-123-A"
    assert "tag1" in chunk.tags
    assert "tag2" in chunk.tags
    assert len(chunk.links) == 1
    assert chunk.links[0].startswith("parent:")
    assert chunk.start == 2
    assert chunk.end == 8


def test_conversion_between_formats():
    """Test conversion between flat and structured formats."""
    builder = ChunkMetadataBuilder(project="TestProject")
    source_id = str(uuid.uuid4())
    
    # Create a structured chunk
    chunk = builder.build_semantic_chunk(
        text="Test conversion",
        language="text",
        type=ChunkType.DOC_BLOCK,
        source_id=source_id,
        tags=["tag1", "tag2"],
        links=[f"parent:{str(uuid.uuid4())}"],
        start=0,
        end=1
    )
    
    # Convert to flat format
    flat_dict = builder.semantic_to_flat(chunk)
    
    # Check flat representation
    assert flat_dict["uuid"] == chunk.uuid
    assert flat_dict["text"] == chunk.text
    assert flat_dict["tags"] == "tag1,tag2"
    assert flat_dict["link_parent"] is not None
    
    # Convert back to structured
    restored = builder.flat_to_semantic(flat_dict)
    
    # Check restored is equivalent to original
    assert restored.uuid == chunk.uuid
    assert restored.text == chunk.text
    assert restored.type == chunk.type
    assert set(restored.tags) == set(chunk.tags)
    assert len(restored.links) == len(chunk.links)
    assert restored.links[0].startswith("parent:") 