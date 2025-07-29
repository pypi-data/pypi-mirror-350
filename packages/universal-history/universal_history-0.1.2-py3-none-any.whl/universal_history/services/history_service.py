"""
History service for managing Universal Histories.
"""
from typing import Dict, List, Optional, Any, Union, Set

from ..models.universal_history import UniversalHistory
from ..models.event_record import DomainType
from ..models.domain_catalog import Organization
from ..storage.repository import HistoryRepository

class HistoryService:
    """
    Service for managing Universal Histories in the Universal History system.
    """
    
    def __init__(self, repository: HistoryRepository):
        """
        Initialize the service with a repository.
        
        Args:
            repository (HistoryRepository): The repository to use for storage
        """
        self.repository = repository
    
    def create_history(self, subject_id: str, organization: Optional[Organization] = None) -> str:
        """
        Create a new Universal History.
        
        Args:
            subject_id (str): ID of the subject
            
        Returns:
            str: ID of the created Universal History
        """
        # Check if a history already exists for this subject
        existing_history = self.repository.get_history_by_subject(subject_id)
        if existing_history:
            return existing_history.hu_id
        
        # Create a new history
        history = UniversalHistory(subject_id=subject_id, organization=organization)
        
        # Save the history
        hu_id = self.repository.save_history(history)
        
        return hu_id
    
    def get_history(self, hu_id: str) -> Optional[UniversalHistory]:
        """
        Get a Universal History by ID.
        
        Args:
            hu_id (str): ID of the history
            
        Returns:
            Optional[UniversalHistory]: The history, or None if not found
        """
        return self.repository.get_history(hu_id)
    
    def get_history_by_subject(self, subject_id: str) -> Optional[UniversalHistory]:
        """
        Get a Universal History by subject ID.
        
        Args:
            subject_id (str): ID of the subject
            
        Returns:
            Optional[UniversalHistory]: The history, or None if not found
        """
        return self.repository.get_history_by_subject(subject_id)
    
    def get_subject_domains(self, subject_id: str) -> Set[str]:
        """
        Get all domains for a subject.
        
        Args:
            subject_id (str): ID of the subject
            
        Returns:
            Set[str]: Set of domain type values
        """
        history = self.repository.get_history_by_subject(subject_id)
        if not history:
            return set()
        
        return history.get_domains()
    
    def verify_event_chains(self, subject_id: str) -> Dict[str, bool]:
        """
        Verify the integrity of all event chains for a subject.
        
        This method checks that each event's previous_re_hash matches the
        current_re_hash of the previous event in the chain, for all domains.
        
        Args:
            subject_id (str): ID of the subject
            
        Returns:
            Dict[str, bool]: Dictionary mapping domain types to verification results
        """
        history = self.repository.get_history_by_subject(subject_id)
        if not history:
            return {}
        
        results = {}
        for domain in history.get_domains():
            results[domain] = history.verify_event_chain(domain)
        
        return results
    
    def export_history(self, subject_id: str, include_events: bool = True, 
                      include_syntheses: bool = True, include_state: bool = True,
                      include_catalogs: bool = True) -> Dict[str, Any]:
        """
        Export a Universal History as a dictionary.
        
        This method allows for selective export of different components of the history.
        
        Args:
            subject_id (str): ID of the subject
            include_events (bool): Whether to include Event Records
            include_syntheses (bool): Whether to include Trajectory Syntheses
            include_state (bool): Whether to include the State Document
            include_catalogs (bool): Whether to include Domain Catalogs
            
        Returns:
            Dict[str, Any]: Dictionary representation of the history
        """
        history = self.repository.get_history_by_subject(subject_id)
        if not history:
            raise ValueError(f"No Universal History found for subject {subject_id}")
        
        # Start with the basic history info
        result = {
            'hu_id': history.hu_id,
            'subject_id': history.subject_id,
            'created_at': history.created_at.isoformat(),
            'last_updated': history.last_updated.isoformat(),
        }
        
        # Add the requested components
        if include_events:
            result['event_records'] = {re_id: er.to_dict() for re_id, er in history.event_records.items()}
        
        if include_syntheses:
            result['trajectory_syntheses'] = {st_id: ts.to_dict() for st_id, ts in history.trajectory_syntheses.items()}
        
        if include_state and history.state_document:
            result['state_document'] = history.state_document.to_dict()
        
        if include_catalogs:
            result['domain_catalogs'] = {domain: catalog.to_dict() for domain, catalog in history.domain_catalogs.items()}
        
        return result
    
    def import_history(self, history_data: Dict[str, Any]) -> str:
        """
        Import a Universal History from a dictionary.
        
        Args:
            history_data (Dict[str, Any]): Dictionary representation of the history
            
        Returns:
            str: ID of the imported Universal History
        """
        # Create a new history from the data
        history = UniversalHistory.from_dict(history_data)
        
        # Save the history
        hu_id = self.repository.save_history(history)
        
        return hu_id
    
    def copy_history(self, source_subject_id: str, target_subject_id: str,
                    include_events: bool = True, include_syntheses: bool = True,
                    include_state: bool = True, include_catalogs: bool = True) -> str:
        """
        Copy a Universal History from one subject to another.
        
        Args:
            source_subject_id (str): ID of the source subject
            target_subject_id (str): ID of the target subject
            include_events (bool): Whether to include Event Records
            include_syntheses (bool): Whether to include Trajectory Syntheses
            include_state (bool): Whether to include the State Document
            include_catalogs (bool): Whether to include Domain Catalogs
            
        Returns:
            str: ID of the copied Universal History
        """
        # Export the source history
        history_data = self.export_history(
            subject_id=source_subject_id,
            include_events=include_events,
            include_syntheses=include_syntheses,
            include_state=include_state,
            include_catalogs=include_catalogs
        )
        
        # Change the subject ID and generate a new history ID
        import uuid
        history_data['subject_id'] = target_subject_id
        history_data['hu_id'] = str(uuid.uuid4())
        
        # Update subject ID in all records if needed
        if include_events and 'event_records' in history_data:
            for event_dict in history_data['event_records'].values():
                event_dict['subject_id'] = target_subject_id
        
        if include_syntheses and 'trajectory_syntheses' in history_data:
            for synthesis_dict in history_data['trajectory_syntheses'].values():
                synthesis_dict['subject_id'] = target_subject_id
        
        if include_state and 'state_document' in history_data:
            history_data['state_document']['subject_id'] = target_subject_id
        
        # Import the history for the new subject
        hu_id = self.import_history(history_data)
        
        return hu_id