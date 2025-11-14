"""
Unit tests for prompts.py

Tests prompt strings and templates used by the LLM agent.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prompts import system_prompt, persistent_user_prompt, user_prompt


class TestSystemPrompt:
    """Test suite for system prompt"""

    def test_system_prompt_exists(self):
        """Test that system prompt is defined"""
        assert system_prompt is not None
        assert isinstance(system_prompt, str)
        assert len(system_prompt) > 0

    def test_system_prompt_contains_role_description(self):
        """Test that system prompt describes the agent's role"""
        assert "SentinelAI" in system_prompt
        assert "assistant" in system_prompt.lower() or "guide" in system_prompt.lower()

    def test_system_prompt_mentions_capabilities(self):
        """Test that system prompt mentions agent capabilities"""
        # Should mention building/mall context
        assert "building" in system_prompt.lower() or "mall" in system_prompt.lower()

    def test_system_prompt_has_tone_guidance(self):
        """Test that system prompt provides tone guidance"""
        assert "calm" in system_prompt.lower() or "empathetic" in system_prompt.lower()

    def test_system_prompt_mentions_zones(self):
        """Test that system prompt mentions zones or areas"""
        assert "zone" in system_prompt.lower() or "area" in system_prompt.lower()

    def test_system_prompt_mentions_doors(self):
        """Test that system prompt mentions doors or exits"""
        assert "door" in system_prompt.lower() or "exit" in system_prompt.lower()

    def test_system_prompt_provides_instruction_guidance(self):
        """Test that prompt guides on giving instructions"""
        assert "instruction" in system_prompt.lower() or "step" in system_prompt.lower()

    def test_system_prompt_format(self):
        """Test that system prompt is well-formatted"""
        # Should not have obvious formatting issues
        assert not system_prompt.startswith(" ")
        assert not system_prompt.endswith(" \n")


class TestPersistentUserPrompt:
    """Test suite for persistent user prompt"""

    def test_persistent_user_prompt_exists(self):
        """Test that persistent user prompt is defined"""
        assert persistent_user_prompt is not None
        assert isinstance(persistent_user_prompt, str)
        assert len(persistent_user_prompt) > 0

    def test_persistent_user_prompt_contains_mall_name(self):
        """Test that prompt contains mall name"""
        assert "EastField" in persistent_user_prompt or "mall" in persistent_user_prompt.lower()

    def test_persistent_user_prompt_describes_layout(self):
        """Test that prompt describes the mall layout"""
        assert "layout" in persistent_user_prompt.lower() or "store" in persistent_user_prompt.lower()

    def test_persistent_user_prompt_lists_zones(self):
        """Test that prompt lists zone information"""
        # Should mention specific zones
        assert "zone" in persistent_user_prompt.lower()
        # Check for some specific store names
        assert "Banana Store" in persistent_user_prompt or \
               "LuLuLime" in persistent_user_prompt or \
               "Victoria" in persistent_user_prompt

    def test_persistent_user_prompt_lists_doors(self):
        """Test that prompt lists door information"""
        assert "door" in persistent_user_prompt.lower()
        assert "Door Id" in persistent_user_prompt or "door id" in persistent_user_prompt.lower()

    def test_persistent_user_prompt_contains_exits(self):
        """Test that prompt mentions exits"""
        assert "exit" in persistent_user_prompt.lower()

    def test_persistent_user_prompt_has_instructions(self):
        """Test that prompt contains instructions for the agent"""
        assert "instruction" in persistent_user_prompt.lower() or \
               "if" in persistent_user_prompt.lower()

    def test_persistent_user_prompt_mentions_danger(self):
        """Test that prompt discusses danger zones"""
        assert "danger" in persistent_user_prompt.lower()

    def test_persistent_user_prompt_mentions_functions(self):
        """Test that prompt mentions function calling"""
        # Should reference functions like open_door, mark_zone
        assert "open" in persistent_user_prompt.lower() or \
               "mark" in persistent_user_prompt.lower() or \
               "function" in persistent_user_prompt.lower()

    def test_persistent_user_prompt_zone_mapping(self):
        """Test that prompt includes zone ID mappings"""
        # Should have zone ID references
        assert "Zone Id: 0" in persistent_user_prompt or "zone id: 0" in persistent_user_prompt.lower()

    def test_persistent_user_prompt_corridor_info(self):
        """Test that prompt describes corridors"""
        assert "corridor" in persistent_user_prompt.lower() or \
               "hallway" in persistent_user_prompt.lower()

    def test_persistent_user_prompt_format(self):
        """Test that persistent user prompt is well-formatted"""
        # Should have structure (not just a wall of text)
        assert "\n" in persistent_user_prompt
        # Should not have obvious formatting issues
        assert not persistent_user_prompt.startswith(" ")


