"""
State service for managing and retrieving state documents.
"""
from typing import Dict, List, Optional, Any, Union
from datetime import datetime

from ..models.event_record import EventRecord, DomainType
from ..models.state_document import StateDocument, DomainState, EventReference, AggregatedInsights
from ..models.trajectory_synthesis import TrajectorySynthesis
from ..storage.repository import HistoryRepository

class StateService:
    """
    Service for managing State Documents in the Universal History system.
    """
    
    def __init__(self, repository: HistoryRepository):
        """
        Initialize the service with a repository.
        
        Args:
            repository (HistoryRepository): The repository to use for storage
        """
        self.repository = repository
    
    def create_state_document(self, subject_id: str) -> str:
        """
        Create a new State Document for a subject.
        
        Args:
            subject_id (str): ID of the subject
            
        Returns:
            str: ID of the created State Document
        """
        # Get the Universal History for this subject
        history = self.repository.get_history_by_subject(subject_id)
        if not history:
            raise ValueError(f"No Universal History found for subject {subject_id}")
        
        # Create an initial general summary
        general_summary = f"State document for subject {subject_id}, created on {datetime.now().isoformat()}"
        
        # Initialize with an empty domain state for each domain that has events
        domains = {}
        for domain in history.get_domains():
            domains[domain] = DomainState(
                last_updated=datetime.now(),
                current_status="No detailed state information available yet",
                key_attributes={},
                recent_events=[],
                significant_events=[],
                trends={},
                domain_specific_data={}
            )
        
        # Create the state document
        state_document = StateDocument(
            subject_id=subject_id,
            general_summary=general_summary,
            domains=domains
        )
        
        # Save the state document
        de_id = self.repository.save_state_document(state_document, history.hu_id)
        
        return de_id
    
    def get_state_document(self, subject_id: str) -> Optional[StateDocument]:
        """
        Get the State Document for a subject.
        
        Args:
            subject_id (str): ID of the subject
            
        Returns:
            Optional[StateDocument]: The State Document, or None if not found
        """
        history = self.repository.get_history_by_subject(subject_id)
        if not history:
            return None
        
        return self.repository.get_state_document(history.hu_id)
    
    def update_domain_state(self, 
                           subject_id: str, 
                           domain_type: Union[str, DomainType],
                           current_status: Optional[str] = None,
                           key_attributes: Optional[Dict[str, Any]] = None,
                           recent_events: Optional[List[Dict[str, str]]] = None,
                           significant_events: Optional[List[Dict[str, str]]] = None,
                           trends: Optional[Dict[str, str]] = None,
                           domain_specific_data: Optional[Dict[str, Any]] = None) -> str:
        """
        Update the state for a specific domain.
        
        Args:
            subject_id (str): ID of the subject
            domain_type (Union[str, DomainType]): The domain type
            current_status (Optional[str]): Current status of the domain
            key_attributes (Optional[Dict[str, Any]]): Key attributes for the domain
            recent_events (Optional[List[Dict[str, str]]]): Recent events (each dict must have 're_id', 'description', and optionally 'impact')
            significant_events (Optional[List[Dict[str, str]]]): Significant events (each dict must have 're_id', 'description', and optionally 'significance')
            trends (Optional[Dict[str, str]]): Trends in the domain
            domain_specific_data (Optional[Dict[str, Any]]): Domain-specific data
            
        Returns:
            str: ID of the updated State Document
        """
        # Get the Universal History for this subject
        history = self.repository.get_history_by_subject(subject_id)
        if not history:
            raise ValueError(f"No Universal History found for subject {subject_id}")
        
        # Get the State Document, or create one if it doesn't exist
        state_document = self.repository.get_state_document(history.hu_id)
        if not state_document:
            de_id = self.create_state_document(subject_id)
            state_document = self.repository.get_state_document(history.hu_id)
            if not state_document:
                raise ValueError(f"Failed to create State Document for subject {subject_id}")
        
        # Convert domain_type to string if it's an enum
        domain_key = domain_type.value if isinstance(domain_type, DomainType) else domain_type
        
        # Get the current domain state or create a new one
        if domain_key in state_document.domains:
            domain_state = state_document.domains[domain_key]
        else:
            domain_state = DomainState(
                last_updated=datetime.now(),
                current_status="No detailed state information available yet",
                key_attributes={},
                recent_events=[],
                significant_events=[],
                trends={},
                domain_specific_data={}
            )
        
        # Update the domain state with the provided values
        if current_status is not None:
            domain_state.current_status = current_status
        
        if key_attributes is not None:
            domain_state.key_attributes = key_attributes
        
        if recent_events is not None:
            domain_state.recent_events = [
                EventReference(
                    re_id=event['re_id'],
                    description=event['description'],
                    impact=event.get('impact')
                )
                for event in recent_events
            ]
        
        if significant_events is not None:
            domain_state.significant_events = [
                EventReference(
                    re_id=event['re_id'],
                    description=event['description'],
                    significance=event.get('significance')
                )
                for event in significant_events
            ]
        
        if trends is not None:
            domain_state.trends = trends
        
        if domain_specific_data is not None:
            domain_state.domain_specific_data = domain_specific_data
        
        # Update the last_updated timestamp
        domain_state.last_updated = datetime.now()
        
        # Update the domain state in the state document
        state_document.update_domain_state(domain_key, domain_state)
        
        # Save the state document
        de_id = self.repository.save_state_document(state_document, history.hu_id)
        
        return de_id
    
    def update_aggregated_insights(self,
                                  subject_id: str,
                                  cross_domain_patterns: Optional[List[str]] = None,
                                  recommended_actions: Optional[List[str]] = None,
                                  potential_opportunities: Optional[List[str]] = None,
                                  potential_risks: Optional[List[str]] = None) -> str:
        """
        Update the aggregated insights in the State Document.
        
        Args:
            subject_id (str): ID of the subject
            cross_domain_patterns (Optional[List[str]]): Patterns across domains
            recommended_actions (Optional[List[str]]): Recommended actions
            potential_opportunities (Optional[List[str]]): Potential opportunities
            potential_risks (Optional[List[str]]): Potential risks
            
        Returns:
            str: ID of the updated State Document
        """
        # Get the Universal History for this subject
        history = self.repository.get_history_by_subject(subject_id)
        if not history:
            raise ValueError(f"No Universal History found for subject {subject_id}")
        
        # Get the State Document, or create one if it doesn't exist
        state_document = self.repository.get_state_document(history.hu_id)
        if not state_document:
            de_id = self.create_state_document(subject_id)
            state_document = self.repository.get_state_document(history.hu_id)
            if not state_document:
                raise ValueError(f"Failed to create State Document for subject {subject_id}")
        
        # Update the aggregated insights
        if cross_domain_patterns is not None:
            state_document.aggregated_insights.cross_domain_patterns = cross_domain_patterns
        
        if recommended_actions is not None:
            state_document.aggregated_insights.recommended_actions = recommended_actions
        
        if potential_opportunities is not None:
            state_document.aggregated_insights.potential_opportunities = potential_opportunities
        
        if potential_risks is not None:
            state_document.aggregated_insights.potential_risks = potential_risks
        
        # Update the last_updated timestamp
        state_document.update_last_updated()
        
        # Save the state document
        de_id = self.repository.save_state_document(state_document, history.hu_id)
        
        return de_id
    
    def update_llm_optimized_summary(self, subject_id: str) -> str:
        """
        Update the LLM-optimized summary in the State Document.
        
        This method generates a new summary optimized for use with LLMs,
        based on the current state of the document.
        
        Args:
            subject_id (str): ID of the subject
            
        Returns:
            str: The updated LLM-optimized summary
        """
        # Get the Universal History for this subject
        history = self.repository.get_history_by_subject(subject_id)
        if not history:
            raise ValueError(f"No Universal History found for subject {subject_id}")
        
        # Get the State Document, or create one if it doesn't exist
        state_document = self.repository.get_state_document(history.hu_id)
        if not state_document:
            de_id = self.create_state_document(subject_id)
            state_document = self.repository.get_state_document(history.hu_id)
            if not state_document:
                raise ValueError(f"Failed to create State Document for subject {subject_id}")
        
        # Generate the LLM-optimized summary
        summary = state_document.generate_llm_optimized_summary()
        
        # Save the state document
        self.repository.save_state_document(state_document, history.hu_id)
        
        return summary
    
    def get_llm_optimized_summary(self, subject_id: str) -> Optional[str]:
        """
        Get the LLM-optimized summary for a subject.
        
        Args:
            subject_id (str): ID of the subject
            
        Returns:
            Optional[str]: The LLM-optimized summary, or None if not found
        """
        state_document = self.get_state_document(subject_id)
        if not state_document:
            return None
        
        # Generate a new summary if it doesn't exist
        if not state_document.llm_optimized_summary:
            return self.update_llm_optimized_summary(subject_id)
        
        return state_document.llm_optimized_summary
    
    def update_state_from_events(self, subject_id: str, domain_type: Union[str, DomainType], limit: int = 10) -> str:
        """
        Update the domain state based on recent events.
        
        This method analyzes the most recent events for a domain and updates
        the domain state accordingly.
        
        Args:
            subject_id (str): ID of the subject
            domain_type (Union[str, DomainType]): The domain type
            limit (int): Maximum number of events to consider
            
        Returns:
            str: ID of the updated State Document
        """
        # Get the Universal History for this subject
        history = self.repository.get_history_by_subject(subject_id)
        if not history:
            raise ValueError(f"No Universal History found for subject {subject_id}")
        
        # Get events for the domain
        events = self.repository.get_events_by_domain(domain_type, history.hu_id)
        
        # Sort by timestamp (newest first) and limit
        sorted_events = sorted(events, key=lambda e: e.timestamp, reverse=True)
        recent_events = sorted_events[:limit]
        
        # Create recent event references
        event_references = [
            {
                're_id': event.re_id,
                'description': f"{event.event_type} - {event.raw_input.content[:50]}..."
            }
            for event in recent_events
        ]
        
        # TODO: Implement more sophisticated analysis of events to update the state
        # For now, just update the recent events and a simple current status
        current_status = f"Based on {len(recent_events)} recent events"
        if recent_events:
            current_status += f", the most recent being a {recent_events[0].event_type} on {recent_events[0].timestamp.isoformat()}"
        
        # Update the domain state
        de_id = self.update_domain_state(
            subject_id=subject_id,
            domain_type=domain_type,
            current_status=current_status,
            recent_events=event_references
        )
        
        return de_id
    
    def update_state_from_synthesis(self, subject_id: str, st_id: str) -> str:
        """
        Update the domain state based on a Trajectory Synthesis.
        
        This method incorporates insights from a Trajectory Synthesis into
        the domain state.
        
        Args:
            subject_id (str): ID of the subject
            st_id (str): ID of the Trajectory Synthesis
            
        Returns:
            str: ID of the updated State Document
        """
        # Get the Universal History for this subject
        history = self.repository.get_history_by_subject(subject_id)
        if not history:
            raise ValueError(f"No Universal History found for subject {subject_id}")
        
        # Get the Trajectory Synthesis
        synthesis = self.repository.get_trajectory_synthesis(st_id, history.hu_id)
        if not synthesis:
            raise ValueError(f"Trajectory Synthesis with ID {st_id} not found")
        
        # Convert domain_type to string if it's an enum
        domain_type = synthesis.domain_type
        
        # Convert significant events from the synthesis to event references
        significant_events = [
            {
                're_id': event.re_id,
                'description': event.description,
                'significance': event.significance
            }
            for event in synthesis.significant_events
        ]
        
        # Convert metrics from the synthesis to key attributes
        key_attributes = {
            metric_name: metric.value
            for metric_name, metric in synthesis.metrics.items()
        }
        
        # Convert patterns from the synthesis to trends
        trends = {
            f"pattern_{i}": pattern
            for i, pattern in enumerate(synthesis.patterns)
        }
        
        # Update the domain state
        de_id = self.update_domain_state(
            subject_id=subject_id,
            domain_type=domain_type,
            current_status=synthesis.summary,
            key_attributes=key_attributes,
            significant_events=significant_events,
            trends=trends
        )
        
        return de_id