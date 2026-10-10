class TrustAIError(Exception):
    """Base exception for TrustAI-specific application errors."""


class DatasetValidationError(TrustAIError):
    """Raised when a dataset or row fails schema validation."""


class ProviderError(TrustAIError):
    """Raised when a model provider request fails."""


class MetricEvaluationError(TrustAIError):
    """Raised when a metric cannot be evaluated meaningfully."""
