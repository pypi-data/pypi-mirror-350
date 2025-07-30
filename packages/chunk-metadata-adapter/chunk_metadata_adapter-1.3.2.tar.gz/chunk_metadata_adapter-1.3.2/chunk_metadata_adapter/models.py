"""
Models for chunk metadata representation using Pydantic.
"""
from enum import Enum
from typing import List, Dict, Optional, Union, Any, Pattern
import re
import uuid
from datetime import datetime, timezone
from pydantic import BaseModel, Field, validator, field_validator


# UUID4 регулярное выражение для валидации
UUID4_PATTERN: Pattern = re.compile(
    r'^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$',
    re.IGNORECASE
)

# ISO 8601 с таймзоной
ISO8601_PATTERN: Pattern = re.compile(
    r'^([0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T([2][0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-][0-9]{2}:[0-9]{2})$'
)


class ChunkType(str, Enum):
    """Types of semantic chunks"""
    DOC_BLOCK = "DocBlock"
    CODE_BLOCK = "CodeBlock"
    MESSAGE = "Message"
    DRAFT = "Draft"
    TASK = "Task"
    SUBTASK = "Subtask"
    TZ = "TZ"
    COMMENT = "Comment"
    LOG = "Log"
    METRIC = "Metric"


class ChunkRole(str, Enum):
    """Roles in the system"""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"
    REVIEWER = "reviewer"
    DEVELOPER = "developer"


class ChunkStatus(str, Enum):
    """
    Status of a chunk processing.
    
    Represents the lifecycle stages of data in the system:
    1. Initial ingestion of raw data (RAW)
    2. Data cleaning/pre-processing (CLEANED)
    3. Verification against rules and standards (VERIFIED)
    4. Validation with cross-references and context (VALIDATED)
    5. Reliable data ready for usage (RELIABLE)
    
    Also includes operational statuses for tracking processing state.
    """
    # Начальный статус для новых данных
    NEW = "new"
    
    # Статусы жизненного цикла данных
    RAW = "raw"                    # Сырые данные, как они поступили в систему
    CLEANED = "cleaned"            # Данные прошли очистку от ошибок и шума
    VERIFIED = "verified"          # Данные проверены на соответствие правилам и стандартам
    VALIDATED = "validated"        # Данные прошли валидацию с учетом контекста и перекрестных ссылок
    RELIABLE = "reliable"          # Надежные данные, готовые к использованию
    
    # Операционные статусы
    INDEXED = "indexed"            # Данные проиндексированы
    OBSOLETE = "obsolete"          # Данные устарели
    REJECTED = "rejected"          # Данные отклонены из-за критических проблем
    IN_PROGRESS = "in_progress"    # Данные в процессе обработки
    
    # Дополнительные статусы для управления жизненным циклом
    NEEDS_REVIEW = "needs_review"  # Требуется ручная проверка
    ARCHIVED = "archived"          # Данные архивированы

    # Case-insensitive parsing support
    @classmethod
    def _missing_(cls, value):
        """Allow case-insensitive mapping from string to enum member."""
        if isinstance(value, str):
            value_lower = value.lower()
            for member in cls:
                if member.value == value_lower:
                    return member
        # Fallthrough to default behaviour
        return super()._missing_(value)


class FeedbackMetrics(BaseModel):
    """Feedback metrics for a chunk"""
    accepted: int = Field(default=0, description="How many times the chunk was accepted")
    rejected: int = Field(default=0, description="How many times the chunk was rejected")
    modifications: int = Field(default=0, description="Number of modifications made after generation")


class ChunkMetrics(BaseModel):
    """Metrics related to chunk quality and usage"""
    quality_score: Optional[float] = Field(default=None, ge=0, le=1, description="Quality score between 0 and 1")
    coverage: Optional[float] = Field(default=None, ge=0, le=1, description="Coverage score between 0 and 1")
    cohesion: Optional[float] = Field(default=None, ge=0, le=1, description="Cohesion score between 0 and 1")
    boundary_prev: Optional[float] = Field(default=None, ge=0, le=1, description="Boundary similarity with previous chunk")
    boundary_next: Optional[float] = Field(default=None, ge=0, le=1, description="Boundary similarity with next chunk")
    matches: Optional[int] = Field(default=None, ge=0, description="How many times matched in retrieval")
    used_in_generation: bool = Field(default=False, description="Whether used in generation")
    used_as_input: bool = Field(default=False, description="Whether used as input")
    used_as_context: bool = Field(default=False, description="Whether used as context")
    feedback: FeedbackMetrics = Field(default_factory=FeedbackMetrics, description="Feedback metrics")


