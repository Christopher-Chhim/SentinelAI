"""
Unit tests for agent.py

Tests the LlmClient class methods and logic for the SentinelAI agent.
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch, MagicMock
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import LlmClient, zone_door_mapping
from custom_types import ResponseRequiredRequest, ResponseResponse, Utterance


class TestZoneDoorMapping:
    """Test suite for the zone_door_mapping constant"""

    def test_zone_door_mapping_exists(self):
        """Test that zone door mapping is defined"""
        assert zone_door_mapping is not None
        assert isinstance(zone_door_mapping, dict)

    def test_zone_door_mapping_has_all_zones(self):
        """Test that mapping includes expected zones"""
        # Should have zones 0-8 (stores and corridors)
        expected_zones = {0, 1, 2, 3, 4, 5, 6, 7, 8}
        assert set(zone_door_mapping.keys()) == expected_zones

    def test_zone_door_mapping_values_are_lists(self):
        """Test that all mapping values are lists"""
        for zone_id, doors in zone_door_mapping.items():
            assert isinstance(doors, list), f"Zone {zone_id} should map to a list"

    def test_zone_door_mapping_door_ids_valid(self):
        """Test that door IDs in mapping are valid integers"""
        for _zone_id, doors in zone_door_mapping.items():
            for door_id in doors:
                assert isinstance(door_id, int), f"Door ID {door_id} should be an integer"
                assert door_id >= 0, f"Door ID {door_id} should be non-negative"

    def test_zone_door_mapping_specific_zones(self):
        """Test specific zone mappings"""
        # Zone 0 should map to door 0
        assert 0 in zone_door_mapping[0]
        
        # Zone 8 (main corridor) should have multiple doors
        assert len(zone_door_mapping[8]) > 1


class TestLlmClientInitialization:
    """Test suite for LlmClient initialization"""

    @patch.dict(os.environ, {'CEREBRAS_API_KEY': 'test_key'})
    def test_llm_client_init(self):
        """Test LlmClient initialization"""
        client = LlmClient()
        assert client is not None
        assert client.supabase is None  # Not initialized until setup_supabase

    @patch.dict(os.environ, {'CEREBRAS_API_KEY': 'test_key'})
    def test_llm_client_has_client_attribute(self):
        """Test that LlmClient has client attribute"""
        client = LlmClient()
        assert hasattr(client, 'client')


class TestDraftBeginMessage:
    """Test suite for draft_begin_message method"""

    @patch.dict(os.environ, {'CEREBRAS_API_KEY': 'test_key'})
    def test_draft_begin_message_returns_response(self):
        """Test that draft_begin_message returns a ResponseResponse"""
        client = LlmClient()
        response = client.draft_begin_message()
        
        assert isinstance(response, ResponseResponse)
        assert response.response_id == 0
        assert response.content_complete is True
        assert response.end_call is False

    @patch.dict(os.environ, {'CEREBRAS_API_KEY': 'test_key'})
    def test_draft_begin_message_content(self):
        """Test that begin message has appropriate content"""
        client = LlmClient()
        response = client.draft_begin_message()
        
        assert len(response.content) > 0
        assert "SentinelAI" in response.content or "emergency" in response.content.lower()

    @patch.dict(os.environ, {'CEREBRAS_API_KEY': 'test_key'})
    def test_draft_begin_message_greeting(self):
        """Test that begin message is a greeting"""
        client = LlmClient()
        response = client.draft_begin_message()
        
        # Should contain greeting-like words
        content_lower = response.content.lower()
        greeting_words = ["hello", "hi", "greetings", "welcome"]
        assert any(word in content_lower for word in greeting_words)


class TestConvertTranscriptToOpenAIMessages:
    """Test suite for convert_transcript_to_openai_messages method"""

    @patch.dict(os.environ, {'CEREBRAS_API_KEY': 'test_key'})
    def test_convert_transcript_empty(self):
        """Test converting empty transcript"""
        client = LlmClient()
        result = client.convert_transcript_to_openai_messages([])
        assert result == []

    @patch.dict(os.environ, {'CEREBRAS_API_KEY': 'test_key'})
    def test_convert_transcript_single_agent_message(self):
        """Test converting single agent message"""
        client = LlmClient()
        transcript = [Utterance(role="agent", content="How can I help?")]
        result = client.convert_transcript_to_openai_messages(transcript)
        
        assert len(result) == 1
        assert result[0]["role"] == "assistant"
        assert result[0]["content"] == "How can I help?"

    @patch.dict(os.environ, {'CEREBRAS_API_KEY': 'test_key'})
    def test_convert_transcript_single_user_message(self):
        """Test converting single user message"""
        client = LlmClient()
        transcript = [Utterance(role="user", content="I need help!")]
        result = client.convert_transcript_to_openai_messages(transcript)
        
        assert len(result) == 1
        assert result[0]["role"] == "user"
        assert result[0]["content"] == "I need help!"

    @patch.dict(os.environ, {'CEREBRAS_API_KEY': 'test_key'})
    def test_convert_transcript_multiple_messages(self):
        """Test converting multiple messages"""
        client = LlmClient()
        transcript = [
            Utterance(role="user", content="Hello"),
            Utterance(role="agent", content="Hi there"),
            Utterance(role="user", content="There's a fire!"),
            Utterance(role="agent", content="I'll help you evacuate")
        ]
        result = client.convert_transcript_to_openai_messages(transcript)
        
        assert len(result) == 4
        assert result[0]["role"] == "user"
        assert result[1]["role"] == "assistant"
        assert result[2]["role"] == "user"
        assert result[3]["role"] == "assistant"

    @patch.dict(os.environ, {'CEREBRAS_API_KEY': 'test_key'})
    def test_convert_transcript_preserves_content(self):
        """Test that content is preserved during conversion"""
        client = LlmClient()
        content = "This is a test message with special chars: !@#$%"
        transcript = [Utterance(role="user", content=content)]
        result = client.convert_transcript_to_openai_messages(transcript)
        
        assert result[0]["content"] == content


class TestPreparePrompt:
    """Test suite for prepare_prompt method"""

    @patch.dict(os.environ, {'CEREBRAS_API_KEY': 'test_key'})
    def test_prepare_prompt_structure(self):
        """Test that prepare_prompt returns correct structure"""
        client = LlmClient()
        transcript = [Utterance(role="user", content="Help!")]
        request = ResponseRequiredRequest(
            interaction_type="response_required",
            response_id=1,
            transcript=transcript
        )
        
        result = client.prepare_prompt(request)
        
        assert isinstance(result, list)
        assert len(result) >= 2  # At least system + persistent user prompt

    @patch.dict(os.environ, {'CEREBRAS_API_KEY': 'test_key'})
    def test_prepare_prompt_has_system_message(self):
        """Test that prompt includes system message"""
        client = LlmClient()
        transcript = [Utterance(role="user", content="Help!")]
        request = ResponseRequiredRequest(
            interaction_type="response_required",
            response_id=1,
            transcript=transcript
        )
        
        result = client.prepare_prompt(request)
        
        assert result[0]["role"] == "system"
        assert len(result[0]["content"]) > 0

    @patch.dict(os.environ, {'CEREBRAS_API_KEY': 'test_key'})
    def test_prepare_prompt_includes_transcript(self):
        """Test that prompt includes transcript messages"""
        client = LlmClient()
        transcript = [
            Utterance(role="user", content="Fire in store!"),
            Utterance(role="agent", content="Evacuating now")
        ]
        request = ResponseRequiredRequest(
            interaction_type="response_required",
            response_id=1,
            transcript=transcript
        )
        
        result = client.prepare_prompt(request)
        
        # Should contain the transcript messages
        user_messages = [msg for msg in result if msg["role"] == "user"]
        assert len(user_messages) >= 1

    @patch.dict(os.environ, {'CEREBRAS_API_KEY': 'test_key'})
    def test_prepare_prompt_reminder_required(self):
        """Test prepare_prompt with reminder_required interaction"""
        client = LlmClient()
        transcript = [Utterance(role="user", content="Hello?")]
        request = ResponseRequiredRequest(
            interaction_type="reminder_required",
            response_id=1,
            transcript=transcript
        )
        
        result = client.prepare_prompt(request)
        
        # Should have additional reminder context
        assert len(result) > 2


class TestPrepareFunctions:
    """Test suite for prepare_functions method"""

    @patch.dict(os.environ, {'CEREBRAS_API_KEY': 'test_key'})
    def test_prepare_functions_returns_list(self):
        """Test that prepare_functions returns a list"""
        client = LlmClient()
        result = client.prepare_functions()
        
        assert isinstance(result, list)
        assert len(result) > 0

    @patch.dict(os.environ, {'CEREBRAS_API_KEY': 'test_key'})
    def test_prepare_functions_has_open_door(self):
        """Test that open_door function is defined"""
        client = LlmClient()
        result = client.prepare_functions()
        
        function_names = [f["function"]["name"] for f in result]
        assert "open_door" in function_names

    @patch.dict(os.environ, {'CEREBRAS_API_KEY': 'test_key'})
    def test_prepare_functions_has_close_door(self):
        """Test that close_door function is defined"""
        client = LlmClient()
        result = client.prepare_functions()
        
        function_names = [f["function"]["name"] for f in result]
        assert "close_door" in function_names

    @patch.dict(os.environ, {'CEREBRAS_API_KEY': 'test_key'})
    def test_prepare_functions_has_mark_zone(self):
        """Test that mark_zone function is defined"""
        client = LlmClient()
        result = client.prepare_functions()
        
        function_names = [f["function"]["name"] for f in result]
        assert "mark_zone" in function_names

    @patch.dict(os.environ, {'CEREBRAS_API_KEY': 'test_key'})
    def test_prepare_functions_structure(self):
        """Test that functions have correct structure"""
        client = LlmClient()
        result = client.prepare_functions()
        
        for func in result:
            assert "type" in func
            assert func["type"] == "function"
            assert "function" in func
            assert "name" in func["function"]
            assert "description" in func["function"]
            assert "parameters" in func["function"]

    @patch.dict(os.environ, {'CEREBRAS_API_KEY': 'test_key'})
    def test_open_door_function_parameters(self):
        """Test open_door function parameters"""
        client = LlmClient()
        functions = client.prepare_functions()
        
        open_door_func = next(f for f in functions if f["function"]["name"] == "open_door")
        params = open_door_func["function"]["parameters"]
        
        assert "door_id" in params["properties"]
        assert "output" in params["properties"]
        assert params["properties"]["door_id"]["type"] == "integer"

    @patch.dict(os.environ, {'CEREBRAS_API_KEY': 'test_key'})
    def test_mark_zone_function_has_status_enum(self):
        """Test mark_zone function has status enum"""
        client = LlmClient()
        functions = client.prepare_functions()
        
        mark_zone_func = next(f for f in functions if f["function"]["name"] == "mark_zone")
        status_param = mark_zone_func["function"]["parameters"]["properties"]["status"]
        
        assert "enum" in status_param
        assert "ok" in status_param["enum"]
        assert "danger" in status_param["enum"]


class TestLlmClientIntegration:
    """Integration tests for LlmClient"""

    @patch.dict(os.environ, {'CEREBRAS_API_KEY': 'test_key'})
    def test_client_workflow(self):
        """Test complete client workflow"""
        client = LlmClient()
        
        # Create request
        transcript = [Utterance(role="user", content="Open door 5")]
        request = ResponseRequiredRequest(
            interaction_type="response_required",
            response_id=1,
            transcript=transcript
        )
        
        # Prepare prompt
        prompt = client.prepare_prompt(request)
        assert len(prompt) > 0
        
        # Get functions
        functions = client.prepare_functions()
        assert len(functions) > 0

    @patch.dict(os.environ, {'CEREBRAS_API_KEY': 'test_key'})
    def test_begin_message_flow(self):
        """Test begin message flow"""
        client = LlmClient()
        
        # Get begin message
        begin_msg = client.draft_begin_message()
        assert begin_msg.response_id == 0
        assert begin_msg.content_complete


if __name__ == "__main__":
    pytest.main([__file__, "-v"])