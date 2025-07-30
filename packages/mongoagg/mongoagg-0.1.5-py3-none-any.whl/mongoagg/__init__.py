"""
MongoDB Aggregation Pipeline Builder
"""

__version__ = "0.1.5"

from .core import AggBuilder
from .exceptions import AggBuilderError, InvalidLookupError, PipelineSerializationError, InvalidStageError
from .models import Expr, Pipeline, ConditionBuilder

__all__ = [
    "AggBuilder",
    "AggBuilderError",
    "InvalidLookupError",
    "PipelineSerializationError",
    "InvalidStageError",
    "Expr",
    "Pipeline",
    "ConditionBuilder",
]