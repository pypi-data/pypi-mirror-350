"""Defines abstraction base class for math task creation."""

from abc import ABC, abstractmethod


class MathTaskComponentFactory(ABC):
    """Abstract base class for simple math task component factory."""

    @classmethod
    @abstractmethod
    def create_question(cls, operand_1: int, operand_2: int) -> str:
        """Create a question to a simple math task."""

    @classmethod
    @abstractmethod
    def create_answer(cls, operand_1: int, operand_2: int) -> str:
        """Create an answer to a simple math task."""
