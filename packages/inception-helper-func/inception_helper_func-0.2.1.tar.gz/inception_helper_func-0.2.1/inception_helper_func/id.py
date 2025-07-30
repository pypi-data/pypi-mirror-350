import re
import random
from typing import Callable, Any
from datetime import datetime


def generate_id(
    owner: str,
    place_owner_after_prefix: bool = False,
    created_by: str = "",
    include_creator: bool = False,
    prefix: str = "",
    random_digits: int = 4,
    cast_func: Callable[[int], Any] = str,
    separator: str = "",
    include_timestamp: bool = False,
) -> str:
    """
    Generate a unique identifier by combining various components.

    Args:
        owner: Required. The owner ID or name.
        place_owner_after_prefix: If True, places the owner ID right after prefix.
        created_by: Optional. ID or name of the creator.
        include_creator: If True, appends the created_by value.
        prefix: Optional prefix string.
        random_digits: Number of digits for the random number.
        cast_func: Function to convert the random number (default: str).
        separator: Separator between components.
        include_timestamp: If True, adds the current timestamp.

    Returns:
        str: The generated ID.
    """
    owner = str(owner).strip()

    if random_digits < 1:
        raise ValueError("random_digits must be greater than 0")

    if include_creator and not created_by:
        raise ValueError("created_by is required when include_creator is True")

    if created_by:
        created_by = str(created_by).strip()

    components = []

    if prefix:
        components.append(prefix)

    if place_owner_after_prefix:
        components.append(owner)

    # Generate random number
    rand_value = random.randrange(10 ** (random_digits - 1), 10**random_digits)
    components.append(cast_func(rand_value))

    # Include timestamp
    if include_timestamp:
        try:
            components.append(datetime.now().strftime("%Y%m%d%H%M%S"))
        except ValueError as e:
            raise ValueError(f"Invalid timestamp format: {e}")

    if not place_owner_after_prefix:
        components.append(owner)

    if include_creator and created_by:
        components.append(created_by)

    return separator.join(filter(None, components))


def slugify_name(name: str) -> str:
    return (
        "-".join(re.sub(r"[^a-zA-Z0-9\s]+", "", word.strip()) for word in name.split())
        .strip()
        .lower()
    )


if __name__ == "__main__":
    # Sample test cases
    test_cases = [
        {"owner": "1234567890", "prefix": "test_", "separator": "-"},
        {
            "owner": "1234567890",
            "created_by": "creator123",
            "include_creator": True,
            "prefix": "test_",
            "separator": "-",
        },
        {
            "owner": "1234567890",
            "prefix": "test_",
            "separator": "-",
            "include_timestamp": True,
        },
        {
            "owner": "1234567890",
            "prefix": "test_",
            "separator": "-",
            "include_timestamp": True,
            "timestamp_format": "%Y%m%d",
        },
    ]

    for case in test_cases:
        try:
            result = generate_id(**case)
            print(f"Test case {case}: {result}")
        except Exception as e:
            print(f"Test case {case} failed: {e}")
