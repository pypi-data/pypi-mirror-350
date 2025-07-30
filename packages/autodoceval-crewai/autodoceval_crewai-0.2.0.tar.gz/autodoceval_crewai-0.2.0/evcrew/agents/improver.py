import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from box import Box
from crewai import Task

from evcrew.utils import write_file

from .base import BaseAgent, ImprovementResult


class DocumentImprover(BaseAgent):
    """Document improvement agent using CrewAI."""

    def __init__(self, extra_prompt: str = ""):
        super().__init__(
            role="Documentation Improver",
            goal="Transform documents into clear, comprehensive, and well-structured content",
            backstory="You are a senior technical writer who specializes in improving documentation",
            extra_prompt=extra_prompt,
        )

    def create_task(self, content: str, **kwargs) -> Task:
        """Create improvement task for the given content."""
        doc_name = kwargs.get("doc_name", "document")
        prompt_path = self.prompts_dir / "improver_task.md"
        base_description = prompt_path.read_text().format(content=content)
        
        # Append extra prompt if provided
        if self.extra_prompt:
            description = f"{base_description}\n\n{self.extra_prompt}"
        else:
            description = base_description
            
        return Task(
            description=description, expected_output="Improved version of the document", agent=self.agent, output_pydantic=ImprovementResult
        )

    def execute(self, content: str, feedback: str) -> str:
        """Execute document improvement based on feedback."""
        prompt_path = self.prompts_dir / "improver.md"
        prompt_template = prompt_path.read_text()
        base_description = prompt_template.format(content=content, feedback=feedback)
        
        # Append extra prompt if provided
        if self.extra_prompt:
            task_description = f"{base_description}\n\n{self.extra_prompt}"
        else:
            task_description = base_description

        result = super().execute(task_description, ImprovementResult)
        return result.improved_content

    def save(self, original_content: str, improved_content: str, score: float, feedback: str, 
             output_dir: str | Path, doc_name: str, input_path: Optional[str] = None) -> None:
        """Save improvement results in a comprehensive JSON file and markdown file."""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create improvement data structure
        data = Box({
            "document": doc_name,
            "input_path": str(input_path) if input_path else None,
            "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "method": "evaluate_and_improve",
            "original": {
                "content": original_content,
                "word_count": len(original_content.split())
            },
            "improved": {
                "score": score,
                "feedback": feedback,
                "word_count": len(improved_content.split()),
                "content": improved_content
            }
        })
        
        # Save comprehensive results
        output_path = output_dir / f"{doc_name}_improved.json"
        write_file(output_path, json.dumps(data.to_dict(), indent=2))
        
        # Save final improved version as .md file
        write_file(output_dir / f"{doc_name}_improved.md", improved_content)
