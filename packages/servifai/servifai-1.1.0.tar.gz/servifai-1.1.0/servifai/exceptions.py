"""Custom exceptions for ServifAI library"""

class ServifAIException(Exception):
    """Base exception for ServifAI library"""
    pass

class AuthenticationError(ServifAIException):
    """Raised when API key is invalid or expired"""
    pass

class SubscriptionError(ServifAIException):
    """Raised when subscription limits are exceeded or tier is invalid"""
    pass

class RateLimitError(ServifAIException):
    """Raised when API rate limits are exceeded"""
    pass

class ProcessingError(ServifAIException):
    """Raised when document processing fails"""
    pass

class APIError(ServifAIException):
    """Raised when API returns an error"""
    
    def __init__(self, message: str, status_code: int = None):
        super().__init__(message)
        self.status_code = status_code

class TimeoutError(ServifAIException):
    """Raised when API request times out"""
    pass
