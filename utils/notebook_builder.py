"""Build Jupyter notebooks programmatically."""

from pathlib import Path
from typing import List

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook


class NotebookBuilder:
    """Fluent builder for Jupyter notebooks."""

    def __init__(self):
        self.cells: List[nbformat.NotebookNode] = []

    # ── Cell adders ───────────────────────────────────────────────────────────

    def add_title(self, title: str, description: str, exercises: list, total_points: int) -> "NotebookBuilder":
        table_rows = "\n".join(
            f"| {i+1}. {ex.get('title', f'Exercise {i+1}')} | {ex.get('points', 0)} |"
            for i, ex in enumerate(exercises)
        )
        source = (
            f"# {title}\n\n"
            f"{description}\n\n"
            f"**Instructions:**\n"
            f"- Write your code only between `### START CODE HERE ###` and `### END CODE HERE ###` markers.\n"
            f"- Run the test cell after each exercise to check your work.\n"
            f"- Submit using the final cell when done.\n\n"
            f"| Exercise | Points |\n"
            f"|----------|--------|\n"
            f"{table_rows}\n"
            f"| **Total** | **{total_points}** |"
        )
        self.cells.append(new_markdown_cell(source))
        return self

    def add_setup_cell(self, imports: List[str], data_loading_code: str) -> "NotebookBuilder":
        source = "# Setup — run this cell first\n" + "\n".join(imports) + "\n\n" + data_loading_code
        self.cells.append(new_code_cell(source))
        return self

    def add_exercise(self, exercise: dict, ex_number: int, difficulty: str) -> "NotebookBuilder":
        title = exercise.get("title", f"Exercise {ex_number}")
        instructions = exercise.get("instructions", "")
        starter_code = exercise.get("starter_code", "")
        function_name = exercise.get("function_name", f"exercise_{ex_number}")
        hints = exercise.get("hints", [])

        # Markdown header
        md_source = f"## {title}\n\n{instructions}"
        if hints and difficulty in ("beginner", "intermediate"):
            md_source += "\n\n" + "\n".join(f"> {h}" for h in hints)
        self.cells.append(new_markdown_cell(md_source))

        # Code cell with starter code
        self.cells.append(new_code_cell(starter_code.strip()))

        # Public test cell
        test_source = (
            f"# Test Exercise {ex_number}\n"
            f"from test_cases_public import test_{function_name}\n"
            f"test_{function_name}({function_name})"
        )
        self.cells.append(new_code_cell(test_source))
        return self

    def add_submission_cell(self, assignment_id: str) -> "NotebookBuilder":
        self.cells.append(new_markdown_cell("## Submit Your Assignment\n\nRun the cell below when all exercises are complete."))
        submit_source = (
            "import sys, os\n"
            "sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath('.')), ''))\n"
            "from core.submission import lab_submit\n"
            f"lab_submit.submit_assignment('{assignment_id}', 'assignment.ipynb')"
        )
        self.cells.append(new_code_cell(submit_source))
        return self

    # ── Build ─────────────────────────────────────────────────────────────────

    def build(self, output_path: str | Path) -> None:
        nb = new_notebook(cells=self.cells)
        nb.metadata.kernelspec = {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        }
        nb.metadata.language_info = {"name": "python", "version": "3.10.0"}
        with open(output_path, "w", encoding="utf-8") as f:
            nbformat.write(nb, f)

    def build_solution(self, output_path: str | Path, exercises: list) -> None:
        """Write the reference solution notebook with solution code filled in."""
        sol_cells: List[nbformat.NotebookNode] = []
        # Copy non-exercise cells (title, setup)
        for cell in self.cells[:2]:
            sol_cells.append(cell)

        for i, exercise in enumerate(exercises):
            title = exercise.get("title", f"Exercise {i+1}")
            sol_cells.append(new_markdown_cell(f"## {title} — Solution"))
            solution_code = exercise.get("solution_code", "# No solution provided")
            sol_cells.append(new_code_cell(solution_code.strip()))

        nb = new_notebook(cells=sol_cells)
        nb.metadata.kernelspec = {"display_name": "Python 3", "language": "python", "name": "python3"}
        nb.metadata.language_info = {"name": "python", "version": "3.10.0"}
        with open(output_path, "w", encoding="utf-8") as f:
            nbformat.write(nb, f)
