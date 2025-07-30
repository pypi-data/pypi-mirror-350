# MLflow IBM COS Registry

A Python library that integrates IBM Cloud Object Storage (COS) with MLflow for model registry capabilities. This package provides an extended MLflow artifact repository implementation that leverages IBM COS for storing, versioning, and retrieving machine learning models.

## Features

- Store and manage ML models in IBM Cloud Object Storage
- Versioning with model fingerprinting
- Specialized support for "latest" model version
- Efficient caching to avoid redundant downloads
- Integration with MLflow's PyFunc model flavor

## Installation

Install the package using pip or any other package manager:

```bash
pip install mlflow-ibmcos
```

Or install from source:

```bash
git clone https://github.com/donielix/mlflow-ibm-cos-registry.git
cd mlflow-ibm-cos-registry
pip install -e .
```

## Requirements

- Python 3.8 or later
- IBM Cloud Object Storage account
- MLflow 2.15.0 or later

## Quick Start

```python
from mlflow_ibmcos import COSModelRegistry

# Initialize registry
registry = COSModelRegistry(
    bucket="my-model-bucket",
    model_name="text-classifier",
    model_version="latest",
    endpoint_url="https://s3.us-south.cloud-object-storage.appdomain.cloud",
    aws_access_key_id="your-access-key",
    aws_secret_access_key="your-secret-key"
)

# Log a model
registry.log_pyfunc_model_as_code(
    model_code_path="path/to/model_code.py",
    artifacts={"model": "path/to/model.pkl"}
)

# Download a model
local_path = registry.download_artifacts(dst_path="models")

# Load a model
model = registry.load_model(local_path)

# Make predictions
predictions = model.predict(data)
```

## Authentication

The registry requires IBM COS credentials which can be provided in several ways:

1. **Direct parameters**:
   ```python
   registry = COSModelRegistry(
       # Required parameters
       model_name="my-model",
       model_version="1.0.0",
       # Authentication parameters
       bucket="my-bucket",
       endpoint_url="https://s3.example.com",
       aws_access_key_id="your-access-key",
       aws_secret_access_key="your-secret-key"
   )
   ```

2. **Environment variables**:
   ```bash
   export AWS_ENDPOINT_URL="https://s3.example.com"
   export AWS_ACCESS_KEY_ID="your-access-key"
   export AWS_SECRET_ACCESS_KEY="your-secret-key"
   export COS_BUCKET_NAME="my-bucket"
   ```

   ```python
   registry = COSModelRegistry(
       model_name="my-model",
       model_version="1.0.0",
   )
   ```

## Usage Examples

### Uploading Models

#### Log a PyFunc Model as Code

```python
# Upload a model defined in a Python file
registry.log_pyfunc_model_as_code(
    model_code_path="path/to/model_code.py",
    artifacts={
        "model": "path/to/model.pkl",
        "encoder": "path/to/encoder.pkl"
    }
)
```

#### Log Model Artifacts Directly

```python
# Upload model artifacts from a directory
registry.log_artifacts(local_dir="path/to/model_directory")
```

### Downloading Models

```python
# Download model artifacts to a specified directory
model_path = registry.download_artifacts(dst_path="models")

# Download and delete other versions
model_path = registry.download_artifacts(
    dst_path="models",
    delete_other_versions=True,
)
```

### Working with Model Versions

#### Using the "latest" Tag

The "latest" tag is special and allows you to continually update a model:

```python
registry = COSModelRegistry(
    model_name="my-model",
    model_version="latest",
    # authentication parameters...
)

# Each time you log artifacts, it will update the "latest" version
registry.log_artifacts("path/to/model_dir")
```

When downloading a model with the "latest" tag, the registry will automatically fetch updates if the remote fingerprint differs from the local one.

#### Using Version Numbers

For stable versioning:

```python
registry = COSModelRegistry(
    model_name="my-model",
    model_version="1.0.0",  # Semantic versioning recommended
    # authentication parameters...
)
```

Version-tagged models won't be overwritten when uploaded again - you'll need to use a different version or the "latest" tag.

### Deleting Models

```python
# Initialize registry pointing to the model version to delete
registry = COSModelRegistry(
    model_name="my-model",
    model_version="1.0.0",
    # authentication parameters...
)

# Delete the model (requires confirmation)
registry.delete_model_version(confirm=True)
```

## API Reference

### COSModelRegistry

The main class for interacting with the IBM COS model registry.

```python
COSModelRegistry(
    model_name: str,
    model_version: str,
    bucket: Optional[str] = None,
    prefix: Optional[str] = None,
    **kwargs
)
```

**Parameters:**
- `model_name`: Name of the model
- `model_version`: Version of the model (can be a semantic version or "latest")
- `bucket`: IBM COS bucket name. If not provided, it will be fetched from COS_BUCKET_NAME environment variable
- `prefix`: Custom prefix for storage path (defaults to "traductor/registry")
- `**kwargs`: Additional parameters including:
  - `endpoint_url`: IBM COS endpoint URL
  - `aws_access_key_id`: Access key for IBM COS
  - `aws_secret_access_key`: Secret key for IBM COS
  - `config`: Additional configuration for the S3 client

**Main Methods:**

- `log_pyfunc_model_as_code(model_code_path, artifacts=None, **kwargs)`: Log a PyFunc model
- `log_artifacts(local_dir, artifact_path=None)`: Log model artifacts
- `download_artifacts(artifact_path=None, dst_path=None, delete_other_versions=False)`: Download model artifacts
- `load_model(model_local_path, **kwargs)`: Load a downloaded model
- `delete_model_version(confirm=False)`: Delete a model version

## Fingerprinting

The registry uses fingerprinting to track model changes and optimize downloads:

- A SHA-512 hash of the model directory is created when logging a model
- When downloading, the fingerprints are compared to avoid redundant downloads
- For "latest" models, differences in fingerprints trigger automatic updates

## Development

### Setting Up Development Environment

1. Clone the repository
2. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
3. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

### Running Tests

```bash
pytest tests/
```

For coverage report:
```bash
pytest --cov=mlflow_ibmcos tests/
```

## Contact

For issues, questions, or contributions, please contact:
- Daniel Diego Horcajuelo (dadiego91@hotmail.com)
