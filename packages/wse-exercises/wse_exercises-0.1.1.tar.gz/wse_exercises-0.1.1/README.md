## WSE Exercise Series

```python
from wse_exercises.core.mathem import (
    AddingExercise,
    RandomOperandGenerator,
)

random_operand_generator = RandomOperandGenerator()
config = {
    'min_value': 2,
    'max_value': 9,
}
exercise = AddingExercise(
    operand_generator=random_operand_generator,
    config=config,
)

task = exercise.create_task()
print(f'{task.question.text = }')
print(f'{task.answer.text = }')
```