"""
Test script for the CharacterAppearance class.

This script tests the functionality of the CharacterAppearance class
by generating a character appearance description and saving it to a file.
"""

import os
import sys
import json
import types

# Stub dependencies before importing project code
openai_stub = types.ModuleType('openai')
openai_stub.OpenAI = lambda *a, **k: types.SimpleNamespace()
sys.modules['openai'] = openai_stub

gpt_tools_stub = types.ModuleType('reseach.gpt_tools')
class DummyGptClient:
    def run_prompt(self, *a, **k):
        return types.SimpleNamespace(choices=[types.SimpleNamespace(message=types.SimpleNamespace(content="{}"))])
gpt_tools_stub.GptClient = DummyGptClient
sys.modules['reseach.gpt_tools'] = gpt_tools_stub

logger_stub = types.ModuleType('support.logger')
class DummyLogger:
    def __init__(self, *a, **k):
        self.logger = None
    def log(self, *a, **k):
        pass
logger_stub.Logger = DummyLogger
logger_stub.delog = lambda: (lambda f: f)
sys.modules['support.logger'] = logger_stub

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from support.character_description import CharacterAppearance

def test_generate_appearance():
    """Test generating a character appearance description."""
    print("Testing CharacterAppearance.generate_appearance...")
    
    # Initialize the CharacterAppearance class
    character_appearance = CharacterAppearance()
    
    # Generate a character appearance description
    character_name = "Sherlock Holmes"
    appearance = character_appearance.generate_appearance(character_name)
    
    # Check if the appearance was generated successfully
    if "error" in appearance:
        print(f"Error generating appearance: {appearance['error']}")
        return False
    
    print(f"Successfully generated appearance for {character_name}")
    
    # Save the appearance to a file
    output_file = os.path.join("temp", f"{character_name.replace(' ', '_')}_appearance.json")
    success = character_appearance.save_appearance_to_file(appearance, output_file)
    
    if success:
        print(f"Appearance saved to {output_file}")
    else:
        print("Failed to save appearance to file")
        return False
    
    # Print some details from the appearance
    print("\nAppearance details:")
    print(f"Build: {appearance['physical_attributes']['build']}")
    print(f"Hair color: {appearance['physical_attributes']['hair']['color']}")
    print(f"Eye color: {appearance['physical_attributes']['eyes']['color']}")
    print(f"Primary outfit: {appearance['primary_outfit']['garment_type']}")
    
    return True

if __name__ == "__main__":
    # Create the temp directory if it doesn't exist
    os.makedirs("temp", exist_ok=True)
    
    # Run the test
    success = test_generate_appearance()
    
    if success:
        print("\nTest completed successfully!")
    else:
        print("\nTest failed!")