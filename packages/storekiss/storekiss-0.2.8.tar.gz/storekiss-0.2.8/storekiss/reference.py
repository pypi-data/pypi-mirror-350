"""
Reference class for representing document references.
"""
from typing import Optional, Any


class Reference:
    """
    A class representing a reference to a document in a collection.
    """

    def __init__(self, collection_path: str, document_id: str):
        """
        Initialize a Reference with collection path and document ID.

        Args:
            collection_path: Path to the collection.
            document_id: ID of the document.
        """
        self._collection_path = collection_path
        self._document_id = document_id

    @property
    def collection_path(self) -> str:
        """Get the collection path."""
        return self._collection_path

    @property
    def document_id(self) -> str:
        """Get the document ID."""
        return self._document_id

    @property
    def path(self) -> str:
        """Get the full path to the document."""
        return f"{self._collection_path}/{self._document_id}"

    def __eq__(self, other) -> bool:
        """Check if two References are equal."""
        if not isinstance(other, Reference):
            return False
        return (
            self.collection_path == other.collection_path and
            self.document_id == other.document_id
        )

    def __repr__(self) -> str:
        """Return string representation of the Reference."""
        return f"Reference(collection_path='{self.collection_path}', document_id='{self.document_id}')"


def reference(collection_path: str, document_id: Optional[str] = None) -> Reference:
    """
    Create a reference to a document in a collection.
    
    Args:
        collection_path: Path to the collection.
        document_id: ID of the document. If None, the reference points to the collection.
        
    Returns:
        A Reference object.
    """
    if document_id is None:
        parts = collection_path.split('/')
        if len(parts) < 2:
            raise ValueError("Invalid path format. Expected 'collection/document'")
        collection_path = '/'.join(parts[:-1])
        document_id = parts[-1]
    
    return Reference(collection_path, document_id)


def is_reference(obj: Any) -> bool:
    """
    Check if an object is a Reference.
    
    Args:
        obj: The object to check.
        
    Returns:
        True if the object is a Reference, False otherwise.
    """
    return isinstance(obj, Reference)
