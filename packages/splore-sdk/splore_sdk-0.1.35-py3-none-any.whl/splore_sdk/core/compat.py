"""Core compatibility utilities."""

from typing import Any, Dict, Type, TypeVar, cast

# Type variables for better typing support
T = TypeVar("T")


def model_dump_or_dict(model: Any) -> Dict[str, Any]:
    """
    Handle compatibility between Pydantic v1 and v2.

    - In Pydantic v1 (Python 3.7), use dict()
    - In Pydantic v2 (Python 3.8+), use model_dump()
    """
    if hasattr(model, "model_dump"):
        return model.model_dump()
    elif hasattr(model, "dict"):
        return model.dict()
    else:
        raise TypeError(f"Object {model} doesn't have dict() or model_dump() method")


def get_model_fields(model_class: Type[T]) -> Dict[str, Any]:
    """
    Get model fields in a compatible way between Pydantic v1 and v2.

    - In Pydantic v1 (Python 3.7), use __fields__
    - In Pydantic v2 (Python 3.8+), use model_fields
    """
    if hasattr(model_class, "model_fields"):
        return cast(Dict[str, Any], model_class.model_fields)
    elif hasattr(model_class, "__fields__"):
        return cast(Dict[str, Any], model_class.__fields__)
    else:
        raise TypeError(
            f"Model class {model_class} doesn't have __fields__ or model_fields attribute"
        )
