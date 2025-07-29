"""Defines the base logic for creation a math exercises."""

import logging
from typing import Any, ClassVar, Type

from pydantic import BaseModel, ValidationError

from wse_exercises.core.mathem.base.services import OperandGenerator
from wse_exercises.core.mathem.enums import Exercises
from wse_exercises.core.mathem.exceptions import OperandGeneratorError
from wse_exercises.core.mathem.task import (
    MathTaskConditions,
    MathTaskConfig,
    MathTextTaskAnswer,
    MathTextTaskQuestion,
    SimpleMathTask,
)

from .task_factory import MathTaskComponentFactory

logger = logging.getLogger(__name__)

MIN_VALUE = 1
MAX_VALUE = 9


class SimpleMathExerciseConfig(BaseModel):
    """Exercise config Data-Transfer-Object."""

    min_value: int = MIN_VALUE
    max_value: int = MAX_VALUE


class BaseSimpleCalculationExercise:
    """Defines a base logic of simple calculation exercise creation.

    Control exercise task creation with:
    - `task_factory`, create question and answer for exercise type;
    - `operand_generator`, get random or exact calculation operands;
    - `config`, set min and max calculation operand value range for
       random generator or as exact operands.
    """

    task_factory: ClassVar[Type[MathTaskComponentFactory]]
    exercise_name: ClassVar[Exercises]

    _operand_1: int
    _operand_2: int

    def __init__(
        self,
        operand_generator: OperandGenerator,
        config: SimpleMathExerciseConfig | dict[str, Any] | None = None,
    ) -> None:
        """Construct the task creation."""
        # Initialize exercise config
        try:
            # Automatic conversion of dictionaries
            # and other types into a model
            self._exercise_config = (
                SimpleMathExerciseConfig.model_validate(config)
                if config is not None
                else SimpleMathExerciseConfig()
            )
        except ValidationError as e:
            logger.error(f'Invalid exercise config: {e.errors()}')
            logger.info('Using default configuration')
            self._exercise_config = SimpleMathExerciseConfig()

        # Initialize calculation value range
        self._min_value = self._exercise_config.min_value
        self._max_value = self._exercise_config.max_value

        # Set up operand generator
        self._operand_generator = operand_generator
        self._operand_generator.set_values(self._min_value, self._max_value)

    def create_task(self) -> SimpleMathTask:
        """Create simple calculation task."""
        self._generate_operands()
        self._create_components()
        task_dto = self._create_task_dto()
        return task_dto

    # Utility methods

    def _generate_operands(self) -> None:
        """Generate task operands."""
        try:
            self._operand_1 = self._operand_generator.generate()
            self._operand_2 = self._operand_generator.generate()

        except OperandGeneratorError as e:
            logger.error(
                'Operand generation failed: %s. '
                'Using fallback values: min_value=%d, max_value=%d',
                str(e),
                self._min_value,
                self._max_value,
            )
            # Fallback to minimal possible values
            # to keep system operational
            self._operand_1 = self._min_value
            self._operand_2 = self._min_value

        except Exception as e:
            logger.critical(
                'Unexpected error during operand generation: %s',
                str(e),
                exc_info=True,
            )
            # Critical fallback to prevent complete failure
            self._operand_1 = 1
            self._operand_2 = 1

    def _create_components(self) -> None:
        """Create simple math task component DTO (question/answer)."""
        self._question = self.task_factory.create_question(
            self._operand_1, self._operand_2
        )
        self._answer = self.task_factory.create_answer(
            self._operand_1, self._operand_2
        )

    def _create_task_dto(self) -> SimpleMathTask:
        """Create simple math task Data Transfer Object."""
        return SimpleMathTask(
            config=MathTaskConfig(
                min_value=self._min_value,
                max_value=self._max_value,
            ),
            conditions=MathTaskConditions(
                operand_1=self._operand_1,
                operand_2=self._operand_2,
            ),
            question=MathTextTaskQuestion(
                text=self._question,
            ),
            answer=MathTextTaskAnswer(
                text=self._answer,
            ),
            exercise_name=self.exercise_name,
        )
