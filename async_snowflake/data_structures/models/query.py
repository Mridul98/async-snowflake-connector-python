from typing import Optional, List, Any, Iterator
from pydantic import BaseModel, ConfigDict, model_validator
from datetime import datetime


class QueryResult(BaseModel):
    """Result from a query execution."""

    model_config = ConfigDict(extra="allow")

    rows: Optional[List[List[Any]]] = None
    columns: Optional[List[str]] = None
    row_count: Optional[int] = None
    query_id: Optional[str] = None
    query_state: Optional[str] = None
    error_message: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def handle_aliases(cls, data):
        if isinstance(data, dict):
            if "data" in data and "rows" not in data:
                data["rows"] = data.pop("data")
            if "status" in data and "query_state" not in data:
                data["query_state"] = data.pop("status")
        return data

    @property
    def data(self) -> Optional[List[List[Any]]]:
        """Alias for rows for backwards compatibility."""
        return self.rows

    @data.setter
    def data(self, value: Optional[List[List[Any]]]):
        """Alias for rows for backwards compatibility."""
        self.rows = value

    @property
    def status(self) -> Optional[str]:
        """Alias for query_state for backwards compatibility."""
        return self.query_state

    @status.setter
    def status(self, value: Optional[str]):
        """Alias for query_state for backwards compatibility."""
        self.query_state = value

    def __iter__(self) -> Iterator[List[Any]]:
        """Iterate over rows."""
        if self.rows:
            return iter(self.rows)
        return iter([])

    def __len__(self) -> int:
        """Return the number of rows."""
        return self.row_count if self.row_count is not None else 0


class QueryStatus(BaseModel):
    """Status of a query."""

    model_config = ConfigDict(extra="allow")

    query_id: str
    state: str
    error_message: Optional[str] = None
    row_count: Optional[int] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None


class QueryHistoryEntry(BaseModel):
    """Entry in query history."""

    model_config = ConfigDict(extra="allow")

    query_id: str
    query_text: str
    status: str
    user_name: str
    database_name: Optional[str] = None
    schema_name: Optional[str] = None
    warehouse_name: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    total_elapsed_time: Optional[int] = None
