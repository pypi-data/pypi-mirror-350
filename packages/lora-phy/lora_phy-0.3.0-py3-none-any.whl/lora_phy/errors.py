class LoRaPHYError(Exception):
    """Base class for LoRaPHY exceptions."""


class NoPreambleError(LoRaPHYError):
    def __init__(self) -> None:
        super().__init__("No preamble detected")


class NoSyncError(LoRaPHYError):
    def __init__(self) -> None:
        super().__init__("No synchorization downchirp detected")


class InvalidCodingRateError(LoRaPHYError):
    def __init__(self) -> None:
        super().__init__("Invalid coding rate")


class InvalidInputError(ValueError, LoRaPHYError):
    """Exception for invalid input.

    This should only be used to validate hyperparameters, not user data.
    That is, any possible RF signal should not raise this exception.
    """

    def __init__(self, message: str) -> None:
        super().__init__(f"Invalid input: {message}")
