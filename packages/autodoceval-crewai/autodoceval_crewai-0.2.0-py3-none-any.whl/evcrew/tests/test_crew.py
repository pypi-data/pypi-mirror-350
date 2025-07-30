#!/usr/bin/env python3
"""Test the DocumentCrew multi-agent workflow."""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from evcrew import DocumentCrew


def test_crew_workflow():
    """Test the evaluate_and_improve crew workflow."""
    # Read the bad README file
    bad_readme = (project_root / "docs" / "input" / "bad_readme.md").read_text()

    # Create crew
    crew = DocumentCrew()

    # Run evaluate and improve workflow
    print("Running crew workflow on bad README...")
    improved_content, score, feedback = crew.evaluate_and_improve(bad_readme)

    print(f"\nOriginal score: {score:.1f}%")
    print(f"Feedback: {feedback}\n")
    print("Improved content:")
    print("-" * 80)
    print(improved_content)
    print("-" * 80)

    # Basic assertions
    assert score <= 50, f"Bad README should have low score, got {score}"
    assert len(improved_content) > len(bad_readme), "Improved content should be longer"
    assert improved_content != bad_readme, "Content should be different after improvement"

    print("\n✅ Crew workflow test passed!")


if __name__ == "__main__":
    # Ensure we have the OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable not set")
        sys.exit(1)

    test_crew_workflow()
