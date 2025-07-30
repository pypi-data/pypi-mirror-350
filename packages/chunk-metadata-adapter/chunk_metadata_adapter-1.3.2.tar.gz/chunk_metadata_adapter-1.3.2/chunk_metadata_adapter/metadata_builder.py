"""
Builder for chunk metadata.

This module provides tools for creating and manipulating chunk metadata
for semantic chunking systems.
"""
import uuid
import hashlib
from typing import Optional, Dict, Any, List, Union
from datetime import datetime, timezone

from .models import (
    SemanticChunk, 
    FlatSemanticChunk, 
    ChunkType, 
    ChunkRole, 
    ChunkStatus,
    ChunkMetrics,
    FeedbackMetrics
)


class ChunkMetadataBuilder:
    """
    Builder for universal chunk metadata.
    
    Used after chunk text is formed to augment it with metadata fields:
    - uuid, sha256, created_at
    - project, status, role, tags, etc.
    
    Supports lifecycle states of data:
    - RAW: initial ingestion of unprocessed data
    - CLEANED: data that has been cleaned and preprocessed
    - VERIFIED: data verified against rules and standards
    - VALIDATED: data validated with cross-references and context
    - RELIABLE: data marked as reliable and ready for use
    
    Supports both flat and structured formats.
    """
    def __init__(
        self, 
        project: Optional[str] = None, 
        unit_id: Optional[str] = None,
        chunking_version: str = "1.0"
    ):
        """
        Initialize a new metadata builder.
        
        Args:
            project: Optional project identifier
            unit_id: Optional identifier for the chunking unit/service
            chunking_version: Version of chunking algorithm used
        """
        self.project = project
        self.unit_id = unit_id or "chunker"
        self.chunking_version = chunking_version

    def generate_uuid(self) -> str:
        """Generate a new UUIDv4 string"""
        return str(uuid.uuid4())

    def compute_sha256(self, text: str) -> str:
        """Compute SHA256 hash of the given text"""
        return hashlib.sha256(text.encode("utf-8")).hexdigest()
        
    def _get_iso_timestamp(self) -> str:
        """Get current timestamp in ISO8601 format with UTC timezone"""
        return datetime.now(timezone.utc).isoformat()

    def build_flat_metadata(
        self, *,
        text: str,
        source_id: str,
        ordinal: int,
        type: Union[str, ChunkType],
        language: str,
        source_path: Optional[str] = None,
        source_lines_start: Optional[int] = None,
        source_lines_end: Optional[int] = None,
        summary: Optional[str] = None,
        tags: Optional[str] = None,
        role: Optional[Union[str, ChunkRole]] = None,
        task_id: Optional[str] = None,
        subtask_id: Optional[str] = None,
        link_parent: Optional[str] = None,
        link_related: Optional[str] = None,
        status: Union[str, ChunkStatus] = ChunkStatus.RAW,  # Default changed to RAW for new lifecycle
        # New quality metrics (optional, range 0-1)
        coverage: Optional[float] = None,
        cohesion: Optional[float] = None,
        boundary_prev: Optional[float] = None,
        boundary_next: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Build chunk metadata in a flat dictionary format.
        
        Args:
            text: The text content of the chunk
            source_id: Identifier of the source (file, document, dialogue)
            ordinal: Order of the chunk within the source
            type: Type of the chunk (see ChunkType)
            language: Programming or natural language of the content
            source_path: Optional path to the source file
            source_lines_start: Start line in source file
            source_lines_end: End line in source file
            summary: Brief summary of the chunk content
            tags: Comma-separated tags
            role: Role of the content creator
            task_id: Task identifier
            subtask_id: Subtask identifier
            link_parent: UUID of the parent chunk
            link_related: UUID of a related chunk
            status: Processing status of the chunk (default: RAW for initial data ingestion)
                   See ChunkStatus for lifecycle states (RAW, CLEANED, VERIFIED, VALIDATED, RELIABLE)
            
        Returns:
            Dictionary with flat metadata
        """
        # Verify UUIDs
        if not isinstance(source_id, str) or not uuid.UUID(source_id, version=4):
            raise ValueError(f"source_id must be a valid UUIDv4 string: {source_id}")
            
        if link_parent is not None and (not isinstance(link_parent, str) or not uuid.UUID(link_parent, version=4)):
            raise ValueError(f"link_parent must be a valid UUIDv4 string: {link_parent}")
            
        if link_related is not None and (not isinstance(link_related, str) or not uuid.UUID(link_related, version=4)):
            raise ValueError(f"link_related must be a valid UUIDv4 string: {link_related}")
        
        # Convert enum types to string values if needed
        if isinstance(type, ChunkType):
            type = type.value
        if isinstance(role, ChunkRole):
            role = role.value
        if isinstance(status, ChunkStatus):
            status = status.value
            
        return {
            "uuid": self.generate_uuid(),
            "source_id": source_id,
            "ordinal": ordinal,
            "sha256": self.compute_sha256(text),
            "text": text,
            "summary": summary,
            "language": language,
            "type": type,
            "source_path": source_path,
            "source_lines_start": source_lines_start,
            "source_lines_end": source_lines_end,
            "project": self.project,
            "task_id": task_id,
            "subtask_id": subtask_id,
            "status": status,
            "unit_id": self.unit_id,
            "created_at": self._get_iso_timestamp(),
            "tags": tags,
            "role": role,
            "link_parent": link_parent,
            "link_related": link_related,
            "quality_score": None,
            "coverage": coverage,
            "cohesion": cohesion,
            "boundary_prev": boundary_prev,
            "boundary_next": boundary_next,
            "used_in_generation": False,
            "feedback_accepted": 0,
            "feedback_rejected": 0
        }
        
    # Alias for backward compatibility
    build_metadata = build_flat_metadata

    def build_semantic_chunk(
        self, *,
        text: str,
        language: str,
        type: Union[str, ChunkType],
        source_id: Optional[str] = None,
        summary: Optional[str] = None,
        role: Optional[Union[str, ChunkRole]] = None,
        source_path: Optional[str] = None,
        source_lines: Optional[List[int]] = None,
        ordinal: Optional[int] = None,
        task_id: Optional[str] = None,
        subtask_id: Optional[str] = None,
        links: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        status: Union[str, ChunkStatus] = ChunkStatus.RAW,
        metrics: Optional[ChunkMetrics] = None,
        coverage: Optional[float] = None,
        cohesion: Optional[float] = None,
        boundary_prev: Optional[float] = None,
        boundary_next: Optional[float] = None,
        start: Optional[int] = None,
        end: Optional[int] = None,
    ) -> SemanticChunk:
        """
        Build a fully-structured SemanticChunk object.
        
        Args:
            text: The text content of the chunk
            language: Programming or natural language of the content
            type: Type of the chunk
            source_id: Optional identifier of the source
            summary: Brief summary of the chunk content
            role: Role of the content creator
            source_path: Optional path to the source file
            source_lines: List of line numbers [start, end]
            ordinal: Order of the chunk within the source
            task_id: Task identifier
            subtask_id: Subtask identifier
            links: List of links to other chunks (format: "relation:uuid")
            tags: List of tags
            status: Processing status of the chunk (default: RAW for initial data ingestion)
                   The data lifecycle includes these states:
                   - RAW: Initial raw data as ingested into the system
                   - CLEANED: Data after cleaning and preprocessing
                   - VERIFIED: Data verified against rules and standards
                   - VALIDATED: Data validated with cross-references
                   - RELIABLE: Data ready for use in critical systems
            start: Start offset of the chunk in the source text (in bytes or characters)
            end: End offset of the chunk in the source text (in bytes or characters)
            
        Returns:
            Fully populated SemanticChunk instance
        """
        # Verify UUIDs
        if source_id is not None and (not isinstance(source_id, str) or not uuid.UUID(source_id, version=4)):
            raise ValueError(f"source_id must be a valid UUIDv4 string: {source_id}")
            
        # Validate links format and UUIDs
        if links:
            for link in links:
                parts = link.split(":", 1)
                if len(parts) != 2 or not parts[0] or not parts[1]:
                    raise ValueError(f"Link must follow 'relation:uuid' format: {link}")
                try:
                    uuid.UUID(parts[1], version=4)
                except (ValueError, AttributeError):
                    raise ValueError(f"Invalid UUID4 in link: {link}")
        
        # Convert string types to enums if needed
        if isinstance(type, str):
            type = ChunkType(type)
        if isinstance(role, str) and role:
            role = ChunkRole(role)
        if isinstance(status, str):
            # Case-insensitive mapping handled by Enum _missing_
            status = ChunkStatus(status)
            
        # Prepare metrics
        if metrics is None:
            metrics = ChunkMetrics(
                coverage=coverage,
                cohesion=cohesion,
                boundary_prev=boundary_prev,
                boundary_next=boundary_next,
            )

        return SemanticChunk(
            uuid=self.generate_uuid(),
            source_id=source_id,
            project=self.project,
            task_id=task_id,
            subtask_id=subtask_id,
            unit_id=self.unit_id,
            type=type,
            role=role,
            language=language,
            text=text,
            summary=summary,
            source_path=source_path,
            source_lines=source_lines,
            ordinal=ordinal,
            sha256=self.compute_sha256(text),
            chunking_version=self.chunking_version,
            status=status,
            links=links or [],
            tags=tags or [],
            metrics=metrics,
            created_at=self._get_iso_timestamp(),
            start=start,
            end=end,
        )

    def flat_to_semantic(self, flat_chunk: Dict[str, Any]) -> SemanticChunk:
        """Convert flat dictionary metadata to SemanticChunk model"""
        flat_model = FlatSemanticChunk(**flat_chunk)
        semantic = flat_model.to_semantic_chunk()
        if flat_model.start is not None:
            semantic.start = flat_model.start
        if flat_model.end is not None:
            semantic.end = flat_model.end
        return semantic
    
    def semantic_to_flat(self, chunk: SemanticChunk) -> Dict[str, Any]:
        """Convert SemanticChunk model to flat dictionary format"""
        flat_model = FlatSemanticChunk.from_semantic_chunk(chunk)
        flat_model.start = getattr(chunk, 'start', None)
        flat_model.end = getattr(chunk, 'end', None)
        return flat_model.model_dump()
