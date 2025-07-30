import os
from typing import List
import mlflow
import cloudpickle
from pydantic.dataclasses import dataclass


@dataclass
class Model:
    """
    This model wraps the following artifacts:

    ```
    class Model:
        PRONOUNS = ["yo", "tu", "el", "ella", "nosotros", "nosotras", "vosotros", "vosotras", "ellos", "ellas"]
        def predict(self, texts: List[List[str]]) -> List[int]:
            # Returns a list of counts of pronouns for each list of words
            # Example:
            # model.predict([["yo", "sabes"], ["el", "y", "ella"]])
            # returns [1, 2]
            return [
                sum([1 for word in text if word in self.PRONOUNS]) for text in texts
            ]

    class Tokenizer:
        def __call__(self, texts: List[str]) -> List[List[str]]:
            # Tokenizes the input texts into lists of words
            # Example:
            # tokenizer(["yo sabes", "el y ella"])
            # returns [["yo", "sabes"], ["el", "y", "ella"]]
            return [text.split() for text in texts]
    ```
    """

    model_path: str
    tokenizer_path: str

    def __post_init__(self):
        with open(os.path.join(self.model_path, "model.pkl"), "rb") as f:
            self.model = cloudpickle.load(f)
        with open(os.path.join(self.tokenizer_path, "tokenizer.pkl"), "rb") as f:
            self.tokenizer = cloudpickle.load(f)

    def predict(self, texts: List[str], lower: bool = True) -> List[str]:
        if lower:
            texts = [text.lower() for text in texts]
        texts = self.tokenizer(texts)
        return self.model.predict(texts)


class TestModelAndTokenizer(mlflow.pyfunc.PythonModel):
    def load_context(self, context):
        model_path = context.artifacts["model"]
        processer_path = context.artifacts["tokenizer"]
        self.model = Model(model_path, processer_path)

    def predict(self, model_input: List[str], params=None) -> List[str]:
        if params is None:
            params = {}
        lower = params.get("lower", True)
        return self.model.predict(model_input, lower=lower)


mlflow.models.set_model(TestModelAndTokenizer())
