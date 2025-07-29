"""Utility enums module.

This module contains auxiliary enums enriched with quality of life functions.
"""

from enum import EnumMeta, IntEnum

__all__ = (
    'IntEnumMember',
    'MetaEnum',
)


class MetaEnum(EnumMeta):
    """Auxiliary enum meta class implementing __contains__ for the `in` operator."""

    def __contains__(cls, item):
        """Check if item is an enum member.

        Args:
            item: Item to check
        Returns:
            :obj`bool`: True if item is enum member, False otherwise
        """
        try:
            cls(item)
            return True
        except ValueError:
            return False


class IntEnumMember(IntEnum, metaclass=MetaEnum):
    """Integer enum base class with member value method."""
