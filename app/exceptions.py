"""Custom exceptions for the EUFM Assistant system."""

class EUFMAssistantException(Exception):
    """Base exception for all application-specific errors."""
    def __init__(self, message: str, error_code: str = None, details: dict = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code or self.__class__.__name__
        self.details = details or {}

    def to_dict(self) -> dict:
        """Convert exception to dictionary for API responses."""
        return {
            'error': self.error_code,
            'message': self.message,
            'details': self.details
        }

class ValidationError(EUFMAssistantException):
    """Raised when input validation fails."""
    pass

class AIServiceError(EUFMAssistantException):
    """Raised when AI service interactions fail."""
    def __init__(self, message: str, service_name: str, details: dict = None):
        super().__init__(message, 'AI_SERVICE_ERROR', details)
        self.service_name = service_name

class AgentExecutionError(EUFMAssistantException):
    """Raised when agent execution fails."""
    def __init__(self, message: str, agent_type: str, agent_id: str, details: dict = None):
        super().__init__(message, 'AGENT_EXECUTION_ERROR', details)
        self.agent_type = agent_type
        self.agent_id = agent_id

class ConfigurationError(EUFMAssistantException):
    """Raised when configuration is invalid or missing."""
    pass


class ResourceNotFoundError(EUFMAssistantException):
    """Raised when an expected resource such as a file is missing."""
    pass
