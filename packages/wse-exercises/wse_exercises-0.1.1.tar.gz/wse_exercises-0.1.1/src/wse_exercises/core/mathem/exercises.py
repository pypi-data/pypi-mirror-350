"""Defines mathematical exercises.

>>> from wse_exercises import (
...     AddingExercise,
...     ExactOperandGenerator,
... )
>>> exercise = AddingExercise(
...     operand_generator=ExactOperandGenerator(),
...     config={'min_value': 2, 'max_value': 9},
... )
>>> task = exercise.create_task()
>>> task.question.text
'2 + 9'
>>> task.answer.text
'11'
"""

from .base.exercise import BaseSimpleCalculationExercise
from .enums import Exercises
from .task_factories import (
    AddingTaskFactory,
    DivisionTaskFactory,
    MultiplicationTaskFactory,
    SubtractionTaskFactory,
)


class AddingExercise(BaseSimpleCalculationExercise):
    """Adding exercise."""

    exercise_name = Exercises.ADDING
    task_factory = AddingTaskFactory


class DivisionExercise(BaseSimpleCalculationExercise):
    """Division exercise."""

    exercise_name = Exercises.DIVISION
    task_factory = DivisionTaskFactory


class MultiplicationExercise(BaseSimpleCalculationExercise):
    """Multiplication exercise."""

    exercise_name = Exercises.MULTIPLICATION
    task_factory = MultiplicationTaskFactory


class SubtractionExercise(BaseSimpleCalculationExercise):
    """Subtraction exercise."""

    exercise_name = Exercises.SUBTRACTION
    task_factory = SubtractionTaskFactory


if __name__ == '__main__':
    import doctest

    doctest.testmod()
