"""
Tests for examples from the examples.py module.
"""
import uuid
import pytest
from chunk_metadata_adapter import (
    ChunkMetadataBuilder,
    ChunkType,
    ChunkRole,
    ChunkStatus,
    SemanticChunk
)
from chunk_metadata_adapter.examples import (
    example_basic_flat_metadata,
    example_structured_chunk,
    example_conversion_between_formats,
    example_chain_processing,
    example_data_lifecycle
)


def test_example_basic_flat_metadata():
    """Test the basic flat metadata example."""
    metadata = example_basic_flat_metadata()
    
    # Check that the example returns valid metadata
    assert isinstance(metadata, dict)
    assert "uuid" in metadata
    assert "sha256" in metadata
    assert "text" in metadata
    assert metadata["type"] == "CodeBlock"
    assert metadata["language"] == "python"


def test_example_structured_chunk():
    """Test the structured chunk example."""
    chunk = example_structured_chunk()
    
    # Check that the example returns a valid chunk
    assert isinstance(chunk, SemanticChunk)
    assert chunk.type == ChunkType.DOC_BLOCK
    assert chunk.language == "markdown"
    assert chunk.summary == "Project introduction section"
    assert len(chunk.links) == 1
    assert chunk.links[0].startswith("parent:")


def test_example_conversion_between_formats():
    """Test the conversion between formats example."""
    result = example_conversion_between_formats()
    
    # Check that the example returns all expected components
    assert "original" in result
    assert "flat" in result
    assert "restored" in result
    
    # Check that conversions maintain integrity
    original = result["original"]
    flat = result["flat"]
    restored = result["restored"]
    
    assert original.uuid == restored.uuid
    assert original.text == restored.text
    assert original.type == restored.type


def test_example_chain_processing():
    """Test the chain processing example."""
    chunks = example_chain_processing()
    
    # Check that the example returns a list of chunks
    assert isinstance(chunks, list)
    assert len(chunks) > 0
    
    # Check chunk relationships and processing
    title_chunk = chunks[0]
    assert title_chunk.ordinal == 0
    
    # Check that all other chunks point to the title
    for i in range(1, len(chunks)):
        child_chunk = chunks[i]
        assert any(link.startswith(f"parent:{title_chunk.uuid}") for link in child_chunk.links)
        assert child_chunk.status == ChunkStatus.INDEXED
        
    # Check metrics were updated
    for chunk in chunks:
        assert chunk.metrics.quality_score is not None
        assert chunk.metrics.used_in_generation is True
        assert chunk.metrics.matches is not None
        assert chunk.metrics.feedback.accepted > 0


def test_example_data_lifecycle():
    """Test the data lifecycle example."""
    result = example_data_lifecycle()
    
    # Check that all lifecycle stages are present
    assert "raw" in result
    assert "cleaned" in result
    assert "verified" in result
    assert "validated" in result
    assert "reliable" in result
    
    # Check the progression of statuses
    assert result["raw"].status == ChunkStatus.RAW
    assert result["cleaned"].status == ChunkStatus.CLEANED
    assert result["verified"].status == ChunkStatus.VERIFIED
    assert result["validated"].status == ChunkStatus.VALIDATED
    assert result["reliable"].status == ChunkStatus.RELIABLE
    
    # Check that all chunks have the same UUID (representing the same data evolving)
    uuid = result["raw"].uuid
    for stage in ["cleaned", "verified", "validated", "reliable"]:
        assert result[stage].uuid == uuid
    
    # Check that the text was corrected (fixed typo)
    assert "eample.com" in result["raw"].text
    assert "example.com" in result["cleaned"].text
    
    # Check that verification tags were added
    assert "verified_email" in result["verified"].tags
    
    # Check that validation added references
    assert any(link.startswith("reference:") for link in result["validated"].links)
    
    # Check that reliable data has a quality score
    assert result["reliable"].metrics.quality_score is not None
    assert result["reliable"].metrics.quality_score > 0.9 