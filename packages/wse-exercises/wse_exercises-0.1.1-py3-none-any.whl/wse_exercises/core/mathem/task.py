"""Defines the math task Data Transfer Objects."""

from pydantic import BaseModel, model_validator

from wse_exercises.base.task import Task


class MathTaskConfig(BaseModel):
    """Math task config."""

    min_value: int
    max_value: int

    @model_validator(mode='after')
    def check_min_leq_max(self) -> 'MathTaskConfig':
        """Check that the minimum value is greater than the maximum."""
        if self.min_value > self.max_value:
            raise ValueError('The minimum value is greater than the maximum')
        return self


class MathTaskConditions(BaseModel):
    """Math task conditions."""

    operand_1: int
    operand_2: int


class MathTextTaskQuestion(BaseModel):
    """Math text task question."""

    text: str


class MathTextTaskAnswer(BaseModel):
    """Math text task answer."""

    text: str


class SimpleMathTask(
    Task[
        MathTaskConfig,
        MathTaskConditions,
        MathTextTaskQuestion,
        MathTextTaskAnswer,
    ]
):
    """Base simple math task with text question/answer."""
