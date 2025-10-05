"""Base schemas for common response formats."""

from typing import Any, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class BaseResponse(BaseModel, Generic[T]):
    """Base response schema with status and data."""
    
    status: str
    data: T | None = None
    message: str | None = None


class ErrorResponse(BaseModel):
    """Error response schema."""
    
    status: str = "error"
    error: dict[str, Any]


class XYPoint(BaseModel):
    """XY point for chart data."""
    
    x: str
    y: float


class ChartResponse(BaseResponse[list[XYPoint]]):
    """Chart response schema."""
    
    pass

