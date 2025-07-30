"""
Data validation utilities inspired by FireStore.
"""
from typing import Any, Dict, List, Optional, Union
import datetime
import base64
from storekiss.exceptions import ValidationError
from storekiss.geopoint import GeoPoint
from storekiss.reference import Reference


class FieldValidator:
    """Base class for field validators."""

    def __init__(self, required: bool = True, indexed: bool = False):
        self.required = required
        self.indexed = indexed

    def validate(self, value: Any) -> Any:
        """Validate a value against this field's rules."""
        if value is None:
            if self.required:
                raise ValidationError("Field is required")
            return None
        return self._validate(value)

    def _validate(self, value: Any) -> Any:
        """Implement specific validation logic in subclasses."""
        return value

    def get_sqlite_type(self) -> str:
        """Get the SQLite type for this field."""
        return "TEXT"


class StringField(FieldValidator):
    """Validator for string fields."""

    def __init__(
        self,
        required: bool = True,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
        indexed: bool = False,
    ):
        super().__init__(required, indexed)
        self.min_length = min_length
        self.max_length = max_length

    def _validate(self, value: Any) -> str:
        if not isinstance(value, str):
            raise ValidationError(f"Expected string, got {type(value).__name__}")

        if self.min_length is not None and len(value) < self.min_length:
            raise ValidationError(
                f"String must be at least {self.min_length} characters"
            )

        if self.max_length is not None and len(value) > self.max_length:
            raise ValidationError(
                f"String must be at most {self.max_length} characters"
            )

        return value


class NumberField(FieldValidator):
    """Validator for numeric fields."""

    def __init__(
        self,
        required: bool = True,
        min_value: Optional[Union[int, float]] = None,
        max_value: Optional[Union[int, float]] = None,
        integer_only: bool = False,
        indexed: bool = False,
    ):
        super().__init__(required, indexed)
        self.min_value = min_value
        self.max_value = max_value
        self.integer_only = integer_only

    def get_sqlite_type(self) -> str:
        """Get the SQLite type for this field."""
        return "INTEGER" if self.integer_only else "REAL"

    def _validate(self, value: Any) -> Union[int, float]:
        if self.integer_only and not isinstance(value, int):
            raise ValidationError(f"Expected integer, got {type(value).__name__}")
        elif not isinstance(value, (int, float)):
            raise ValidationError(f"Expected number, got {type(value).__name__}")

        if self.min_value is not None and value < self.min_value:
            raise ValidationError(f"Number must be at least {self.min_value}")

        if self.max_value is not None and value > self.max_value:
            raise ValidationError(f"Number must be at most {self.max_value}")

        return value


class BooleanField(FieldValidator):
    """Validator for boolean fields."""
    # 親クラスのコンストラクタと同じ実装なので省略可能

    def get_sqlite_type(self) -> str:
        """Get the SQLite type for this field."""
        return "INTEGER"

    def _validate(self, value: Any) -> bool:
        if not isinstance(value, bool):
            raise ValidationError(f"Expected boolean, got {type(value).__name__}")
        return value


class DateTimeField(FieldValidator):
    """Validator for datetime fields."""
    # 親クラスのコンストラクタと同じ実装なので省略可能

    def get_sqlite_type(self) -> str:
        """Get the SQLite type for this field."""
        return "TEXT"

    def _validate(self, value: Any) -> datetime.datetime:
        if isinstance(value, str):
            try:
                return datetime.datetime.fromisoformat(value)
            except ValueError as exc:
                raise ValidationError("Invalid datetime format: %s" % value) from exc
        elif isinstance(value, datetime.datetime):
            return value
        else:
            raise ValidationError(
                "Expected datetime or ISO format string, got %s" % type(value).__name__
            )


class ListField(FieldValidator):
    """
    Validator for list fields.
    
    Supports:
    - Type checking for elements
    - Multi-dimensional arrays
    - Min/max length validation
    - Element validation using a validator
    """

    def __init__(
        self,
        item_validator: Optional[FieldValidator] = None,
        required: bool = True,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
        indexed: bool = False,
        element_type: Optional[type] = None,
    ):
        super().__init__(required, indexed)
        self.item_validator = item_validator
        self.min_length = min_length
        self.max_length = max_length
        self.element_type = element_type
        
        if self.item_validator is not None and self.element_type is not None:
            import logging
            logging.warning(
                "Both item_validator and element_type are specified. "
                "item_validator will take precedence."
            )

    def _validate(self, value: Any) -> List[Any]:
        if not isinstance(value, list):
            raise ValidationError(f"Expected list, got {type(value).__name__}")

        if self.min_length is not None and len(value) < self.min_length:
            raise ValidationError(f"List must have at least {self.min_length} items")

        if self.max_length is not None and len(value) > self.max_length:
            raise ValidationError(f"List must have at most {self.max_length} items")
        
        validated_items = []
        for i, item in enumerate(value):
            try:
                if self.item_validator is not None:
                    validated_items.append(self.item_validator.validate(item))
                elif self.element_type is not None:
                    if not isinstance(item, self.element_type):
                        raise ValidationError(
                            f"Item at index {i} expected to be {self.element_type.__name__}, "
                            f"got {type(item).__name__}"
                        )
                    validated_items.append(item)
                else:
                    validated_items.append(item)
            except Exception as e:
                raise ValidationError("Error at index %d: %s" % (i, str(e))) from e
                
        return validated_items


