from pathlib import Path
from typing import Any, Callable, Dict, Generator

import mlflow
import mlflow.exceptions
from pydantic import ValidationError
from mlflow_ibmcos.core.exceptions import (
    MODEL_ALREADY_EXISTS,
    ArgumentRequired,
    ModelAlreadyExistsError,
)
from mlflow_ibmcos.model_registry import COSModelRegistry
import pytest

FIXTURES_PATH = Path(__file__).parent / "fixtures"


@pytest.fixture(scope="session")
def push_tagged_model(bucket_name: str) -> Generator[COSModelRegistry, Any, None]:
    """
    Creates a test tagged model and pushes it to the COS Model Registry.

    This function serves as a test fixture that creates a COSModelRegistry instance,
    logs a PyFunc model as code, and yields the registry for testing purposes.
    After the test is complete, it cleans up by deleting the model version.

    Parameters
    ----------
    bucket_name : str
        The name of the COS bucket to use for the model registry.

    Yields
    ------
    COSModelRegistry
        A configured model registry instance with a test model pushed to it.

    Notes
    -----
    This is designed to be used as a pytest fixture with cleanup handling.
    """

    # Create a test model and push it to the registry
    registry = COSModelRegistry(
        bucket=bucket_name,
        model_name="test",
        model_version="0.0.1",
    )
    registry.log_pyfunc_model_as_code(
        model_code_path=FIXTURES_PATH / "modelascode" / "modelcode.py",
        artifacts={"model": FIXTURES_PATH / "artifacts" / "model.pkl"},
    )
    yield registry

    # Clean up the test model
    registry.delete_model_version(confirm=True)


def test_model_registration_process(
    bucket_name: str, mock_hash: Callable, tmp_path: Path, models_to_delete: Callable
):
    """
    Test the end-to-end model registration process using COSModelRegistry.

    This test verifies the full workflow of:
    1. Logging a PyFunc model with code and artifacts to the registry
    2. Verifying the model fingerprint
    3. Downloading the model artifacts
    4. Checking the structure of downloaded artifacts
    5. Loading the model
    6. Making predictions with the loaded model

    Parameters
    ----------
    bucket_name : str
        Name of the COS bucket to use for the model registry.
        You can set this up using the environment variable COS_BUCKET_NAME.
    mock_hash : Callable
        Mock function for generating fingerprints
    tmp_path : Path
        Temporary path provided by pytest fixture for artifact storage

    Notes
    -----
    This test requires fixture files: modelcode.py and model.pkl
    """
    mock_hash(tmp_path)

    registry = COSModelRegistry(
        bucket=bucket_name,
        model_name="test",
        model_version="latest",
    )
    models_to_delete(registry)
    registry.log_pyfunc_model_as_code(
        model_code_path=FIXTURES_PATH / "modelascode" / "modelcode.py",
        artifacts={"model": FIXTURES_PATH / "artifacts" / "model.pkl"},
    )
    assert registry.artifact_uri == f"s3://{bucket_name}/{registry.PREFIX}/test/latest"
    remote_fingerprint = registry._get_remote_fingerprint()
    assert tmp_path.joinpath("fingerprint").read_text() == remote_fingerprint

    # Now download the model
    path = registry.download_artifacts(dst_path=tmp_path)
    model_files = set(Path(path).glob("**/*"))
    expected_files = {
        tmp_path.joinpath("test/latest/modelcode.py"),
        tmp_path.joinpath("test/latest/python_env.yaml"),
        tmp_path.joinpath("test/latest/conda.yaml"),
        tmp_path.joinpath("test/latest/requirements.txt"),
        tmp_path.joinpath("test/latest/artifacts/model.pkl"),
        tmp_path.joinpath("test/latest/MLmodel"),
        tmp_path.joinpath("test/latest/fingerprint"),
        tmp_path.joinpath("test/latest/artifacts"),
    }
    assert model_files == expected_files

    model = registry.load_model(model_local_path=path)

    prediction = model.predict(
        [
            {"text": "Hello"},
            {"text": "World"},
        ]
    )
    assert prediction == ["5", "5"]


