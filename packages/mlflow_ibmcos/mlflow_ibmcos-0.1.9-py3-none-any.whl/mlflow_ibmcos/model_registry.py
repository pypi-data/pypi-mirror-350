from contextlib import nullcontext
import os
from pathlib import Path
import shutil
from typing import Dict, Optional, Union
from warnings import warn
from mlflow.store.artifact.s3_artifact_repo import S3ArtifactRepository
import ibm_boto3
from ibm_botocore.config import Config
from dirhash import dirhash
from functools import lru_cache
from mlflow.utils.file_utils import TempDir
from pydantic import validate_call
from mlflow_ibmcos.core.decorators import move_artifacts_hook
from mlflow_ibmcos.core.exceptions import (
    COS_ARGUMENT_REQUIRED,
    FINGERPRINT_RETRIEVAL_ERROR,
    MODEL_ALREADY_EXISTS,
    ArgumentRequired,
    FingerPrintNotFound,
    ModelAlreadyExistsError,
)
import mlflow
from mlflow_ibmcos.logger import Logger
from mlflow_ibmcos.schemas import ModelPath, NonEmptyDict
from mlflow_ibmcos.utils import Color, print_colored_message

logger = Logger(module=__name__)


class COSModelRegistry(S3ArtifactRepository):
    """
    IBM Cloud Object Storage (COS) based model registry implementation.
    This class provides functionality to store and manage machine learning models
    in IBM Cloud Object Storage, implementing a versioned model registry pattern.
    It extends the S3ArtifactRepository to provide specific model registry capabilities
    including version management, fingerprinting, and proper artifact organization.

    Class Attributes
    ----------------
    - `PREFIX` (str): The base prefix for all models stored in the registry
    - `FINGERPRINT_NAME` (str): The name of the file used to store the model's hash fingerprint
    - `FINGERPRINT_IGNORE` (tuple): Files to be ignored when calculating the model fingerprint
    - `FINGERPRINT_ALGORITHM` (str): The algorithm used for calculating directory hashes

    Instance Arguments
    ------------------
    `model_name` (str):
        The name of the model to be registered
    `model_version` (str):
        The version identifier for the model. It can be a tagged version or 'latest'.
    `prefix` (Optional[str]):
        The prefix within the bucket where models will be stored. Defaults to `traductor/registry`.
    `**kwargs`:
        Additional keyword arguments for S3 client configuration:
            - `bucket` (str): The name of the IBM COS bucket to use for storage.
            - `endpoint_url` (str): IBM COS service endpoint URL
            - `aws_access_key_id` (str): Access key for IBM COS authentication
            - `aws_secret_access_key` (str): Secret key for IBM COS authentication
            - `config`: A dict with additional configuration for the S3 client (e.g., proxy settings)

    Environment Variables
    ---------------------
    - `COS_BUCKET_NAME`: Can be used instead of the `bucket` kwarg.
    - `AWS_ENDPOINT_URL`: Can be used instead of the `endpoint_url` kwarg.
    - `AWS_ACCESS_KEY_ID`: Can be used instead of the `aws_access_key_id` kwarg.
    - `AWS_SECRET_ACCESS_KEY`: Can be used instead of the `aws_secret_access_key` kwarg.

    Raises
    ------
    - `ArgumentRequired`: If any required authentication or configuration parameters are missing
    - `ModelAlreadyExistsError`: When attempting to overwrite an existing model version

    Example
    -------
        >>> registry = COSModelRegistry(
        ...     model_name="text-classifier",
        ...     model_version="1.0.0",
        ...     bucket="models-bucket",
        ...     endpoint_url="https://s3.us-south.cloud-object-storage.appdomain.cloud"
        ... )
        >>> registry.log_artifacts("model-dir")
    """

    PREFIX = "traductor/registry"
    FINGERPRINT_NAME = "fingerprint"
    FINGERPRINT_IGNORE = ("MLmodel",)
    FINGERPRINT_ALGORITHM = "sha512"

    @validate_call
    def __init__(
        self,
        model_name: str,
        model_version: str,
        prefix: Optional[str] = None,
        **kwargs,
    ):
        self._model_name = model_name
        self._model_version = model_version
        self._bucket = (
            kwargs.get("bucket")
            or os.environ.get("COS_BUCKET_NAME")
            or self._raise_missing_argument_error("bucket")
        )
        self._key = f"{prefix if prefix else self.PREFIX}/{model_name}/{model_version}"
        self._endpoint_url = (
            kwargs.get("endpoint_url")
            or os.environ.get("AWS_ENDPOINT_URL")
            or self._raise_missing_argument_error("endpoint_url")
        )
        self._aws_access_key_id = (
            kwargs.get("aws_access_key_id")
            or os.environ.get("AWS_ACCESS_KEY_ID")
            or self._raise_missing_argument_error("aws_access_key_id")
        )
        self._aws_secret_access_key = (
            kwargs.get("aws_secret_access_key")
            or os.environ.get("AWS_SECRET_ACCESS_KEY")
            or self._raise_missing_argument_error("aws_secret_access_key")
        )
        self._config = (
            Config(**kwargs.get("config"))
            if kwargs.get("config") and isinstance(kwargs.get("config"), dict)
            else None
        )
        super().__init__(artifact_uri=f"s3://{self._bucket}/{self._key}")

    @lru_cache(maxsize=64)
    def _get_s3_client(self):
        """
        Creates and returns an IBM Cloud Object Storage S3 client.

        Uses the instance's configuration parameters (endpoint_url,
        aws_access_key_id, aws_secret_access_key, and config) to
        establish the connection.

        Returns:
            ibm_boto3.client: An authenticated S3 client for IBM Cloud Object Storage.
            This object is cached for performance optimization.
        """

        return ibm_boto3.client(
            "s3",
            endpoint_url=self._endpoint_url,
            aws_access_key_id=self._aws_access_key_id,
            aws_secret_access_key=self._aws_secret_access_key,
            config=self._config,
        )

    @validate_call
    def log_pyfunc_model_as_code(
        self,
        model_code_path: ModelPath,
        artifacts: Optional[Dict[str, ModelPath]] = None,
        local_path_storage: Optional[Union[str, Path]] = None,
        **kwargs,
    ):
        """
        Log a MLFlow's Python model to the model registry as code.

        This method saves a PyFunc model using MLflow and then logs the model artifacts to storage.

        Args:
            model_code_path (str | Path): Path to the Python model code. It must exist.
            artifacts (Optional[Dict]): Dictionary of artifacts to be saved with the model.
                Each artifact is logged as a separate file within the model directory.
            **kwargs: Additional keyword arguments passed to mlflow.pyfunc.save_model().

        Note:
            The model is temporarily saved to disk before being logged to the configured
            artifact storage system.
        """
        context = nullcontext() if local_path_storage is not None else TempDir()
        artifact_path_arg = "placeholder" if local_path_storage is not None else None
        with context as tmp:
            local_path = (
                os.path.join(local_path_storage, self._model_name)
                if local_path_storage is not None
                else tmp.path("model")  # type: ignore
            )
            mlflow.pyfunc.save_model(
                path=local_path,
                python_model=model_code_path,
                artifacts=artifacts,
                **kwargs,
            )

            self.log_artifacts(local_dir=local_path, artifact_path=artifact_path_arg)

    @validate_call(validate_return=True)
    def _get_remote_fingerprint(self) -> str:
        """
        Retrieves the fingerprint of the model from remote storage.

        Returns:
            str: The decoded fingerprint string.

        Raises:
            FingerPrintNotFound: If the fingerprint couldn't be retrieved from remote storage.
        """
        try:
            return (
                self._get_s3_client()
                .get_object(
                    Bucket=self._bucket, Key=f"{self._key}/{self.FINGERPRINT_NAME}"
                )["Body"]
                .read()
                .decode()
            )
        except ibm_boto3.exceptions.Boto3Error as e:
            raise FingerPrintNotFound(FINGERPRINT_RETRIEVAL_ERROR.format(str(e)))

    @staticmethod
    @validate_call
    def _get_local_fingerprint(fingerprint_path: str) -> str:
        """
        Retrieves the fingerprint from a local file.

        Args:
            fingerprint_path (str): Path to the fingerprint file.

        Returns:
            str: The contents of the fingerprint file.
        """
        with open(fingerprint_path, "r") as f:
            return f.read()

    @validate_call(config={"arbitrary_types_allowed": True}, validate_return=True)
    def load_remote_model(
        self,
        dst_path: Optional[Union[str, Path]] = None,
        delete_other_versions: bool = False,
    ) -> mlflow.pyfunc.PyFuncModel:
        """
        Load the model from remote storage to a local directory.

        This method downloads the model artifacts from the configured IBM COS bucket
        to a local directory. It uses fingerprint-based caching to avoid redundant downloads.
        Then, it loads the model using MLflow's load_model() method.

        Args:
            dst_path (Optional[str | Path]): Destination directory where artifacts should be
                downloaded. Defaults to current working directory if None.
            delete_other_versions (bool): If True, deletes any existing model directory
                with the same name before downloading. Defaults to False.

        Returns:
            str: Path to the directory containing the downloaded model artifacts.
        """
        path = self.download_artifacts(
            dst_path=dst_path, delete_other_versions=delete_other_versions
        )
        # Load the model using MLflow
        model = self.load_model(model_local_path=path)
        return model

    @move_artifacts_hook
    def download_artifacts(
        self,
        artifact_path: Optional[str] = None,
        dst_path: Optional[Union[str, Path]] = None,
        delete_other_versions: bool = False,
        move_artifacts: Optional[NonEmptyDict] = None,
    ) -> str:
        """
        Download model artifacts from remote storage to a local directory.
        This method downloads model artifacts to a directory structure of
        {dst_path}/{model_name}/{model_version}/. It implements fingerprint-based
        caching to avoid redundant downloads - if the local fingerprint matches
        the remote one, it skips the download. For models tagged as 'latest',
        it automatically updates the artifacts if the fingerprint changes.
        Args:
            artifact_path (Optional[str]): Just a placeholder for compatibility.
                This argument is not used in this implementation.
            dst_path (Optional[str | Path]): Destination directory where artifacts should be
                downloaded. Defaults to current working directory if None.
            delete_other_versions (bool): If True, deletes any existing model directory
                with the same name before downloading. Defaults to False.
            move_artifacts (Optional[NonEmptyDict]): Dictionary of artifacts to be moved
                to a final location after download.
        Returns:
            str: Path to the directory containing the downloaded model artifacts.
        Raises:
            FingerPrintNotFound: If the fingerprint couldn't be retrieved from remote storage.
        Notes:
            - If artifacts are already present with matching fingerprint, download is skipped.
            - For version-tagged models (not 'latest'), a warning is shown if remote
              fingerprint differs from local.
            - For 'latest' models, artifacts are automatically redownloaded if remote
              fingerprint differs from local.
        """
        # TODO use E-Tag instead of fingerprint, so that the flow becomes more robust
        if isinstance(dst_path, Path):
            dst_path = str(dst_path)
        # if no destination path is provided, set to .models/ folder in current working directory
        if not dst_path:
            dst_path = os.path.join(os.getcwd(), ".models")
        # Create the destination directory if it doesn't exist
        os.makedirs(dst_path, exist_ok=True)

        # Create folders for model name and version under dst_path
        # The final structure will be {dst_path}/{model_name}/{model_version}/
        model_dir = os.path.join(dst_path, self._model_name, self._model_version)
        os.makedirs(model_dir, exist_ok=True)

        # If `fingerprint` file doesn't exist in the model directory, then download the artifacts
        # from the remote storage and returns
        fingerprint_path = os.path.join(model_dir, self.FINGERPRINT_NAME)
        if not os.path.exists(fingerprint_path):
            logger.info(
                f"Fingerprint file not found. Downloading artifacts to {model_dir}"
            )
            if delete_other_versions is True:
                # Delete any existing model version with the same name
                self._delete_old_model_versions(model_dir)
            return super().download_artifacts(artifact_path="", dst_path=model_dir)

        # Read the fingerprint from the local file
        local_fingerprint = self._get_local_fingerprint(fingerprint_path)

        # Read the fingerprint from the remote file

        remote_fingerprint = self._get_remote_fingerprint()

        # If fingerprints match, return without downloading
        if local_fingerprint == remote_fingerprint:
            msg = f"Fingerprint matches. Artifacts already stored in {model_dir}"
            logger.info(msg)
            print_colored_message(color=Color.YELLOW, message=msg)
            return os.path.abspath(model_dir)

        # If fingerprints don't match, download the artifacts only if model version is 'latest'
        if self._model_version != "latest":
            msg = "Your version tagged model has changed. You should review it."
            logger.warning(msg)
            warn(msg)
            return os.path.abspath(model_dir)

        # ==== For 'latest' version ====
        # Remove the existing model directory (model_name + version)
        shutil.rmtree(model_dir, ignore_errors=True)
        # Recreate the model directory (model_name + version)
        os.makedirs(model_dir, exist_ok=True)
        if delete_other_versions is True:
            # Delete any existing model version with the same name
            self._delete_old_model_versions(model_dir)

        return super().download_artifacts(artifact_path="", dst_path=model_dir)

    @staticmethod
    @validate_call
    def _delete_old_model_versions(model_dir: str) -> None:
        """
        Deletes old model versions by removing the parent directory and recreating the model directory.

        This method completely removes the parent directory of the specified model directory,
        effectively deleting all content within it, and then recreates the model directory itself.

        Args:
            model_dir (str): Path to the model directory to be preserved.

        Returns:
            None: This function does not return anything.

        Note:
            This is a destructive operation that removes the entire parent directory.
            Make sure that the parent directory contains only model-related files that can be safely deleted.
        """

        # Remove parent directory
        parent_dir = os.path.dirname(model_dir)
        msg = f"Deleting existing model directory: {parent_dir}"
        logger.info(msg)
        print_colored_message(color=Color.YELLOW, message=msg)
        shutil.rmtree(parent_dir, ignore_errors=True)
        # Recreate the model directory
        os.makedirs(model_dir, exist_ok=True)

    @validate_call(config={"arbitrary_types_allowed": True}, validate_return=True)
    def load_model(
        self, model_local_path: Union[str, Path], **kwargs
    ) -> mlflow.pyfunc.PyFuncModel:
        """
        Load the model from the specified local path.

        Args:
            model_local_path (str | Path): Local path to the model directory.
            **kwargs: Additional keyword arguments passed to mlflow.pyfunc.load_model().

        Returns:
            mlflow.pyfunc.PythonModel: The loaded MLflow Python model.
        """
        if isinstance(model_local_path, Path):
            model_local_path = str(model_local_path)

        if not os.path.exists(model_local_path):
            msg = f"Model path {model_local_path} does not exist."
            logger.error(msg)
            raise FileNotFoundError(msg)
        # Load the model using MLflow
        return mlflow.pyfunc.load_model(model_local_path, **kwargs)

    @validate_call
    def log_artifacts(self, local_dir: str, artifact_path: Optional[str] = None):
        """
        Log the artifacts in the specified local directory to the configured IBM COS bucket.

        This method uploads the contents of the local directory to the IBM COS storage location,
        creating a model registry entry. If an entry already exists at the specified location
        (except for entries ending with "latest"), it will raise an error to prevent overwriting.

        Before uploading, this method removes any __pycache__ files and generates a hash of the
        model files for versioning and tracking purposes.

        Args:
            local_dir (str): Local directory containing the artifacts to upload.
            artifact_path (Optional[str]): Not used in this implementation.
                This argument is included for compatibility with the base class.

        Raises:
            ModelAlreadyExistsError: If a model already exists at the specified location and
                the key doesn't end with "latest".

        Returns:
            None
        """
        client = self._get_s3_client()
        if client.list_objects_v2(Bucket=self._bucket, Prefix=self._key, MaxKeys=1)[
            "KeyCount"
        ] and not self._key.endswith("latest"):
            raise ModelAlreadyExistsError(MODEL_ALREADY_EXISTS)
        self.clean_pycache_files(local_dir)
        self.write_hash(directory=local_dir)
        if artifact_path is None:
            super().log_artifacts(local_dir)
            msg = f"Model {self._model_name} version {self._model_version} has been logged to the registry: {self.artifact_uri}"
            logger.info(msg)
            print_colored_message(
                color=Color.GREEN_BOLD,
                message=msg,
            )

    @staticmethod
    @validate_call
    def _raise_missing_argument_error(argument_name: str):
        """
        Raises an exception when a required argument is missing.

        Args:
            argument_name (str): Name of the missing argument.

        Raises:
            ArgumentRequired: Exception with a formatted message indicating which argument is required.
        """
        raise ArgumentRequired(COS_ARGUMENT_REQUIRED.format(argument_name))

    @staticmethod
    @validate_call
    def clean_pycache_files(local_path: str) -> None:
        """
        Recursively removes all '__pycache__' directories under the specified path.

        This function searches for Python cache directories created during
        execution and removes them along with their contents to clean up
        temporary files.

        Args:
            local_path (str): Root directory path to start searching from

        Returns:
            None

        Note:
            Any errors during directory removal are ignored.
        """
        for pycache in Path(local_path).rglob("__pycache__"):
            shutil.rmtree(pycache, ignore_errors=True)

    @classmethod
    @validate_call
    def write_hash(cls, directory: str) -> None:
        """
        Computes and writes a hash fingerprint of the specified directory.

        This method generates a hash of the directory contents using the configured
        hashing algorithm, while ignoring specified files and the fingerprint file itself.
        The resulting hash is then written to a fingerprint file within the directory.

        Args:
            directory (str): Path to the directory for which to compute and store the hash.

        Returns:
            None

        Side Effects:
            Creates or overwrites a fingerprint file in the specified directory.
        """
        directory_path = Path(directory)
        hash_ = dirhash(
            directory_path,
            algorithm=cls.FINGERPRINT_ALGORITHM,
            ignore=cls.FINGERPRINT_IGNORE + (cls.FINGERPRINT_NAME,),
        )
        # Write the hash to the fingerprint file
        with open(directory_path / cls.FINGERPRINT_NAME, "w") as f:
            f.write(hash_)

    @validate_call
    def delete_model_version(self, *, confirm: bool = False) -> None:
        """
        Remove the model version from the remote registry.

        This method deletes the model version from the IBM Cloud Object Storage
        bucket, including all associated artifacts and metadata.
        It requires confirmation to prevent accidental deletions.

        Args:
            confirm (bool): If True, the model version will be deleted. If False,
                a warning message will be printed and no action will be taken.
                Defaults to False.
                This is a safety feature to prevent accidental deletions.
                Set explicitly confirm=True to proceed with the deletion.

        Returns:
            None
        """
        if not confirm:
            msg = (
                "This action will delete the model version from the registry. "
                "If you want to proceed, please set confirm=True when calling this method."
            )
            logger.warning(msg)
            print_colored_message(color=Color.YELLOW, message=msg)
            return
        # Delete the model version from the registry
        # using the S3 client
        client = self._get_s3_client()
        keys = [
            dict(Key=i["Key"])
            for i in client.list_objects(Bucket=self._bucket, Prefix=self._key)[
                "Contents"
            ]
        ]
        client.delete_objects(Bucket=self._bucket, Delete=dict(Objects=keys))
        msg = f"Model version {self._model_version} has been removed from the registry."
        logger.info(msg)
        print_colored_message(color=Color.YELLOW, message=msg)
