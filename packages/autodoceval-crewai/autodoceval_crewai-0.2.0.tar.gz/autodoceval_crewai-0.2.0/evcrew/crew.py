"""Crew-based workflows for document evaluation and improvement."""

from pathlib import Path

from crewai import Crew, Process

from .agents import DocumentEvaluator, DocumentImprover
from .process import DocumentIterator
from .utils import write_file

__all__ = ["DocumentCrew"]


class DocumentCrew:
    """Crew for multi-agent document workflows."""

    def __init__(self, target_score: float = 85, max_iterations: int = 2, evaluator_extra_prompt: str = "", improver_extra_prompt: str = ""):
        self.evaluator = DocumentEvaluator(extra_prompt=evaluator_extra_prompt)
        self.improver = DocumentImprover(extra_prompt=improver_extra_prompt)
        self.target_score = target_score
        self.max_iterations = max_iterations
        self.crew = Crew(
            agents=[self.evaluator.agent, self.improver.agent],
            tasks=[],  # Tasks will be set before kickoff
            process=Process.sequential,
            memory=True,
            embedder={"provider": "openai", "config": {"model": "text-embedding-3-small"}},
            verbose=False,
        )

    def evaluate_one(self, content: str) -> tuple[float, str]:
        """Evaluate a document and return (score, feedback)."""
        return self.evaluator.execute(content)

    def improve_one(self, content: str, feedback: str) -> str:
        """Improve a document based on feedback and return improved content."""
        return self.improver.execute(content, feedback)

    def evaluate_and_improve_one(self, content: str, doc_name: str = "document") -> tuple[str, float, str]:
        """Evaluate and improve a document in one workflow returning (improved_content, score, feedback)."""
        eval_task = self.evaluator.create_task(content, doc_name=doc_name)
        improve_task = self.improver.create_task(content, doc_name=doc_name)
        improve_task.context = [eval_task]

        self.crew.tasks = [eval_task, improve_task]
        result = self.crew.kickoff()

        eval_result = result.tasks_output[0].pydantic
        improve_result = result.tasks_output[1].pydantic

        return improve_result.improved_content, eval_result.score, eval_result.feedback

    def auto_improve_one(self, content: str, output_dir: Path | str, doc_name: str = "document", doc_path: str = "unknown") -> DocumentIterator:
        """Auto-improve document until target score or max iterations reached, returns DocumentIterator with all data."""
        iterator = DocumentIterator(self.evaluator, self.improver, doc_name, doc_path, content, self.target_score, self.max_iterations)

        status = "unknown"
        try:
            for _ in iterator:  # Iterator handles its own printing
                pass

        except StopIteration as e:
            status = str(e)

        output_dir = Path(output_dir)
        iterator.save_results(output_dir, status)
        write_file(output_dir / f"{doc_name}_final.md", iterator.final_content)

        return iterator
