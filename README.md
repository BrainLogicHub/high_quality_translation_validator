## Details

| Developed by | BrainLogic AI |
| --- | --- |
| Date of development | Feb 15, 2024 |
| Validator type | Quality |
| Blog | - |
| License | Apache 2 |
| Input/Output | Output |

## Description

This validator enforces quality constraints to check if a translated text is of sufficiently good quality. This validator works on the outputs of an LLM when you’re using the LLM primarily for translation.

Under the hood, this validator uses the open source `Unbabel/wmt22-cometkiwi-da` model to check for translation quality.

### Intended use

- Primary intended uses: This validator is useful when you’re using an LLM to perform machine translation.
- Out-of-scope use cases: N/A

## Example Usage Guide

### Installation

```bash
$ gudardrails hub install is-high-quality-translation
```

### Initialization

```python
from guardrails.hub import IsHighQualityTranslation

# Create validator
translation_validator = IsHighQualityTranslation(on_fail="noop")

# Create Guard with Validator
guard = Guard.from_string(
    validators=[translation_validator, ...],
    num_reasks=2,
)
```

### Invocation

```python
guard(
    "Translated_text",
    metadata={"translation_source": "Original text"}
)
```

## API Ref

N/A

## Expected deployment metrics

|  | CPU | GPU |
| --- | --- | --- |
| Latency |  | - |
| Memory |  | - |
| Cost |  | - |
| Expected quality |  | - |

## Resources required

- Dependencies:
    - Install the `unbabel-comet` from source: `pip install git+https://github.com/Unbabel/COMET`
    - Please accept the model license from: https://huggingface.co/Unbabel/wmt22-cometkiwi-da
    - Login into Huggingface Hub using: huggingface-cli login --token $HUGGINGFACE_TOKEN
- Foundation model access keys: Huggingface auth
- Compute: Yes

## Validator Performance

### Evaluation Dataset

N/A

### Model Performance Measures

| Accuracy | - |
| --- | --- |
| F1 Score | - |

### Decision thresholds

0.5
