class AggBuilderError(Exception):
    """Base exception for AggBuilder related errors."""
    pass

class InvalidLookupError(AggBuilderError):
    """Raised when lookup parameters are invalid."""
    pass

class PipelineSerializationError(AggBuilderError):
    """Raised when there's an error serializing the pipeline to JSON."""
    pass

class InvalidStageError(AggBuilderError):
    """Raised when an invalid stage is added to the pipeline."""
    pass 