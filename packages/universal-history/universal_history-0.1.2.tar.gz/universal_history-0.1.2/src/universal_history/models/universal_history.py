"""
Universal History module representing the complete history of a subject.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any, Set
import uuid
import json

from .event_record import EventRecord, DomainType
from .trajectory_synthesis import TrajectorySynthesis
from .state_document import StateDocument
from .domain_catalog import DomainCatalog, Organization

@dataclass
class UniversalHistory:
    """
    Represents a Universal History (HU) in the Universal History system.
    
    A Universal History is a complete record of a subject's trajectory across
    multiple domains, including Event Records, Trajectory Syntheses, and
    a State Document reflecting the current state.
    """
    subject_id: str
    organization: Optional[Organization] = None
    
    hu_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)
    event_records: Dict[str, EventRecord] = field(default_factory=dict)  # ID -> EventRecord
    trajectory_syntheses: Dict[str, TrajectorySynthesis] = field(default_factory=dict)  # ID -> TrajectorySynthesis
    state_document: Optional[StateDocument] = None
    domain_catalogs: Dict[str, DomainCatalog] = field(default_factory=dict)  # Domain type -> DomainCatalog
    
    def add_event_record(self, event_record: EventRecord) -> None:
        """
        Add an Event Record to the Universal History.
        
        Args:
            event_record (EventRecord): The Event Record to add
        """
        # Check that the subject IDs match
        if event_record.subject_id != self.subject_id:
            raise ValueError(f"Event Record subject ID {event_record.subject_id} does not match Universal History subject ID {self.subject_id}")
        
        # Update hash chain if there are previous events in the same domain
        domain_events = self.get_events_by_domain(event_record.domain_type)
        if domain_events:
            # Find the most recent event in the domain by timestamp
            most_recent = max(domain_events, key=lambda e: e.timestamp)
            event_record.previous_re_hash = most_recent.current_re_hash
        
        # Update the hash of the new event
        event_record.update_hash()
        
        # Add the event to the history
        self.event_records[event_record.re_id] = event_record
        
        # Update last_updated timestamp
        self.last_updated = datetime.now()
    
    def add_trajectory_synthesis(self, trajectory_synthesis: TrajectorySynthesis) -> None:
        """
        Add a Trajectory Synthesis to the Universal History.
        
        Args:
            trajectory_synthesis (TrajectorySynthesis): The Trajectory Synthesis to add
        """
        # Check that the subject IDs match
        if trajectory_synthesis.subject_id != self.subject_id:
            raise ValueError(f"Trajectory Synthesis subject ID {trajectory_synthesis.subject_id} does not match Universal History subject ID {self.subject_id}")
        
        # Add the synthesis to the history
        self.trajectory_syntheses[trajectory_synthesis.st_id] = trajectory_synthesis
        
        # Update last_updated timestamp
        self.last_updated = datetime.now()
    
    def set_state_document(self, state_document: StateDocument) -> None:
        """
        Set the State Document for the Universal History.
        
        Args:
            state_document (StateDocument): The State Document to set
        """
        # Check that the subject IDs match
        if state_document.subject_id != self.subject_id:
            raise ValueError(f"State Document subject ID {state_document.subject_id} does not match Universal History subject ID {self.subject_id}")
        
        # Set the state document
        self.state_document = state_document
        
        # Update last_updated timestamp
        self.last_updated = datetime.now()
    
    def add_domain_catalog(self, domain_catalog: DomainCatalog) -> None:
        """
        Add a Domain Catalog to the Universal History.
        
        Args:
            domain_catalog (DomainCatalog): The Domain Catalog to add
        """
        domain_key = domain_catalog.domain_type.value if isinstance(domain_catalog.domain_type, DomainType) else domain_catalog.domain_type
        self.domain_catalogs[domain_key] = domain_catalog
        
        # Update last_updated timestamp
        self.last_updated = datetime.now()
    
    def get_event_record(self, re_id: str) -> Optional[EventRecord]:
        """
        Get an Event Record by ID.
        
        Args:
            re_id (str): The ID of the Event Record to get
            
        Returns:
            Optional[EventRecord]: The Event Record or None if not found
        """
        return self.event_records.get(re_id)
    
    def get_trajectory_synthesis(self, st_id: str) -> Optional[TrajectorySynthesis]:
        """
        Get a Trajectory Synthesis by ID.
        
        Args:
            st_id (str): The ID of the Trajectory Synthesis to get
            
        Returns:
            Optional[TrajectorySynthesis]: The Trajectory Synthesis or None if not found
        """
        return self.trajectory_syntheses.get(st_id)
    
    def get_domain_catalog(self, domain_type: DomainType) -> Optional[DomainCatalog]:
        """
        Get a Domain Catalog by domain type.
        
        Args:
            domain_type (DomainType): The domain type to get the catalog for
            
        Returns:
            Optional[DomainCatalog]: The Domain Catalog or None if not found
        """
        domain_key = domain_type.value if isinstance(domain_type, DomainType) else domain_type
        return self.domain_catalogs.get(domain_key)
    
    def get_events_by_domain(self, domain_type: DomainType) -> List[EventRecord]:
        """
        Get all Event Records for a specific domain.
        
        Args:
            domain_type (DomainType): The domain type to filter by
            
        Returns:
            List[EventRecord]: List of Event Records for the specified domain
        """
        domain_type_value = domain_type.value if isinstance(domain_type, DomainType) else domain_type
        return [er for er in self.event_records.values() if 
                (er.domain_type.value if isinstance(er.domain_type, DomainType) else er.domain_type) == domain_type_value]
    
    def get_syntheses_by_domain(self, domain_type: DomainType) -> List[TrajectorySynthesis]:
        """
        Get all Trajectory Syntheses for a specific domain.
        
        Args:
            domain_type (DomainType): The domain type to filter by
            
        Returns:
            List[TrajectorySynthesis]: List of Trajectory Syntheses for the specified domain
        """
        domain_type_value = domain_type.value if isinstance(domain_type, DomainType) else domain_type
        return [ts for ts in self.trajectory_syntheses.values() if 
                (ts.domain_type.value if isinstance(ts.domain_type, DomainType) else ts.domain_type) == domain_type_value]
    
    def get_recent_events(self, limit: int = 10) -> List[EventRecord]:
        """
        Get the most recent Event Records.
        
        Args:
            limit (int): Maximum number of events to return
            
        Returns:
            List[EventRecord]: List of recent Event Records
        """
        sorted_events = sorted(self.event_records.values(), key=lambda er: er.timestamp, reverse=True)
        return sorted_events[:limit]
    
    def get_domains(self) -> Set[str]:
        """
        Get all domains that have events in this history.
        
        Returns:
            Set[str]: Set of domain type values
        """
        domains = set()
        for er in self.event_records.values():
            domain_type_value = er.domain_type.value if isinstance(er.domain_type, DomainType) else er.domain_type
            domains.add(domain_type_value)
        return domains
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the UniversalHistory to a dictionary.
        
        Returns:
            Dict[str, Any]: Dictionary representation of the UniversalHistory
        """
        result = {
            'hu_id': self.hu_id,
            'subject_id': self.subject_id,
            'created_at': self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
            'last_updated': self.last_updated.isoformat() if isinstance(self.last_updated, datetime) else self.last_updated,
        }
        
        # Add event_records safely
        if hasattr(self, 'event_records') and self.event_records:
            event_records_dict = {}
            for re_id, er in self.event_records.items():
                try:
                    if hasattr(er, 'to_dict') and callable(getattr(er, 'to_dict')):
                        event_records_dict[re_id] = er.to_dict()
                    else:
                        # Simple representation if to_dict not available
                        event_records_dict[re_id] = {
                            're_id': getattr(er, 're_id', re_id),
                            'subject_id': getattr(er, 'subject_id', self.subject_id),
                            'domain_type': getattr(er, 'domain_type', None),
                            'event_type': getattr(er, 'event_type', None)
                        }
                except RecursionError:
                    # Fallback in case of recursion
                    event_records_dict[re_id] = {
                        're_id': re_id,
                        'subject_id': self.subject_id,
                        'note': 'Full representation unavailable due to recursion'
                    }
            result['event_records'] = event_records_dict
        else:
            result['event_records'] = {}
            
        # Add trajectory_syntheses safely
        if hasattr(self, 'trajectory_syntheses') and self.trajectory_syntheses:
            syntheses_dict = {}
            for st_id, ts in self.trajectory_syntheses.items():
                try:
                    if hasattr(ts, 'to_dict') and callable(getattr(ts, 'to_dict')):
                        syntheses_dict[st_id] = ts.to_dict()
                    else:
                        # Simple representation if to_dict not available
                        syntheses_dict[st_id] = {
                            'st_id': getattr(ts, 'st_id', st_id),
                            'subject_id': getattr(ts, 'subject_id', self.subject_id),
                            'domain_type': getattr(ts, 'domain_type', None),
                            'synthesis_type': getattr(ts, 'synthesis_type', None)
                        }
                except RecursionError:
                    # Fallback in case of recursion
                    syntheses_dict[st_id] = {
                        'st_id': st_id,
                        'subject_id': self.subject_id,
                        'note': 'Full representation unavailable due to recursion'
                    }
            result['trajectory_syntheses'] = syntheses_dict
        else:
            result['trajectory_syntheses'] = {}
            
        # Add domain_catalogs safely
        if hasattr(self, 'domain_catalogs') and self.domain_catalogs:
            catalogs_dict = {}
            for domain, catalog in self.domain_catalogs.items():
                try:
                    if hasattr(catalog, 'to_dict') and callable(getattr(catalog, 'to_dict')):
                        catalogs_dict[domain] = catalog.to_dict()
                    else:
                        # Simple representation if to_dict not available
                        domain_type_value = domain
                        catalogs_dict[domain] = {
                            'domain_type': domain_type_value,
                            'cdd_id': getattr(catalog, 'cdd_id', None),
                        }
                except RecursionError:
                    # Fallback in case of recursion
                    catalogs_dict[domain] = {
                        'domain_type': domain,
                        'note': 'Full representation unavailable due to recursion'
                    }
            result['domain_catalogs'] = catalogs_dict
        else:
            result['domain_catalogs'] = {}
        
        # Add state_document safely
        if self.state_document:
            try:
                if hasattr(self.state_document, 'to_dict') and callable(getattr(self.state_document, 'to_dict')):
                    result['state_document'] = self.state_document.to_dict()
                else:
                    # Simple representation if to_dict not available
                    result['state_document'] = {
                        'de_id': getattr(self.state_document, 'de_id', None),
                        'subject_id': getattr(self.state_document, 'subject_id', self.subject_id)
                    }
            except RecursionError:
                # Fallback in case of recursion
                result['state_document'] = {
                    'subject_id': self.subject_id,
                    'note': 'Full representation unavailable due to recursion'
                }
            
        return result
    
    def to_json(self) -> str:
        """
        Convert the UniversalHistory to a JSON string.
        
        Returns:
            str: JSON representation of the UniversalHistory
        """
        return json.dumps(self.to_dict(), default=str)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UniversalHistory':
        """
        Create a UniversalHistory from a dictionary.
        
        Args:
            data (Dict[str, Any]): Dictionary containing UniversalHistory data
            
        Returns:
            UniversalHistory: New UniversalHistory instance
        """
        # Create a copy to avoid modifying the original
        history_data = data.copy()
        
        # Create a basic history with just the subject ID
        subject_id = history_data.pop('subject_id')
        history = cls(subject_id=subject_id)
        
        # Set basic attributes
        if 'hu_id' in history_data:
            history.hu_id = history_data['hu_id']
            
        if 'created_at' in history_data and isinstance(history_data['created_at'], str):
            history.created_at = datetime.fromisoformat(history_data['created_at'])
            
        if 'last_updated' in history_data and isinstance(history_data['last_updated'], str):
            history.last_updated = datetime.fromisoformat(history_data['last_updated'])
        
        # Add Event Records
        if 'event_records' in history_data:
            for re_id, er_data in history_data['event_records'].items():
                history.event_records[re_id] = EventRecord.from_dict(er_data)
        
        # Add Trajectory Syntheses
        if 'trajectory_syntheses' in history_data:
            for st_id, ts_data in history_data['trajectory_syntheses'].items():
                history.trajectory_syntheses[st_id] = TrajectorySynthesis.from_dict(ts_data)
        
        # Set State Document
        if 'state_document' in history_data and history_data['state_document']:
            history.state_document = StateDocument.from_dict(history_data['state_document'])
        
        # Add Domain Catalogs
        if 'domain_catalogs' in history_data:
            for domain, catalog_data in history_data['domain_catalogs'].items():
                history.domain_catalogs[domain] = DomainCatalog.from_dict(catalog_data)
        
        return history
    
    @classmethod
    def from_json(cls, json_str: str) -> 'UniversalHistory':
        """
        Create a UniversalHistory from a JSON string.
        
        Args:
            json_str (str): JSON string containing UniversalHistory data
            
        Returns:
            UniversalHistory: New UniversalHistory instance
        """
        data = json.loads(json_str)
        return cls.from_dict(data)
    
    def verify_event_chain(self, domain_type: DomainType) -> bool:
        """
        Verify the integrity of the event chain for a specific domain.
        
        This method checks that each event's previous_re_hash matches the
        current_re_hash of the previous event in the chain.
        
        Args:
            domain_type (DomainType): The domain type to verify
            
        Returns:
            bool: True if the chain is valid, False otherwise
        """
        # Get events for the domain sorted by timestamp
        events = sorted(self.get_events_by_domain(domain_type), key=lambda e: e.timestamp)
        
        if not events:
            return True  # No events to verify
        
        # Check first event has no previous hash (or it's None)
        if events[0].previous_re_hash not in (None, ""):
            return False
        
        # Check that each event's current hash is correct
        for event in events:
            calculated_hash = event.calculate_hash()
            if event.current_re_hash != calculated_hash:
                return False
        
        # Check the chain
        for i in range(1, len(events)):
            if events[i].previous_re_hash != events[i-1].current_re_hash:
                return False
        
        return True
