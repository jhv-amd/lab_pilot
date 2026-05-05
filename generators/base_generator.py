"""Base class for all topic-specific lab generators."""

import json
import time
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List

import yaml
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from components.dataset_manager import DatasetManager
from components.rubric_generator import RubricGenerator
from utils.code_generator import CodeGenerator
from utils.notebook_builder import NotebookBuilder
from utils.validation import LabValidator

console = Console()

CONFIG_DIR = Path(__file__).parent.parent / "config"


def _load_difficulty(difficulty: str) -> Dict:
    path = CONFIG_DIR / "difficulty_levels.yaml"
    with open(path) as f:
        return yaml.safe_load(f).get(difficulty, {})


class BaseLabGenerator(ABC):
    """Base class all topic generators inherit from."""

    def __init__(
        self,
        topic: str,
        dataset: str,
        difficulty: str,
        output_dir: str | Path,
        course: str = "",
        exercises_filter: List[str] | None = None,
    ):
        self.topic = topic
        self.dataset = dataset
        self.difficulty = difficulty
        self.output_dir = Path(output_dir)
        self.course = course
        self.exercises_filter = exercises_filter
        self.difficulty_cfg = _load_difficulty(difficulty)
        self.assignment_id = self.output_dir.name
        self._exercises: List[Dict] = []

    # ── Abstract interface ────────────────────────────────────────────────────

    @abstractmethod
    def get_exercises(self) -> List[Dict[str, Any]]:
        """Return the ordered list of exercise specification dicts."""

    @abstractmethod
    def get_imports(self) -> List[str]:
        """Return Python import statements for the setup cell."""

    @abstractmethod
    def get_description(self) -> str:
        """Return a short paragraph describing the lab."""

    @abstractmethod
    def get_learning_objectives(self) -> List[str]:
        """Return bullet-point learning objectives."""

    @property
    def task_type(self) -> str:
        return "classification"

    # ── Public generate API ───────────────────────────────────────────────────

    def generate_all(self) -> Dict[str, Any]:
        """Generate the complete lab kit. Returns a summary dict."""
        start = time.time()
        self.output_dir.mkdir(parents=True, exist_ok=True)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            tid = progress.add_task("Generating lab...", total=None)

            exercises = self.get_exercises()
            if self.exercises_filter:
                exercises = [e for e in exercises if e.get("function_name") in self.exercises_filter]
            self._exercises = exercises

            progress.update(tid, description="Building assignment notebook...")
            self.generate_assignment(exercises)

            progress.update(tid, description="Writing public tests...")
            self.generate_public_tests(exercises)

            progress.update(tid, description="Writing hidden tests...")
            self.generate_hidden_tests(exercises)

            progress.update(tid, description="Writing reference solution...")
            self.generate_solution(exercises)

            progress.update(tid, description="Preparing dataset...")
            dataset_meta = self.prepare_dataset()

            progress.update(tid, description="Writing utilities...")
            self.generate_utils()

            progress.update(tid, description="Writing metadata & README...")
            meta = self.generate_metadata(exercises, dataset_meta)
            self.generate_readme(meta)
            self.generate_rubric(exercises)

        elapsed = time.time() - start
        return {
            "exercises": len(exercises),
            "output_dir": str(self.output_dir),
            "elapsed_seconds": round(elapsed, 2),
            "files": self._list_generated_files(),
        }

    def generate_assignment(self, exercises: List[Dict]) -> None:
        total_pts = sum(e.get("points", 0) for e in exercises)
        imports = self.get_imports()
        data_loading = DatasetManager.generate_data_loading_code(self.dataset)

        builder = NotebookBuilder()
        builder.add_title(self.topic, self.get_description(), exercises, total_pts)
        builder.add_setup_cell(imports, data_loading)
        for i, ex in enumerate(exercises, start=1):
            builder.add_exercise(ex, i, self.difficulty)
        builder.add_submission_cell(self.assignment_id)
        builder.build(self.output_dir / "assignment.ipynb")

    def generate_public_tests(self, exercises: List[Dict]) -> None:
        code = CodeGenerator.generate_public_tests_module(exercises, self.task_type)
        (self.output_dir / "test_cases_public.py").write_text(code, encoding="utf-8")

    def generate_hidden_tests(self, exercises: List[Dict]) -> None:
        code = CodeGenerator.generate_hidden_tests_module(exercises, self.difficulty_cfg)
        (self.output_dir / "test_cases_hidden.py").write_text(code, encoding="utf-8")

    def generate_solution(self, exercises: List[Dict]) -> None:
        imports = self.get_imports()
        data_loading = DatasetManager.generate_data_loading_code(self.dataset)
        builder = NotebookBuilder()
        builder.add_title(f"{self.topic} — Reference Solution", self.get_description(), exercises, 0)
        builder.add_setup_cell(imports, data_loading)
        builder.build_solution(self.output_dir / "reference_solution.ipynb", exercises)

    def prepare_dataset(self) -> Dict:
        return DatasetManager.prepare_dataset(self.dataset, self.output_dir)

    def generate_utils(self) -> None:
        code = CodeGenerator.generate_utils_module(self.topic, self.task_type)
        (self.output_dir / "utils.py").write_text(code, encoding="utf-8")

    def generate_metadata(self, exercises: List[Dict], dataset_meta: Dict) -> Dict:
        total_pts = sum(e.get("points", 0) for e in exercises)
        meta = {
            "assignment_id": self.assignment_id,
            "topic": self.topic,
            "course": self.course,
            "dataset": self.dataset,
            "difficulty": self.difficulty,
            "total_points": total_pts,
            "exercises": [
                {"name": e.get("function_name"), "title": e.get("title"), "points": e.get("points", 0)}
                for e in exercises
            ],
            "dataset_meta": dataset_meta,
            "generator_version": "1.0.0",
        }
        (self.output_dir / "metadata.json").write_text(json.dumps(meta, indent=2))
        return meta

    def generate_readme(self, meta: Dict) -> None:
        total_pts = meta.get("total_points", 0)
        rows = "\n".join(
            f"| {e['title']} | {e['points']} |"
            for e in meta.get("exercises", [])
        )
        objectives = "\n".join(f"- {o}" for o in self.get_learning_objectives())
        content = (
            f"# {self.topic}\n\n"
            f"**Course:** {self.course}  \n"
            f"**Difficulty:** {self.difficulty}  \n"
            f"**Total Points:** {total_pts}\n\n"
            f"## Learning Objectives\n\n{objectives}\n\n"
            f"## Getting Started\n\n"
            f"```bash\njupyter lab assignment.ipynb\n```\n\n"
            f"## Exercises\n\n"
            f"| Exercise | Points |\n|----------|--------|\n{rows}\n"
            f"| **Total** | **{total_pts}** |\n\n"
            f"## Submission\n\nRun the last cell in the notebook.\n\n"
            f"## Dataset\n\n{meta.get('dataset_meta', {}).get('description', self.dataset)}\n"
        )
        (self.output_dir / "README.md").write_text(content, encoding="utf-8")

    def generate_rubric(self, exercises: List[Dict]) -> None:
        rubric = RubricGenerator.generate(exercises, self.difficulty)
        md = RubricGenerator.to_markdown(rubric)
        (self.output_dir / "RUBRIC.md").write_text(md, encoding="utf-8")

    def _list_generated_files(self) -> List[str]:
        return [str(p.relative_to(self.output_dir)) for p in sorted(self.output_dir.rglob("*")) if p.is_file()]
