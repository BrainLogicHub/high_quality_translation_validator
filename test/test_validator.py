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
                "text": "Ich komme aus Bonn, Deutschland und ich bin 25 Jahre alt. Ich habe ein Hund."
            }
            """,
            {
                "translation_source": "I am from Bonn, Germany and I am 25 years old. I have a dog."
            },
        ),
        (
            """
            {
                "text": "The cat slept soundly under the warm afternoon sun, oblivious to the hustle and bustle of the city. Meanwhile, the leaves of the trees danced to the rhythm of the wind, painting a picture of peace and serenity."
            }
            """,
            {
                "translation_source": "El gato dormía plácidamente bajo el cálido sol de la tarde, ajeno al bullicio de la ciudad. Mientras tanto, las hojas de los árboles danzaban al ritmo del viento, pintando un cuadro de paz y serenidad."
            },
        ),
    ],
)
def test_happy_path(value, metadata):
    # Create a guard from the pydantic model
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
                "text": "Ich komme aus Bonn, Deutschland und ich bin 25 Jahre alt. Ich habe ein Hund."
            }
            """,
            {"translation_source": "I is Bonn but was 25 years. You is dog."},
        ),
        (
            """
            {
                "text": "Dog is sleeping under sun."
            }
            """,
            {
                "translation_source": "El gato dormía plácidamente bajo el cálido sol de la tarde, ajeno al bullicio de la ciudad. Mientras tanto, las hojas de los árboles danzaban al ritmo del viento, pintando un cuadro de paz y serenidad."
            },
        ),
    ],
)
def test_fail_path(value, metadata):
    # Create a guard from the pydantic model
    guard = Guard.from_pydantic(output_class=ValidatorTestObject)

    with pytest.raises(Exception):
        response = guard.parse(value, metadata=metadata)
        print("Fail path response", response)
