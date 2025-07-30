import asyncio
from math import sqrt 
from toolio.llm_helper import local_model_runner
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

SQUARE_ROOT_METADATA = {
    'name': 'square_root', 
    'description': 'Get the square root of the given number',
    'parameters': {
        'type': 'object', 
        'properties': {
            'square': {
                'type': 'number',
                'description': 'Number from which to find the square root'
            }
        },
        'required': ['square']
    }
}

toolio_mm = local_model_runner('mlx-community/Hermes-2-Theta-Llama-3-8B-4bit',
                          tool_reg=[(sqrt, SQUARE_ROOT_METADATA)],
                          logger=logger)

async def query_sq_root(tmm):
    msgs = [{'role': 'user', 'content': 'What is the square root of 256?'}]
    try:
        resp = await tmm.complete_with_tools(msgs, tools=['square_root'])
        print(resp)
    except Exception as e:
        logger.exception("Error during completion")

if __name__ == "__main__":
    asyncio.run(query_sq_root(toolio_mm))