class APIError(Exception):
    """Exception raised for errors in the API responses."""
    pass


class ConfigurationError(Exception):
    """Exception raised for errors in the configuration."""
    pass


class DownloadError(Exception):
    """Exception raised for errors during data download."""
    pass


class ValidationError(Exception):
    """Exception raised for invalid request parameters."""
    pass