def test_model_registration_with_tagged_model_and_no_bucket(
    mock_hash: Callable, models_to_delete: Callable, tmp_path: Path
):
    mock_hash(tmp_path)

    registry = COSModelRegistry(
        model_name="test",
        model_version="0.0.0",
    )
    registry.log_pyfunc_model_as_code(
        model_code_path=FIXTURES_PATH / "modelascode" / "modelcode.py",
        artifacts={"model": FIXTURES_PATH / "artifacts" / "model.pkl"},
    )
    models_to_delete(registry)
    assert (
        registry.artifact_uri == f"s3://{registry._bucket}/{registry.PREFIX}/test/0.0.0"
    )

    remote_fingerprint = registry._get_remote_fingerprint()
    assert tmp_path.joinpath("fingerprint").read_text() == remote_fingerprint

    # Now download the model
    path = registry.download_artifacts(dst_path=tmp_path)
    model_files = set(Path(path).glob("**/*"))
    expected_files = {
        tmp_path.joinpath("test/0.0.0/modelcode.py"),
        tmp_path.joinpath("test/0.0.0/python_env.yaml"),
        tmp_path.joinpath("test/0.0.0/conda.yaml"),
        tmp_path.joinpath("test/0.0.0/requirements.txt"),
        tmp_path.joinpath("test/0.0.0/artifacts/model.pkl"),
        tmp_path.joinpath("test/0.0.0/MLmodel"),
        tmp_path.joinpath("test/0.0.0/fingerprint"),
        tmp_path.joinpath("test/0.0.0/artifacts"),
    }
    assert model_files == expected_files

    model = registry.load_model(model_local_path=path)

    prediction = model.predict(
        [
            {"text": "Hello"},
            {"text": "World"},
        ]
    )
    assert prediction == ["5", "5"]


def test_registering_model_which_already_exists(push_tagged_model: COSModelRegistry):
    """
    Test that attempting to register a tagged model that already exists raises ModelAlreadyExistsError.

    This test verifies that the COSModelRegistry correctly raises a ModelAlreadyExistsError
    when trying to log a PyFunc model that has already been registered. The test expects
    the error message to match the predefined MODEL_ALREADY_EXISTS constant.

    Args:
        push_model (COSModelRegistry): A fixture providing a COSModelRegistry instance
                                      with a model already registered.
    """

    with pytest.raises(
        expected_exception=ModelAlreadyExistsError, match=MODEL_ALREADY_EXISTS
    ):
        push_tagged_model.log_pyfunc_model_as_code(
            model_code_path=FIXTURES_PATH / "modelascode" / "modelcode.py",
            artifacts={"model": FIXTURES_PATH / "artifacts" / "model.pkl"},
        )


def test_model_load_from_remote(
    tmp_path: Path,
    push_tagged_model: COSModelRegistry,
):
    model = push_tagged_model.load_remote_model(dst_path=tmp_path)
    predictions = model.predict(
        [
            {"text": "Hello"},
            {"text": "World"},
        ]
    )
    assert predictions == ["5", "5"]


def test_model_registration_process_with_custom_config(
    bucket_name: str,
    tmp_path: Path,
    proxy: Dict[str, str],
    mock_hash: Callable,
    models_to_delete: Callable,
):
    """
    Test the custom configuration of the COSModelRegistry class.

    This test verifies that the custom configuration is correctly applied
    and that the model registry behaves as expected with the custom settings.
    """
    mock_hash(tmp_path)

    registry = COSModelRegistry(
        bucket=bucket_name,
        model_name="test",
        model_version="latest",
        config=dict(proxies=proxy),
    )
    models_to_delete(registry)
    registry.log_pyfunc_model_as_code(
        model_code_path=FIXTURES_PATH / "modelascode" / "modelcode.py",
        artifacts={"model": FIXTURES_PATH / "artifacts" / "model.pkl"},
    )
    assert registry.artifact_uri == f"s3://{bucket_name}/{registry.PREFIX}/test/latest"
    remote_fingerprint = registry._get_remote_fingerprint()
    assert tmp_path.joinpath("fingerprint").read_text() == remote_fingerprint

    # Now download the model
    path = registry.download_artifacts(dst_path=tmp_path)
    model_files = set(Path(path).glob("**/*"))
    expected_files = {
        tmp_path.joinpath("test/latest/modelcode.py"),
        tmp_path.joinpath("test/latest/python_env.yaml"),
        tmp_path.joinpath("test/latest/conda.yaml"),
        tmp_path.joinpath("test/latest/requirements.txt"),
        tmp_path.joinpath("test/latest/artifacts/model.pkl"),
        tmp_path.joinpath("test/latest/MLmodel"),
        tmp_path.joinpath("test/latest/fingerprint"),
        tmp_path.joinpath("test/latest/artifacts"),
    }
    assert model_files == expected_files

    model = registry.load_model(model_local_path=path)

    prediction = model.predict(
        [
            {"text": "Hello"},
            {"text": "World"},
        ]
    )
    assert prediction == ["5", "5"]


