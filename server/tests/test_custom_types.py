"""
Unit tests for custom_types.py

Tests Pydantic models for Retell webhook events and responses.
"""

import pytest
from pydantic import ValidationError
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from custom_types import (
    Utterance,
    PingPongRequest,
    CallDetailsRequest,
    UpdateOnlyRequest,
    ResponseRequiredRequest,
    ConfigResponse,
    PingPongResponse,
    ResponseResponse,
    AgentInterruptResponse,
    ToolCallInvocationResponse,
    ToolCallResultResponse,
)


class TestUtterance:
    """Test suite for Utterance model"""

    def test_utterance_valid_agent_role(self):
        """Test creating utterance with agent role"""
        utterance = Utterance(role="agent", content="Hello, how can I help?")
        assert utterance.role == "agent"
        assert utterance.content == "Hello, how can I help?"

    def test_utterance_valid_user_role(self):
        """Test creating utterance with user role"""
        utterance = Utterance(role="user", content="I need help!")
        assert utterance.role == "user"
        assert utterance.content == "I need help!"

    def test_utterance_valid_system_role(self):
        """Test creating utterance with system role"""
        utterance = Utterance(role="system", content="System message")
        assert utterance.role == "system"

    def test_utterance_invalid_role(self):
        """Test that invalid role raises validation error"""
        with pytest.raises(ValidationError):
            Utterance(role="invalid_role", content="Test")

    def test_utterance_empty_content(self):
        """Test utterance with empty content"""
        utterance = Utterance(role="agent", content="")
        assert utterance.content == ""


class TestPingPongRequest:
    """Test suite for PingPongRequest model"""

    def test_ping_pong_request_valid(self):
        """Test creating valid ping pong request"""
        request = PingPongRequest(interaction_type="ping_pong", timestamp=1234567890)
        assert request.interaction_type == "ping_pong"
        assert request.timestamp == 1234567890

    def test_ping_pong_request_invalid_interaction_type(self):
        """Test that invalid interaction type raises error"""
        with pytest.raises(ValidationError):
            PingPongRequest(interaction_type="invalid", timestamp=1234567890)

    def test_ping_pong_request_missing_timestamp(self):
        """Test that missing timestamp raises error"""
        with pytest.raises(ValidationError):
            PingPongRequest(interaction_type="ping_pong")


class TestCallDetailsRequest:
    """Test suite for CallDetailsRequest model"""

    def test_call_details_request_valid(self):
        """Test creating valid call details request"""
        call_data = {"call_id": "123", "from_number": "+1234567890"}
        request = CallDetailsRequest(interaction_type="call_details", call=call_data)
        assert request.interaction_type == "call_details"
        assert request.call == call_data

    def test_call_details_request_empty_call_dict(self):
        """Test with empty call dictionary"""
        request = CallDetailsRequest(interaction_type="call_details", call={})
        assert request.call == {}


class TestUpdateOnlyRequest:
    """Test suite for UpdateOnlyRequest model"""

    def test_update_only_request_valid(self):
        """Test creating valid update only request"""
        transcript = [
            Utterance(role="user", content="Hello"),
            Utterance(role="agent", content="Hi there")
        ]
        request = UpdateOnlyRequest(interaction_type="update_only", transcript=transcript)
        assert request.interaction_type == "update_only"
        assert len(request.transcript) == 2

    def test_update_only_request_empty_transcript(self):
        """Test with empty transcript"""
        request = UpdateOnlyRequest(interaction_type="update_only", transcript=[])
        assert len(request.transcript) == 0


class TestResponseRequiredRequest:
    """Test suite for ResponseRequiredRequest model"""

    def test_response_required_request_valid(self):
        """Test creating valid response required request"""
        transcript = [Utterance(role="user", content="Help me!")]
        request = ResponseRequiredRequest(
            interaction_type="response_required",
            response_id=42,
            transcript=transcript
        )
        assert request.interaction_type == "response_required"
        assert request.response_id == 42
        assert len(request.transcript) == 1

    def test_reminder_required_request_valid(self):
        """Test creating valid reminder required request"""
        transcript = [Utterance(role="user", content="Are you there?")]
        request = ResponseRequiredRequest(
            interaction_type="reminder_required",
            response_id=43,
            transcript=transcript
        )
        assert request.interaction_type == "reminder_required"
        assert request.response_id == 43

    def test_response_required_request_invalid_interaction_type(self):
        """Test that invalid interaction type raises error"""
        with pytest.raises(ValidationError):
            ResponseRequiredRequest(
                interaction_type="invalid",
                response_id=1,
                transcript=[]
            )

    def test_response_required_request_multiple_utterances(self):
        """Test with multiple utterances in transcript"""
        transcript = [
            Utterance(role="user", content="Hello"),
            Utterance(role="agent", content="Hi"),
            Utterance(role="user", content="I need help")
        ]
        request = ResponseRequiredRequest(
            interaction_type="response_required",
            response_id=1,
            transcript=transcript
        )
        assert len(request.transcript) == 3


class TestConfigResponse:
    """Test suite for ConfigResponse model"""

    def test_config_response_default(self):
        """Test creating config response with defaults"""
        response = ConfigResponse()
        assert response.response_type == "config"
        assert isinstance(response.config, dict)

    def test_config_response_custom_config(self):
        """Test config response with custom configuration"""
        custom_config = {"auto_reconnect": True, "call_details": False}
        response = ConfigResponse(config=custom_config)
        assert response.config["auto_reconnect"] is True
        assert response.config["call_details"] is False