class MapField(FieldValidator):
    """
    Validator for map/dict fields.
    
    Supports:
    - Nested field validation
    - Dot notation for accessing nested fields
    - Schema validation with allow_extra_fields option
    - Partial updates for nested structures
    """

    def __init__(
        self,
        field_validators: Dict[str, FieldValidator],
        required: bool = True,
        allow_extra_fields: bool = False,
        indexed: bool = False,
    ):
        super().__init__(required, indexed)
        self.field_validators = field_validators
        self.allow_extra_fields = allow_extra_fields

    def _validate(self, value: Any) -> Dict[str, Any]:
        if not isinstance(value, dict):
            raise ValidationError(f"Expected dict, got {type(value).__name__}")

        result = {}

        for field_name, validator in self.field_validators.items():
            if "." in field_name:
                parts = field_name.split(".", 1)
                parent, child = parts[0], parts[1]
                
                if parent in value:
                    if not isinstance(value[parent], dict):
                        raise ValidationError(
                            f"Expected dict for nested field '{parent}', "
                            f"got {type(value[parent]).__name__}"
                        )
                    
                    nested_value = self._get_nested_value(value[parent], child)
                    if nested_value is not None:
                        if parent not in result:
                            result[parent] = {}
                        
                        self._set_nested_value(
                            result[parent], 
                            child, 
                            validator.validate(nested_value)
                        )
                    elif validator.required:
                        raise ValidationError(f"Required nested field '{field_name}' is missing")
                elif validator.required:
                    raise ValidationError(f"Required parent field '{parent}' for '{field_name}' is missing")
            else:
                if field_name in value:
                    result[field_name] = validator.validate(value[field_name])
                elif validator.required:
                    raise ValidationError(f"Required field '{field_name}' is missing")
                else:
                    result[field_name] = None

        # 追加フィールドの処理
        if self.allow_extra_fields:
            for field_name in value:
                if field_name not in result and field_name not in self.field_validators:
                    result[field_name] = value[field_name]
        else:
            # スキーマで定義されていないフィールドをチェック
            defined_fields = set()
            for field_name in self.field_validators:
                if "." in field_name:
                    defined_fields.add(field_name.split(".", 1)[0])
                else:
                    defined_fields.add(field_name)
                    
            extra_fields = set(value.keys()) - defined_fields
            if extra_fields:
                raise ValidationError(f"Unexpected fields: {', '.join(extra_fields)}")

        return result
    
    def _get_nested_value(self, data: Dict[str, Any], path: str) -> Any:
        """ドット表記のパスを使用してネストされた値を取得"""
        if "." in path:
            parts = path.split(".", 1)
            key, rest = parts[0], parts[1]
            
            if key in data and isinstance(data[key], dict):
                return self._get_nested_value(data[key], rest)
            return None
        else:
            return data.get(path)
    
    def _set_nested_value(self, data: Dict[str, Any], path: str, value: Any) -> None:
        """ドット表記のパスを使用してネストされた値を設定"""
        if "." in path:
            parts = path.split(".", 1)
            key, rest = parts[0], parts[1]
            
            if key not in data:
                data[key] = {}
            
            if not isinstance(data[key], dict):
                data[key] = {}
                
            self._set_nested_value(data[key], rest, value)
        else:
            data[path] = value


class BytesField(FieldValidator):
    """Validator for binary data fields."""
    # 親クラスのコンストラクタと同じ実装なので省略可能

    def get_sqlite_type(self) -> str:
        """Get the SQLite type for this field."""
        return "BLOB"

    def _validate(self, value: Any) -> bytes:
        if isinstance(value, str):
            try:
                return base64.b64decode(value)
            except Exception as exc:
                raise ValidationError("Invalid base64 encoded string: %s" % value) from exc
        elif isinstance(value, bytes):
            return value
        else:
            raise ValidationError("Expected bytes or base64 string, got %s" % type(value).__name__)


class GeoPointField(FieldValidator):
    """Validator for geographic point fields."""

    def __init__(
        self, 
        required: bool = True, 
        indexed: bool = False,
        geopoint_class_name: str = "GeoPoint"
    ):
        super().__init__(required, indexed)
        self.geopoint_class_name = geopoint_class_name

    def _validate(self, value: Any) -> GeoPoint:
        if isinstance(value, GeoPoint):
            return value
            
        if hasattr(value, "__class__") and value.__class__.__name__ == self.geopoint_class_name:
            try:
                iterator = iter(value)
                latitude = next(iterator)
                longitude = next(iterator)
                return GeoPoint(latitude, longitude)
            except (TypeError, StopIteration) as exc:
                raise ValidationError("GeoPoint must be iterable with latitude and longitude") from exc
                
        if isinstance(value, dict) and "latitude" in value and "longitude" in value:
            try:
                return GeoPoint(value["latitude"], value["longitude"])
            except (TypeError, ValueError) as e:
                raise ValidationError("Invalid GeoPoint dict: %s" % e) from e
                
        if isinstance(value, (list, tuple)) and len(value) == 2:
            try:
                return GeoPoint(value[0], value[1])
            except (TypeError, ValueError) as e:
                raise ValidationError("Invalid GeoPoint coordinates: %s" % e) from e
                
        raise ValidationError("Expected GeoPoint, got %s" % type(value).__name__)


