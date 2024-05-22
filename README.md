# Overview

| Developed by | Guardrails AI |
| Date of development | Feb 15, 2024 |
| Validator type | Format |
| Blog |  |
| License | Apache 2 |
| Input/Output | Output |

## Description

### Intended Use
This validator evaluates whether a translation is of high quality. It is useful for validating the output of language models that generate translations.

### Requirements

* Dependencies: 
    - guardrails-ai>=0.4.0 
    - unbabel-comet

* **IMPORTANT**: Steps to follow ***before** installing the validator*:
    - Please accept the gated model license from:
        https://huggingface.co/Unbabel/wmt22-cometkiwi-da
    - Get your Huggingface token from:
        https://huggingface.co/settings/tokens
        (Either create a new token or use an existing one)
    - Download Huggingface CLI:
        `pip install -U "huggingface_hub[cli]"`
    - Login into Huggingface Hub using the token:
        `huggingface-cli login --token $HUGGINGFACE_TOKEN`

## Installation

```bash
$ guardrails hub install hub://brainlogic/high_quality_translation
```

## Usage Examples

### Validating string output via Python

In this example, we use the `high_quality_translation` validator on any LLM generated text.

```python
# Import Guard and Validator
from guardrails.hub import HighQualityTranslation
from guardrails import Guard

# Use the Guard with the validator
if __name__ == "__main__":
    guard = Guard().use(
        HighQualityTranslation, threshold=0.75, on_fail="exception"
)

    # Test passing response
    guard.validate(
        "The capital of France is Paris.",
        metadata={"translation_source": "Die Hauptstadt von Frankreich ist Paris."},
    )

    try:
        # Test failing response
        guard.validate(
            "France capital Paris is of The.",
            metadata={"translation_source": "Die Hauptstadt von Frankreich ist Paris."},
        )
    except Exception as e:
        print(e)
```
Output:
```console
Validation failed for field with errors: France capital Paris is of The. is a low quality translation. 
```

# API Reference

**`__init__(self, threshold=0.75, on_fail="noop")`**
<ul>
Initializes a new instance of the Validator class.

**Parameters:**
- **`threshold`** *(float)*: The minimum score required for a translation to be considered high quality. The score is a float between 0 and 1, where 1 is the highest quality. The default is 0.75.
- **`on_fail`** *(str, Callable):* The policy to enact when a validator fails. If `str`, must be one of `reask`, `fix`, `filter`, `refrain`, `noop`, `exception` or `fix_reask`. Otherwise, must be a function that is called when the validator fails.
</ul>
<br/>

**`__call__(self, value, metadata={}) -> ValidationResult`**
<ul>
Validates the given `value` using the rules defined in this validator, relying on the `metadata` provided to customize the validation process. This method is automatically invoked by `guard.parse(...)`, ensuring the validation logic is applied to the input data.

Note:

1. This method should not be called directly by the user. Instead, invoke `guard.parse(...)` where this method will be called internally for each associated Validator.
2. When invoking `guard.parse(...)`, ensure to pass the appropriate `metadata` dictionary that includes keys and values required by this validator. If `guard` is associated with multiple validators, combine all necessary metadata into a single dictionary.

**Parameters**
- **`value`** *(Any)*: The input value to validate.
- **`metadata`** *(dict)*: A dictionary containing metadata required for validation. Keys and values must match the expectations of this validator.
    
    
    | Key | Type | Description | Default |
    | --- | --- | --- | --- |
    | `translation_source` | String | The original source text that was translated. | N/A |
</ul>
