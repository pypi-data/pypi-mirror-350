# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Environment Setup

```bash
# Create and activate a Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package in development mode
uv pip install -e .

# Set your OpenAI API key
export OPENAI_API_KEY=your_api_key_here
```

### Development Commands

```bash
# Run linting checks
ruff check .

# Run formatting
ruff format .

# Build the package
python -m build

# Run Just workflows
just evaluate-all
just max_iterations=3 all
```

## Architecture Overview

AutoDocEval is a document evaluation and improvement system using CrewAI agents with persistent memory capabilities.

### Core Components

1. **Agent System**: Two main agent types handle document processing:

   - `DocumentEvaluator`: Assesses document clarity and provides feedback (implemented in `evcrew/agents/evaluator.py`)
   - `DocumentImprover`: Revises documents based on evaluation feedback (implemented in `evcrew/agents/improver.py`)

2. **Memory System**: CrewAI-based persistent memory allows agents to:

   - Remember previous document evaluations and improvements
   - Learn from past experiences for more consistent results
   - Recognize patterns across multiple documents
   - Memory IDs can be customized to control context sharing

3. **Core Functions**: The main API is exposed in `evcrew/core.py`:

   - `evaluate_document()`: Analyzes document quality and provides a score and feedback
   - `improve_document()`: Generates improved content based on feedback
   - `auto_improve_document()`: Runs an iterative improvement loop until target quality or iteration limit

4. **Workflow System**: Just is used for defining document processing workflows:
   - All workflow commands and configuration in `Justfile`
   - Commands for document evaluation and improvement

### Data Flow

1. Documents are read from the filesystem (typically from `docs/input/`)
2. Documents are evaluated by the `DocumentEvaluator` agent
3. Feedback is used by the `DocumentImprover` agent to create improved versions
4. Results are written to `docs/output/{document_name}/` with appropriate metadata
5. For auto-improvement, this cycle repeats until quality target or iteration limit is reached

### Agent Implementation

The agents are implemented with CrewAI's agent framework, which handles:

- Agent initialization with roles, goals, and backstories
- Memory persistence and retrieval
- Task execution and completion

Each agent uses the OpenAI GPT-4 model by default and includes persistent memory capabilities for improved performance over time.

### instructions

- If there is comment in the code, make sure it is inline, and goes after code
- Line length is 170
- If whole expression can sit in single string, do not split it into multiline one.
- Use one liners for all docstrings
- Remove multi line comments in the code, if they are needed, create function
- Add type annotations
- Be consice and refactor code
- Update README.md in each commit
- Use Just https://just.systems/ as command runner
- use ruff as linter
- use uv instaead pip or twine
- uses Miller https://miller.readthedocs.io/en/6.13.0/
- each function and module and file should have 1-line docstring
- used functional programming style where possible
- avoid one-line functions
- commit after each change
- update documentation when commit
- always use virtualenv
- do not use fallbacks
- do not support backward compatibility
- use short and consice function and method names
- avoid redefinitions
- promts max lenghs is 100
- tests should be located within respectful moodule
- when writing python or justfile code, be pythonic
