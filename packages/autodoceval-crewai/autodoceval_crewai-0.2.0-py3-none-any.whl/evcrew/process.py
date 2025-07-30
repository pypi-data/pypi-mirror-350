"""Document processing iterators and workflows."""

import json
from collections.abc import Iterator
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Optional

from box import Box

from .utils import write_file

if TYPE_CHECKING:
    from .agents import DocumentEvaluator, DocumentImprover


@dataclass
class IterationData:
    """Data for a single iteration."""
    iteration: int
    content: str
    score: float
    feedback: str
    word_count: int
    improvement_delta: Optional[float] = None
    timestamp: str = field(default_factory=lambda: datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"))


@dataclass
class DocumentIterator:
    """Iterator for document improvement with integrated tracking."""
    
    evaluator: "DocumentEvaluator"
    improver: "DocumentImprover"
    doc_name: str
    doc_path: str
    initial_content: str
    target_score: float = 85
    max_iterations: int = 2
    
    # State fields
    _current_content: str = field(init=False)
    _current_feedback: str = field(default="", init=False)
    _iteration_count: int = field(default=0, init=False)
    _iterations: list[IterationData] = field(default_factory=list, init=False)
    _start_time: datetime = field(default_factory=datetime.utcnow, init=False)
    _launch_id: str = field(init=False)
    
    def __post_init__(self):
        """Initialize iterator state."""
        self._current_content = self.initial_content
        self._launch_id = f"doc-improve-{self.doc_name}-{self._start_time.strftime('%Y%m%d-%H%M%S')}"
        
    def __iter__(self) -> Iterator[IterationData]:
        """Return iterator instance."""
        return self
        
    def __next__(self) -> IterationData:
        """Return iteration data for each improvement step."""
        if self._iteration_count == 0:
            print(f"📊 Evaluating {self.doc_name}... ", end="", flush=True)
            
            score, feedback = self.evaluator.execute(self.initial_content)
            word_count = len(self.initial_content.split())
            
            print(f"{score:.0f}%")
            
            iteration_data = IterationData(
                iteration=0,
                content=self.initial_content,
                score=score,
                feedback=feedback,
                word_count=word_count
            )
            self._iterations.append(iteration_data)
            self._current_feedback = feedback
            self._iteration_count += 1
            
            if score >= self.target_score:
                self._print_final_status("target_met_original")
                raise StopIteration("target_met_original")
                
            return iteration_data
            
        elif self._iteration_count <= self.max_iterations:
            print(f"   → Improving (iteration {self._iteration_count}/{self.max_iterations})... ", end="", flush=True)
                
            improved_content = self.improver.execute(self._current_content, self._current_feedback)
            score, feedback = self.evaluator.execute(improved_content)
            
            prev_score = self._iterations[-1].score
            improvement_delta = score - prev_score
            
            print(f"{score:.0f}% ({improvement_delta:+.0f}%)")
            
            iteration_data = IterationData(
                iteration=self._iteration_count,
                content=improved_content,
                score=score,
                feedback=feedback,
                word_count=len(improved_content.split()),
                improvement_delta=improvement_delta
            )
            
            self._iterations.append(iteration_data)
            self._current_content = improved_content
            self._current_feedback = feedback
            self._iteration_count += 1
            
            if score >= self.target_score:
                self._print_final_status("target_reached")
                raise StopIteration("target_reached")
                
            return iteration_data
            
        else:
            self._print_final_status("max_iterations_reached")
            raise StopIteration("max_iterations_reached")
    
    def _print_final_status(self, status: str) -> None:
        """Print status when iteration completes."""
        icons = {"target_met_original": "✅", "target_reached": "✅", "max_iterations_reached": "⚠️"}
        if icon := icons.get(status):
            print(f"   {icon} Final score: {self.final_score:.0f}% ({status.replace('_', ' ')})")
    
    @property        
    def final_content(self) -> str:
        """Get the final improved content."""
        return self._iterations[-1].content if self._iterations else self.initial_content
    
    @property    
    def final_score(self) -> float:
        """Get the final score."""
        return self._iterations[-1].score if self._iterations else 0.0
    
    @property    
    def total_improvement(self) -> float:
        """Get total improvement from initial to final."""
        if len(self._iterations) > 1:
            return self._iterations[-1].score - self._iterations[0].score
        return 0.0
    
    def save_results(self, output_dir: Path | str, status: str) -> None:
        """Save all results including content in a single comprehensive JSON file."""
        output_dir = Path(output_dir)
        
        data = Box({
            "launch_id": self._launch_id,
            "document": self.doc_name,
            "input_path": self.doc_path,
            "timestamp": self._start_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "duration_seconds": (datetime.utcnow() - self._start_time).total_seconds(),
            "status": status,
            "parameters": {
                "target_score": self.target_score,
                "max_iterations": self.max_iterations
            },
            "summary": {
                "iterations_completed": len(self._iterations) - 1,  # Exclude initial
                "initial_score": self._iterations[0].score if self._iterations else 0,
                "final_score": self.final_score,
                "total_improvement": self.total_improvement,
            },
            "iterations": [
                {
                    "iteration": iter_data.iteration,
                    "type": "initial_evaluation" if iter_data.iteration == 0 else f"improvement_{iter_data.iteration}",
                    "score": iter_data.score,
                    "feedback": iter_data.feedback,
                    "word_count": iter_data.word_count,
                    "improvement_delta": iter_data.improvement_delta,
                    "timestamp": iter_data.timestamp,
                    "content": iter_data.content
                }
                for iter_data in self._iterations
            ]
        })
        
        # Save comprehensive results
        output_path = output_dir / f"{self.doc_name}_results.json"
        write_file(output_path, json.dumps(data.to_dict(), indent=2))