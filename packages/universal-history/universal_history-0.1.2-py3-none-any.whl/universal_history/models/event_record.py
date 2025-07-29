"""
Event Record module representing the basic unit of information in the Universal History system.
"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any, Union
import uuid
import json

class DomainType(str, Enum):
    """Enumeration of possible domains for an Event Record."""
    EDUCATION = "education"
    HEALTH = "health"
    WORK = "work"
    SPORTS = "sports"
    FINANCIAL = "financial"
    PERSONAL = "personal"
    OTHER = "other"

class ContentType(str, Enum):
    """Enumeration of possible content types for raw input."""
    TEXT = "text"
    AUDIO = "audio"
    VIDEO = "video"
    IMAGE = "image"

class SourceType(str, Enum):
    """Enumeration of possible source types for an Event Record."""
    INSTITUTION = "institution"
    INDIVIDUAL = "individual"
    SYSTEM = "system"
    SENSOR = "sensor"
    OTHER = "other"

class InputMethod(str, Enum):
    """Enumeration of possible input methods for an Event Record."""
    MANUAL = "manual"
    AUTOMATIC = "automatic"
    MIXED = "mixed"

class ProcessingMethod(str, Enum):
    """Enumeration of possible processing methods for an Event Record."""
    AI_ANALYSIS = "AI_analysis"
    HUMAN_INTERPRETATION = "human_interpretation"
    STANDARDIZED_TEST = "standardized_test"
    SENSOR_READING = "sensor_reading"
    OTHER = "other"

class ConfidentialityLevel(str, Enum):
    """Enumeration of possible confidentiality levels for an Event Record."""
    PUBLIC = "public"
    RESTRICTED = "restricted"
    CONFIDENTIAL = "confidential"
    HIGHLY_CONFIDENTIAL = "highly_confidential"

class ConfidenceLevel(str, Enum):
    """Enumeration of possible confidence levels for data in an Event Record."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class VerificationStatus(str, Enum):
    """Enumeration of possible verification statuses for an Event Record."""
    VERIFIED = "verified"
    PENDING = "pending"
    REJECTED = "rejected"

@dataclass
class RawInput:
    """Represents the raw input data for an Event Record."""
    type: ContentType
    content: str
    duration: Optional[str] = None
    context: Optional[str] = None

@dataclass
class ProcessedData:
    """Represents the processed data derived from the raw input."""
    quantitative_metrics: Dict[str, float] = field(default_factory=dict)
    qualitative_assessments: Dict[str, str] = field(default_factory=dict)
    derived_insights: List[str] = field(default_factory=list)

@dataclass
class Creator:
    """Represents the creator of the Event Record."""
    id: str
    role: str
    name: str
    qualifications: List[str] = field(default_factory=list)
    experience_years: Optional[int] = None

@dataclass
class Source:
    """Represents the source of the Event Record."""
    type: SourceType
    id: str
    name: str
    creator: Optional[Creator] = None
    input_method: InputMethod = InputMethod.MANUAL
    processing_method: ProcessingMethod = ProcessingMethod.HUMAN_INTERPRETATION

@dataclass
class Context:
    """Represents the context in which the Event Record was created."""
    location: Optional[str] = None
    participants: List[str] = field(default_factory=list)
    environmental_factors: List[str] = field(default_factory=list)

@dataclass
class Metadata:
    """Represents metadata about the Event Record."""
    confidentiality_level: ConfidentialityLevel = ConfidentialityLevel.RESTRICTED
    access_level: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    related_documents: List[str] = field(default_factory=list)
    version: str = "1.0"
    last_modified: datetime = field(default_factory=datetime.now)
    modified_by: Optional[str] = None

@dataclass
class DataConfidence:
    """Represents confidence levels for different types of data in the Event Record."""
    raw_data: ConfidenceLevel = ConfidenceLevel.MEDIUM
    processed_data: ConfidenceLevel = ConfidenceLevel.MEDIUM

