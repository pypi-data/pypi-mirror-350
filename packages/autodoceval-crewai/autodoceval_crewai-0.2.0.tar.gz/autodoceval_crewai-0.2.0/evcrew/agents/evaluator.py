import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from box import Box
from crewai import Task

from evcrew.utils import write_file

from .base import BaseAgent, EvaluationResult


class DocumentEvaluator(BaseAgent):
    """Document evaluation agent using CrewAI."""

    def __init__(self, extra_prompt: str = ""):
        super().__init__(
            role="Document Quality Evaluator",
            goal="Evaluate document clarity and provide constructive feedback",
            backstory="You are an expert technical writer with years of experience evaluating documentation quality",
            extra_prompt=extra_prompt,
        )

    def create_task(self, content: str, **kwargs) -> Task:
        """Create evaluation task for the given content."""
        doc_name = kwargs.get("doc_name", "document")
        prompt_path = self.prompts_dir / "evaluator.md"
        base_description = prompt_path.read_text().format(content=content)
        
        # Append extra prompt if provided
        if self.extra_prompt:
            description = f"{base_description}\n\n{self.extra_prompt}"
        else:
            description = base_description
            
        return Task(
            description=description,
            expected_output="Document evaluation with score and feedback",
            agent=self.agent,
            output_pydantic=EvaluationResult,
        )

    def execute(self, content: str) -> tuple[float, str]:
        """Execute document evaluation and return a score and feedback string."""
        prompt_path = self.prompts_dir / "evaluator.md"
        prompt_template = prompt_path.read_text()
        base_description = prompt_template.format(content=content)
        
        # Append extra prompt if provided
        if self.extra_prompt:
            task_description = f"{base_description}\n\n{self.extra_prompt}"
        else:
            task_description = base_description

        result = super().execute(task_description, EvaluationResult)
        return result.score, result.feedback.strip()

    def save(self, score: float, feedback: str, content: str, output_dir: str | Path, doc_name: str, input_path: Optional[str] = None) -> None:
        """Save evaluation results in a comprehensive JSON file."""
        output_dir = Path(output_dir)
        
        # Create evaluation data structure
        data = Box({
            "document": doc_name,
            "input_path": str(input_path) if input_path else None,
            "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "evaluation": {
                "score": score,
                "feedback": feedback,
                "word_count": len(content.split())
            },
            "content": content
        })
        
        # Save as JSON
        output_path = output_dir / f"{doc_name}_evaluation.json"
        write_file(output_path, json.dumps(data.to_dict(), indent=2))
