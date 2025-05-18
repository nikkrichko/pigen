import sys
import types
import json
import tempfile
import unittest
from unittest.mock import patch, MagicMock

# Stub external modules used in support.functions
openai_stub = types.ModuleType('openai')
openai_stub.Client = object
openai_stub.LengthFinishReasonError = Exception
sys.modules['openai'] = openai_stub

if 'support.logger' in sys.modules:
    logger_stub = sys.modules['support.logger']
else:
    logger_stub = types.ModuleType('support.logger')
    sys.modules['support.logger'] = logger_stub
logger_stub.delog = lambda: (lambda f: f)
logger_stub.Logger = MagicMock

if 'support.decorators' in sys.modules:
    decorators_stub = sys.modules['support.decorators']
else:
    decorators_stub = types.ModuleType('support.decorators')
    sys.modules['support.decorators'] = decorators_stub
decorators_stub.spinner_decorator = lambda f: f
decorators_stub.execution_time_decorator = lambda f: f
decorators_stub.log_function_info_and_debug = lambda logger=None: (lambda f: f)

import support.functions as sf


class IllStoryTests(unittest.TestCase):
    """Tests for the ill_story command and its supporting functions."""

    def setUp(self):
        """Set up test fixtures."""
        self.sample_story = """
        Once upon a time, there was a brave knight named Sir Arthur. 
        He lived in a castle with his loyal squire, Thomas. 
        One day, an evil dragon attacked the nearby village. 
        Sir Arthur mounted his white horse and rode to face the dragon.
        The battle was fierce, but Sir Arthur prevailed and saved the village.
        """
        
        self.mock_client = MagicMock()
        self.model = "test-model"
        
        # Sample validation response
        self.validation_response = {
            "is_story": True,
            "reason": "This is a narrative story with characters and plot.",
            "estimated_scenes": 5
        }
        
        # Sample characters response
        self.characters_response = {
            "Sir Arthur": {
                "physical_appearance": "A brave knight in shining armor",
                "clothing": "Silver armor with a red cape",
                "distinctive_features": "Carries a legendary sword"
            },
            "Thomas": {
                "physical_appearance": "Young squire with brown hair",
                "clothing": "Simple tunic and leather boots",
                "distinctive_features": "Always carries Sir Arthur's shield"
            },
            "Dragon": {
                "physical_appearance": "Large red dragon with scales",
                "clothing": "None",
                "distinctive_features": "Breathes fire and has sharp claws"
            }
        }
        
        # Sample scenes response
        self.scenes_response = [
            {
                "scene_number": 1,
                "description": "Sir Arthur in his castle with Thomas",
                "characters": ["Sir Arthur", "Thomas"],
                "setting": "Castle interior",
                "objects": ["Armor", "Weapons"]
            },
            {
                "scene_number": 2,
                "description": "Dragon attacking the village",
                "characters": ["Dragon"],
                "setting": "Village under attack",
                "objects": ["Burning houses", "Villagers fleeing"]
            },
            {
                "scene_number": 3,
                "description": "Sir Arthur riding to battle",
                "characters": ["Sir Arthur"],
                "setting": "Path to village",
                "objects": ["White horse", "Sword"]
            }
        ]

    @patch('support.functions.validate_story')
    def test_validate_story_success(self, mock_validate):
        """Test successful story validation."""
        mock_validate.return_value = self.validation_response
        
        result = sf.validate_story(self.sample_story, self.mock_client, self.model)
        
        self.assertTrue(result["is_story"])
        self.assertEqual(result["estimated_scenes"], 5)

    @patch('support.functions.extract_characters')
    def test_extract_characters_success(self, mock_extract):
        """Test successful character extraction."""
        mock_extract.return_value = self.characters_response
        
        result = sf.extract_characters(self.sample_story, self.mock_client, self.model)
        
        self.assertEqual(len(result), 3)
        self.assertIn("Sir Arthur", result)
        self.assertIn("Thomas", result)
        self.assertIn("Dragon", result)

    @patch('support.functions.generate_scenes')
    def test_generate_scenes_success(self, mock_generate):
        """Test successful scene generation."""
        mock_generate.return_value = self.scenes_response
        
        result = sf.generate_scenes(
            self.sample_story, 
            3, 
            self.characters_response, 
            self.mock_client, 
            self.model
        )
        
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]["scene_number"], 1)
        self.assertEqual(result[1]["scene_number"], 2)
        self.assertEqual(result[2]["scene_number"], 3)

    def test_create_story_illustration_json(self):
        """Test creation of the final JSON structure."""
        result = sf.create_story_illustration_json(
            self.sample_story,
            self.characters_response,
            self.scenes_response
        )
        
        self.assertIn("story_summary", result)
        self.assertIn("characters", result)
        self.assertIn("scenes", result)
        self.assertIn("metadata", result)
        
        self.assertEqual(result["characters"], self.characters_response)
        self.assertEqual(result["scenes"], self.scenes_response)
        self.assertEqual(result["metadata"]["num_characters"], 3)
        self.assertEqual(result["metadata"]["num_scenes"], 3)

    @patch('support.functions.validate_story')
    @patch('support.functions.extract_characters')
    @patch('support.functions.generate_scenes')
    def test_illustrate_story_success(self, mock_generate, mock_extract, mock_validate):
        """Test successful story illustration end-to-end."""
        mock_validate.return_value = self.validation_response
        mock_extract.return_value = self.characters_response
        mock_generate.return_value = self.scenes_response
        
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = f"{tmpdir}/test_output.json"
            
            result = sf.illustrate_story(
                self.sample_story,
                output_file,
                3,
                self.mock_client,
                self.model
            )
            
            self.assertEqual(result, output_file)
            
            # Verify the file was created and contains the expected data
            with open(output_file, 'r') as f:
                data = json.load(f)
                
            self.assertIn("characters", data)
            self.assertIn("scenes", data)
            self.assertEqual(len(data["characters"]), 3)
            self.assertEqual(len(data["scenes"]), 3)

    @patch('support.functions.validate_story')
    def test_illustrate_story_validation_failure(self, mock_validate):
        """Test story illustration when validation fails."""
        mock_validate.return_value = {
            "is_story": False,
            "reason": "This is technical documentation, not a story.",
            "estimated_scenes": 0
        }
        
        result = sf.illustrate_story(
            "This is a technical manual for a computer program.",
            "output.json",
            3,
            self.mock_client,
            self.model
        )
        
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()