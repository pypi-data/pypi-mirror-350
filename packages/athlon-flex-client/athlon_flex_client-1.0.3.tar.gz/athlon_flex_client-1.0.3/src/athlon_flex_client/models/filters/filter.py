"""The Filter Base class is extended by specific filters.

It provides some common functionality to convert the filter to request parameters.
"""

from __future__ import annotations

from pydantic import BaseModel


class Filter(BaseModel):
    """Base class for filters."""

    def to_request_params(self) -> dict:
        """Return the filter as request parameters, to be provied to api request."""
        return {
            f"Filters.{key}": self.bool_to_str(value)
            if isinstance(value, bool)
            else value
            for key, value in self.model_dump(exclude_none=True).items()
        }

    @staticmethod
    def bool_to_str(value: bool) -> str:  # noqa: FBT001
        """Convert a boolean value to a string, as understood by the API."""
        return "true" if value else "false"


class EmptyFilter(Filter):
    """Empty filter for loading all items."""