def test_model_registration_process_with_params(
    bucket_name: str, mock_hash: Callable, tmp_path: Path, models_to_delete: Callable
):
    mock_hash(tmp_path)

    registry = COSModelRegistry(
        bucket=bucket_name,
        model_name="testwithparams",
        model_version="latest",
    )
    models_to_delete(registry)
    registry.log_pyfunc_model_as_code(
        model_code_path=FIXTURES_PATH / "modelascode" / "modelcodewithparams.py",
        artifacts={"model": FIXTURES_PATH / "artifacts" / "modelwithparams.pkl"},
        input_example=(
            ["hello", "world"],
            {
                "capitalize_only_first": True,
                "add_prefix": "prefix_",
            },
        ),
    )
    assert (
        registry.artifact_uri
        == f"s3://{bucket_name}/{registry.PREFIX}/testwithparams/latest"
    )
    remote_fingerprint = registry._get_remote_fingerprint()
    assert tmp_path.joinpath("fingerprint").read_text() == remote_fingerprint

    # Now download the model
    path = registry.download_artifacts(dst_path=tmp_path)
    model_files = set(Path(path).glob("**/*"))
    expected_files = {
        tmp_path.joinpath("testwithparams/latest/modelcodewithparams.py"),
        tmp_path.joinpath("testwithparams/latest/python_env.yaml"),
        tmp_path.joinpath("testwithparams/latest/conda.yaml"),
        tmp_path.joinpath("testwithparams/latest/requirements.txt"),
        tmp_path.joinpath("testwithparams/latest/artifacts/modelwithparams.pkl"),
        tmp_path.joinpath("testwithparams/latest/MLmodel"),
        tmp_path.joinpath("testwithparams/latest/fingerprint"),
        tmp_path.joinpath("testwithparams/latest/artifacts"),
        tmp_path.joinpath("testwithparams/latest/serving_input_example.json"),
        tmp_path.joinpath("testwithparams/latest/input_example.json"),
    }
    assert model_files == expected_files

    model = registry.load_model(model_local_path=path)

    prediction = model.predict(
        ["hi", "there"],
        params={
            "capitalize_only_first": False,
            "add_prefix": "prefix_",
        },
    )
    assert prediction == ["prefix_HI", "prefix_THERE"]

    # If we don't pass the params, it should use the default values
    # which are: capitalize_only_first=True, add_prefix="prefix_"
    prediction = model.predict(
        ["hi", "there"],
    )
    assert prediction == ["prefix_Hi", "prefix_There"]

    # If we juts pass the capitalize_only_first param, it should use the default value for add_prefix
    # which is: add_prefix="prefix_"
    prediction = model.predict(
        ["hi", "there"],
        params={
            "capitalize_only_first": False,
        },
    )
    assert prediction == ["prefix_HI", "prefix_THERE"]


def test_model_registration_process_with_none_params(
    bucket_name: str, mock_hash: Callable, tmp_path: Path, models_to_delete: Callable
):
    mock_hash(tmp_path)

    registry = COSModelRegistry(
        bucket=bucket_name,
        model_name="testwithparams",
        model_version="latest",
    )
    models_to_delete(registry)
    with pytest.raises(expected_exception=mlflow.exceptions.MlflowException):
        registry.log_pyfunc_model_as_code(
            model_code_path=FIXTURES_PATH / "modelascode" / "modelcodewithparams.py",
            artifacts={"model": FIXTURES_PATH / "artifacts" / "modelwithparams.pkl"},
            input_example=(
                ["hello", "world"],
                {
                    "capitalize_only_first": True,
                    "add_prefix": None,
                },
            ),
        )
    assert (
        registry.artifact_uri
        == f"s3://{bucket_name}/{registry.PREFIX}/testwithparams/latest"
    )


