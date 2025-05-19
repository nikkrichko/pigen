"""
Unit tests for the SceneGenerator class.

This module contains unit tests for the SceneGenerator class using the unittest framework
and mocking to avoid actual API calls during testing.
"""

import sys
import json
import unittest
from unittest.mock import patch, MagicMock

# Add the project root directory to the Python path
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from support.sceneDescription import SceneGenerator, SceneDescription


class TestSceneGenerator(unittest.TestCase):
    """Tests for the SceneGenerator class."""

    def setUp(self):
        """Set up test fixtures."""
        self.scene_generator = SceneGenerator()
        
        # Sample story context
        self.story_context = """
        Once upon a time, there was a brave knight named Sir Arthur. 
        He lived in a castle with his loyal squire, Thomas. 
        One day, an evil dragon attacked the nearby village. 
        Sir Arthur mounted his white horse and rode to face the dragon.
        The battle was fierce, but Sir Arthur prevailed and saved the village.
        """
        
        # Sample characters
        self.characters = ["Sir Arthur", "Thomas", "Dragon"]
        
        # Sample scene data
        self.sample_scene_data = {
            "scene_number": 1,
            "description": "Sir Arthur in his castle with Thomas",
            "characters": ["Sir Arthur", "Thomas"],
            "characters_interaction": "Sir Arthur is discussing battle plans with Thomas",
            "setting": "Castle interior",
            "objects": ["Armor", "Weapons", "Maps"],
            "mood": "Serious",
            "time_of_day": "Morning",
            "weather": "Sunny"
        }
        
        # Create a mock message with content
        self.mock_message = MagicMock()
        self.mock_message.content = json.dumps(self.sample_scene_data)
        
        # Create a mock choice with message
        self.mock_choice = MagicMock()
        self.mock_choice.message = self.mock_message
        
        # Create a mock prompt result with choices
        self.mock_prompt_result = MagicMock()
        self.mock_prompt_result.choices = [self.mock_choice]

    @patch('support.sceneDescription.GptClient')
    def test_generate_scene(self, mock_gpt_client):
        """Test generating a scene description."""
        # Configure the mock
        mock_client_instance = mock_gpt_client.return_value
        mock_client_instance.run_prompt.return_value = self.mock_prompt_result
        
        # Call the method
        scene = self.scene_generator.generate_scene(1, self.story_context, self.characters)
        
        # Verify the result
        self.assertEqual(scene["scene_number"], 1)
        self.assertEqual(scene["description"], "Sir Arthur in his castle with Thomas")
        self.assertEqual(scene["characters"], ["Sir Arthur", "Thomas"])
        self.assertEqual(scene["setting"], "Castle interior")
        self.assertEqual(scene["objects"], ["Armor", "Weapons", "Maps"])
        
        # Verify the mock was called correctly
        mock_client_instance.run_prompt.assert_called_once()

    @patch('support.sceneDescription.GptClient')
    def test_generate_scenes_from_story(self, mock_gpt_client):
        """Test generating multiple scene descriptions from a story."""
        # Configure the mock
        mock_client_instance = mock_gpt_client.return_value
        mock_client_instance.run_prompt.return_value = self.mock_prompt_result
        
        # Call the method
        scenes = self.scene_generator.generate_scenes_from_story(self.story_context, 2, self.characters)
        
        # Verify the result
        self.assertEqual(len(scenes), 2)
        self.assertIn("1", scenes)
        self.assertIn("2", scenes)
        
        # Verify the mock was called twice (once for each scene)
        self.assertEqual(mock_client_instance.run_prompt.call_count, 2)

    def test_convert_message_to_json(self):
        """Test converting a message to JSON."""
        # Call the method
        result = self.scene_generator._convert_message_to_json(self.mock_message)
        
        # Verify the result
        self.assertEqual(result["scene_number"], 1)
        self.assertEqual(result["description"], "Sir Arthur in his castle with Thomas")
        self.assertEqual(result["characters"], ["Sir Arthur", "Thomas"])

    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_save_scene_to_file(self, mock_open):
        """Test saving a scene to a file."""
        # Call the method
        result = self.scene_generator.save_scene_to_file(self.sample_scene_data, "test_scene.json")
        
        # Verify the result
        self.assertTrue(result)
        mock_open.assert_called_once_with("test_scene.json", 'w', encoding='utf-8')
        mock_open().write.assert_called_once()


if __name__ == "__main__":
    unittest.main()