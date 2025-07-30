from typing import List
import mlflow
from pydantic import BaseModel
import cloudpickle


class ModelInput(BaseModel):
    text: str


class TestModel(mlflow.pyfunc.PythonModel):
    def load_context(self, context):
        # The model just have a predict method which returns str(len(text))
        with open(context.artifacts["model"], "rb") as f:
            self.model = cloudpickle.load(f)

    def preprocess(self, text: str) -> str:
        # Example preprocessing step
        return text.lower()

    def predict(self, model_input: List[ModelInput]) -> List[str]:
        return [self.model.predict(self.preprocess(item.text)) for item in model_input]


mlflow.models.set_model(TestModel())