def test_model_registration_process_without_required_params(
    bucket_name: str, mock_hash: Callable, tmp_path: Path, models_to_delete: Callable
):
    mock_hash(tmp_path)

    registry = COSModelRegistry(
        bucket=bucket_name,
        model_name="testwithparams",
        model_version="latest",
    )
    models_to_delete(registry)
    registry.log_pyfunc_model_as_code(
        model_code_path=FIXTURES_PATH / "modelascode" / "modelcodewithparams.py",
        artifacts={"model": FIXTURES_PATH / "artifacts" / "modelwithparams.pkl"},
        input_example=["hello", "world"],
    )
    assert (
        registry.artifact_uri
        == f"s3://{bucket_name}/{registry.PREFIX}/testwithparams/latest"
    )
    assert (
        registry.artifact_uri
        == f"s3://{bucket_name}/{registry.PREFIX}/testwithparams/latest"
    )
    remote_fingerprint = registry._get_remote_fingerprint()
    assert tmp_path.joinpath("fingerprint").read_text() == remote_fingerprint

    # Now download the model
    path = registry.download_artifacts(dst_path=tmp_path)
    model_files = set(Path(path).glob("**/*"))
    expected_files = {
        tmp_path.joinpath("testwithparams/latest/modelcodewithparams.py"),
        tmp_path.joinpath("testwithparams/latest/python_env.yaml"),
        tmp_path.joinpath("testwithparams/latest/conda.yaml"),
        tmp_path.joinpath("testwithparams/latest/requirements.txt"),
        tmp_path.joinpath("testwithparams/latest/artifacts/modelwithparams.pkl"),
        tmp_path.joinpath("testwithparams/latest/MLmodel"),
        tmp_path.joinpath("testwithparams/latest/fingerprint"),
        tmp_path.joinpath("testwithparams/latest/artifacts"),
        tmp_path.joinpath("testwithparams/latest/serving_input_example.json"),
        tmp_path.joinpath("testwithparams/latest/input_example.json"),
    }
    assert model_files == expected_files

    model = registry.load_model(model_local_path=path)
    with pytest.raises(expected_exception=KeyError):
        model.predict(
            ["hi", "there"],
            params={
                "capitalize_only_first": False,
                "add_prefix": "prefix_",
            },
        )


def test_model_registration_wrong_artifacts_path(
    bucket_name: str, models_to_delete: Callable
):
    registry = COSModelRegistry(
        bucket=bucket_name,
        model_name="testnoartifacts",
        model_version="latest",
    )
    models_to_delete(registry)
    with pytest.raises(
        expected_exception=ValidationError, match="Path fakepath does not exist"
    ):
        registry.log_pyfunc_model_as_code(
            model_code_path=FIXTURES_PATH / "modelascode" / "modelcodewithparams.py",
            artifacts={"model": "fakepath"},
            input_example=(
                ["hello", "world"],
                {
                    "capitalize_only_first": True,
                    "add_prefix": None,
                },
            ),
        )


def test_model_registration_with_no_bucket(mock_clear_env):
    with pytest.raises(expected_exception=ArgumentRequired, match="bucket"):
        COSModelRegistry(
            model_name="test",
            model_version="latest",
        )
    with pytest.raises(expected_exception=ArgumentRequired, match="endpoint_url"):
        COSModelRegistry(
            bucket="fakebucket",
            model_name="test",
            model_version="latest",
        )
    with pytest.raises(expected_exception=ArgumentRequired, match="aws_access_key_id"):
        COSModelRegistry(
            bucket="fakebucket",
            model_name="test",
            model_version="latest",
            endpoint_url="fakeendpoint",
        )
    with pytest.raises(
        expected_exception=ArgumentRequired, match="aws_secret_access_key"
    ):
        COSModelRegistry(
            bucket="fakebucket",
            model_name="test",
            model_version="latest",
            endpoint_url="fakeendpoint",
            aws_access_key_id="fakekey",
        )


