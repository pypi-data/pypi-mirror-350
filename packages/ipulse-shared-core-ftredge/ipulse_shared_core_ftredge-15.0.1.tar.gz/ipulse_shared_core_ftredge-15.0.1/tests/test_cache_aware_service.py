"""Tests for the CacheAwareFirestoreService."""

import unittest
import logging
from unittest.mock import MagicMock, patch, AsyncMock
from pydantic import BaseModel
from ipulse_shared_core_ftredge.cache.shared_cache import SharedCache
from ipulse_shared_core_ftredge.services import CacheAwareFirestoreService


# Configure logging for tests
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Create a simple model for testing
class TestModel(BaseModel):
    id: str
    name: str
    description: str


class TestCacheAwareFirestoreService(unittest.TestCase):
    """Test cases for CacheAwareFirestoreService."""

    def setUp(self):
        """Set up test fixtures."""
        # Create mock Firestore client
        self.db_mock = MagicMock()

        # Create mock caches
        self.document_cache = SharedCache[dict](
            name="TestDocCache",
            ttl=1.0,
            enabled=True,
            logger=logger
        )

        self.collection_cache = SharedCache[list](
            name="TestCollectionCache",
            ttl=1.0,
            enabled=True,
            logger=logger
        )

        # Create service instance with mocks
        self.service = CacheAwareFirestoreService[TestModel](
            db=self.db_mock,
            collection_name="test_collection",
            resource_type="test_resource",
            logger=logger,
            document_cache=self.document_cache,
            collection_cache=self.collection_cache,
            timeout=5.0
        )

    @patch('ipulse_shared_core_ftredge.services.BaseFirestoreService.get_document')
    async def test_get_document_cache_hit(self, mock_get_document):
        """Test get_document with cache hit."""
        # Prepare cached data
        test_data = {"id": "doc123", "name": "Test Doc", "description": "This is a test"}
        self.document_cache.set("doc123", test_data)

        # Execute get_document
        result = await self.service.get_document("doc123")

        # Verify result comes from cache
        self.assertEqual(result, test_data)

        # Verify Firestore was not called
        mock_get_document.assert_not_called()

    @patch('ipulse_shared_core_ftredge.services.BaseFirestoreService.get_document')
    async def test_get_document_cache_miss(self, mock_get_document):
        """Test get_document with cache miss."""
        # Configure mock to return data
        mock_data = {"id": "doc123", "name": "Test Doc", "description": "This is a test"}
        mock_get_document.return_value = mock_data

        # Execute get_document
        result = await self.service.get_document("doc123")

        # Verify Firestore was called
        mock_get_document.assert_called_once_with("doc123")

        # Verify result is correct
        self.assertEqual(result, mock_data)

        # Verify data was cached
        cached_data = self.document_cache.get("doc123")
        self.assertEqual(cached_data, mock_data)

    @patch('ipulse_shared_core_ftredge.services.BaseFirestoreService.get_all_documents')
    async def test_get_all_documents_cache_hit(self, mock_get_all):
        """Test get_all_documents with cache hit."""
        # Prepare cached data
        test_docs = [
            {"id": "doc1", "name": "Doc 1", "description": "First doc"},
            {"id": "doc2", "name": "Doc 2", "description": "Second doc"}
        ]
        self.collection_cache.set("test_cache_key", test_docs)

        # Execute get_all_documents
        result = await self.service.get_all_documents("test_cache_key")

        # Verify result comes from cache
        self.assertEqual(result, test_docs)

        # Verify Firestore was not called
        mock_get_all.assert_not_called()

    @patch('ipulse_shared_core_ftredge.services.BaseFirestoreService.get_all_documents')
    async def test_get_all_documents_cache_miss(self, mock_get_all):
        """Test get_all_documents with cache miss."""
        # Configure mock to return data
        mock_docs = [
            {"id": "doc1", "name": "Doc 1", "description": "First doc"},
            {"id": "doc2", "name": "Doc 2", "description": "Second doc"}
        ]
        mock_get_all.return_value = mock_docs

        # Execute get_all_documents
        result = await self.service.get_all_documents("test_cache_key")

        # Verify Firestore was called
        mock_get_all.assert_called_once()

        # Verify result is correct
        self.assertEqual(result, mock_docs)

        # Verify data was cached
        cached_docs = self.collection_cache.get("test_cache_key")
        self.assertEqual(cached_docs, mock_docs)

    @patch('ipulse_shared_core_ftredge.services.BaseFirestoreService.update_document')
    async def test_update_document_invalidates_cache(self, mock_update):
        """Test that update_document invalidates cache."""
        # Prepare cached data
        test_data = {"id": "doc123", "name": "Test Doc", "description": "This is a test"}
        self.document_cache.set("doc123", test_data)

        # Configure mock to return updated data
        updated_data = {"id": "doc123", "name": "Updated Doc", "description": "This was updated"}
        mock_update.return_value = updated_data

        # Execute update_document
        await self.service.update_document("doc123", {"name": "Updated Doc"}, "user123")

        # Verify cache was invalidated
        self.assertIsNone(self.document_cache.get("doc123"))

        # Verify collection cache was also invalidated
        if self.collection_cache.get("all_documents"):
            self.fail("Collection cache was not invalidated")

    @patch('ipulse_shared_core_ftredge.services.BaseFirestoreService.create_document')
    async def test_create_document_invalidates_cache(self, mock_create):
        """Test that create_document invalidates cache."""
        # Prepare collection cache data
        test_docs = [{"id": "doc1", "name": "Doc 1"}]
        self.collection_cache.set("all_documents", test_docs)

        # Configure mock to return created data
        new_data = {"id": "doc2", "name": "New Doc", "description": "Newly created"}
        mock_create.return_value = new_data

        # Create model instance
        new_model = TestModel(id="doc2", name="New Doc", description="Newly created")

        # Execute create_document
        await self.service.create_document("doc2", new_model, "user123")

        # Verify collection cache was invalidated
        self.assertIsNone(self.collection_cache.get("all_documents"))

    @patch('ipulse_shared_core_ftredge.services.BaseFirestoreService.delete_document')
    async def test_delete_document_invalidates_cache(self, mock_delete):
        """Test that delete_document invalidates cache."""
        # Prepare cached data
        test_data = {"id": "doc123", "name": "Test Doc", "description": "This is a test"}
        self.document_cache.set("doc123", test_data)

        test_docs = [test_data]
        self.collection_cache.set("all_documents", test_docs)

        # Execute delete_document
        await self.service.delete_document("doc123")

        # Verify document cache was invalidated
        self.assertIsNone(self.document_cache.get("doc123"))

        # Verify collection cache was also invalidated
        self.assertIsNone(self.collection_cache.get("all_documents"))

    def test_invalidate_document_cache(self):
        """Test _invalidate_document_cache method."""
        # Prepare cached data
        test_data = {"id": "doc123", "name": "Test Doc"}
        self.document_cache.set("doc123", test_data)

        # Execute invalidation
        self.service._invalidate_document_cache("doc123")

        # Verify cache was invalidated
        self.assertIsNone(self.document_cache.get("doc123"))

    def test_invalidate_collection_cache(self):
        """Test _invalidate_collection_cache method."""
        # Prepare cached data
        test_docs = [{"id": "doc1", "name": "Doc 1"}, {"id": "doc2", "name": "Doc 2"}]
        cache_key_to_invalidate = "all_documents"
        self.collection_cache.set(cache_key_to_invalidate, test_docs)

        # Execute invalidation
        self.service._invalidate_collection_cache(cache_key_to_invalidate)

        # Verify cache is empty for that key
        self.assertIsNone(self.collection_cache.get(cache_key_to_invalidate))

    def test_invalidate_collection_cache_custom_key(self):
        """Test _invalidate_collection_cache method with custom key."""
        # Prepare cached data
        test_docs = [{"id": "doc1", "name": "Doc 1"}, {"id": "doc2", "name": "Doc 2"}]
        self.collection_cache.set("custom_key", test_docs)

        # Execute invalidation
        self.service._invalidate_collection_cache("custom_key")

        # Verify cache was invalidated
        self.assertIsNone(self.collection_cache.get("custom_key"))


if __name__ == "__main__":
    unittest.main()
