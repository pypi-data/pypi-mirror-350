"""
Chunk Metadata Adapter - A package for managing metadata for chunked content.

This package provides tools for creating, managing, and converting metadata 
for chunks of content in various systems, including RAG pipelines, document 
processing, and machine learning training datasets.
"""

from .metadata_builder import ChunkMetadataBuilder
from .models import (
    SemanticChunk,
    FlatSemanticChunk,
    ChunkType,
    ChunkRole,
    ChunkStatus,
    ChunkMetrics,
    FeedbackMetrics
)

__version__ = "1.3.0"
__all__ = [
    "ChunkMetadataBuilder",
    "SemanticChunk",
    "FlatSemanticChunk",
    "ChunkType",
    "ChunkRole",
    "ChunkStatus",
    "ChunkMetrics",
    "FeedbackMetrics",
]
