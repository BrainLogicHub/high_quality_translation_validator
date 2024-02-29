from guardrails import Guard
from pydantic import BaseModel, Field
from validator import HighQualityTranslation
import pytest


# Create a pydantic model with a field that uses the custom validator
class ValidatorTestObject(BaseModel):
    text: str = Field(validators=[HighQualityTranslation(on_fail="exception")])


# Test happy path
@pytest.mark.parametrize(
    "value, metadata",
    [
        (
            """
            {
                "text": "The capital of France is Paris."
            }
            """,
            {"translation_source": "Die Hauptstadt von Frankreich ist Paris."},
        ),
        (
            """
            {
                "text": "¿Tienes una hamburguesa vegetariana con queso?"
            }
            """,
            {"translation_source": "Do you have a vegetarian burger with cheese?"},
        ),
    ],
)
def test_happy_path(value, metadata):
    """Test happy path."""
    guard = Guard.from_pydantic(output_class=ValidatorTestObject)
    response = guard.parse(value, metadata=metadata)
    print("Happy path response", response)
    assert response.validation_passed is True


# Test fail path
@pytest.mark.parametrize(
    "value, metadata",
    [
        (
            """
            {
                "text": "France capital Paris is of The."
            }
            """,
            {"translation_source": "Die Hauptstadt von Frankreich ist Paris."},
        ),
        (
            """
            {
                "text": "Hatten Sir eines vegetarische Burger ohne Käse?"
            }
            """,
            {"translation_source": "Do you have a vegetarian burger with cheese?"},
        ),
    ],
)
def test_fail_path(value, metadata):
    """Test fail path."""
    guard = Guard.from_pydantic(output_class=ValidatorTestObject)
    with pytest.raises(Exception):
        response = guard.parse(
            value,
            metadata=metadata,
        )
        print("Fail path response", response)