class ReferenceField(FieldValidator):
    """Validator for document reference fields."""
    # 親クラスのコンストラクタと同じ実装なので省略可能

    def _validate(self, value: Any) -> Reference:
        if isinstance(value, Reference):
            return value
            
        if isinstance(value, str):
            parts = value.split('/')
            if len(parts) < 2:
                raise ValidationError(f"Invalid reference path: {value}")
                
            collection_path = '/'.join(parts[:-1])
            document_id = parts[-1]
            return Reference(collection_path, document_id)
            
        raise ValidationError(f"Expected Reference, got {type(value).__name__}")


class Schema:
    """Schema definition for document validation.

    Firestoreと同様に、デフォルトですべてのフィールドを許可します。
    スキーマで定義されたフィールドは型チェックされますが、
    定義されていないフィールドも自由に書き込むことができます。
    """

    def __init__(
        self,
        fields: Dict[str, FieldValidator],
        allow_extra_fields: bool = True,
        index_all_fields: bool = False,
    ):
        self.fields = fields
        self.allow_extra_fields = allow_extra_fields  # デフォルトでTrue（すべてのフィールドを許可）
        self.index_all_fields = index_all_fields

        if index_all_fields:
            for field in self.fields.values():
                field.indexed = True

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate data against this schema.

        スキーマで定義されたフィールドのみ検証し、
        定義されていないフィールドはそのまま通過させます。
        """
        if not isinstance(data, dict):
            raise ValidationError(f"Expected dict, got {type(data).__name__}")

        result = {}

        # スキーマで定義されたフィールドを検証
        dot_notation_fields = {}
        regular_fields = {}
        
        for field_name, validator in self.fields.items():
            if "." in field_name:
                dot_notation_fields[field_name] = validator
            else:
                regular_fields[field_name] = validator
        
        for field_name, validator in regular_fields.items():
            if field_name in data:
                result[field_name] = validator.validate(data[field_name])
            elif validator.required:
                raise ValidationError(f"Required field '{field_name}' is missing")
            else:
                result[field_name] = None
        
        for field_name, validator in dot_notation_fields.items():
            parts = field_name.split(".")
            parent = parts[0]
            child_path = ".".join(parts[1:])
            
            if parent in data:
                if not isinstance(data[parent], dict):
                    raise ValidationError(
                        f"Expected dict for nested field '{parent}', "
                        f"got {type(data[parent]).__name__}"
                    )
                
                nested_value = self._get_nested_value(data[parent], child_path)
                if nested_value is not None:
                    if parent not in result:
                        result[parent] = {}
                    
                    self._set_nested_value(
                        result[parent], 
                        child_path, 
                        validator.validate(nested_value)
                    )
                elif validator.required:
                    raise ValidationError(f"Required nested field '{field_name}' is missing")
            elif validator.required:
                raise ValidationError(f"Required parent field '{parent}' for '{field_name}' is missing")

        # 追加フィールドの処理
        # allow_extra_fieldsがFalseの場合でも、警告のみ出して通過させる
        if not self.allow_extra_fields:
            defined_fields = set(regular_fields.keys())
            for field_name in dot_notation_fields:
                defined_fields.add(field_name.split(".")[0])
                
            extra_fields = set(data.keys()) - defined_fields
            if extra_fields:
                import logging
                logging.warning(
                    "Unexpected fields in document: %s", 
                    ", ".join(extra_fields)
                )

        # すべてのフィールドをresultに追加
        for field_name in data:
            if field_name not in result and field_name not in self.fields:
                result[field_name] = data[field_name]

        return result
        
    def _get_nested_value(self, data: Dict[str, Any], path: str) -> Any:
        """ドット表記のパスを使用してネストされた値を取得"""
        if "." in path:
            parts = path.split(".", 1)
            key, rest = parts[0], parts[1]
            
            if key in data and isinstance(data[key], dict):
                return self._get_nested_value(data[key], rest)
            return None
        else:
            return data.get(path)
    
    def _set_nested_value(self, data: Dict[str, Any], path: str, value: Any) -> None:
        """ドット表記のパスを使用してネストされた値を設定"""
        if "." in path:
            parts = path.split(".", 1)
            key, rest = parts[0], parts[1]
            
            if key not in data:
                data[key] = {}
            
            if not isinstance(data[key], dict):
                data[key] = {}
                
            self._set_nested_value(data[key], rest, value)
        else:
            data[path] = value
