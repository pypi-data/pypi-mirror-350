"""
Synthesis service for creating and managing trajectory syntheses.
"""
from typing import Dict, List, Optional, Any, Union, Tuple
from datetime import datetime

from ..models.event_record import DomainType
from ..models.trajectory_synthesis import TrajectorySynthesis, TimeFrame, SignificantEvent, Metric
from ..models.state_document import StateDocument
from ..storage.repository import HistoryRepository

class SynthesisService:
    """
    Service for managing Trajectory Syntheses in the Universal History system.
    """
    
    def __init__(self, repository: HistoryRepository):
        """
        Initialize the service with a repository.
        
        Args:
            repository (HistoryRepository): The repository to use for storage
        """
        self.repository = repository
    
    def create_trajectory_synthesis(self,
                                   subject_id: str,
                                   domain_type: Union[str, DomainType],
                                   summary: str,
                                   start_date: datetime,
                                   end_date: datetime,
                                   source_events: List[str],
                                   key_insights: Optional[List[str]] = None,
                                   significant_events: Optional[List[Dict[str, str]]] = None,
                                   metrics: Optional[Dict[str, Dict[str, Any]]] = None,
                                   patterns: Optional[List[str]] = None,
                                   recommendations: Optional[List[str]] = None,
                                   level: int = 1) -> Tuple[str, str]:
        """
        Create a new Trajectory Synthesis.
        
        Args:
            subject_id (str): ID of the subject
            domain_type (Union[str, DomainType]): The domain type
            summary (str): Summary of the trajectory
            start_date (datetime): Start date of the period covered
            end_date (datetime): End date of the period covered
            source_events (List[str]): IDs of the source Event Records
            key_insights (Optional[List[str]]): Key insights from the synthesis
            significant_events (Optional[List[Dict[str, str]]]): Significant events (each dict must have 're_id', 'description', and 'significance')
            metrics (Optional[Dict[str, Dict[str, Any]]]): Metrics (metric_name -> {value, trend, analysis})
            patterns (Optional[List[str]]): Patterns identified
            recommendations (Optional[List[str]]): Recommendations
            level (int): Hierarchical level (1=most detailed, higher numbers=more summarized)
            
        Returns:
            Tuple[str, str]: (History ID, Trajectory Synthesis ID)
        """
        # Get the Universal History for this subject
        history = self.repository.get_history_by_subject(subject_id)
        if not history:
            raise ValueError(f"No Universal History found for subject {subject_id}")
        
        # Convert domain_type to enum if it's a string
        if isinstance(domain_type, str):
            domain_type = DomainType(domain_type)
        
        # Create the time frame
        time_frame = TimeFrame(
            start=start_date,
            end=end_date
        )
        
        # Create significant events if provided
        sig_events = []
        if significant_events:
            sig_events = [
                SignificantEvent(
                    re_id=event['re_id'],
                    description=event['description'],
                    significance=event['significance']
                )
                for event in significant_events
            ]
        
        # Create metrics if provided
        metrics_dict = {}
        if metrics:
            metrics_dict = {
                metric_name: Metric(
                    value=metric_data['value'],
                    trend=metric_data['trend'],
                    analysis=metric_data.get('analysis')
                )
                for metric_name, metric_data in metrics.items()
            }
        
        # Create the trajectory synthesis
        synthesis = TrajectorySynthesis(
            subject_id=subject_id,
            domain_type=domain_type,
            time_frame=time_frame,
            summary=summary,
            level=level,
            source_events=source_events,
            key_insights=key_insights or [],
            significant_events=sig_events,
            metrics=metrics_dict,
            patterns=patterns or [],
            recommendations=recommendations or []
        )
        
        # Save the trajectory synthesis
        st_id = self.repository.save_trajectory_synthesis(synthesis, history.hu_id)
        
        return history.hu_id, st_id
    
    def get_trajectory_synthesis(self, st_id: str, hu_id: str) -> Optional[TrajectorySynthesis]:
        """
        Get a Trajectory Synthesis by ID.
        
        Args:
            st_id (str): ID of the synthesis
            hu_id (str): ID of the history
            
        Returns:
            Optional[TrajectorySynthesis]: The synthesis, or None if not found
        """
        return self.repository.get_trajectory_synthesis(st_id, hu_id)
    
    def get_syntheses_by_domain(self, subject_id: str, domain_type: Union[str, DomainType]) -> List[TrajectorySynthesis]:
        """
        Get all Trajectory Syntheses for a specific domain and subject.
        
        Args:
            subject_id (str): ID of the subject
            domain_type (Union[str, DomainType]): The domain type
            
        Returns:
            List[TrajectorySynthesis]: List of syntheses
        """
        history = self.repository.get_history_by_subject(subject_id)
        if not history:
            return []
        
        return self.repository.get_syntheses_by_domain(domain_type, history.hu_id)
    
    def get_syntheses_by_level(self, subject_id: str, level: int, domain_type: Optional[Union[str, DomainType]] = None) -> List[TrajectorySynthesis]:
        """
        Get all Trajectory Syntheses for a specific level.
        
        Args:
            subject_id (str): ID of the subject
            level (int): The hierarchical level to filter by
            domain_type (Optional[Union[str, DomainType]]): The domain type to filter by
            
        Returns:
            List[TrajectorySynthesis]: List of syntheses
        """
        history = self.repository.get_history_by_subject(subject_id)
        if not history:
            return []
        
        # Get syntheses, filtered by domain if specified
        if domain_type:
            syntheses = self.repository.get_syntheses_by_domain(domain_type, history.hu_id)
        else:
            # Get all syntheses for this history
            syntheses = []
            for domain in history.get_domains():
                domain_syntheses = self.repository.get_syntheses_by_domain(domain, history.hu_id)
                syntheses.extend(domain_syntheses)
        
        # Filter by level
        return [s for s in syntheses if s.level == level]
    
    def generate_synthesis_from_events(self,
                                      subject_id: str,
                                      domain_type: Union[str, DomainType],
                                      start_date: datetime,
                                      end_date: datetime,
                                      level: int = 1) -> str:
        """
        Generate a Trajectory Synthesis from Event Records.
        
        This method analyzes the events in a specific time period and domain,
        and generates a synthesis of the trajectory.
        
        Args:
            subject_id (str): ID of the subject
            domain_type (Union[str, DomainType]): The domain type
            start_date (datetime): Start date of the period to analyze
            end_date (datetime): End date of the period to analyze
            level (int): Hierarchical level of the synthesis
            
        Returns:
            str: ID of the generated Trajectory Synthesis
        """
        # Get the Universal History for this subject
        history = self.repository.get_history_by_subject(subject_id)
        if not history:
            raise ValueError(f"No Universal History found for subject {subject_id}")
        
        # Get events for the domain
        events = self.repository.get_events_by_domain(domain_type, history.hu_id)
        
        # Filter events by date range
        filtered_events = [
            e for e in events 
            if start_date <= e.timestamp <= end_date
        ]
        
        if not filtered_events:
            raise ValueError(f"No events found for domain {domain_type} in the specified time period")
        
        # Sort events by timestamp
        sorted_events = sorted(filtered_events, key=lambda e: e.timestamp)
        
        # Get event IDs
        source_events = [e.re_id for e in sorted_events]
        
        # Generate a simple summary
        summary = f"Synthesis of {len(sorted_events)} events in domain {domain_type} from {start_date.isoformat()} to {end_date.isoformat()}"
        
        # TODO: Implement more sophisticated analysis to generate insights, metrics, patterns, etc.
        # For now, create a basic synthesis with just a summary and source events
        
        # Create the synthesis
        _, st_id = self.create_trajectory_synthesis(
            subject_id=subject_id,
            domain_type=domain_type,
            summary=summary,
            start_date=start_date,
            end_date=end_date,
            source_events=source_events,
            level=level
        )
        
        return st_id
    
    def generate_higher_level_synthesis(self,
                                       subject_id: str,
                                       domain_type: Union[str, DomainType],
                                       source_synthesis_ids: List[str]) -> str:
        """
        Generate a higher-level Trajectory Synthesis from lower-level ones.
        
        This method combines multiple syntheses into a higher-level synthesis
        that covers a broader time period or provides a more summarized view.
        
        Args:
            subject_id (str): ID of the subject
            domain_type (Union[str, DomainType]): The domain type
            source_synthesis_ids (List[str]): IDs of the source Trajectory Syntheses
            
        Returns:
            str: ID of the generated Trajectory Synthesis
        """
        # Get the Universal History for this subject
        history = self.repository.get_history_by_subject(subject_id)
        if not history:
            raise ValueError(f"No Universal History found for subject {subject_id}")
        
        # Get the source syntheses
        source_syntheses = []
        for st_id in source_synthesis_ids:
            synthesis = self.repository.get_trajectory_synthesis(st_id, history.hu_id)
            if synthesis:
                source_syntheses.append(synthesis)
        
        if not source_syntheses:
            raise ValueError("No valid source syntheses found")
        
        # Determine the level of the new synthesis
        max_level = max(s.level for s in source_syntheses)
        new_level = max_level + 1
        
        # Determine the time frame of the new synthesis
        start_dates = [s.time_frame.start for s in source_syntheses]
        end_dates = [s.time_frame.end for s in source_syntheses]
        start_date = min(start_dates)
        end_date = max(end_dates)
        
        # Collect source events from all syntheses
        source_events = []
        for synthesis in source_syntheses:
            source_events.extend(synthesis.source_events)
        # Remove duplicates
        source_events = list(set(source_events))
        
        # Collect key insights from all syntheses
        key_insights = []
        for synthesis in source_syntheses:
            key_insights.extend(synthesis.key_insights)
        
        # Collect significant events from all syntheses
        significant_events = []
        for synthesis in source_syntheses:
            for event in synthesis.significant_events:
                # Check if this event is already included
                if not any(e['re_id'] == event.re_id for e in significant_events):
                    significant_events.append({
                        're_id': event.re_id,
                        'description': event.description,
                        'significance': event.significance
                    })
        
        # Generate a simple summary
        summary = f"Higher-level synthesis of {len(source_syntheses)} lower-level syntheses in domain {domain_type} from {start_date.isoformat()} to {end_date.isoformat()}"
        
        # TODO: Implement more sophisticated analysis to generate combined metrics, patterns, recommendations, etc.
        
        # Create the synthesis
        _, st_id = self.create_trajectory_synthesis(
            subject_id=subject_id,
            domain_type=domain_type,
            summary=summary,
            start_date=start_date,
            end_date=end_date,
            source_events=source_events,
            key_insights=key_insights,
            significant_events=significant_events,
            level=new_level
        )
        
        return st_id