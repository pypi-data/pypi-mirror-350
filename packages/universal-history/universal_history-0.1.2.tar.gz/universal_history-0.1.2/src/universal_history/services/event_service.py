"""
Event service for creating and retrieving event records.
"""
from typing import Dict, List, Optional, Any, Union, Tuple
from datetime import datetime

from ..models.event_record import EventRecord, DomainType, RawInput, Source, SourceType, ProcessedData
from ..models.universal_history import UniversalHistory
from ..storage.repository import HistoryRepository

class EventService:
    """
    Service for managing Event Records in the Universal History system.
    """
    
    def __init__(self, repository: HistoryRepository):
        """
        Initialize the service with a repository.
        
        Args:
            repository (HistoryRepository): The repository to use for storage
        """
        self.repository = repository
    
    def create_event_record(self, 
                           subject_id: str,
                           domain_type: Union[str, DomainType],
                           event_type: str,
                           content: str,
                           content_type: str,
                           source_type: str,
                           source_id: str,
                           source_name: str,
                           creator_id: Optional[str] = None,
                           creator_name: Optional[str] = None,
                           creator_role: Optional[str] = None,
                           context: Optional[Dict[str, Any]] = None,
                           metrics: Optional[Dict[str, float]] = None,
                           assessments: Optional[Dict[str, str]] = None,
                           insights: Optional[List[str]] = None,
                           tags: Optional[List[str]] = None) -> Tuple[str, str]:
        """
        Create a new Event Record and add it to the appropriate Universal History.
        
        Args:
            subject_id (str): ID of the subject
            domain_type (Union[str, DomainType]): The domain type
            event_type (str): Type of event
            content (str): Raw content of the event
            content_type (str): Type of content (text, audio, video, image)
            source_type (str): Type of source (institution, individual, system, etc.)
            source_id (str): ID of the source
            source_name (str): Name of the source
            creator_id (Optional[str]): ID of the creator
            creator_name (Optional[str]): Name of the creator
            creator_role (Optional[str]): Role of the creator
            context (Optional[Dict[str, Any]]): Context information
            metrics (Optional[Dict[str, float]]): Quantitative metrics
            assessments (Optional[Dict[str, str]]): Qualitative assessments
            insights (Optional[List[str]]): Derived insights
            tags (Optional[List[str]]): Tags for the event
            
        Returns:
            Tuple[str, str]: (History ID, Event Record ID)
        """
        # Get or create the Universal History for this subject
        history = self.repository.get_history_by_subject(subject_id)
        if not history:
            # Create a new history
            history = UniversalHistory(subject_id=subject_id)
            self.repository.save_history(history)
        
        # Convert domain_type to enum if it's a string
        if isinstance(domain_type, str):
            domain_type = DomainType(domain_type)
        
        # Create the raw input
        raw_input = RawInput(
            type=content_type,
            content=content
        )
        
        # Create the source
        source_kwargs = {
            'type': source_type,
            'id': source_id,
            'name': source_name
        }
        
        # Add creator if provided
        if creator_id and creator_name and creator_role:
            from ..models.event_record import Creator
            source_kwargs['creator'] = Creator(
                id=creator_id,
                name=creator_name,
                role=creator_role
            )
        
        source = Source(**source_kwargs)
        
        # Create the event record
        event_record_kwargs = {
            'subject_id': subject_id,
            'domain_type': domain_type,
            'event_type': event_type,
            'raw_input': raw_input,
            'source': source
        }
        
        # Set processed data if provided
        if metrics or assessments or insights:
            event_record_kwargs['processed_data'] = ProcessedData(
                quantitative_metrics=metrics or {},
                qualitative_assessments=assessments or {},
                derived_insights=insights or []
            )
        
        # Set context if provided
        if context:
            from ..models.event_record import Context
            event_record_kwargs['context'] = Context(
                location=context.get('location'),
                participants=context.get('participants', []),
                environmental_factors=context.get('environmental_factors', [])
            )
        
        # Set tags if provided
        if tags:
            from ..models.event_record import Metadata
            event_record_kwargs['metadata'] = Metadata(
                tags=tags
            )
        
        # Create the event record
        event_record = EventRecord(**event_record_kwargs)
        
        # Add the event record to the history
        event_record_id = self.repository.save_event_record(event_record, history.hu_id)
        
        return history.hu_id, event_record_id
    
    def get_event_record(self, re_id: str, hu_id: str) -> Optional[EventRecord]:
        """
        Get an Event Record by ID.
        
        Args:
            re_id (str): ID of the event record
            hu_id (str): ID of the history
            
        Returns:
            Optional[EventRecord]: The event record, or None if not found
        """
        return self.repository.get_event_record(re_id, hu_id)
    
    def get_events_by_domain(self, subject_id: str, domain_type: Union[str, DomainType]) -> List[EventRecord]:
        """
        Get all Event Records for a specific domain and subject.
        
        Args:
            subject_id (str): ID of the subject
            domain_type (Union[str, DomainType]): The domain type
            
        Returns:
            List[EventRecord]: List of event records
        """
        history = self.repository.get_history_by_subject(subject_id)
        if not history:
            return []
        
        return self.repository.get_events_by_domain(domain_type, history.hu_id)
    
    def get_recent_events(self, subject_id: str, limit: int = 10) -> List[EventRecord]:
        """
        Get the most recent Event Records for a subject.
        
        Args:
            subject_id (str): ID of the subject
            limit (int): Maximum number of events to return
            
        Returns:
            List[EventRecord]: List of recent event records
        """
        history = self.repository.get_history_by_subject(subject_id)
        if not history:
            return []
        
        # Get all events for this history
        all_events = []
        for domain in history.get_domains():
            domain_events = self.repository.get_events_by_domain(domain, history.hu_id)
            all_events.extend(domain_events)
        
        # Sort by timestamp (newest first) and limit
        sorted_events = sorted(all_events, key=lambda e: e.timestamp, reverse=True)
        return sorted_events[:limit]
    
    def search_events(self, 
                     subject_id: str, 
                     domain_type: Optional[Union[str, DomainType]] = None,
                     event_type: Optional[str] = None,
                     start_date: Optional[datetime] = None,
                     end_date: Optional[datetime] = None,
                     tags: Optional[List[str]] = None) -> List[EventRecord]:
        """
        Search for Event Records with specific criteria.
        
        Args:
            subject_id (str): ID of the subject
            domain_type (Optional[Union[str, DomainType]]): The domain type to filter by
            event_type (Optional[str]): The event type to filter by
            start_date (Optional[datetime]): Include events after this date
            end_date (Optional[datetime]): Include events before this date
            tags (Optional[List[str]]): Include events with any of these tags
            
        Returns:
            List[EventRecord]: List of matching event records
        """
        history = self.repository.get_history_by_subject(subject_id)
        if not history:
            return []
        
        # Get events, filtered by domain if specified
        if domain_type:
            events = self.repository.get_events_by_domain(domain_type, history.hu_id)
        else:
            # Get all events for this history
            events = []
            for domain in history.get_domains():
                domain_events = self.repository.get_events_by_domain(domain, history.hu_id)
                events.extend(domain_events)
        
        # Apply additional filters
        filtered_events = []
        for event in events:
            # Filter by event type
            if event_type and event.event_type != event_type:
                continue
                
            # Filter by date range
            if start_date and event.timestamp < start_date:
                continue
            if end_date and event.timestamp > end_date:
                continue
                
            # Filter by tags
            if tags:
                event_tags = event.metadata.tags if hasattr(event.metadata, 'tags') else []
                if not any(tag in event_tags for tag in tags):
                    continue
            
            filtered_events.append(event)
        
        # Sort by timestamp (newest first)
        return sorted(filtered_events, key=lambda e: e.timestamp, reverse=True)
    
    def verify_event_chain(self, subject_id: str, domain_type: Union[str, DomainType]) -> bool:
        """
        Verify the integrity of the event chain for a specific domain and subject.
        
        Args:
            subject_id (str): ID of the subject
            domain_type (Union[str, DomainType]): The domain type
            
        Returns:
            bool: True if the chain is valid, False otherwise
        """
        history = self.repository.get_history_by_subject(subject_id)
        if not history:
            return True  # No history, so technically valid
        
        return history.verify_event_chain(domain_type)
