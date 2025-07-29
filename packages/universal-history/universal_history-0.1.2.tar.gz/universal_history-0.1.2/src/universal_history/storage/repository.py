"""
Repository interfaces and implementations for storage of Universal History objects.
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Union
import json
import os
import shutil
from datetime import datetime

from ..models.event_record import EventRecord, DomainType
from ..models.trajectory_synthesis import TrajectorySynthesis
from ..models.state_document import StateDocument
from ..models.domain_catalog import DomainCatalog
from ..models.universal_history import UniversalHistory

class HistoryRepository(ABC):
    """
    Abstract base class for Universal History repositories.
    
    This class defines the interface that all storage implementations must follow.
    """
    
    @abstractmethod
    def save_history(self, history: UniversalHistory) -> str:
        """
        Save a Universal History.
        
        Args:
            history (UniversalHistory): The history to save
            
        Returns:
            str: The ID of the saved history
        """
        pass
    
    @abstractmethod
    def get_history(self, hu_id: str) -> Optional[UniversalHistory]:
        """
        Get a Universal History by ID.
        
        Args:
            hu_id (str): The ID of the history to get
            
        Returns:
            Optional[UniversalHistory]: The history or None if not found
        """
        pass
    
    @abstractmethod
    def get_history_by_subject(self, subject_id: str) -> Optional[UniversalHistory]:
        """
        Get a Universal History by subject ID.
        
        Args:
            subject_id (str): The subject ID to look for
            
        Returns:
            Optional[UniversalHistory]: The history or None if not found
        """
        pass
    
    @abstractmethod
    def save_event_record(self, event_record: EventRecord, hu_id: str) -> str:
        """
        Save an Event Record to a Universal History.
        
        Args:
            event_record (EventRecord): The event record to save
            hu_id (str): The ID of the history to save to
            
        Returns:
            str: The ID of the saved event record
        """
        pass
    
    @abstractmethod
    def get_event_record(self, re_id: str, hu_id: str) -> Optional[EventRecord]:
        """
        Get an Event Record by ID from a Universal History.
        
        Args:
            re_id (str): The ID of the event record to get
            hu_id (str): The ID of the history to get from
            
        Returns:
            Optional[EventRecord]: The event record or None if not found
        """
        pass
    
    @abstractmethod
    def save_trajectory_synthesis(self, synthesis: TrajectorySynthesis, hu_id: str) -> str:
        """
        Save a Trajectory Synthesis to a Universal History.
        
        Args:
            synthesis (TrajectorySynthesis): The synthesis to save
            hu_id (str): The ID of the history to save to
            
        Returns:
            str: The ID of the saved synthesis
        """
        pass
    
    @abstractmethod
    def get_trajectory_synthesis(self, st_id: str, hu_id: str) -> Optional[TrajectorySynthesis]:
        """
        Get a Trajectory Synthesis by ID from a Universal History.
        
        Args:
            st_id (str): The ID of the synthesis to get
            hu_id (str): The ID of the history to get from
            
        Returns:
            Optional[TrajectorySynthesis]: The synthesis or None if not found
        """
        pass
    
    @abstractmethod
    def save_state_document(self, state_document: StateDocument, hu_id: str) -> str:
        """
        Save a State Document to a Universal History.
        
        Args:
            state_document (StateDocument): The state document to save
            hu_id (str): The ID of the history to save to
            
        Returns:
            str: The ID of the saved state document
        """
        pass
    
    @abstractmethod
    def get_state_document(self, hu_id: str) -> Optional[StateDocument]:
        """
        Get the State Document from a Universal History.
        
        Args:
            hu_id (str): The ID of the history to get from
            
        Returns:
            Optional[StateDocument]: The state document or None if not found
        """
        pass
    
    @abstractmethod
    def save_domain_catalog(self, domain_catalog: DomainCatalog, hu_id: str) -> str:
        """
        Save a Domain Catalog to a Universal History.
        
        Args:
            domain_catalog (DomainCatalog): The domain catalog to save
            hu_id (str): The ID of the history to save to
            
        Returns:
            str: The ID of the saved domain catalog
        """
        pass
    
    @abstractmethod
    def get_domain_catalog(self, domain_type: Union[str, DomainType], hu_id: str) -> Optional[DomainCatalog]:
        """
        Get a Domain Catalog by domain type from a Universal History.
        
        Args:
            domain_type (Union[str, DomainType]): The domain type to get the catalog for
            hu_id (str): The ID of the history to get from
            
        Returns:
            Optional[DomainCatalog]: The domain catalog or None if not found
        """
        pass
    
    @abstractmethod
    def get_events_by_domain(self, domain_type: Union[str, DomainType], hu_id: str) -> List[EventRecord]:
        """
        Get all Event Records for a specific domain from a Universal History.
        
        Args:
            domain_type (Union[str, DomainType]): The domain type to filter by
            hu_id (str): The ID of the history to get from
            
        Returns:
            List[EventRecord]: List of Event Records for the specified domain
        """
        pass
    
    @abstractmethod
    def get_syntheses_by_domain(self, domain_type: Union[str, DomainType], hu_id: str) -> List[TrajectorySynthesis]:
        """
        Get all Trajectory Syntheses for a specific domain from a Universal History.
        
        Args:
            domain_type (Union[str, DomainType]): The domain type to filter by
            hu_id (str): The ID of the history to get from
            
        Returns:
            List[TrajectorySynthesis]: List of Trajectory Syntheses for the specified domain
        """
        pass

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

class FileHistoryRepository(HistoryRepository):
    """
    File-based implementation of the HistoryRepository.
    
    This implementation stores data in JSON files, which is suitable for
    small to medium-scale usage and persists data across restarts.
    """
    
    def __init__(self, storage_dir: str):
        """
        Initialize the repository with a storage directory.
        
        Args:
            storage_dir (str): Directory where history files will be stored
        """
        self.storage_dir = storage_dir
        
        # Create directories if they don't exist
        os.makedirs(self.storage_dir, exist_ok=True)
        os.makedirs(os.path.join(self.storage_dir, "histories"), exist_ok=True)
        os.makedirs(os.path.join(self.storage_dir, "indexes"), exist_ok=True)
        
        # Load or create the subject index
        self.subject_index_path = os.path.join(self.storage_dir, "indexes", "subject_to_history.json")
        self.subject_to_history = self._load_subject_index()
    
    def _load_subject_index(self) -> Dict[str, str]:
        """
        Load the subject index from disk.
        
        Returns:
            Dict[str, str]: The subject index (subject_id -> hu_id)
        """
        if os.path.exists(self.subject_index_path):
            with open(self.subject_index_path, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_subject_index(self) -> None:
        """Save the subject index to disk."""
        with open(self.subject_index_path, 'w') as f:
            json.dump(self.subject_to_history, f)
    
    def _get_history_path(self, hu_id: str) -> str:
        """
        Get the path to a history file.
        
        Args:
            hu_id (str): The ID of the history
            
        Returns:
            str: The path to the history file
        """
        return os.path.join(self.storage_dir, "histories", f"{hu_id}.json")
    
    def save_history(self, history: UniversalHistory) -> str:
        """
        Save a Universal History.
        
        Args:
            history (UniversalHistory): The history to save
            
        Returns:
            str: The ID of the saved history
        """
        # Save the history
        history_path = self._get_history_path(history.hu_id)
        with open(history_path, 'w') as f:
            json.dump(history.to_dict(), f, default=str)
        
        # Update the subject index
        self.subject_to_history[history.subject_id] = history.hu_id
        self._save_subject_index()
        
        return history.hu_id
    
    def get_history(self, hu_id: str) -> Optional[UniversalHistory]:
        """
        Get a Universal History by ID.
        
        Args:
            hu_id (str): The ID of the history to get
            
        Returns:
            Optional[UniversalHistory]: The history or None if not found
        """
        history_path = self._get_history_path(hu_id)
        
        if not os.path.exists(history_path):
            return None
        
        with open(history_path, 'r') as f:
            history_data = json.load(f)
            
        return UniversalHistory.from_dict(history_data)
    
    def get_history_by_subject(self, subject_id: str) -> Optional[UniversalHistory]:
        """
        Get a Universal History by subject ID.
        
        Args:
            subject_id (str): The subject ID to look for
            
        Returns:
            Optional[UniversalHistory]: The history or None if not found
        """
        hu_id = self.subject_to_history.get(subject_id)
        if not hu_id:
            return None
            
        return self.get_history(hu_id)
    
    def save_event_record(self, event_record: EventRecord, hu_id: str) -> str:
        """
        Save an Event Record to a Universal History.
        
        Args:
            event_record (EventRecord): The event record to save
            hu_id (str): The ID of the history to save to
            
        Returns:
            str: The ID of the saved event record
        """
        # Get the history
        history = self.get_history(hu_id)
        if not history:
            raise ValueError(f"Universal History with ID {hu_id} not found")
        
        # Add the event record
        history.add_event_record(event_record)
        
        # Save the history
        self.save_history(history)
        
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
        history = self.get_history(hu_id)
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
        # Get the history
        history = self.get_history(hu_id)
        if not history:
            raise ValueError(f"Universal History with ID {hu_id} not found")
        
        # Add the synthesis
        history.add_trajectory_synthesis(synthesis)
        
        # Save the history
        self.save_history(history)
        
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
        history = self.get_history(hu_id)
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
        # Get the history
        history = self.get_history(hu_id)
        if not history:
            raise ValueError(f"Universal History with ID {hu_id} not found")
        
        # Set the state document
        history.set_state_document(state_document)
        
        # Save the history
        self.save_history(history)
        
        return state_document.de_id
    
    def get_state_document(self, hu_id: str) -> Optional[StateDocument]:
        """
        Get the State Document from a Universal History.
        
        Args:
            hu_id (str): The ID of the history to get from
            
        Returns:
            Optional[StateDocument]: The state document or None if not found
        """
        history = self.get_history(hu_id)
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
        # Get the history
        history = self.get_history(hu_id)
        if not history:
            raise ValueError(f"Universal History with ID {hu_id} not found")
        
        # Add the domain catalog
        history.add_domain_catalog(domain_catalog)
        
        # Save the history
        self.save_history(history)
        
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
        history = self.get_history(hu_id)
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
        history = self.get_history(hu_id)
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
        history = self.get_history(hu_id)
        if not history:
            return []
            
        return history.get_syntheses_by_domain(domain_type)
    
    def backup(self, backup_dir: str) -> None:
        """
        Create a backup of all histories.
        
        Args:
            backup_dir (str): Directory where the backup will be stored
        """
        # Create the backup directory
        os.makedirs(backup_dir, exist_ok=True)
        
        # Copy all files
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(backup_dir, f"backup_{timestamp}")
        shutil.copytree(self.storage_dir, backup_path)
