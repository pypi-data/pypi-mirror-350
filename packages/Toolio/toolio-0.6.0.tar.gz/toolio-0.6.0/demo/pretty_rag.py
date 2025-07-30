'''
demo/pretty_rag.py

Using polars & great_tables to visualize RAG results

* https://github.com/pola-rs/polars
* https://posit-dev.github.io/great-tables/examples/
'''

import asyncio
from enum import Enum  # , auto

from toolio.tool import tool, param
from toolio.llm_helper import local_model_runner


class arithmetic_op(Enum):
    ADD = 'add'
    SUBTRACT = 'subtract'
    MULTIPLY = 'multiply'
    DIVIDE = 'divide'


@tool('arithmetic_calc', params=[
    param('num1', float, 'Number on the left hand side of the calculation', True),
    param('num2', float, 'Number on the left hand side of the calculation', True),
    param('op', arithmetic_op, 'Arithmetic operation to make on the two numbers', True),
    ])
async def arithmetic_calc(num1=None, num2=None, op=None):
    'Very basic arithmetic calculator'
    match op:
        case arithmetic_op.ADD:
            result = num1 + num2
        case arithmetic_op.SUBTRACT:
            result = num1 - num2
        case arithmetic_op.MULTIPLY:
            result = num1 * num2
        case arithmetic_op.DIVIDE:
            result = num1 / num2
        case _:
            raise ValueError('Unknown operator')  # Shouldn't happen
    return result


# MLX_MODEL_PATH = 'mlx-community/Mistral-Nemo-Instruct-2407-4bit'
MLX_MODEL_PATH = 'mlx-community/Llama-3.2-3B-Instruct-4bit'

toolio_mm = local_model_runner(MLX_MODEL_PATH, tool_reg=[arithmetic_calc])

# Use this to try parallel function calling
# PROMPT = 'Solve the following calculations: 42 * 42, 24 * 24, 5 * 5, 89 * 75, 42 * 46, 69 * 85, 422 * 420, 753 * 321, 72 * 55, 240 * 204, 789 * 654, 123 * 321, 432 * 89, 564 * 321?'  # noqa: E501
PROMPT = 'Solve the following calculation: 4242 * 2424.2'
async def async_main(tmm):
    msgs = [ {'role': 'user', 'content': PROMPT} ]
    print((await tmm.complete_with_tools(msgs)).first_choice_text)

asyncio.run(async_main(toolio_mm))