class SemanticChunk(BaseModel):
    """
    Main model representing a universal semantic chunk with metadata.
    
    This is the full, structured representation based on the specification.
    """
    uuid: str = Field(..., description="Unique identifier (UUIDv4)")
    type: ChunkType = Field(..., description="Type of chunk")
    role: Optional[ChunkRole] = Field(default=None, description="Role of the creator")
    project: Optional[str] = Field(default=None, description="Project identifier")
    task_id: Optional[str] = Field(default=None, description="Task identifier")
    subtask_id: Optional[str] = Field(default=None, description="Subtask identifier")
    unit_id: Optional[str] = Field(default=None, description="Unit/service identifier")
    
    text: str = Field(..., description="Chunk content")
    summary: Optional[str] = Field(default=None, description="Brief summary")
    language: str = Field(..., description="Content language/format")
    
    source_id: Optional[str] = Field(default=None, description="Source identifier (UUIDv4)")
    source_path: Optional[str] = Field(default=None, description="Path to source")
    source_lines: Optional[List[int]] = Field(default=None, description="Source line numbers")
    ordinal: Optional[int] = Field(default=None, ge=0, description="Order in source")
    
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat(), description="Creation timestamp (ISO8601)")
    status: ChunkStatus = Field(default=ChunkStatus.NEW, description="Processing status")
    chunking_version: Optional[str] = Field(default="1.0", description="Chunking algorithm version")
    
    sha256: str = Field(..., description="Content hash for integrity")
    embedding: Optional[Any] = Field(default=None, description="Vector embedding")
    
    links: List[str] = Field(default_factory=list, description="References to other chunks")
    tags: List[str] = Field(default_factory=list, description="Categorical tags")
    
    metrics: ChunkMetrics = Field(default_factory=ChunkMetrics, description="Quality and usage metrics")
    
    start: int = Field(..., description="Start offset of the chunk in the source text (in bytes or characters)")  # Start offset of the chunk in the source text
    end: int = Field(..., description="End offset of the chunk in the source text (in bytes or characters)")  # End offset of the chunk in the source text
    
    @field_validator('uuid')
    @classmethod
    def validate_uuid(cls, v: str) -> str:
        """Validate UUID format"""
        if not UUID4_PATTERN.match(v):
            try:
                # Try to parse and see if it's a valid UUID
                uuid_obj = uuid.UUID(v, version=4)
                if str(uuid_obj) != v.lower():
                    raise ValueError("UUID version or format doesn't match")
            except (ValueError, AttributeError):
                raise ValueError(f"Invalid UUID4 format: {v}")
        return v
    
    @field_validator('source_id')
    @classmethod
    def validate_source_id(cls, v: Optional[str]) -> Optional[str]:
        """Validate source_id UUID format if present"""
        if v is not None and not UUID4_PATTERN.match(v):
            try:
                uuid_obj = uuid.UUID(v, version=4)
                if str(uuid_obj) != v.lower():
                    raise ValueError("Source ID UUID version or format doesn't match")
            except (ValueError, AttributeError):
                raise ValueError(f"Invalid source_id UUID4 format: {v}")
        return v
    
    @field_validator('created_at')
    @classmethod
    def validate_created_at(cls, v: str) -> str:
        """Validate that created_at is in ISO8601 format with timezone"""
        if not ISO8601_PATTERN.match(v):
            try:
                # Try to parse and see if it's valid ISO format
                dt = datetime.fromisoformat(v.replace('Z', '+00:00'))
                # Ensure timezone is present
                if dt.tzinfo is None:
                    raise ValueError("Missing timezone information")
                # Return canonicalized format
                return dt.isoformat()
            except (ValueError, AttributeError):
                raise ValueError(f"Invalid ISO8601 format with timezone: {v}")
        return v
    
    @field_validator('links')
    @classmethod
    def validate_links(cls, links: List[str]) -> List[str]:
        """Validate that links follow the format 'relation:uuid'"""
        for link in links:
            parts = link.split(":", 1)
            if len(parts) != 2 or not parts[0] or not parts[1]:
                raise ValueError(f"Link must follow 'relation:uuid' format: {link}")
            
            # Validate that UUID part is valid
            uuid_part = parts[1]
            if not UUID4_PATTERN.match(uuid_part):
                try:
                    uuid_obj = uuid.UUID(uuid_part, version=4)
                    if str(uuid_obj) != uuid_part.lower():
                        raise ValueError("Link UUID version or format doesn't match")
                except (ValueError, AttributeError):
                    raise ValueError(f"Invalid UUID4 format in link: {link}")
        return links


