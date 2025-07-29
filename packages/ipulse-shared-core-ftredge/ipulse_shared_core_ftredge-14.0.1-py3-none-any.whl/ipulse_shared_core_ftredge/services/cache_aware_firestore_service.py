"""Cache-aware Firestore service base class."""
import time
from typing import TypeVar, Generic, Dict, Any, List, Optional
from google.cloud import firestore
from ipulse_shared_core_ftredge.services.base_firestore_service import BaseFirestoreService
from ipulse_shared_core_ftredge.services.base_service_exceptions import ResourceNotFoundError, ServiceError
from ipulse_shared_core_ftredge.cache.shared_cache import SharedCache
from ipulse_shared_core_ftredge import BaseDataModel

T = TypeVar('T', bound=BaseDataModel)

class CacheAwareFirestoreService(BaseFirestoreService[T], Generic[T]):
    """
    Base service class that adds caching capabilities to BaseFirestoreService.
    Supports both document-level and collection-level caching.
    """

    def __init__(
        self,
        db: firestore.Client,
        collection_name: str,
        resource_type: str,
        logger,
        document_cache: Optional[SharedCache] = None,
        collection_cache: Optional[SharedCache] = None,
        timeout: float = 30.0
    ):
        super().__init__(db, collection_name, resource_type, logger)
        self.document_cache = document_cache
        self.collection_cache = collection_cache
        self.timeout = timeout

        # Log cache configuration
        if self.document_cache:
            self.logger.info(f"Document cache enabled for {resource_type}: {self.document_cache.name}")
        if self.collection_cache:
            self.logger.info(f"Collection cache enabled for {resource_type}: {self.collection_cache.name}")

    async def get_document(self, doc_id: str) -> Dict[str, Any]:
        """
        Get a document with caching support.

        Args:
            doc_id: Document ID to fetch

        Returns:
            Document data as dictionary

        Raises:
            ResourceNotFoundError: If document doesn't exist
        """
        # Check cache first
        if self.document_cache:
            start_time = time.time()
            cached_doc = self.document_cache.get(doc_id)
            cache_check_time = (time.time() - start_time) * 1000

            if cached_doc is not None:
                self.logger.debug(f"Cache HIT for document {doc_id} in {cache_check_time:.2f}ms")
                return cached_doc
            else:
                self.logger.debug(f"Cache MISS for document {doc_id} - checking Firestore")

        # Fetch from Firestore
        start_time = time.time()
        doc_ref = self.db.collection(self.collection_name).document(doc_id)
        doc = doc_ref.get(timeout=self.timeout)
        firestore_time = (time.time() - start_time) * 1000

        if not doc.exists:
            self.logger.info(f"Document {doc_id} not found in Firestore after {firestore_time:.2f}ms")
            raise ResourceNotFoundError(self.resource_type, doc_id)

        doc_data = doc.to_dict()
        self.logger.debug(f"Fetched document {doc_id} from Firestore in {firestore_time:.2f}ms")

        # Cache the result
        if self.document_cache and doc_data:
            self.document_cache.set(doc_id, doc_data)
            self.logger.debug(f"Cached document {doc_id}")

        return doc_data

    async def get_all_documents(self, cache_key: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Retrieves all documents from the collection.
        Uses collection_cache if cache_key is provided and cache is available.
        Also populates document_cache for each retrieved document.
        """
        if cache_key and self.collection_cache:
            cached_collection_data = self.collection_cache.get(cache_key)
            if cached_collection_data is not None:
                self.logger.debug(f"Cache HIT for collection key '{cache_key}' in {self.collection_cache.name}")
                # Ensure individual documents are also in document_cache if possible
                if self.document_cache:
                    for doc_data in cached_collection_data:
                        if "id" in doc_data and not self.document_cache.get(doc_data["id"]):
                            self._cache_document_data(doc_data["id"], doc_data)
                return cached_collection_data
            else:
                self.logger.debug(f"Cache MISS for collection key '{cache_key}' in {self.collection_cache.name} - checking Firestore")

        self.logger.info(f"Fetching all documents for {self.resource_type} from Firestore.")
        start_time = time.time()

        try:
            docs_stream = self.db.collection(self.collection_name).stream(timeout=self.timeout)
            docs_data_list = []
            for doc in docs_stream:
                doc_data = doc.to_dict()
                if doc_data is not None:
                    doc_data["id"] = doc.id  # Ensure 'id' field is present
                    docs_data_list.append(doc_data)

            fetch_time = (time.time() - start_time) * 1000
            self.logger.debug(f"Fetched {len(docs_data_list)} documents for {self.resource_type} from Firestore in {fetch_time:.2f}ms")

            # Cache the entire collection if cache_key and collection_cache are available
            if cache_key and self.collection_cache:
                self.collection_cache.set(cache_key, docs_data_list)
                self.logger.debug(f"Cached collection with key '{cache_key}' in {self.collection_cache.name}")

            # Populate individual document cache
            if self.document_cache:
                self.logger.debug(f"Populating document cache ({self.document_cache.name}) with {len(docs_data_list)} items for {self.resource_type}.")
                for doc_data in docs_data_list:
                    # _cache_document_data expects 'id' to be in doc_data for keying
                    self._cache_document_data(doc_data["id"], doc_data)

            return docs_data_list

        except Exception as e:
            self.logger.error(f"Error fetching all documents for {self.resource_type}: {str(e)}", exc_info=True)
            raise ServiceError(operation=f"fetching all {self.resource_type}s", error=e, resource_type=self.resource_type) from e

    def _cache_document_data(self, doc_id: str, data: Dict[str, Any]):
        """Helper to cache document data if document_cache is available."""
        if self.document_cache:
            self.document_cache.set(doc_id, data)
            self.logger.debug(f"Cached item {doc_id} in {self.document_cache.name}")

    async def create_document(self, doc_id: str, data: T, creator_uid: str) -> Dict[str, Any]:
        """Create document and invalidate cache."""
        result = await super().create_document(doc_id, data, creator_uid)
        self._invalidate_document_cache(doc_id)
        return result

    async def update_document(self, doc_id: str, update_data: Dict[str, Any], updater_uid: str) -> Dict[str, Any]:
        """Update document and invalidate cache."""
        result = await super().update_document(doc_id, update_data, updater_uid)
        self._invalidate_document_cache(doc_id)
        return result

    async def delete_document(self, doc_id: str, deleter_uid: Optional[str] = None) -> None:
        """Delete document and invalidate cache."""
        await super().delete_document(doc_id)
        self._invalidate_document_cache(doc_id)

    def _invalidate_document_cache(self, doc_id: str) -> None:
        """Invalidate document cache for a specific document."""
        if self.document_cache:
            self.document_cache.invalidate(doc_id)
            self.logger.debug(f"Invalidated cache for document {doc_id}")

    def _invalidate_collection_cache(self, cache_key: str) -> None:
        """Invalidate collection cache for a specific cache key."""
        if self.collection_cache:
            self.collection_cache.invalidate(cache_key)
            self.logger.debug(f"Invalidated collection cache for key {cache_key}")
