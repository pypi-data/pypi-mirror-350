"""
Type definitions for the SQLite adapter.
"""

from typing import Any, Dict, List, Optional, Tuple, TypedDict, Union

# Type for a single row result
Row = Dict[str, Any]

# Type for query parameters
Parameters = Union[Tuple[Any, ...], Dict[str, Any], None]

# Type for query results
class Result(TypedDict):
    """Type for query results."""
    rows: List[Row]
    rowcount: int
    lastrowid: Optional[int] 