class FlatSemanticChunk(BaseModel):
    """
    Flat representation of the semantic chunk with all fields in a flat structure.
    
    Used for storage systems that prefer flat structures.
    """
    # Core identifiers
    uuid: str
    source_id: Optional[str] = None
    project: Optional[str] = None
    task_id: Optional[str] = None
    subtask_id: Optional[str] = None
    unit_id: Optional[str] = None
    
    # Content info
    type: str
    role: Optional[str] = None
    language: str
    text: str
    summary: Optional[str] = None
    
    # Source tracking
    ordinal: Optional[int] = None
    sha256: str
    created_at: str
    status: str = ChunkStatus.NEW.value
    source_path: Optional[str] = None
    source_lines_start: Optional[int] = None
    source_lines_end: Optional[int] = None
    
    # Tags & Links
    tags: Optional[str] = None  # Comma-separated tags
    link_related: Optional[str] = None
    link_parent: Optional[str] = None
    
    # Flat metrics
    quality_score: Optional[float] = None
    coverage: Optional[float] = None
    cohesion: Optional[float] = None
    boundary_prev: Optional[float] = None
    boundary_next: Optional[float] = None
    used_in_generation: bool = False
    feedback_accepted: int = 0
    feedback_rejected: int = 0
    
    start: Optional[int] = Field(default=None, description="Start offset of the chunk in the source text (in bytes or characters)")  # Start offset of the chunk in the source text
    end: Optional[int] = Field(default=None, description="End offset of the chunk in the source text (in bytes or characters)")  # End offset of the chunk in the source text
    
    @field_validator('uuid')
    @classmethod
    def validate_uuid(cls, v: str) -> str:
        """Validate UUID format"""
        if not UUID4_PATTERN.match(v):
            try:
                uuid_obj = uuid.UUID(v, version=4)
                if str(uuid_obj) != v.lower():
                    raise ValueError("UUID version or format doesn't match")
            except (ValueError, AttributeError):
                raise ValueError(f"Invalid UUID4 format: {v}")
        return v
    
    @field_validator('source_id')
    @classmethod
    def validate_source_id(cls, v: Optional[str]) -> Optional[str]:
        """Validate source_id UUID format if present"""
        if v is not None and not UUID4_PATTERN.match(v):
            try:
                uuid_obj = uuid.UUID(v, version=4)
                if str(uuid_obj) != v.lower():
                    raise ValueError("Source ID UUID version or format doesn't match")
            except (ValueError, AttributeError):
                raise ValueError(f"Invalid source_id UUID4 format: {v}")
        return v
    
    @field_validator('created_at')
    @classmethod
    def validate_created_at(cls, v: str) -> str:
        """Validate that created_at is in ISO8601 format with timezone"""
        if not ISO8601_PATTERN.match(v):
            try:
                dt = datetime.fromisoformat(v.replace('Z', '+00:00'))
                if dt.tzinfo is None:
                    raise ValueError("Missing timezone information")
                return dt.isoformat()
            except (ValueError, AttributeError):
                raise ValueError(f"Invalid ISO8601 format with timezone: {v}")
        return v
    
    @field_validator('link_related', 'link_parent')
    @classmethod
    def validate_link_uuid(cls, v: Optional[str]) -> Optional[str]:
        """Validate link UUIDs if present"""
        if v is not None and not UUID4_PATTERN.match(v):
            try:
                uuid_obj = uuid.UUID(v, version=4)
                if str(uuid_obj) != v.lower():
                    raise ValueError("Link UUID version or format doesn't match")
            except (ValueError, AttributeError):
                raise ValueError(f"Invalid UUID4 format in link: {v}")
        return v
    
    @classmethod
    def from_semantic_chunk(cls, chunk: SemanticChunk) -> 'FlatSemanticChunk':
        """Convert a full SemanticChunk to flat representation"""
        source_lines_start = None
        source_lines_end = None
        if chunk.source_lines and len(chunk.source_lines) >= 2:
            source_lines_start = chunk.source_lines[0]
            source_lines_end = chunk.source_lines[1]
            
        # Extract link references
        link_parent = None
        link_related = None
        for link in chunk.links:
            if link.startswith("parent:"):
                link_parent = link.split(":", 1)[1]
            elif link.startswith("related:"):
                link_related = link.split(":", 1)[1]
                
        return cls(
            uuid=chunk.uuid,
            source_id=chunk.source_id,
            project=chunk.project,
            task_id=chunk.task_id,
            subtask_id=chunk.subtask_id,
            unit_id=chunk.unit_id,
            type=chunk.type.value,
            role=chunk.role.value if chunk.role else None,
            language=chunk.language,
            text=chunk.text,
            summary=chunk.summary,
            ordinal=chunk.ordinal,
            sha256=chunk.sha256,
            created_at=chunk.created_at,
            status=chunk.status.value,
            source_path=chunk.source_path,
            source_lines_start=source_lines_start,
            source_lines_end=source_lines_end,
            tags=",".join(chunk.tags) if chunk.tags else None,
            link_related=link_related,
            link_parent=link_parent,
            quality_score=chunk.metrics.quality_score,
            coverage=chunk.metrics.coverage,
            cohesion=getattr(chunk.metrics, "cohesion", None),
            boundary_prev=getattr(chunk.metrics, "boundary_prev", None),
            boundary_next=getattr(chunk.metrics, "boundary_next", None),
            used_in_generation=chunk.metrics.used_in_generation,
            feedback_accepted=chunk.metrics.feedback.accepted,
            feedback_rejected=chunk.metrics.feedback.rejected,
            start=chunk.start,
            end=chunk.end
        )
        
    def to_semantic_chunk(self) -> SemanticChunk:
        """Convert flat representation to full SemanticChunk"""
        # Prepare links
        links = []
        if self.link_parent:
            links.append(f"parent:{self.link_parent}")
        if self.link_related:
            links.append(f"related:{self.link_related}")
            
        # Prepare tags
        tags = self.tags.split(",") if self.tags else []
        
        # Prepare source lines
        source_lines = None
        if self.source_lines_start is not None and self.source_lines_end is not None:
            source_lines = [self.source_lines_start, self.source_lines_end]
            
        # Prepare metrics
        metrics = ChunkMetrics(
            quality_score=self.quality_score,
            coverage=self.coverage,
            cohesion=self.cohesion,
            boundary_prev=self.boundary_prev,
            boundary_next=self.boundary_next,
            used_in_generation=self.used_in_generation,
            feedback=FeedbackMetrics(
                accepted=self.feedback_accepted,
                rejected=self.feedback_rejected
            )
        )
        
        return SemanticChunk(
            uuid=self.uuid,
            type=self.type,
            role=self.role,
            project=self.project,
            task_id=self.task_id,
            subtask_id=self.subtask_id,
            unit_id=self.unit_id,
            text=self.text,
            summary=self.summary,
            language=self.language,
            source_id=self.source_id,
            source_path=self.source_path,
            source_lines=source_lines,
            ordinal=self.ordinal,
            created_at=self.created_at,
            status=self.status,
            sha256=self.sha256,
            links=links,
            tags=tags,
            metrics=metrics,
            start=self.start,
            end=self.end
        ) 