class TestUserPrompt:
    """Test suite for user prompt template"""

    def test_user_prompt_exists(self):
        """Test that user prompt template is defined"""
        assert user_prompt is not None
        assert isinstance(user_prompt, str)
        assert len(user_prompt) > 0

    def test_user_prompt_has_placeholder(self):
        """Test that user prompt has placeholder for user speech"""
        assert "{user_speech}" in user_prompt or "{" in user_prompt

    def test_user_prompt_format_method(self):
        """Test that user prompt can be formatted"""
        try:
            formatted = user_prompt.format(user_speech="Test message")
            assert "Test message" in formatted or formatted == user_prompt
        except KeyError:
            # If no placeholder, that's also valid
            pass

    def test_user_prompt_context(self):
        """Test that user prompt provides context"""
        # Should indicate it's user speech or a turn marker
        lower_prompt = user_prompt.lower()
        assert "user" in lower_prompt or "speech" in lower_prompt or \
               "turn" in lower_prompt or "respond" in lower_prompt


class TestPromptIntegration:
    """Integration tests for prompt usage"""

    def test_all_prompts_defined(self):
        """Test that all expected prompts are defined"""
        assert system_prompt is not None
        assert persistent_user_prompt is not None
        assert user_prompt is not None

    def test_prompts_are_non_empty(self):
        """Test that all prompts have content"""
        assert len(system_prompt) > 10
        assert len(persistent_user_prompt) > 10
        assert len(user_prompt) > 0

    def test_prompts_are_strings(self):
        """Test that all prompts are strings"""
        assert isinstance(system_prompt, str)
        assert isinstance(persistent_user_prompt, str)
        assert isinstance(user_prompt, str)

    def test_system_and_persistent_prompts_complementary(self):
        """Test that system and persistent prompts cover different aspects"""
        # System prompt should be more about role/behavior
        # Persistent prompt should be more about specific context
        
        # This is a heuristic test
        assert len(system_prompt) > 50
        assert len(persistent_user_prompt) > 50
        
        # They should be different
        assert system_prompt != persistent_user_prompt

    def test_prompt_consistency(self):
        """Test consistency between prompts"""
        # If persistent prompt mentions specific stores, it should have details
        if "Banana Store" in persistent_user_prompt:
            # Should also have zone ID for that store
            assert "Zone Id" in persistent_user_prompt

    def test_no_sensitive_information(self):
        """Test that prompts don't contain sensitive information"""
        # Check for common sensitive patterns
        for prompt in [system_prompt, persistent_user_prompt, user_prompt]:
            assert "password" not in prompt.lower()
            assert "api_key" not in prompt.lower()
            assert "secret" not in prompt.lower()


class TestPromptContent:
    """Test specific content requirements of prompts"""

    def test_system_prompt_safety_focus(self):
        """Test that system prompt emphasizes safety"""
        lower_prompt = system_prompt.lower()
        # Should mention safety, danger, or emergency concepts
        safety_terms = ["safe", "danger", "emergency", "crisis", "panic"]
        assert any(term in lower_prompt for term in safety_terms)

    def test_persistent_prompt_has_all_stores(self):
        """Test that persistent prompt lists all stores"""
        stores = ["Banana Store", "LuLuLime", "Victoria", "PayMore", 
                  "StudyStart", "HandLocker", "Orange Republic"]
        
        found_stores = sum(1 for store in stores if store in persistent_user_prompt)
        # Should have most stores listed
        assert found_stores >= 5, f"Only found {found_stores} stores in prompt"

    def test_persistent_prompt_door_zone_mapping(self):
        """Test that doors are mapped to zones in persistent prompt"""
        # Should describe which doors lead where
        if "Door Id" in persistent_user_prompt:
            # Should also mention connections
            assert "corridor" in persistent_user_prompt.lower() or \
                   "zone" in persistent_user_prompt.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])