def test_model_registration_moving_artifacts(
    push_tagged_model: COSModelRegistry, tmp_path: Path
):
    """
    Test the model registration process with moving artifacts.

    This test verifies that the model artifacts are moved to the correct location
    after the model is registered. It checks that the artifacts are no longer in
    the original location and are present in the new location.

    Args:
        push_tagged_model (COSModelRegistry): A fixture providing a COSModelRegistry instance
                                              with a model already registered.
    """

    path = push_tagged_model.download_artifacts(
        dst_path=tmp_path, move_artifacts=dict(model=str(tmp_path / "new_model.pkl"))
    )
    assert set(Path(path).joinpath("artifacts").glob("**/*")) == set()
    assert Path(tmp_path).joinpath("new_model.pkl").exists()
    model = push_tagged_model.load_model(path)
    predictions = model.predict(
        [
            {"text": "Hello"},
            {"text": "World"},
        ]
    )
    assert predictions == ["5", "5"]
    # Now, we download the model again to the same path
    # and check that the artifacts are not moved again
    # and the model is still in the new location
    path = push_tagged_model.download_artifacts(
        dst_path=tmp_path, move_artifacts=dict(model=str(tmp_path / "new_model.pkl"))
    )
    assert set(Path(path).joinpath("artifacts").glob("**/*")) == set()
    assert Path(tmp_path).joinpath("new_model.pkl").exists()
    # Load the model again and check that the predictions are still the same
    model = push_tagged_model.load_model(path)
    predictions = model.predict(
        [
            {"text": "Hello"},
            {"text": "World"},
        ]
    )
    assert predictions == ["5", "5"]


def test_model_registration_multiple_artifacts(
    bucket_name: str, mock_hash: Callable, tmp_path: Path, models_to_delete: Callable
):
    mock_hash(tmp_path)

    registry = COSModelRegistry(
        bucket=bucket_name,
        model_name="test",
        model_version="latest",
    )
    models_to_delete(registry)
    registry.log_pyfunc_model_as_code(
        model_code_path=FIXTURES_PATH / "modelascode" / "modelandtokenizer.py",
        artifacts={
            "model": FIXTURES_PATH / "artifacts" / "modelwithtokenizer" / "model",
            "tokenizer": FIXTURES_PATH
            / "artifacts"
            / "modelwithtokenizer"
            / "tokenizer",
        },
        input_example=(["yo sabes", "el y ella"], dict(lower=True)),
    )
    assert registry.artifact_uri == f"s3://{bucket_name}/{registry.PREFIX}/test/latest"
    remote_fingerprint = registry._get_remote_fingerprint()
    assert tmp_path.joinpath("fingerprint").read_text() == remote_fingerprint

    # Now download the model
    path = registry.download_artifacts(dst_path=tmp_path)
    model_files = set(Path(path).glob("**/*"))
    expected_files = {
        tmp_path.joinpath("test/latest/modelandtokenizer.py"),
        tmp_path.joinpath("test/latest/python_env.yaml"),
        tmp_path.joinpath("test/latest/conda.yaml"),
        tmp_path.joinpath("test/latest/requirements.txt"),
        tmp_path.joinpath("test/latest/artifacts/model/model.pkl"),
        tmp_path.joinpath("test/latest/artifacts/tokenizer/tokenizer.pkl"),
        tmp_path.joinpath("test/latest/MLmodel"),
        tmp_path.joinpath("test/latest/fingerprint"),
        tmp_path.joinpath("test/latest/artifacts"),
        tmp_path.joinpath("test/latest/artifacts/model"),
        tmp_path.joinpath("test/latest/artifacts/tokenizer"),
        tmp_path.joinpath("test/latest/serving_input_example.json"),
        tmp_path.joinpath("test/latest/input_example.json"),
    }
    assert model_files == expected_files

    model = registry.load_model(model_local_path=path)

    prediction_lowering = model.predict(
        [
            "Yo sabes",
            "El y Ella",
        ],
        params={
            "lower": True,
        },
    )
    assert prediction_lowering == [1, 2]
    prediction_no_lowering = model.predict(
        [
            "Yo sabes",
            "El y Ella",
        ],
        params={
            "lower": False,
        },
    )
    assert prediction_no_lowering == [0, 0]


