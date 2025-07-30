# SPDX-FileCopyrightText: 2024-present Oori Data <info@oori.dev>
# SPDX-License-Identifier: Apache-2.0
# test/test_integration.py
from unittest.mock import Mock, patch
import pytest

pytest.skip(allow_module_level=True)

# We'll patch these imports
from toolio.llm_helper import model_manager
from toolio.schema_helper import Model

class DummyLLM:
    def __init__(self):
        self.model = Mock()
        self.model.model_type = 'dummy'

    def load(self, model_path):
        pass  # Do nothing, as we've already set up the mock

    async def _do_completion(self, messages, full_schema, responder, cache_prompt=cache_prompt,
                                                max_tokens=max_tokens, temperature=temperature):
        pass

    def completion(self, prompt, schema, **kwargs):
        yield {'op': 'evaluatedPrompt', 'token_count': 2}
        yield {'op': 'generatedTokens', 'text': f"Dummy response to: {prompt}"}
        yield {'op': 'stop', 'reason': 'end', 'token_count': 3}

    # def complete_with_tools(self, prompt)

@pytest.fixture
def dummy_model_manager():
    with patch('toolio.llm_helper.Model', DummyLLM):
        with patch('toolio.schema_helper.Model', DummyLLM):
            mm = model_manager('dummy_path')
            yield mm

@pytest.mark.asyncio
async def test_integration_completion(dummy_model_manager):
    result = [r async for r in dummy_model_manager.complete(['Test prompt'])]
    assert len(result) == 2
    assert "Dummy response to: ['Test prompt']" in result[0]['text']

@pytest.mark.asyncio
async def test_integration_complete_with_tools(dummy_model_manager):
    msgs = [ {'role': 'user', 'content': 'Test prompt with tools'} ]
    result = [r async for r in dummy_model_manager.complete_with_tools(msgs)]
    assert len(result) == 2
    assert "Dummy response to: ['Test prompt with tools']" in result[0]['text']
