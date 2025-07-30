from typing import List
import mlflow
import cloudpickle


class TestModelWithParams(mlflow.pyfunc.PythonModel):
    """
    It wraps the following model:

    ```python
    class Model:
        def predict(self, texts: List[str], capitalize_only_first: bool, add_prefix: Optional[str]=None) -> List[str]:
            if add_prefix is None:
                add_prefix = ""
            return [add_prefix + i.capitalize() if capitalize_only_first else add_prefix + i.upper() for i in texts]
    ```
    """

    def load_context(self, context):
        # The model just have a predict method which returns str(len(text))
        with open(context.artifacts["model"], "rb") as f:
            self.model = cloudpickle.load(f)

    def predict(self, model_input: List[str], params=None) -> List[str]:
        return self.model.predict(
            model_input,
            capitalize_only_first=params["capitalize_only_first"],
            add_prefix=params["add_prefix"],
        )


mlflow.models.set_model(TestModelWithParams())
