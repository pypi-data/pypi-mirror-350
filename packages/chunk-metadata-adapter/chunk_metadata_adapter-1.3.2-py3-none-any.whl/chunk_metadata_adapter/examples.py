"""
Examples of how to use the Chunk Metadata Adapter.

This module contains practical examples for various use cases.
"""
import uuid

from chunk_metadata_adapter import (
    ChunkMetadataBuilder,
    SemanticChunk,
    FlatSemanticChunk,
    ChunkType,
    ChunkRole,
    ChunkStatus
)


def example_basic_flat_metadata():
    """Example of creating basic flat metadata for a chunk."""
    # Create a builder instance for a specific project
    builder = ChunkMetadataBuilder(project="MyProject", unit_id="chunker-service-1")
    
    # Generate UUID for the source document
    source_id = str(uuid.uuid4())
    
    # Create metadata for a piece of code
    metadata = builder.build_flat_metadata(
        text="def hello_world():\n    print('Hello, World!')",
        source_id=source_id,
        ordinal=1,  # First chunk in the document
        type=ChunkType.CODE_BLOCK,  # Using enum
        language="python",
        source_path="src/hello.py",
        source_lines_start=10,
        source_lines_end=12,
        tags="example,hello",
        role=ChunkRole.DEVELOPER
    )
    
    # Access the metadata
    print(f"Generated UUID: {metadata['uuid']}")
    print(f"SHA256: {metadata['sha256']}")
    print(f"Created at: {metadata['created_at']}")
    
    return metadata


def example_structured_chunk():
    """Example of creating a structured SemanticChunk instance."""
    # Create a builder for a project with task
    builder = ChunkMetadataBuilder(
        project="DocumentationProject",
        unit_id="docs-generator"
    )
    
    # Generate a source document ID
    source_id = str(uuid.uuid4())
    
    # Create a structured chunk 
    chunk = builder.build_semantic_chunk(
        text="# Introduction\n\nThis is the documentation for the system.",
        language="markdown",
        type=ChunkType.DOC_BLOCK,
        source_id=source_id,
        summary="Project introduction section",
        role=ChunkRole.DEVELOPER,
        source_path="docs/intro.md",
        source_lines=[1, 3],
        ordinal=0,
        task_id="DOC-123",
        subtask_id="DOC-123-A",
        tags=["introduction", "documentation", "overview"],
        links=[f"parent:{str(uuid.uuid4())}"],
        start=0,
        end=56
    )
    
    # Access the data
    print(f"Chunk UUID: {chunk.uuid}")
    print(f"Content summary: {chunk.summary}")
    print(f"Links: {chunk.links}")
    
    return chunk


def example_conversion_between_formats():
    """Example of converting between structured and flat formats."""
    # Create a builder instance
    builder = ChunkMetadataBuilder(project="ConversionExample")
    
    # Start with a structured chunk
    structured_chunk = builder.build_semantic_chunk(
        text="This is a sample chunk for conversion demonstration.",
        language="text",
        type=ChunkType.COMMENT,
        source_id=str(uuid.uuid4()),
        role=ChunkRole.REVIEWER,
        start=0,
        end=1
    )
    
    # Convert to flat dictionary
    flat_dict = builder.semantic_to_flat(structured_chunk)
    print(f"Flat representation has {len(flat_dict)} fields")
    
    # Convert back to structured format
    restored_chunk = builder.flat_to_semantic(flat_dict)
    print(f"Restored structured chunk: {restored_chunk.uuid}")
    
    # Verify they're equivalent
    assert restored_chunk.uuid == structured_chunk.uuid
    assert restored_chunk.text == structured_chunk.text
    assert restored_chunk.type == structured_chunk.type
    
    return {
        "original": structured_chunk,
        "flat": flat_dict,
        "restored": restored_chunk
    }


def example_chain_processing():
    """Example of a chain of processing for document chunks."""
    # Create a document with multiple chunks
    builder = ChunkMetadataBuilder(project="ChainExample", unit_id="processor")
    source_id = str(uuid.uuid4())
    
    # Create a sequence of chunks from a document
    chunks = []
    for i, text in enumerate([
        "# Document Title",
        "## Section 1\n\nThis is the content of section 1.",
        "## Section 2\n\nThis is the content of section 2.",
        "## Conclusion\n\nFinal thoughts on the topic."
    ]):
        chunk = builder.build_semantic_chunk(
            text=text,
            language="markdown",
            type=ChunkType.DOC_BLOCK,
            source_id=source_id,
            ordinal=i,
            summary=f"Section {i}" if i > 0 else "Title",
            start=0,
            end=1
        )
        chunks.append(chunk)
    
    # Create explicit links between chunks (parent-child relationships)
    for i in range(1, len(chunks)):
        # Add parent link to the title chunk
        chunks[i].links.append(f"parent:{chunks[0].uuid}")
        # Update status to show progress
        chunks[i].status = ChunkStatus.INDEXED
    
    # Simulate processing and updating metrics
    for chunk in chunks:
        # Update metrics based on some processing
        chunk.metrics.quality_score = 0.95
        chunk.metrics.used_in_generation = True
        chunk.metrics.matches = 3
        
        # Add feedback
        chunk.metrics.feedback.accepted = 2
        
    # Print the processed chain
    print(f"Processed {len(chunks)} chunks from source {source_id}")
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i}: {chunk.summary} - Status: {chunk.status.value}")
    
    return chunks


