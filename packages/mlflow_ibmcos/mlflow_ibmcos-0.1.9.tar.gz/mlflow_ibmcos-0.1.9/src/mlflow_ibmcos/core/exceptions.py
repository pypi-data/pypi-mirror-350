MODEL_ALREADY_EXISTS = "Current model already exists on S3 registry, please push it with another version or use 'latest' tag"
COS_ARGUMENT_REQUIRED = (
    "Argument {} is required to establish connection to the S3 registry"
)
FINGERPRINT_RETRIEVAL_ERROR = "Error retrieving fingerprint from S3 registry, please check the model name and version: {}"
MLMODEL_FILE_NOT_FOUND = "MLmodel file not found in {}. Cannot move artifacts."


class ModelAlreadyExistsError(Exception):
    """Exception raised when a model already exists in the registry."""

    pass


class ArgumentRequired(Exception):
    """Exception raised when a required argument is missing."""

    pass


class FingerPrintNotFound(Exception):
    """Exception raised when a fingerprint is not found."""

    pass


class MLModelNotFoundError(Exception):
    """Exception raised when the MLmodel file is not found."""

    pass


class ArtifactNotFoundError(Exception):
    """Exception raised when an artifact is not found."""

    pass
