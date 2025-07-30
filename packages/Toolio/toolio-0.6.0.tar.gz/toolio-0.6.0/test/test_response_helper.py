# SPDX-FileCopyrightText: 2024-present Oori Data <info@oori.dev>
# SPDX-License-Identifier: Apache-2.0
# test/test_response_helper.py
import json
import pytest

from toolio.response_helper import llm_response, llm_response_type

# Dummy generation response object for testing from_generation_response.
class DummyGenResp:
    def __init__(self, text, finish_reason, prompt_tokens=5, generation_tokens=10):
        self.text = text
        self.finish_reason = finish_reason
        self.prompt_tokens = prompt_tokens
        self.generation_tokens = generation_tokens

def test_from_openai_chat_plain_message():
    # Typical response from an OpenAI-powered chat endpoint.
    dummy_response = {
        'choices': [{
            'index': 0,
            'message': {'content': 'Hello, world!'},
            'finish_reason': 'stop'
        }],
        'usage': {'prompt_tokens': 5, 'completion_tokens': 10, 'total_tokens': 15},
        'object': 'chat.completion',
        'id': 'cmpl-test',
        'created': 1234567890,
        'model': 'dummy-model',
        'toolio.model_type': 'dummy'
    }
    resp_obj = llm_response.from_openai_chat(dummy_response)
    assert resp_obj.response_type == llm_response_type.MESSAGE
    assert resp_obj.usage == {'prompt_tokens': 5, 'completion_tokens': 10, 'total_tokens': 15}
    # Check that the first_choice_text property returns the expected message.
    assert 'Hello, world!' in resp_obj.first_choice_text

def test_from_openai_chat_tool_call():
    # Construct a dummy response that includes a tool call.
    dummy_response = {
        'choices': [{
            'index': 0,
            'message': {
                'tool_calls': [{
                    'id': 'call_1',
                    'function': {
                        'name': 'my_tool',
                        'arguments': '{"arg1": "val1"}'
                    }
                }]
            },
            'finish_reason': 'tool_calls'
        }],
        'usage': {'prompt_tokens': 6, 'completion_tokens': 8, 'total_tokens': 14},
        'object': 'chat.completion',
        'id': 'cmpl-tool',
        'created': 123,
        'model': 'tool-model',
        'toolio.model_type': 'dummy'
    }
    resp_obj = llm_response.from_openai_chat(dummy_response)
    assert resp_obj.response_type == llm_response_type.TOOL_CALL
    # Verify that the tool_calls field is populated properly.
    assert resp_obj.tool_calls is not None
    assert len(resp_obj.tool_calls) == 1
    tool_call_obj = resp_obj.tool_calls[0]
    assert tool_call_obj.name == 'my_tool'
    # The arguments should be parsed into a dictionary.
    assert tool_call_obj.arguments.get('arg1') == 'val1'

def test_from_generation_response_message():
    # Prepare a dummy generation response with non-empty text.
    gen_resp = DummyGenResp('Generated text.', 'stop', prompt_tokens=3, generation_tokens=7)
    response_obj = llm_response.from_generation_response(gen_resp, model_name='gen-model', model_type='dummy')
    assert response_obj is not None
    # The finish_reason from the generation response should be reflected.
    assert response_obj.choices[0]['finish_reason'] == 'stop'
    # Usage should be computed as the sum of prompt and generation tokens.
    expected_usage = {'prompt_tokens': 3, 'completion_tokens': 7, 'total_tokens': 10}
    assert response_obj.usage == expected_usage
    # Check that the response text contains the generated text.
    fc_text = response_obj.first_choice_text
    assert 'Generated text.' in fc_text

def test_from_generation_response_empty():
    # If the generated text is empty, the conversion should return None.
    gen_resp = DummyGenResp('', 'stop')
    response_obj = llm_response.from_generation_response(gen_resp)
    assert response_obj is None

def test_to_dict_and_to_json():
    dummy_response = {
        'choices': [{
            'index': 0,
            'message': {'content': 'Test Message'},
            'finish_reason': 'stop'
        }],
        'usage': {'prompt_tokens': 2, 'completion_tokens': 3, 'total_tokens': 5},
        'object': 'chat.completion',
        'id': 'cmpl-json',
        'created': 1000,
        'model': 'json-model',
        'toolio.model_type': 'dummy'
    }
    resp_obj = llm_response.from_openai_chat(dummy_response)
    resp_dict = resp_obj.to_dict()
    # Verify that expected keys exist in the dictionary.
    assert 'choices' in resp_dict
    assert 'usage' in resp_dict
    # Convert the response to a JSON string and back to a dictionary.
    json_str = resp_obj.to_json()
    parsed = json.loads(json_str)
    assert parsed['id'] == 'cmpl-json'

def test_first_choice_text_from_delta():
    # Test for the fallback when _first_choice_text is not explicitly set.
    dummy_response = {
        'choices': [{
            'index': 0,
            'delta': {'content': 'Delta message content'},
            'finish_reason': 'stop'
        }],
        'usage': {'prompt_tokens': 2, 'completion_tokens': 3, 'total_tokens': 5},
        'object': 'chat.completion',
        'id': 'cmpl-delta',
        'created': 1234,
        'model': 'delta-model',
        'toolio.model_type': 'dummy'
    }
    resp_obj = llm_response.from_openai_chat(dummy_response)
    fc_text = resp_obj.first_choice_text
    assert fc_text == 'Delta message content'