class TestPingPongResponse:
    """Test suite for PingPongResponse model"""

    def test_ping_pong_response_valid(self):
        """Test creating valid ping pong response"""
        response = PingPongResponse(timestamp=1234567890)
        assert response.response_type == "ping_pong"
        assert response.timestamp == 1234567890

    def test_ping_pong_response_zero_timestamp(self):
        """Test with zero timestamp"""
        response = PingPongResponse(timestamp=0)
        assert response.timestamp == 0


class TestResponseResponse:
    """Test suite for ResponseResponse model"""

    def test_response_response_complete(self):
        """Test creating complete response"""
        response = ResponseResponse(
            response_id=1,
            content="I can help you with that.",
            content_complete=True,
            end_call=False
        )
        assert response.response_type == "response"
        assert response.response_id == 1
        assert response.content == "I can help you with that."
        assert response.content_complete is True
        assert response.end_call is False

    def test_response_response_partial(self):
        """Test creating partial response (streaming)"""
        response = ResponseResponse(
            response_id=2,
            content="Let me think",
            content_complete=False
        )
        assert response.content_complete is False
        assert response.end_call is False  # Default value

    def test_response_response_end_call(self):
        """Test response that ends the call"""
        response = ResponseResponse(
            response_id=3,
            content="Goodbye!",
            content_complete=True,
            end_call=True
        )
        assert response.end_call is True

    def test_response_response_with_transfer(self):
        """Test response with transfer number"""
        response = ResponseResponse(
            response_id=4,
            content="Transferring you now",
            content_complete=True,
            transfer_number="+1234567890"
        )
        assert response.transfer_number == "+1234567890"

    def test_response_response_empty_content(self):
        """Test response with empty content (final chunk)"""
        response = ResponseResponse(
            response_id=5,
            content="",
            content_complete=True
        )
        assert response.content == ""


class TestAgentInterruptResponse:
    """Test suite for AgentInterruptResponse model"""

    def test_agent_interrupt_response_basic(self):
        """Test creating basic agent interrupt response"""
        response = AgentInterruptResponse(
            interrupt_id=1,
            content="Let me clarify",
            content_complete=True
        )
        assert response.response_type == "agent_interrupt"
        assert response.interrupt_id == 1
        assert response.content == "Let me clarify"

    def test_agent_interrupt_no_interruption_allowed(self):
        """Test interrupt response that disallows further interruptions"""
        response = AgentInterruptResponse(
            interrupt_id=2,
            content="Please let me finish",
            content_complete=True,
            no_interruption_allowed=True
        )
        assert response.no_interruption_allowed is True

    def test_agent_interrupt_with_transfer(self):
        """Test interrupt with transfer"""
        response = AgentInterruptResponse(
            interrupt_id=3,
            content="Transferring",
            content_complete=True,
            transfer_number="+1234567890"
        )
        assert response.transfer_number == "+1234567890"


class TestToolCallInvocationResponse:
    """Test suite for ToolCallInvocationResponse model"""

    def test_tool_call_invocation_response_valid(self):
        """Test creating valid tool call invocation"""
        response = ToolCallInvocationResponse(
            tool_call_id="call_123",
            name="open_door",
            arguments='{"door_id": 5}'
        )
        assert response.response_type == "tool_call_invocation"
        assert response.tool_call_id == "call_123"
        assert response.name == "open_door"
        assert response.arguments == '{"door_id": 5}'

    def test_tool_call_invocation_empty_arguments(self):
        """Test with empty arguments"""
        response = ToolCallInvocationResponse(
            tool_call_id="call_124",
            name="get_status",
            arguments=""
        )
        assert response.arguments == ""


class TestToolCallResultResponse:
    """Test suite for ToolCallResultResponse model"""

    def test_tool_call_result_response_valid(self):
        """Test creating valid tool call result"""
        response = ToolCallResultResponse(
            tool_call_id="call_123",
            content="Door opened successfully"
        )
        assert response.response_type == "tool_call_result"
        assert response.tool_call_id == "call_123"
        assert response.content == "Door opened successfully"

    def test_tool_call_result_error_content(self):
        """Test with error content"""
        response = ToolCallResultResponse(
            tool_call_id="call_124",
            content="Error: Door is jammed"
        )
        assert "Error" in response.content


class TestModelIntegration:
    """Integration tests for model interactions"""

    def test_request_response_flow(self):
        """Test complete request-response flow"""
        # Create request
        transcript = [
            Utterance(role="user", content="Open door 5"),
            Utterance(role="agent", content="Opening door 5 now")
        ]
        request = ResponseRequiredRequest(
            interaction_type="response_required",
            response_id=100,
            transcript=transcript
        )
        
        # Create response
        response = ResponseResponse(
            response_id=request.response_id,
            content="Door 5 has been opened",
            content_complete=True
        )
        
        assert response.response_id == request.response_id

    def test_json_serialization(self):
        """Test that models can be serialized to JSON"""
        response = ResponseResponse(
            response_id=1,
            content="Test",
            content_complete=True
        )
        
        json_dict = response.model_dump()
        assert "response_type" in json_dict
        assert "response_id" in json_dict
        assert "content" in json_dict


if __name__ == "__main__":
    pytest.main([__file__, "-v"])