from functools import partial
import os
from pathlib import Path
from typing import Callable, Dict, List
import pytest
from pytest_mock import MockerFixture

from mlflow_ibmcos.model_registry import COSModelRegistry


@pytest.fixture
def models_to_delete(request: pytest.FixtureRequest) -> Callable:
    """
    A fixture that provides a function to delete model versions.
    The models will be deleted immediately when the function is called,
    and a cleanup hook ensures all registered models are deleted when the test finishes.
    """
    models_to_delete: List[COSModelRegistry] = []

    def wrapper(model: COSModelRegistry) -> None:
        # Register the model for potential cleanup at the end of the test
        models_to_delete.append(model)

    def finalizer():
        # Cleanup hook that runs when the test function finishes
        for model in models_to_delete:
            try:
                model.delete_model_version(confirm=True)
            except Exception:
                # Ignore errors during cleanup - model might already be deleted
                pass

    request.addfinalizer(finalizer)

    return wrapper


@pytest.fixture(scope="session")
def bucket_name() -> str:
    return os.getenv("COS_BUCKET_NAME", "")


@pytest.fixture(scope="session")
def proxy() -> Dict[str, str]:
    """
    Fixture to provide proxy settings for the test environment.
    This fixture retrieves the HTTP and HTTPS proxy settings from environment variables
    """
    return {
        "http": os.getenv("HTTP_PROXY", ""),
        "https": os.getenv("HTTPS_PROXY", ""),
    }


@pytest.fixture
def mock_hash(mocker: MockerFixture):
    """
    Creates a test fixture that mocks the COSModelRegistry.write_hash method.

    This fixture allows tests to capture the generated fingerprint hash during model registration
    by copying it to a specified temporary path. This is useful for verifying that fingerprinting
    is correctly performed in tests without having to recalculate hashes.

    Args:
        mocker (MockerFixture): The pytest-mock fixture that provides patching functionality.

    Returns:
        callable: A wrapper function that accepts a tmp_path parameter and returns the mock patch.
            The returned function signature is:
                wrapper(tmp_path: Path) -> MagicMock
    """
    original_write_hash = COSModelRegistry.write_hash

    def mocked_write_hash(directory: str, tmp_path: Path):
        original_write_hash(directory)
        with open(os.path.join(directory, "fingerprint")) as f:
            hash_ = f.read()
        with open(os.path.join(tmp_path, "fingerprint"), "w") as f:
            f.write(hash_)
        return

    def wrapper(tmp_path: Path):
        return mocker.patch.object(
            target=COSModelRegistry,
            attribute="write_hash",
            new=partial(mocked_write_hash, tmp_path=tmp_path),
        )

    return wrapper


@pytest.fixture
def mock_clear_env(mocker: MockerFixture):
    mocker.patch.dict(os.environ, clear=True)
