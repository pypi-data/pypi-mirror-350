'''
python test/tool_tracer.py mlx-community/Mistral-Nemo-Instruct-2407-4bit
'''

import sys
import asyncio
import logging
import pprint

# import click

from toolio.llm_helper import model_manager
from toolio.toolcall import process_tools_for_sysmsg
from toolio.responder import ToolCallStreamingResponder, ToolCallResponder


class tracing_model_manager(model_manager):
    async def _completion_trip(self, messages, stream, req_tool_spec, max_tokens=128, temperature=0.1):
        # schema, tool_sysmsg = process_tool_sysmsg(req_tool_spec, self.logger, leadin=self.sysmsg_leadin)
        # Schema, including no-tool fallback, plus string spec of available tools, for use in constructing sysmsg
        full_schema, tool_schemas, sysmsg = process_tools_for_sysmsg(req_tool_spec)
        pprint.pprint(full_schema)
        pprint.pprint(sysmsg)
        if stream:
            responder = ToolCallStreamingResponder(self.model, self.model_path)
        else:
            responder = ToolCallResponder(self.model_path, self.model_type)
        messages = self.reconstruct_messages(messages, sysmsg=sysmsg)
        # Turn off prompt caching until we figure out https://github.com/OoriData/Toolio/issues/12
        cache_prompt=False
        async for resp in self._do_completion(messages, full_schema, responder, cache_prompt=cache_prompt,
                                                max_tokens=max_tokens, temperature=temperature):
            yield resp


async def amain_psyche(mm):
    # Give the LLm a tool it doesn't need
    from toolio.tool.demo import today_kfabe
    prompt = 'Write a haiku about AI'
    mm.register_tool(today_kfabe)
    # msgs = [ {'role': 'user', 'content': prompt} ]
    msgs = [ {'role': 'user', 'content': prompt} ]
    print(mm.complete_with_tools(msgs, tools=['today_kfabe']))

async def amain_birthday(mm):
    # Multiple tool calls, required in order
    from toolio.tool.demo import birthday_lookup, today_kfabe
    prompt = 'Write a nice note for each employee who has a birthday today.'
    mm.register_tool(birthday_lookup)
    mm.register_tool(today_kfabe)
    msgs = [ {'role': 'user', 'content': prompt} ]
    # msgs = [ {'role': 'system', 'content': sysprompt}, {'role': 'user', 'content': prompt} ]
    print(mm.complete_with_tools(msgs, tools=['birthday_lookup', 'today_kfabe']))

amain = amain_psyche

model = sys.argv[1]

logging.basicConfig(level=logging.DEBUG)
logging.getLogger().setLevel('DEBUG')  # Seems redundant, but is necessary. Python logging is quirky
logger = logging.getLogger(__name__)

mm = tracing_model_manager(model, logger=logger)
print('Model type:', mm.model_type)

resp = asyncio.run(amain(mm))

# @click.command()
# @click.option('--model', type=str, help='HuggingFace ID or disk path for locally-hosted MLF format model')
# def main(model):
#     print('XXX', model)
#     mm = model_manager(model)
#     resp = asyncio.run(amain(mm))
