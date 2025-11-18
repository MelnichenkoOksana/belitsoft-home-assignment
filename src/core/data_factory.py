from faker import Faker
from dataclasses import dataclass, asdict
from typing import Dict, Any

_fake = Faker(locale="en_US")


@dataclass
class UserPayload:
    """
    Data model representing a synthetic user entity generated for API testing.

    Attributes:
        name: Full name of the user.
        email: Valid email address.
        city: Randomly generated city name.
    """
    name: str
    email: str
    city: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def generate_user_payload() -> UserPayload:
    """
    Generates a synthetic user payload with realistic random values.

    Returns:
        UserPayload: Object containing name, email and city.
    """
    return UserPayload(
        name=_fake.name(),
        email=_fake.email(),
        city=_fake.city(),
    )


def generate_query_param() -> Dict[str, str]:
    """
    Generates a random single key-value pair to be used as query parameters.

    Example:
        {"search": "apple"}

    Returns:
        Dict[str, str]: Random query parameter dictionary.
    """
    key = _fake.word()
    value = _fake.word()
    return {key: value}
