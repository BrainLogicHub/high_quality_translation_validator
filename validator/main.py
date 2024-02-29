from typing import Any, Dict, cast, Optional, Callable
from guardrails.validator_base import (
    FailResult,
    PassResult,
    ValidationResult,
    Validator,
    register_validator,
)

from comet import download_model, load_from_checkpoint


@register_validator(name="brainlogic/high_quality_translation", data_type="string")
class HighQualityTranslation(Validator):
    """Validates that the translation is of high quality.

    **Key Properties**

    | Property                      | Description                               |
    | ----------------------------- | ----------------------------------------- |
    | Name for `format` attribute   | `brainlogic/high_quality_translation`     |
    | Supported data types          | `string`                                  |
    | Programmatic fix              | None                                      |

    Other parameters: Metadata
        translation_source (str): The source of the translation.

    This validator uses one of the reference-free models from Unbabel/COMET
    to check the quality of the translation. Specifically, it uses the
    `Unbabel/wmt22-cometkiwi-da` model.

    Unbabel/COMET details: https://github.com/Unbabel/COMET
    Model details: https://huggingface.co/Unbabel/wmt22-cometkiwi-da

    Pre-requisites:
        - Please accept the gated model license from:
            https://huggingface.co/Unbabel/wmt22-cometkiwi-da
        - Get your Huggingface token from:
            https://huggingface.co/settings/tokens
            (Either create a new token or use an existing one)
        - Download Huggingface CLI:
            `pip install -U "huggingface_hub[cli]"`
        - Login into Huggingface Hub using the token:
            `huggingface-cli login --token $HUGGINGFACE_TOKEN`
    """

    def __init__(
        self,
        threshold: float = 0.75,
        on_fail: Optional[Callable] = None,
        **kwargs,
    ):
        super().__init__(on_fail, threshold=threshold, **kwargs)
        self._model_name = "Unbabel/wmt22-cometkiwi-da"
        self._quality_threshold = threshold

        try:
            # Download and load the model
            print(f"Loading the model {self._model_name}...")
            model_path = download_model(self._model_name)
            self.model = load_from_checkpoint(model_path)
        except Exception as e:
            raise RuntimeError(
                f"Error while downloading the model {self._model_name} "
                "from COMET: {e}.\n Please review the validator "
                "documentation for more details on the pre-requisites."
                "Ensure that you are logged into Huggingface Hub."
            ) from e

    def validate(self, value: Any, metadata: Dict) -> ValidationResult:
        """Validation method of the validator."""

        if "translation_source" not in metadata:
            raise RuntimeError("The validator expects `translation_source` in metadata")

        model_output = self.model.predict(
            [{"src": metadata["translation_source"], "mt": value}],
            accelerator="cpu",
        )
        model_output = cast(Any, model_output)
        translation_quality = model_output.scores[0]
        if translation_quality < self._quality_threshold:
            return FailResult(
                error_message=f"{value} is a low quality translation. ",
                fix_value="",
            )
        return PassResult()
