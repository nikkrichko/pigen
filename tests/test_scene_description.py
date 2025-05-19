"""
Test script for the SceneGenerator class.

This script tests the functionality of the SceneGenerator class
by generating scene descriptions and saving them to files.
"""

import os
import sys
import json

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from support.sceneDescription import SceneGenerator, SceneDescription

def test_generate_scene():
    """Test generating a single scene description."""
    print("Testing SceneGenerator.generate_scene...")
    
    # Initialize the SceneGenerator class
    scene_generator = SceneGenerator()
    
    # Sample story context
    story_context = """
    Once upon a time, there was a brave knight named Sir Arthur. 
    He lived in a castle with his loyal squire, Thomas. 
    One day, an evil dragon attacked the nearby village. 
    Sir Arthur mounted his white horse and rode to face the dragon.
    The battle was fierce, but Sir Arthur prevailed and saved the village.
    """
    
    # Sample characters
    characters = ["Sir Arthur", "Thomas", "Dragon"]
    
    # Generate a scene description
    scene_number = 1
    scene = scene_generator.generate_scene(scene_number, story_context, characters)
    
    # Check if the scene was generated successfully
    if "error" in scene:
        print(f"Error generating scene: {scene['error']}")
        return False
    
    print(f"Successfully generated scene {scene_number}")
    
    # Save the scene to a file
    os.makedirs("temp", exist_ok=True)
    output_file = os.path.join("temp", f"scene_{scene_number}.json")
    success = scene_generator.save_scene_to_file(scene, output_file)
    
    if success:
        print(f"Scene saved to {output_file}")
    else:
        print("Failed to save scene to file")
        return False
    
    # Print some details from the scene
    print("\nScene details:")
    print(f"Scene number: {scene['scene_number']}")
    print(f"Description: {scene['description'][:100]}...")
    print(f"Characters: {', '.join(scene['characters'])}")
    print(f"Setting: {scene['setting']}")
    
    return True

def test_generate_scenes_from_story():
    """Test generating multiple scene descriptions from a story."""
    print("\nTesting SceneGenerator.generate_scenes_from_story...")
    
    # Initialize the SceneGenerator class
    scene_generator = SceneGenerator()
    
    # Sample story context
    story_context = """
    Once upon a time, there was a brave knight named Sir Arthur. 
    He lived in a castle with his loyal squire, Thomas. 
    One day, an evil dragon attacked the nearby village. 
    Sir Arthur mounted his white horse and rode to face the dragon.
    The battle was fierce, but Sir Arthur prevailed and saved the village.
    The villagers celebrated Sir Arthur's victory with a grand feast.
    """
    
    # Sample characters
    characters = ["Sir Arthur", "Thomas", "Dragon", "Villagers"]
    
    # Generate multiple scene descriptions
    num_scenes = 2
    scenes = scene_generator.generate_scenes_from_story(story_context, num_scenes, characters)
    
    # Check if the scenes were generated successfully
    if not scenes:
        print("Error generating scenes")
        return False
    
    print(f"Successfully generated {len(scenes)} scenes")
    
    # Save the scenes to files
    os.makedirs("temp", exist_ok=True)
    for scene_number, scene in scenes.items():
        output_file = os.path.join("temp", f"scene_{scene_number}.json")
        success = scene_generator.save_scene_to_file(scene, output_file)
        
        if success:
            print(f"Scene {scene_number} saved to {output_file}")
        else:
            print(f"Failed to save scene {scene_number} to file")
            return False
    
    return True

if __name__ == "__main__":
    # Create the temp directory if it doesn't exist
    os.makedirs("temp", exist_ok=True)
    
    # Run the tests
    success1 = test_generate_scene()
    success2 = test_generate_scenes_from_story()
    
    if success1 and success2:
        print("\nAll tests completed successfully!")
    else:
        print("\nSome tests failed!")