def test_model_registration_multiple_artifacts_with_moving(
    bucket_name: str, mock_hash: Callable, tmp_path: Path, models_to_delete: Callable
):
    mock_hash(tmp_path)

    registry = COSModelRegistry(
        bucket=bucket_name,
        model_name="test",
        model_version="latest",
    )
    models_to_delete(registry)
    registry.log_pyfunc_model_as_code(
        model_code_path=FIXTURES_PATH / "modelascode" / "modelandtokenizer.py",
        artifacts={
            "model": FIXTURES_PATH / "artifacts" / "modelwithtokenizer" / "model",
            "tokenizer": FIXTURES_PATH
            / "artifacts"
            / "modelwithtokenizer"
            / "tokenizer",
        },
        input_example=(["yo sabes", "el y ella"], dict(lower=True)),
    )
    assert registry.artifact_uri == f"s3://{bucket_name}/{registry.PREFIX}/test/latest"
    remote_fingerprint = registry._get_remote_fingerprint()
    assert tmp_path.joinpath("fingerprint").read_text() == remote_fingerprint

    # Now download the model
    path = registry.download_artifacts(
        dst_path=tmp_path,
        move_artifacts=dict(
            tokenizer=str(tmp_path / "tokenizer_subpath" / "tokenizer")
        ),
    )
    model_files = set(Path(path).glob("**/*"))
    expected_files = {
        tmp_path.joinpath("test/latest/modelandtokenizer.py"),
        tmp_path.joinpath("test/latest/python_env.yaml"),
        tmp_path.joinpath("test/latest/conda.yaml"),
        tmp_path.joinpath("test/latest/requirements.txt"),
        tmp_path.joinpath("test/latest/artifacts/model/model.pkl"),
        tmp_path.joinpath("test/latest/MLmodel"),
        tmp_path.joinpath("test/latest/fingerprint"),
        tmp_path.joinpath("test/latest/artifacts"),
        tmp_path.joinpath("test/latest/artifacts/model"),
        tmp_path.joinpath("test/latest/serving_input_example.json"),
        tmp_path.joinpath("test/latest/input_example.json"),
    }
    assert model_files == expected_files

    model = registry.load_model(model_local_path=path)
    prediction_lowering = model.predict(
        [
            "Yo sabes",
            "El y Ella",
        ],
        params={
            "lower": True,
        },
    )
    assert prediction_lowering == [1, 2]


def test_local_model_registry(bucket_name: str, tmp_path: Path):
    registry = COSModelRegistry(
        bucket=bucket_name,
        model_name="test",
        model_version="latest",
    )
    registry.log_pyfunc_model_as_code(
        model_code_path=FIXTURES_PATH / "modelascode" / "modelandtokenizer.py",
        artifacts={
            "model": FIXTURES_PATH / "artifacts" / "modelwithtokenizer" / "model",
            "tokenizer": FIXTURES_PATH
            / "artifacts"
            / "modelwithtokenizer"
            / "tokenizer",
        },
        input_example=(["yo sabes", "el y ella"], dict(lower=True)),
        local_path_storage=tmp_path,
    )
    expected_files = {
        tmp_path.joinpath("test/"),
        tmp_path.joinpath("test/modelandtokenizer.py"),
        tmp_path.joinpath("test/python_env.yaml"),
        tmp_path.joinpath("test/conda.yaml"),
        tmp_path.joinpath("test/requirements.txt"),
        tmp_path.joinpath("test/artifacts/model/model.pkl"),
        tmp_path.joinpath("test/artifacts/tokenizer/"),
        tmp_path.joinpath("test/artifacts/tokenizer/tokenizer.pkl"),
        tmp_path.joinpath("test/MLmodel"),
        tmp_path.joinpath("test/fingerprint"),
        tmp_path.joinpath("test/artifacts"),
        tmp_path.joinpath("test/artifacts/model"),
        tmp_path.joinpath("test/serving_input_example.json"),
        tmp_path.joinpath("test/input_example.json"),
    }
    assert set(tmp_path.glob("**/*")) == expected_files