@dataclass
class EventRecord:
    """
    Represents a Record of Event (RE) in the Universal History system.
    
    An Event Record is the basic unit of information in the Universal History,
    capturing a specific event or observation in the subject's trajectory.
    """
    subject_id: str
    domain_type: DomainType
    event_type: str
    raw_input: RawInput
    source: Source
    
    re_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    previous_re_hash: Optional[str] = None
    current_re_hash: Optional[str] = None
    processed_data: ProcessedData = field(default_factory=ProcessedData)
    context: Context = field(default_factory=Context)
    metadata: Metadata = field(default_factory=Metadata)
    confidence_level: DataConfidence = field(default_factory=DataConfidence)
    verification_status: VerificationStatus = VerificationStatus.PENDING
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the EventRecord to a dictionary.
        
        Returns:
            Dict[str, Any]: Dictionary representation of the EventRecord
        """
        # Crear un diccionario directamente con las propiedades clave
        result = {
            "subject_id": self.subject_id,
            "domain_type": self.domain_type.value if isinstance(self.domain_type, Enum) else self.domain_type,
            "event_type": self.event_type,
            "re_id": self.re_id,
            "timestamp": self.timestamp.isoformat() if isinstance(self.timestamp, datetime) else self.timestamp,
            "previous_re_hash": self.previous_re_hash,
            "current_re_hash": self.current_re_hash,
            "verification_status": self.verification_status.value if isinstance(self.verification_status, Enum) else self.verification_status
        }
        
        # Convertir raw_input
        if self.raw_input:
            result["raw_input"] = {
                "type": self.raw_input.type.value if isinstance(self.raw_input.type, Enum) else self.raw_input.type,
                "content": self.raw_input.content,
                "duration": self.raw_input.duration,
                "context": self.raw_input.context
            }
        
        # Convertir source
        if self.source:
            source_dict = {
                "type": self.source.type.value if isinstance(self.source.type, Enum) else self.source.type,
                "id": self.source.id,
                "name": self.source.name,
                "input_method": self.source.input_method.value if isinstance(self.source.input_method, Enum) else self.source.input_method,
                "processing_method": self.source.processing_method.value if isinstance(self.source.processing_method, Enum) else self.source.processing_method
            }
            
            # Añadir creator si existe
            if self.source.creator:
                source_dict["creator"] = {
                    "id": self.source.creator.id,
                    "role": self.source.creator.role,
                    "name": self.source.creator.name,
                    "qualifications": self.source.creator.qualifications,
                    "experience_years": self.source.creator.experience_years
                }
            
            result["source"] = source_dict
        
        # Convertir processed_data
        if hasattr(self, 'processed_data') and self.processed_data:
            result["processed_data"] = {
                "quantitative_metrics": self.processed_data.quantitative_metrics,
                "qualitative_assessments": self.processed_data.qualitative_assessments,
                "derived_insights": self.processed_data.derived_insights
            }
        
        # Convertir context
        if hasattr(self, 'context') and self.context:
            result["context"] = {
                "location": self.context.location,
                "participants": self.context.participants,
                "environmental_factors": self.context.environmental_factors
            }
        
        # Convertir metadata
        if hasattr(self, 'metadata') and self.metadata:
            result["metadata"] = {
                "confidentiality_level": self.metadata.confidentiality_level.value if isinstance(self.metadata.confidentiality_level, Enum) else self.metadata.confidentiality_level,
                "access_level": self.metadata.access_level,
                "tags": self.metadata.tags,
                "related_documents": self.metadata.related_documents,
                "version": self.metadata.version,
                "last_modified": self.metadata.last_modified.isoformat() if isinstance(self.metadata.last_modified, datetime) else self.metadata.last_modified,
                "modified_by": self.metadata.modified_by
            }
        
        # Convertir confidence_level
        if hasattr(self, 'confidence_level') and self.confidence_level:
            result["confidence_level"] = {
                "raw_data": self.confidence_level.raw_data.value if isinstance(self.confidence_level.raw_data, Enum) else self.confidence_level.raw_data,
                "processed_data": self.confidence_level.processed_data.value if isinstance(self.confidence_level.processed_data, Enum) else self.confidence_level.processed_data
            }
        
        return result
    
    def to_json(self) -> str:
        """
        Convert the EventRecord to a JSON string.
        
        Returns:
            str: JSON representation of the EventRecord
        """
        return json.dumps(self.to_dict(), default=str)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EventRecord':
        """
        Create an EventRecord from a dictionary.
        
        Args:
            data (Dict[str, Any]): Dictionary containing EventRecord data
            
        Returns:
            EventRecord: New EventRecord instance
        """
        # Create copies of data to avoid modifying the original
        event_data = data.copy()
        
        # Handle nested objects
        if 'raw_input' in event_data:
            raw_input_data = event_data.pop('raw_input')
            raw_input_data['type'] = ContentType(raw_input_data['type'])
            event_data['raw_input'] = RawInput(**raw_input_data)
        
        if 'processed_data' in event_data:
            event_data['processed_data'] = ProcessedData(**event_data['processed_data'])
        
        if 'source' in event_data:
            source_data = event_data.pop('source')
            source_data['type'] = SourceType(source_data['type'])
            source_data['input_method'] = InputMethod(source_data['input_method'])
            source_data['processing_method'] = ProcessingMethod(source_data['processing_method'])
            
            if 'creator' in source_data:
                source_data['creator'] = Creator(**source_data['creator'])
            
            event_data['source'] = Source(**source_data)
        
        if 'context' in event_data:
            event_data['context'] = Context(**event_data['context'])
        
        if 'metadata' in event_data:
            metadata_data = event_data.pop('metadata')
            metadata_data['confidentiality_level'] = ConfidentialityLevel(
                metadata_data['confidentiality_level']
            )
            if 'last_modified' in metadata_data and isinstance(metadata_data['last_modified'], str):
                metadata_data['last_modified'] = datetime.fromisoformat(metadata_data['last_modified'])
            event_data['metadata'] = Metadata(**metadata_data)
        
        if 'confidence_level' in event_data:
            confidence_data = event_data.pop('confidence_level')
            confidence_data['raw_data'] = ConfidenceLevel(confidence_data['raw_data'])
            confidence_data['processed_data'] = ConfidenceLevel(confidence_data['processed_data'])
            event_data['confidence_level'] = DataConfidence(**confidence_data)
        
        if 'verification_status' in event_data:
            event_data['verification_status'] = VerificationStatus(event_data['verification_status'])
        
        if 'domain_type' in event_data:
            event_data['domain_type'] = DomainType(event_data['domain_type'])
        
        if 'timestamp' in event_data and isinstance(event_data['timestamp'], str):
            event_data['timestamp'] = datetime.fromisoformat(event_data['timestamp'])
        
        return cls(**event_data)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'EventRecord':
        """
        Create an EventRecord from a JSON string.
        
        Args:
            json_str (str): JSON string containing EventRecord data
            
        Returns:
            EventRecord: New EventRecord instance
        """
        data = json.loads(json_str)
        return cls.from_dict(data)
    
    def calculate_hash(self) -> str:
        """
        Calculate the hash of the current EventRecord.
        
        This method should be called after all fields have been set except current_re_hash.
        
        Returns:
            str: Hash of the EventRecord
        """
        # We need to make a copy of the object to avoid modifying it
        temp_dict = self.to_dict()
        # Remove the current_re_hash from the hash calculation
        temp_dict.pop('current_re_hash', None)
        # Convert to string and hash
        import hashlib
        data_str = json.dumps(temp_dict, sort_keys=True, default=str)
        return hashlib.sha256(data_str.encode()).hexdigest()
    
    def update_hash(self) -> None:
        """
        Update the current_re_hash field based on the current state of the EventRecord.
        """
        self.current_re_hash = self.calculate_hash()
