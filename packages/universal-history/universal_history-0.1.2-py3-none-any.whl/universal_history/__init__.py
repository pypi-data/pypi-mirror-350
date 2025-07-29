"""
Universal History library for creating, maintaining, and utilizing Universal Histories across multiple domains.
"""

__version__ = "0.1.0"

from .models.event_record import EventRecord, DomainType
from .models.trajectory_synthesis import TrajectorySynthesis
from .models.state_document import StateDocument
from .models.domain_catalog import DomainCatalog
from .models.universal_history import UniversalHistory

from .storage.repository import HistoryRepository
from .storage.memory_repository import MemoryHistoryRepository
try:
    from .storage.mongodb_repository import MongoDBHistoryRepository
except ImportError:
    # MongoDB dependencies not installed
    pass

from .services.event_service import EventService
from .services.synthesis_service import SynthesisService
from .services.state_service import StateService
from .services.history_service import HistoryService

from .config import Config, configure

# Client for easy access to all functionality
class UniversalHistoryClient:
    """
    Client for interacting with the Universal History system.
    
    This class provides a unified interface to all the services in the system.
    """
    
    def __init__(self, storage_dir: str = None, mongodb_connection: str = None):
        """
        Initialize the client with a storage configuration.
        
        Args:
            storage_dir (str, optional): Directory for file storage. If provided, 
                                       uses FileHistoryRepository.
            mongodb_connection (str, optional): MongoDB connection string. If provided,
                                             uses MongoDBHistoryRepository.
        """
        # Import here to avoid circular imports
        from .storage.repository import HistoryRepository
        from .storage.memory_repository import MemoryHistoryRepository
        
        # Determine which repository to use
        if mongodb_connection:
            try:
                from .storage.mongodb_repository import MongoDBHistoryRepository
                self.repository = MongoDBHistoryRepository(mongodb_connection)
            except ImportError:
                raise ImportError(
                    "MongoDB support requires additional dependencies. "
                    "Install them with 'pip install universal-history[mongodb]'"
                )
        elif storage_dir:
            from .config import Config
            config = Config()
            config.storage_type = "file"
            config.storage_dir = storage_dir
            
            try:
                from .storage.file_repository import FileHistoryRepository
                self.repository = FileHistoryRepository(storage_dir)
            except ImportError:
                # File repository not available, use memory repository with warning
                import warnings
                warnings.warn(
                    "File repository not available. Using memory repository instead. "
                    "Data will not persist between sessions."
                )
                self.repository = MemoryHistoryRepository()
        else:
            # Default to memory repository
            self.repository = MemoryHistoryRepository()
        
        # Initialize services
        self.event_service = EventService(self.repository)
        self.synthesis_service = SynthesisService(self.repository)
        self.state_service = StateService(self.repository)
        self.history_service = HistoryService(self.repository)
    
    # Delegate methods to appropriate services
    # Methods for EventService
    def create_event(self, **kwargs):
        """Create an event record. See EventService.create_event_record for details."""
        return self.event_service.create_event_record(**kwargs)
    
    def get_event(self, re_id, hu_id):
        """Get an event record by ID. See EventService.get_event_record for details."""
        return self.event_service.get_event_record(re_id, hu_id)
    
    def search_events(self, **kwargs):
        """Search for events. See EventService.search_events for details."""
        return self.event_service.search_events(**kwargs)
    
    # Methods for SynthesisService
    def create_synthesis(self, **kwargs):
        """Create a trajectory synthesis. See SynthesisService.create_trajectory_synthesis for details."""
        return self.synthesis_service.create_trajectory_synthesis(**kwargs)
    
    def get_synthesis(self, st_id, hu_id):
        """Get a synthesis by ID. See SynthesisService.get_trajectory_synthesis for details."""
        return self.synthesis_service.get_trajectory_synthesis(st_id, hu_id)
    
    def generate_synthesis_from_events(self, **kwargs):
        """Generate a synthesis from events. See SynthesisService.generate_synthesis_from_events for details."""
        return self.synthesis_service.generate_synthesis_from_events(**kwargs)
    
    # Methods for StateService
    def create_state_document(self, subject_id):
        """Create a state document. See StateService.create_state_document for details."""
        return self.state_service.create_state_document(subject_id)
    
    def update_domain_state(self, **kwargs):
        """Update a domain state. See StateService.update_domain_state for details."""
        return self.state_service.update_domain_state(**kwargs)
    
    def get_state_document(self, subject_id):
        """Get a state document. See StateService.get_state_document for details."""
        return self.state_service.get_state_document(subject_id)
    
    def update_state_from_events(self, **kwargs):
        """Update state from events. See StateService.update_state_from_events for details."""
        return self.state_service.update_state_from_events(**kwargs)
    
    def get_llm_context(self, subject_id, **kwargs):
        """Get LLM-optimized context. See StateService.get_llm_optimized_summary for details."""
        return self.state_service.get_llm_optimized_summary(subject_id, **kwargs)
    
    # Methods for HistoryService
    def create_history(self, subject_id):
        """Create a history. See HistoryService.create_history for details."""
        return self.history_service.create_history(subject_id)
    
    def get_history(self, hu_id):
        """Get a history by ID. See HistoryService.get_history for details."""
        return self.history_service.get_history(hu_id)
    
    def get_history_by_subject(self, subject_id):
        """Get a history by subject ID. See HistoryService.get_history_by_subject for details."""
        return self.history_service.get_history_by_subject(subject_id)
    
    def export_history(self, **kwargs):
        """Export a history. See HistoryService.export_history for details."""
        return self.history_service.export_history(**kwargs)
    
    def import_history(self, history_data):
        """Import a history. See HistoryService.import_history for details."""
        return self.history_service.import_history(history_data)
