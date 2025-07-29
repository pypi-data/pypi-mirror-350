"""
MongoDB repository implementation for storage of Universal History objects.
"""
from typing import Dict, List, Optional, Any, Union
import json
from datetime import datetime

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from ..models.event_record import EventRecord, DomainType
from ..models.trajectory_synthesis import TrajectorySynthesis
from ..models.state_document import StateDocument
from ..models.domain_catalog import DomainCatalog
from ..models.universal_history import UniversalHistory
from .repository import HistoryRepository

class MongoDBHistoryRepository(HistoryRepository):
    """
    MongoDB implementation of the HistoryRepository.
    
    This implementation stores data in a MongoDB database, which is suitable for
    production usage with persistence and scalability.
    """
    
    def __init__(self, connection_string: str, database_name: str = "universal_history"):
        """
        Initialize the repository with a MongoDB connection.
        
        Args:
            connection_string (str): MongoDB connection string
            database_name (str): Name of the database to use
        """
        self.client = MongoClient(connection_string)
        self.db: Database = self.client[database_name]
        
        # Collections
        self.histories: Collection = self.db.histories
        self.event_records: Collection = self.db.event_records
        self.trajectory_syntheses: Collection = self.db.trajectory_syntheses
        self.state_documents: Collection = self.db.state_documents
        self.domain_catalogs: Collection = self.db.domain_catalogs
        
        # Indexes
        self.histories.create_index("hu_id", unique=True)
        self.histories.create_index("subject_id", unique=True)
        self.event_records.create_index("re_id", unique=True)
        self.event_records.create_index(["hu_id", "domain_type"])
        self.trajectory_syntheses.create_index("st_id", unique=True)
        self.trajectory_syntheses.create_index(["hu_id", "domain_type"])
        self.state_documents.create_index("de_id", unique=True)
        self.state_documents.create_index("hu_id", unique=True)
        self.domain_catalogs.create_index(["hu_id", "domain_type"], unique=True)
    
    def _serialize_datetime(self, obj: Any) -> Any:
        """
        Recursively convert datetimes to ISO format strings in a dictionary.
        
        Args:
            obj (Any): The object to convert
            
        Returns:
            Any: The converted object
        """
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, dict):
            return {k: self._serialize_datetime(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._serialize_datetime(item) for item in obj]
        return obj
    
    def save_history(self, history: UniversalHistory) -> str:
        """
        Save a Universal History.
        
        Args:
            history (UniversalHistory): The history to save
            
        Returns:
            str: The ID of the saved history
        """
        # Convert the history to a dictionary
        history_dict = history.to_dict()
        
        # Remove nested objects that will be stored separately
        history_dict.pop('event_records', None)
        history_dict.pop('trajectory_syntheses', None)
        history_dict.pop('state_document', None)
        history_dict.pop('domain_catalogs', None)
        
        # Convert datetimes to strings
        history_dict = self._serialize_datetime(history_dict)
        
        # Save or update the history
        self.histories.update_one(
            {"hu_id": history.hu_id},
            {"$set": history_dict},
            upsert=True
        )
        
        # Save event records
        for re_id, event_record in history.event_records.items():
            self.save_event_record(event_record, history.hu_id)
        
        # Save trajectory syntheses
        for st_id, synthesis in history.trajectory_syntheses.items():
            self.save_trajectory_synthesis(synthesis, history.hu_id)
        
        # Save state document if it exists
        if history.state_document:
            self.save_state_document(history.state_document, history.hu_id)
        
        # Save domain catalogs
        for domain_type, catalog in history.domain_catalogs.items():
            self.save_domain_catalog(catalog, history.hu_id)
        
        return history.hu_id
    
    def get_history(self, hu_id: str) -> Optional[UniversalHistory]:
        """
        Get a Universal History by ID.
        
        Args:
            hu_id (str): The ID of the history to get
            
        Returns:
            Optional[UniversalHistory]: The history or None if not found
        """
        # Get the basic history
        history_dict = self.histories.find_one({"hu_id": hu_id})
        if not history_dict:
            return None
        
        # Create a new history
        history = UniversalHistory(subject_id=history_dict["subject_id"])
        
        # Set other basic attributes
        history.hu_id = history_dict["hu_id"]
        if "created_at" in history_dict:
            history.created_at = datetime.fromisoformat(history_dict["created_at"])
        if "last_updated" in history_dict:
            history.last_updated = datetime.fromisoformat(history_dict["last_updated"])
        
        # Get event records
        event_records = self.event_records.find({"hu_id": hu_id})
        for er_dict in event_records:
            # Remove MongoDB _id
            er_dict.pop("_id", None)
            er_dict.pop("hu_id", None)
            
            event_record = EventRecord.from_dict(er_dict)
            history.event_records[event_record.re_id] = event_record
        
        # Get trajectory syntheses
        syntheses = self.trajectory_syntheses.find({"hu_id": hu_id})
        for s_dict in syntheses:
            # Remove MongoDB _id
            s_dict.pop("_id", None)
            s_dict.pop("hu_id", None)
            
            synthesis = TrajectorySynthesis.from_dict(s_dict)
            history.trajectory_syntheses[synthesis.st_id] = synthesis
        
        # Get state document
        state_dict = self.state_documents.find_one({"hu_id": hu_id})
        if state_dict:
            # Remove MongoDB _id
            state_dict.pop("_id", None)
            state_dict.pop("hu_id", None)
            
            history.state_document = StateDocument.from_dict(state_dict)
        
        # Get domain catalogs
        catalogs = self.domain_catalogs.find({"hu_id": hu_id})
        for c_dict in catalogs:
            # Remove MongoDB _id
            c_dict.pop("_id", None)
            c_dict.pop("hu_id", None)
            
            catalog = DomainCatalog.from_dict(c_dict)
            domain_type = catalog.domain_type.value if isinstance(catalog.domain_type, DomainType) else catalog.domain_type
            history.domain_catalogs[domain_type] = catalog
        
        return history
    
    def get_history_by_subject(self, subject_id: str) -> Optional[UniversalHistory]:
        """
        Get a Universal History by subject ID.
        
        Args:
            subject_id (str): The subject ID to look for
            
        Returns:
            Optional[UniversalHistory]: The history or None if not found
        """
        history_dict = self.histories.find_one({"subject_id": subject_id})
        if not history_dict:
            return None
        
        return self.get_history(history_dict["hu_id"])
    
    def save_event_record(self, event_record: EventRecord, hu_id: str) -> str:
        """
        Save an Event Record to a Universal History.
        
        Args:
            event_record (EventRecord): The event record to save
            hu_id (str): The ID of the history to save to
            
        Returns:
            str: The ID of the saved event record
        """
        # Check if the history exists
        history_dict = self.histories.find_one({"hu_id": hu_id})
        if not history_dict:
            raise ValueError(f"Universal History with ID {hu_id} not found")
        
        # Check for previous event hash if not provided
        if not event_record.previous_re_hash:
            # Find the most recent event in the same domain
            domain_type = event_record.domain_type.value if isinstance(event_record.domain_type, DomainType) else event_record.domain_type
            latest_event = self.event_records.find_one(
                {"hu_id": hu_id, "domain_type": domain_type},
                sort=[("timestamp", -1)]
            )
            if latest_event:
                event_record.previous_re_hash = latest_event.get("current_re_hash")
        
        # Update the hash
        if not event_record.current_re_hash:
            event_record.update_hash()
        
        # Convert the event record to a dictionary
        er_dict = event_record.to_dict()
        
        # Add the history ID
        er_dict["hu_id"] = hu_id
        
        # Convert datetimes to strings
        er_dict = self._serialize_datetime(er_dict)
        
        # Save or update the event record
        self.event_records.update_one(
            {"re_id": event_record.re_id},
            {"$set": er_dict},
            upsert=True
        )
        
        # Update the last_updated timestamp of the history
        self.histories.update_one(
            {"hu_id": hu_id},
            {"$set": {"last_updated": datetime.now().isoformat()}}
        )
        
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
        er_dict = self.event_records.find_one({"re_id": re_id, "hu_id": hu_id})
        if not er_dict:
            return None
        
        # Remove MongoDB _id and hu_id
        er_dict.pop("_id", None)
        er_dict.pop("hu_id", None)
        
        return EventRecord.from_dict(er_dict)
    
    def save_trajectory_synthesis(self, synthesis: TrajectorySynthesis, hu_id: str) -> str:
        """
        Save a Trajectory Synthesis to a Universal History.
        
        Args:
            synthesis (TrajectorySynthesis): The synthesis to save
            hu_id (str): The ID of the history to save to
            
        Returns:
            str: The ID of the saved synthesis
        """
        # Check if the history exists
        history_dict = self.histories.find_one({"hu_id": hu_id})
        if not history_dict:
            raise ValueError(f"Universal History with ID {hu_id} not found")
        
        # Convert the synthesis to a dictionary
        s_dict = synthesis.to_dict()
        
        # Add the history ID
        s_dict["hu_id"] = hu_id
        
        # Convert datetimes to strings
        s_dict = self._serialize_datetime(s_dict)
        
        # Save or update the synthesis
        self.trajectory_syntheses.update_one(
            {"st_id": synthesis.st_id},
            {"$set": s_dict},
            upsert=True
        )
        
        # Update the last_updated timestamp of the history
        self.histories.update_one(
            {"hu_id": hu_id},
            {"$set": {"last_updated": datetime.now().isoformat()}}
        )
        
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
        s_dict = self.trajectory_syntheses.find_one({"st_id": st_id, "hu_id": hu_id})
        if not s_dict:
            return None
        
        # Remove MongoDB _id and hu_id
        s_dict.pop("_id", None)
        s_dict.pop("hu_id", None)
        
        return TrajectorySynthesis.from_dict(s_dict)
    
    def save_state_document(self, state_document: StateDocument, hu_id: str) -> str:
        """
        Save a State Document to a Universal History.
        
        Args:
            state_document (StateDocument): The state document to save
            hu_id (str): The ID of the history to save to
            
        Returns:
            str: The ID of the saved state document
        """
        # Check if the history exists
        history_dict = self.histories.find_one({"hu_id": hu_id})
        if not history_dict:
            raise ValueError(f"Universal History with ID {hu_id} not found")
        
        # Convert the state document to a dictionary
        sd_dict = state_document.to_dict()
        
        # Add the history ID
        sd_dict["hu_id"] = hu_id
        
        # Convert datetimes to strings
        sd_dict = self._serialize_datetime(sd_dict)
        
        # Save or update the state document
        self.state_documents.update_one(
            {"hu_id": hu_id},
            {"$set": sd_dict},
            upsert=True
        )
        
        # Update the last_updated timestamp of the history
        self.histories.update_one(
            {"hu_id": hu_id},
            {"$set": {"last_updated": datetime.now().isoformat()}}
        )
        
        return state_document.de_id
    
    def get_state_document(self, hu_id: str) -> Optional[StateDocument]:
        """
        Get the State Document from a Universal History.
        
        Args:
            hu_id (str): The ID of the history to get from
            
        Returns:
            Optional[StateDocument]: The state document or None if not found
        """
        sd_dict = self.state_documents.find_one({"hu_id": hu_id})
        if not sd_dict:
            return None
        
        # Remove MongoDB _id and hu_id
        sd_dict.pop("_id", None)
        sd_dict.pop("hu_id", None)
        
        return StateDocument.from_dict(sd_dict)
    
    def save_domain_catalog(self, domain_catalog: DomainCatalog, hu_id: str) -> str:
        """
        Save a Domain Catalog to a Universal History.
        
        Args:
            domain_catalog (DomainCatalog): The domain catalog to save
            hu_id (str): The ID of the history to save to
            
        Returns:
            str: The ID of the saved domain catalog
        """
        # Check if the history exists
        history_dict = self.histories.find_one({"hu_id": hu_id})
        if not history_dict:
            raise ValueError(f"Universal History with ID {hu_id} not found")
        
        # Convert the domain catalog to a dictionary
        dc_dict = domain_catalog.to_dict()
        
        # Add the history ID
        dc_dict["hu_id"] = hu_id
        
        # Get the domain type
        domain_type = domain_catalog.domain_type.value if isinstance(domain_catalog.domain_type, DomainType) else domain_catalog.domain_type
        
        # Convert datetimes to strings
        dc_dict = self._serialize_datetime(dc_dict)
        
        # Save or update the domain catalog
        self.domain_catalogs.update_one(
            {"hu_id": hu_id, "domain_type": domain_type},
            {"$set": dc_dict},
            upsert=True
        )
        
        # Update the last_updated timestamp of the history
        self.histories.update_one(
            {"hu_id": hu_id},
            {"$set": {"last_updated": datetime.now().isoformat()}}
        )
        
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
        domain_type_value = domain_type.value if isinstance(domain_type, DomainType) else domain_type
        
        dc_dict = self.domain_catalogs.find_one({"hu_id": hu_id, "domain_type": domain_type_value})
        if not dc_dict:
            return None
        
        # Remove MongoDB _id and hu_id
        dc_dict.pop("_id", None)
        dc_dict.pop("hu_id", None)
        
        return DomainCatalog.from_dict(dc_dict)
    
    def get_events_by_domain(self, domain_type: Union[str, DomainType], hu_id: str) -> List[EventRecord]:
        """
        Get all Event Records for a specific domain from a Universal History.
        
        Args:
            domain_type (Union[str, DomainType]): The domain type to filter by
            hu_id (str): The ID of the history to get from
            
        Returns:
            List[EventRecord]: List of Event Records for the specified domain
        """
        domain_type_value = domain_type.value if isinstance(domain_type, DomainType) else domain_type
        
        events = []
        for er_dict in self.event_records.find({"hu_id": hu_id, "domain_type": domain_type_value}):
            # Remove MongoDB _id and hu_id
            er_dict.pop("_id", None)
            er_dict.pop("hu_id", None)
            
            events.append(EventRecord.from_dict(er_dict))
        
        return events
    
    def get_syntheses_by_domain(self, domain_type: Union[str, DomainType], hu_id: str) -> List[TrajectorySynthesis]:
        """
        Get all Trajectory Syntheses for a specific domain from a Universal History.
        
        Args:
            domain_type (Union[str, DomainType]): The domain type to filter by
            hu_id (str): The ID of the history to get from
            
        Returns:
            List[TrajectorySynthesis]: List of Trajectory Syntheses for the specified domain
        """
        domain_type_value = domain_type.value if isinstance(domain_type, DomainType) else domain_type
        
        syntheses = []
        for s_dict in self.trajectory_syntheses.find({"hu_id": hu_id, "domain_type": domain_type_value}):
            # Remove MongoDB _id and hu_id
            s_dict.pop("_id", None)
            s_dict.pop("hu_id", None)
            
            syntheses.append(TrajectorySynthesis.from_dict(s_dict))
        
        return syntheses
    
    def close(self):
        """Close the MongoDB connection."""
        if self.client:
            self.client.close()