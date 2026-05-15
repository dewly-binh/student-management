from typing import Annotated, Any

from pydantic.functional_validators import BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(str)]


def get_link_id(value: Any) -> Any:
    if value is None:
        return None

    if hasattr(value, "id"):
        return value.id

    ref = getattr(value, "ref", None)
    if ref is not None and hasattr(ref, "id"):
        return ref.id

    return value
