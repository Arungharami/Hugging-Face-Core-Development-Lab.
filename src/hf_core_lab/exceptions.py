"""
Custom exceptions hierarchy for Hugging Face Core Development Lab.
"""


class HFCoreLabError(Exception):
    """Base exception for all errors in hf_core_lab."""

    pass


class HubConnectionError(HFCoreLabError):
    """Raised when communication with Hugging Face Hub API fails."""

    pass


class AuthenticationError(HFCoreLabError):
    """Raised when Hugging Face API token is invalid or missing."""

    pass


class ValidationError(HFCoreLabError):
    """Raised when model card, dataset card, or input metadata validation fails."""

    pass


class DiscoveryError(HFCoreLabError):
    """Raised when hub search or discovery operation fails."""

    pass


class InferenceError(HFCoreLabError):
    """Raised when model inference execution fails."""

    pass
