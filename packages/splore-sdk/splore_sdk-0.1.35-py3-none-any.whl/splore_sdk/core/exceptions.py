class SDKError(Exception):
    """Base exception for SDK."""


class ValidationError(SDKError):
    """Validation error."""


class APIError(SDKError):
    """API interaction error."""


class AgentIdError(SDKError):
    """agent_id mandotory error."""


class S3Error(SDKError):
    """S3 interaction error."""