def example_data_lifecycle():
    """
    Example of data lifecycle processing from raw to reliable data.
    
    This example demonstrates the transition of data through the following stages:
    1. RAW - Initial ingestion of raw, unprocessed data
    2. CLEANED - Data that has been cleaned and preprocessed
    3. VERIFIED - Data verified against rules and standards
    4. VALIDATED - Data validated with cross-references and context
    5. RELIABLE - Reliable data ready for use in critical systems
    """
    # Create a builder instance
    builder = ChunkMetadataBuilder(project="DataLifecycleDemo", unit_id="data-processor")
    source_id = str(uuid.uuid4())
    
    # Step 1: Create a chunk with RAW status - initial data ingestion
    raw_chunk = builder.build_semantic_chunk(
        text="Customer data: John Doe, jdoe@eample.com, 123-456-7890, New York",
        language="text",
        type=ChunkType.DOC_BLOCK,
        source_id=source_id,
        status=ChunkStatus.RAW,  # Mark as raw data
        summary="Customer contact information",
        tags=["customer", "contact", "personal"],
        start=0,
        end=1
    )
    print(f"RAW data created: {raw_chunk.uuid} (Status: {raw_chunk.status.value})")
    
    # Step 2: Clean the data (fix formatting, typos, etc.)
    cleaned_chunk = SemanticChunk(**raw_chunk.model_dump())
    cleaned_chunk.text = "Customer data: John Doe, jdoe@example.com, 123-456-7890, New York"  # Fixed email typo
    cleaned_chunk.status = ChunkStatus.CLEANED
    print(f"Data CLEANED: {cleaned_chunk.uuid} (Status: {cleaned_chunk.status.value})")
    
    # Step 3: Verify the data against rules (email format, phone number format)
    verified_chunk = SemanticChunk(**cleaned_chunk.model_dump())
    verified_chunk.status = ChunkStatus.VERIFIED
    # Add verification metadata
    verified_chunk.tags.append("verified_email")
    verified_chunk.tags.append("verified_phone")
    print(f"Data VERIFIED: {verified_chunk.uuid} (Status: {verified_chunk.status.value})")
    
    # Step 4: Validate data with cross-references
    validated_chunk = SemanticChunk(**verified_chunk.model_dump())
    validated_chunk.status = ChunkStatus.VALIDATED
    # Add reference to CRM system where this was cross-checked
    validated_chunk.links.append(f"reference:{str(uuid.uuid4())}")
    validated_chunk.tags.append("crm_validated")
    print(f"Data VALIDATED: {validated_chunk.uuid} (Status: {validated_chunk.status.value})")
    
    # Step 5: Mark as reliable data, ready for use in critical systems
    reliable_chunk = SemanticChunk(**validated_chunk.model_dump())
    reliable_chunk.status = ChunkStatus.RELIABLE
    reliable_chunk.metrics.quality_score = 0.98  # High quality score
    print(f"Data marked as RELIABLE: {reliable_chunk.uuid} (Status: {reliable_chunk.status.value})")
    
    return {
        "raw": raw_chunk,
        "cleaned": cleaned_chunk,
        "verified": verified_chunk,
        "validated": validated_chunk,
        "reliable": reliable_chunk
    }


def example_metrics_extension():
    """Example of using extended metrics fields in chunk creation."""
    builder = ChunkMetadataBuilder(project="MetricsDemo", unit_id="metrics-unit")
    source_id = str(uuid.uuid4())
    chunk = builder.build_semantic_chunk(
        text="Sample text for metrics.",
        language="text",
        type=ChunkType.DOC_BLOCK,
        source_id=source_id,
        status=ChunkStatus.RELIABLE,
        coverage=0.95,
        cohesion=0.8,
        boundary_prev=0.7,
        boundary_next=0.9,
        start=0,
        end=1
    )
    print(f"Chunk with extended metrics: {chunk.metrics}")
    return chunk


if __name__ == "__main__":
    print("Running examples...")
    example_basic_flat_metadata()
    example_structured_chunk()
    example_conversion_between_formats()
    example_chain_processing()
    example_data_lifecycle()
    example_metrics_extension()
    print("All examples completed.") 