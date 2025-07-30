# AutoDocEval with CrewAI

Document evaluation and improvement using CrewAI agents with persistent memory capabilities.

## What is CrewAI?

[CrewAI](https://github.com/crewai/crewai) is a framework for orchestrating role-playing autonomous AI agents. In AutoDocEval, we use CrewAI to create specialized agents for document evaluation and improvement, leveraging their collaborative capabilities for more effective documentation enhancement.

## Installation

```bash
# Clone the repository
git clone https://github.com/krybc/autodoceval-crewai.git
cd autodoceval-crewai

# Create and activate virtual environment (requires Python 3.10+)
python3.12 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package in development mode
uv pip install -e .
```

Set your OpenAI API key:

```bash
export OPENAI_API_KEY=your_api_key_here
```

## Usage

### Using Just Commands

All document processing is handled through Just commands:

```bash
# Install just (if not already installed)
brew install just  # macOS
# or: cargo install just

# Auto-improve all documents in docs/input/
just all

# Just evaluate all documents without improvement
just evaluate-all

# Evaluate single document
just evaluate-one myfile

# Evaluate and improve all documents
just evaluate-and-improve-all

# Evaluate and improve single document
just evaluate-and-improve-one myfile

# Auto-improve single document from custom path
just auto-improve-one path/to/doc.md mydoc

# Clean outputs
just clean


# Show all available commands
just
```

Place your markdown documents in `docs/input/` and the workflow will:
- **evaluate-all/evaluate-one**: Evaluate documents and save scores/feedback
- **evaluate-and-improve-all/evaluate-and-improve-one**: Evaluate and improve in one workflow
- **auto-improve-all/auto-improve-one**: Iteratively improve until target score reached
- Outputs saved to `docs/output/{name}/` as JSON files with all metadata and content

### Python API

For programmatic usage:

```python
from evcrew import DocumentCrew

# Create crew instance with defaults (target_score=85, max_iterations=2)
crew = DocumentCrew()
# Or with custom parameters
crew = DocumentCrew(target_score=90, max_iterations=5)

# Evaluate a document
score, feedback = crew.evaluate_one("Document content here...")
print(f"Score: {score:.0f}%, Feedback: {feedback}")

# Improve a document
improved_content = crew.improve_one("Document content...", "Feedback about issues...")

# Evaluate and improve in one workflow
improved_content, score, feedback = crew.evaluate_and_improve_one("Document content...")

# Auto-improve with iteration tracking
from pathlib import Path
iterator = crew.auto_improve_one("Document content...", "docs/output/example")
print(f"Final score: {iterator.final_score:.0f}%, Total improvement: {iterator.total_improvement:.0f}%")
```

## Architecture

AutoDocEval uses CrewAI agents to evaluate and improve documentation:

### Iteration Tracking

The system includes a comprehensive iteration tracking system that captures:
- Document metadata (ID, path, timestamps)
- Quality metrics for each iteration (scores, feedback)
- Improvement deltas between iterations
- File paths for each improved version
- Total duration and iteration count

Tracking data is saved as JSON files for analysis and monitoring. The system uses 
python-box for cleaner dictionary access with dot notation.

### Agents

- **DocumentEvaluator**: Analyzes document clarity, completeness, and coherence
  - Returns scores on a 0-100 scale
  - Provides specific, actionable feedback
  - Maintains consistency across evaluations

- **DocumentImprover**: Revises documents based on evaluation feedback
  - Applies feedback to enhance clarity
  - Preserves document intent and technical accuracy
  - Learns from previous improvements

### Agent System

The system uses specialized agents for document processing:

- **BaseAgent**: Abstract base class with common functionality
  - `create_task()`: Abstract method for creating agent-specific tasks
  - `save_results()`: Generic method for saving results with metadata
- **DocumentEvaluator**: Analyzes document clarity and provides structured feedback
  - Implements `create_task()` for evaluation tasks
  - `save_results()`: Saves evaluation scores and feedback using base class functionality
- **DocumentImprover**: Transforms documents based on evaluation feedback
  - Implements `create_task()` for improvement tasks
  - `save_results()`: Saves improved documents to disk
- **DocumentCrew**: Orchestrates multi-agent workflows
  - `evaluate_one()`: Evaluate single document
  - `improve_one()`: Improve single document with feedback
  - `evaluate_and_improve_one()`: Combined evaluation and improvement
  - `auto_improve_one()`: Iterative improvement until target score reached
- **DocumentIterator**: Handles iteration state and progress tracking
- Agents handle their own file I/O for better encapsulation

### Workflow System

The Just command runner handles:
- Batch processing of multiple documents
- Iterative improvement loops
- Progress tracking and reporting
- Automatic file organization
- Additional development commands (test, lint, format)

## Configuration

Default values:
- `target_score`: 85 (default parameter of DocumentCrew)
- `max_iterations`: 2 (default parameter of DocumentCrew)

To use different values, instantiate DocumentCrew with desired parameters in Python code:

```python
crew = DocumentCrew(target_score=90, max_iterations=5)
```

## Project Structure

```
autodoceval-crewai/
├── evcrew/              # Core package
│   ├── agents/          # Agent implementations
│   │   ├── base.py      # Base agent class
│   │   ├── evaluator.py # Document evaluator
│   │   ├── improver.py  # Document improver
│   │   └── prompts/     # Agent prompt templates
│   │       ├── evaluator.md     # Evaluation prompt
│   │       ├── improver.md      # Improvement prompt
│   │       └── improver_task.md # Improvement task prompt
│   ├── tests/           # Unit tests
│   │   ├── test_crew.py     # Crew tests
│   │   └── test_evaluator.py # Evaluator tests
│   ├── __init__.py      # Package exports
│   ├── crew.py          # DocumentCrew workflow class
│   ├── tracking.py      # Iteration tracking system
│   └── utils.py         # File operation utilities
├── docs/                # Document storage
│   ├── input/           # Input documents
│   └── output/          # Evaluation results
├── config/              # Configuration files
│   └── CLAUDE.md        # AI assistant instructions
├── Justfile             # Workflow definitions
├── pyproject.toml       # Package metadata
└── README.md            # This file
```

## Requirements

- Python 3.10+ (3.12 recommended)
- OpenAI API key
- Dependencies installed via `uv pip install -e .`

## License

MIT