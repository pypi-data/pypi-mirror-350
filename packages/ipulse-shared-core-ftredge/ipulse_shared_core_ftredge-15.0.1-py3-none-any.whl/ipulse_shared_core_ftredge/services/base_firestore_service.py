""" Base class for Firestore services with common CRUD operations """
from typing import Dict, Any, List, TypeVar, Generic, Optional
import logging
import time
from datetime import datetime, timezone
from pydantic import BaseModel
from google.cloud import firestore
from .base_service_exceptions import ResourceNotFoundError, ValidationError, ServiceError

T = TypeVar('T', bound=BaseModel)

class BaseFirestoreService(Generic[T]):
    """Base class for Firestore services with common CRUD operations"""

    def __init__(
        self,
        db: firestore.Client,
        collection_name: str,
        resource_type: str,
        logger: logging.Logger,
        timeout: float = 15.0  # Default to 15 seconds, but allow override
    ):
        self.db = db
        self.collection_name = collection_name
        self.resource_type = resource_type
        self.logger = logger
        self.timeout = timeout  # Store the timeout as an instance attribute
        self.logger.info(f"Initialized {self.resource_type} service with timeout={timeout}s")

    async def create_document(self, doc_id: str, data: T, creator_uid: str) -> Dict[str, Any]:
        """Standard create method with audit fields"""
        try:
            current_time = datetime.now(timezone.utc)
            doc_data = data.model_dump(mode='json')

            # Add audit fields
            doc_data.update({
                'created_at': current_time.isoformat(),
                'created_by': creator_uid,
                'updated_at': current_time.isoformat(),
                'updated_by': creator_uid
            })

            doc_ref = self.db.collection(self.collection_name).document(doc_id)
            # Apply timeout to the set operation
            doc_ref.set(doc_data, timeout=self.timeout)

            self.logger.info(f"Created {self.resource_type}: {doc_id}")
            return doc_data

        except Exception as e:
            self.logger.error(f"Error creating {self.resource_type}: {e}", exc_info=True)
            raise ServiceError(
                operation=f"creating {self.resource_type}",
                error=e,
                resource_type=self.resource_type,
                resource_id=doc_id
            ) from e

    async def create_batch_documents(self, documents: List[T], creator_uid: str) -> List[Dict[str, Any]]:
        """Standard batch create method"""
        try:
            batch = self.db.batch()
            current_time = datetime.now(timezone.utc)
            created_docs = []

            for doc in documents:
                doc_data = doc.model_dump(mode='json')
                doc_data.update({
                    'created_at': current_time.isoformat(),
                    'created_by': creator_uid,
                    'updated_at': current_time.isoformat(),
                    'updated_by': creator_uid
                })

                doc_ref = self.db.collection(self.collection_name).document(doc_data.get('id'))
                batch.set(doc_ref, doc_data)
                created_docs.append(doc_data)

            # Apply timeout to the commit operation
            batch.commit(timeout=self.timeout)
            self.logger.info(f"Created {len(documents)} {self.resource_type}s in batch")
            return created_docs

        except Exception as e:
            self.logger.error(f"Error batch creating {self.resource_type}s: {e}", exc_info=True)
            raise ServiceError(
                operation=f"batch creating {self.resource_type}s",
                error=e,
                resource_type=self.resource_type,
                resource_id=doc_data.get('id')
            ) from e

    async def get_document(self, doc_id: str) -> Dict[str, Any]:
        """Get a document by ID with standardized error handling"""
        self.logger.debug(f"Getting {self.resource_type} document: {doc_id} with timeout={self.timeout}s")
        start_time = time.time()

        try:
            doc_ref = self.db.collection(self.collection_name).document(doc_id)

            # Apply timeout to the get operation
            doc = doc_ref.get(timeout=self.timeout)

            elapsed = (time.time() - start_time) * 1000
            self.logger.debug(f"Firestore get for {doc_id} completed in {elapsed:.2f}ms")

            if not doc.exists:
                self.logger.warning(f"Document {doc_id} not found in {self.collection_name}")
                raise ResourceNotFoundError(
                    resource_type=self.resource_type,
                    resource_id=doc_id,
                    additional_info={"collection": self.collection_name}
                )

            return doc.to_dict()

        except ResourceNotFoundError:
            raise
        except Exception as e:
            elapsed = (time.time() - start_time) * 1000
            self.logger.error(f"Error getting document {doc_id} after {elapsed:.2f}ms: {str(e)}", exc_info=True)
            raise ServiceError(
                operation=f"retrieving {self.resource_type}",
                error=e,
                resource_type=self.resource_type,
                resource_id=doc_id,
                additional_info={"collection": self.collection_name, "timeout": self.timeout}
            ) from e

    async def update_document(self, doc_id: str, update_data: Dict[str, Any], updater_uid: str) -> Dict[str, Any]:
        """Standard update method with validation and audit fields"""
        try:
            doc_ref = self.db.collection(self.collection_name).document(doc_id)

            # Apply timeout to the get operation
            if not doc_ref.get(timeout=self.timeout).exists:
                raise ResourceNotFoundError(
                    resource_type=self.resource_type,
                    resource_id=doc_id,
                    additional_info={"collection": self.collection_name}
                )

            valid_fields = self._validate_update_fields(update_data)

            # Add audit fields
            valid_fields.update({
                'updated_at': datetime.now(timezone.utc).isoformat(),
                'updated_by': updater_uid
            })

            # Apply timeout to the update operation
            doc_ref.update(valid_fields, timeout=self.timeout)
            # Apply timeout to the get operation
            return doc_ref.get(timeout=self.timeout).to_dict()

        except (ResourceNotFoundError, ValidationError):
            raise
        except Exception as e:
            self.logger.error(f"Error updating {self.resource_type}: {e}", exc_info=True)
            raise ServiceError(
                operation=f"updating {self.resource_type}",
                error=e,
                resource_type=self.resource_type,
                resource_id=doc_id
            ) from e

    async def delete_document(self, doc_id: str) -> None:
        """Standard delete method"""
        try:
            doc_ref = self.db.collection(self.collection_name).document(doc_id)
            # Apply timeout to the get operation
            if not doc_ref.get(timeout=self.timeout).exists:
                raise ResourceNotFoundError(
                    resource_type=self.resource_type,
                    resource_id=doc_id
                )

            # Apply timeout to the delete operation
            doc_ref.delete(timeout=self.timeout)
            self.logger.info(f"Deleted {self.resource_type}: {doc_id}")

        except ResourceNotFoundError:
            raise
        except Exception as e:
            self.logger.error(f"Error deleting {self.resource_type}: {e}", exc_info=True)
            raise ServiceError(
                operation=f"deleting {self.resource_type}",
                error=e,
                resource_type=self.resource_type,
                resource_id=doc_id
            ) from e

    # Add query method with timeout
    async def query_documents(
        self,
        filters: Optional[List[tuple]] = None,
        limit: Optional[int] = None,
        order_by: Optional[tuple] = None
    ) -> List[Dict[str, Any]]:
        """Query documents with filters, limit, and ordering"""
        try:
            # Start with the collection reference
            query = self.db.collection(self.collection_name)

            # Apply filters if provided
            if filters:
                for field, op, value in filters:
                    query = query.where(field=field, op_string=op, value=value)

            # Apply ordering if provided
            if order_by:
                field, direction = order_by
                query = query.order_by(field, direction=direction)

            # Apply limit if provided
            if limit:
                query = query.limit(limit)

            # Execute query with timeout
            docs = query.stream(timeout=self.timeout)
            return [doc.to_dict() for doc in docs]

        except Exception as e:
            self.logger.error(f"Error querying {self.resource_type}: {e}", exc_info=True)
            raise ServiceError(
                operation=f"querying {self.resource_type}",
                error=e,
                resource_type=self.resource_type
            ) from e

    def _validate_update_fields(self, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Centralized update fields validation"""
        if not isinstance(update_data, dict):
            update_data = update_data.model_dump(exclude_unset=True)

        valid_fields = {
            k: v for k, v in update_data.items()
            if v is not None and not (isinstance(v, (list, dict, set)) and len(v) == 0)
        }

        if not valid_fields:
            raise ValidationError(
                resource_type=self.resource_type,
                detail="No valid fields to update",
                resource_id=None
            )

        return valid_fields
