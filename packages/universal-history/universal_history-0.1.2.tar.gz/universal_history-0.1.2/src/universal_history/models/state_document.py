"""
State Document module representing the real-time state of a subject derived from their history.
"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any, Union
import uuid
import json

from .event_record import DomainType

@dataclass
class EventReference:
    """Reference to an original Event Record with description of its significance."""
    re_id: str
    description: str
    impact: Optional[str] = None
    significance: Optional[str] = None

@dataclass
class DomainState:
    """Represents the current state for a specific domain."""
    last_updated: datetime
    current_status: str
    key_attributes: Dict[str, Any] = field(default_factory=dict)
    recent_events: List[EventReference] = field(default_factory=list)
    significant_events: List[EventReference] = field(default_factory=list)
    trends: Dict[str, str] = field(default_factory=dict)
    domain_specific_data: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {
            'last_updated': self.last_updated.isoformat(),
            'current_status': self.current_status,
            'key_attributes': self.key_attributes,
            'recent_events': [er.__dict__ for er in self.recent_events],
            'significant_events': [er.__dict__ for er in self.significant_events],
            'trends': self.trends,
            'domain_specific_data': self.domain_specific_data
        }
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DomainState':
        """Create from dictionary."""
        domain_data = data.copy()
        
        # Handle datetime
        if 'last_updated' in domain_data and isinstance(domain_data['last_updated'], str):
            domain_data['last_updated'] = datetime.fromisoformat(domain_data['last_updated'])
            
        # Handle event references
        if 'recent_events' in domain_data:
            domain_data['recent_events'] = [
                EventReference(**event) for event in domain_data['recent_events']
            ]
            
        if 'significant_events' in domain_data:
            domain_data['significant_events'] = [
                EventReference(**event) for event in domain_data['significant_events']
            ]
            
        return cls(**domain_data)

@dataclass
class AggregatedInsights:
    """Cross-domain insights derived from analysis of multiple domains."""
    cross_domain_patterns: List[str] = field(default_factory=list)
    recommended_actions: List[str] = field(default_factory=list)
    potential_opportunities: List[str] = field(default_factory=list)
    potential_risks: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return self.__dict__.copy()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AggregatedInsights':
        """Create from dictionary."""
        return cls(**data)

@dataclass
class StateDocumentMetadata:
    """Metadata for the State Document."""
    generated_by: str
    generated_on: datetime
    confidence_level: str  # high, medium, low
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'generated_by': self.generated_by,
            'generated_on': self.generated_on.isoformat(),
            'confidence_level': self.confidence_level
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'StateDocumentMetadata':
        """Create from dictionary."""
        metadata_data = data.copy()
        
        # Handle datetime
        if 'generated_on' in metadata_data and isinstance(metadata_data['generated_on'], str):
            metadata_data['generated_on'] = datetime.fromisoformat(metadata_data['generated_on'])
            
        return cls(**metadata_data)

@dataclass
class StateDocument:
    """
    Represents a State Document (DE) in the Universal History system.
    
    A State Document is a real-time representation of the current state of a subject,
    derived from analysis of their history and optimized for AI context.
    """
    subject_id: str
    general_summary: str
    domains: Dict[str, DomainState]
    
    de_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    last_updated: datetime = field(default_factory=datetime.now)
    version: str = "1.0"
    aggregated_insights: AggregatedInsights = field(default_factory=AggregatedInsights)
    llm_optimized_summary: Optional[str] = None
    source_events: List[str] = field(default_factory=list)
    source_syntheses: List[str] = field(default_factory=list)
    metadata: StateDocumentMetadata = field(default_factory=lambda: StateDocumentMetadata(
        generated_by="system",
        generated_on=datetime.now(),
        confidence_level="medium"
    ))
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the StateDocument to a dictionary.
        
        Returns:
            Dict[str, Any]: Dictionary representation of the StateDocument
        """
        result = {
            'de_id': self.de_id,
            'subject_id': self.subject_id,
            'general_summary': self.general_summary,
            'last_updated': self.last_updated.isoformat() if isinstance(self.last_updated, datetime) else self.last_updated,
            'version': self.version,
            'llm_optimized_summary': self.llm_optimized_summary,
            'source_events': self.source_events.copy() if hasattr(self, 'source_events') else [],
            'source_syntheses': self.source_syntheses.copy() if hasattr(self, 'source_syntheses') else []
        }
        
        # Add domains safely
        try:
            if hasattr(self, 'domains') and self.domains:
                domains_dict = {}
                for k, v in self.domains.items():
                    if hasattr(v, 'to_dict') and callable(getattr(v, 'to_dict')):
                        domains_dict[k] = v.to_dict()
                    else:
                        domains_dict[k] = {
                            'last_updated': v.last_updated.isoformat() if hasattr(v, 'last_updated') and isinstance(v.last_updated, datetime) else None,
                            'current_status': getattr(v, 'current_status', None)
                        }
                result['domains'] = domains_dict
            else:
                result['domains'] = {}
        except (RecursionError, AttributeError):
            result['domains'] = {}
            
        # Add aggregated_insights safely
        try:
            if hasattr(self, 'aggregated_insights') and self.aggregated_insights:
                if hasattr(self.aggregated_insights, 'to_dict') and callable(getattr(self.aggregated_insights, 'to_dict')):
                    result['aggregated_insights'] = self.aggregated_insights.to_dict()
                else:
                    result['aggregated_insights'] = {
                        'cross_domain_patterns': getattr(self.aggregated_insights, 'cross_domain_patterns', []),
                        'recommended_actions': getattr(self.aggregated_insights, 'recommended_actions', [])
                    }
            else:
                result['aggregated_insights'] = {}
        except (RecursionError, AttributeError):
            result['aggregated_insights'] = {}
            
        # Add metadata safely
        try:
            if hasattr(self, 'metadata') and self.metadata:
                if hasattr(self.metadata, 'to_dict') and callable(getattr(self.metadata, 'to_dict')):
                    result['metadata'] = self.metadata.to_dict()
                else:
                    result['metadata'] = {
                        'generated_by': getattr(self.metadata, 'generated_by', 'system'),
                        'generated_on': getattr(self.metadata, 'generated_on', datetime.now()).isoformat() if isinstance(getattr(self.metadata, 'generated_on', None), datetime) else None,
                        'confidence_level': getattr(self.metadata, 'confidence_level', 'medium')
                    }
            else:
                result['metadata'] = {}
        except (RecursionError, AttributeError):
            result['metadata'] = {}
            
        return result
    
    def to_json(self) -> str:
        """
        Convert the StateDocument to a JSON string.
        
        Returns:
            str: JSON representation of the StateDocument
        """
        return json.dumps(self.to_dict(), default=str)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'StateDocument':
        """
        Create a StateDocument from a dictionary.
        
        Args:
            data (Dict[str, Any]): Dictionary containing StateDocument data
            
        Returns:
            StateDocument: New StateDocument instance
        """
        # Create a copy to avoid modifying the original
        state_data = data.copy()
        
        # Handle domains
        if 'domains' in state_data:
            domains_data = state_data.pop('domains')
            state_data['domains'] = {
                domain_key: DomainState.from_dict(domain_data) 
                for domain_key, domain_data in domains_data.items()
            }
        
        # Handle aggregated insights
        if 'aggregated_insights' in state_data:
            state_data['aggregated_insights'] = AggregatedInsights.from_dict(state_data['aggregated_insights'])
        
        # Handle metadata
        if 'metadata' in state_data:
            state_data['metadata'] = StateDocumentMetadata.from_dict(state_data['metadata'])
        
        # Handle datetime
        if 'last_updated' in state_data and isinstance(state_data['last_updated'], str):
            state_data['last_updated'] = datetime.fromisoformat(state_data['last_updated'])
        
        return cls(**state_data)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'StateDocument':
        """
        Create a StateDocument from a JSON string.
        
        Args:
            json_str (str): JSON string containing StateDocument data
            
        Returns:
            StateDocument: New StateDocument instance
        """
        data = json.loads(json_str)
        return cls.from_dict(data)
    
    def get_domain_state(self, domain_type: Union[str, DomainType]) -> Optional[DomainState]:
        """
        Get the state for a specific domain.
        
        Args:
            domain_type (Union[str, DomainType]): Domain to get state for
            
        Returns:
            Optional[DomainState]: The domain state or None if not found
        """
        domain_key = domain_type.value if isinstance(domain_type, DomainType) else domain_type
        return self.domains.get(domain_key)
    
    def update_domain_state(self, domain_type: Union[str, DomainType], domain_state: DomainState) -> None:
        """
        Update or add a domain state.
        
        Args:
            domain_type (Union[str, DomainType]): Domain to update
            domain_state (DomainState): New domain state
        """
        domain_key = domain_type.value if isinstance(domain_type, DomainType) else domain_type
        self.domains[domain_key] = domain_state
        self.last_updated = datetime.now()
        # Update metadata to reflect the change
        self.metadata.generated_on = datetime.now()
    
    def generate_llm_optimized_summary(self) -> str:
        """
        Generate a summary optimized for LLM context.
        
        This method should be overridden with a more sophisticated implementation
        that creates a well-structured summary for LLM consumption.
        
        Returns:
            str: LLM-optimized summary
        """
        # Basic implementation - in practice this would be more sophisticated
        summary_parts = [f"Subject ID: {self.subject_id}"]
        summary_parts.append(f"General summary: {self.general_summary}")
        
        # Add domain summaries
        for domain_key, domain_state in self.domains.items():
            summary_parts.append(f"\n## {domain_key.upper()} (Updated: {domain_state.last_updated.isoformat()})")
            summary_parts.append(f"Current status: {domain_state.current_status}")
            
            if domain_state.key_attributes:
                summary_parts.append("\nKey attributes:")
                for k, v in domain_state.key_attributes.items():
                    summary_parts.append(f"- {k}: {v}")
            
            if domain_state.significant_events:
                summary_parts.append("\nSignificant events:")
                for event in domain_state.significant_events[:3]:  # Limit to top 3
                    summary_parts.append(f"- {event.description}")
        
        # Add insights
        if self.aggregated_insights.cross_domain_patterns:
            summary_parts.append("\n## CROSS-DOMAIN PATTERNS")
            for pattern in self.aggregated_insights.cross_domain_patterns:
                summary_parts.append(f"- {pattern}")
        
        self.llm_optimized_summary = "\n".join(summary_parts)
        return self.llm_optimized_summary
    
    def update_last_updated(self) -> None:
        """Update the last_updated timestamp."""
        self.last_updated = datetime.now()
        self.metadata.generated_on = datetime.now()
