"""Defines base class for task."""

from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel, Field

from wse_exercises.core.mathem.enums import Exercises

AnswerT = TypeVar('AnswerT')
QuestionT = TypeVar('QuestionT')
TaskConfigT = TypeVar('TaskConfigT')
TaskConditionsT = TypeVar('TaskConditionsT')


class TaskT(Generic[TaskConfigT, TaskConditionsT, QuestionT, AnswerT]):
    """Abstraction base task class."""

    config: TaskConfigT
    conditions: TaskConditionsT
    question: QuestionT
    answer: AnswerT
    exercise_name: Exercises
    error_msg: str
    created: datetime


class Task(BaseModel, TaskT[TaskConfigT, TaskConditionsT, QuestionT, AnswerT]):
    """Base class for DTO exercise task."""

    config: TaskConfigT
    conditions: TaskConditionsT
    question: QuestionT
    answer: AnswerT
    exercise_name: Exercises
    created: datetime = Field(default_factory=datetime.now)
    error_msg: str = ''
