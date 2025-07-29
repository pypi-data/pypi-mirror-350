"""
Memory repository implementation for storage of Universal History objects.
"""
from typing import Dict, List, Optional, Any, Union

from ..models.event_record import EventRecord, DomainType
from ..models.trajectory_synthesis import TrajectorySynthesis
from ..models.state_document import StateDocument
from ..models.domain_catalog import DomainCatalog
from ..models.universal_history import UniversalHistory
from .repository import HistoryRepository

class MemoryHistoryRepository(HistoryRepository):
    """
    In-memory implementation of the HistoryRepository.
    
    This implementation stores all data in memory, which is suitable for
    testing and small-scale usage, but does not persist data across restarts.
    """
    
    def __init__(self):
        """Initialize the repository with empty dictionaries."""
        self.histories: Dict[str, UniversalHistory] = {}
        self.subject_to_history: Dict[str, str] = {}  # subject_id -> hu_id
    
    def save_history(self, history: UniversalHistory) -> str:
        """
        Save a Universal History.
        
        Args:
            history (UniversalHistory): The history to save
            
        Returns:
            str: The ID of the saved history
        """
        self.histories[history.hu_id] = history
        self.subject_to_history[history.subject_id] = history.hu_id
        return history.hu_id
    
    def get_history(self, hu_id: str) -> Optional[UniversalHistory]:
        """
        Get a Universal History by ID.
        
        Args:
            hu_id (str): The ID of the history to get
            
        Returns:
            Optional[UniversalHistory]: The history or None if not found
        """
        return self.histories.get(hu_id)
    
    def get_history_by_subject(self, subject_id: str) -> Optional[UniversalHistory]:
        """
        Get a Universal History by subject ID.
        
        Args:
            subject_id (str): The subject ID to look for
            
        Returns:
            Optional[UniversalHistory]: The history or None if not found
        """
        hu_id = self.subject_to_history.get(subject_id)
        if hu_id:
            return self.histories.get(hu_id)
        return None
    
    def save_event_record(self, event_record: EventRecord, hu_id: str) -> str:
        """
        Save an Event Record to a Universal History.
        
        Args:
            event_record (EventRecord): The event record to save
            hu_id (str): The ID of the history to save to
            
        Returns:
            str: The ID of the saved event record
        """
        history = self.histories.get(hu_id)
        if not history:
            raise ValueError(f"Universal History with ID {hu_id} not found")
        
        history.add_event_record(event_record)
        return event_record.re_id
    
    def get_event_record(self, re_id: str, hu_id: str) -> Optional[EventRecord]:
        """
        Get an Event Record by ID from a Universal History.
        
        Args:
            re_id (str): The ID of the event record to get
            hu_id (str): The ID of the history to get from
            
        Returns:
            Optional[EventRecord]: The event record or None if not found
        """
        history = self.histories.get(hu_id)
        if not history:
            return None
        
        return history.get_event_record(re_id)
    
    def save_trajectory_synthesis(self, synthesis: TrajectorySynthesis, hu_id: str) -> str:
        """
        Save a Trajectory Synthesis to a Universal History.
        
        Args:
            synthesis (TrajectorySynthesis): The synthesis to save
            hu_id (str): The ID of the history to save to
            
        Returns:
            str: The ID of the saved synthesis
        """
        history = self.histories.get(hu_id)
        if not history:
            raise ValueError(f"Universal History with ID {hu_id} not found")
        
        history.add_trajectory_synthesis(synthesis)
        return synthesis.st_id
    
    def get_trajectory_synthesis(self, st_id: str, hu_id: str) -> Optional[TrajectorySynthesis]:
        """
        Get a Trajectory Synthesis by ID from a Universal History.
        
        Args:
            st_id (str): The ID of the synthesis to get
            hu_id (str): The ID of the history to get from
            
        Returns:
            Optional[TrajectorySynthesis]: The synthesis or None if not found
        """
        history = self.histories.get(hu_id)
        if not history:
            return None
        
        return history.get_trajectory_synthesis(st_id)
    
    def save_state_document(self, state_document: StateDocument, hu_id: str) -> str:
        """
        Save a State Document to a Universal History.
        
        Args:
            state_document (StateDocument): The state document to save
            hu_id (str): The ID of the history to save to
            
        Returns:
            str: The ID of the saved state document
        """
        history = self.histories.get(hu_id)
        if not history:
            raise ValueError(f"Universal History with ID {hu_id} not found")
        
        history.set_state_document(state_document)
        return state_document.de_id
    
    def get_state_document(self, hu_id: str) -> Optional[StateDocument]:
        """
        Get the State Document from a Universal History.
        
        Args:
            hu_id (str): The ID of the history to get from
            
        Returns:
            Optional[StateDocument]: The state document or None if not found
        """
        history = self.histories.get(hu_id)
        if not history:
            return None
        
        return history.state_document
    
    def save_domain_catalog(self, domain_catalog: DomainCatalog, hu_id: str) -> str:
        """
        Save a Domain Catalog to a Universal History.
        
        Args:
            domain_catalog (DomainCatalog): The domain catalog to save
            hu_id (str): The ID of the history to save to
            
        Returns:
            str: The ID of the saved domain catalog
        """
        history = self.histories.get(hu_id)
        if not history:
            raise ValueError(f"Universal History with ID {hu_id} not found")
        
        history.add_domain_catalog(domain_catalog)
        return domain_catalog.cdd_id
    
    def get_domain_catalog(self, domain_type: Union[str, DomainType], hu_id: str) -> Optional[DomainCatalog]:
        """
        Get a Domain Catalog by domain type from a Universal History.
        
        Args:
            domain_type (Union[str, DomainType]): The domain type to get the catalog for
            hu_id (str): The ID of the history to get from
            
        Returns:
            Optional[DomainCatalog]: The domain catalog or None if not found
        """
        history = self.histories.get(hu_id)
        if not history:
            return None
        
        return history.get_domain_catalog(domain_type)
    
    def get_events_by_domain(self, domain_type: Union[str, DomainType], hu_id: str) -> List[EventRecord]:
        """
        Get all Event Records for a specific domain from a Universal History.
        
        Args:
            domain_type (Union[str, DomainType]): The domain type to filter by
            hu_id (str): The ID of the history to get from
            
        Returns:
            List[EventRecord]: List of Event Records for the specified domain
        """
        history = self.histories.get(hu_id)
        if not history:
            return []
        
        return history.get_events_by_domain(domain_type)
    
    def get_syntheses_by_domain(self, domain_type: Union[str, DomainType], hu_id: str) -> List[TrajectorySynthesis]:
        """
        Get all Trajectory Syntheses for a specific domain from a Universal History.
        
        Args:
            domain_type (Union[str, DomainType]): The domain type to filter by
            hu_id (str): The ID of the history to get from
            
        Returns:
            List[TrajectorySynthesis]: List of Trajectory Syntheses for the specified domain
        """
        history = self.histories.get(hu_id)
        if not history:
            return []
        
        return history.get_syntheses_by_domain(domain_type)