"""Validate generated lab kits for correctness and completeness."""

import ast
import json
from pathlib import Path
from typing import Dict, List


REQUIRED_FILES = [
    "assignment.ipynb",
    "test_cases_public.py",
    "test_cases_hidden.py",
    "reference_solution.ipynb",
    "utils.py",
    "metadata.json",
    "README.md",
]

REQUIRED_DATA_FILES = ["data/train.csv", "data/test.csv"]


class LabValidator:
    """Validate a generated lab kit directory."""

    def __init__(self, lab_dir: str | Path):
        self.lab_dir = Path(lab_dir)
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate_lab(self) -> Dict:
        self.errors = []
        self.warnings = []

        self._check_required_files()
        self._check_data_files()
        self._check_notebook_valid("assignment.ipynb")
        self._check_notebook_valid("reference_solution.ipynb")
        self._check_python_syntax("test_cases_public.py")
        self._check_python_syntax("test_cases_hidden.py")
        self._check_python_syntax("utils.py")
        self._check_metadata()
        self._check_start_end_markers()

        return {
            "valid": len(self.errors) == 0,
            "errors": self.errors,
            "warnings": self.warnings,
        }

    def _check_required_files(self):
        for fname in REQUIRED_FILES:
            if not (self.lab_dir / fname).exists():
                self.errors.append(f"Missing required file: {fname}")

    def _check_data_files(self):
        for fname in REQUIRED_DATA_FILES:
            if not (self.lab_dir / fname).exists():
                self.warnings.append(f"Data file not found (run generate_data.py): {fname}")

    def _check_notebook_valid(self, fname: str):
        path = self.lab_dir / fname
        if not path.exists():
            return
        try:
            import nbformat
            nbformat.read(str(path), as_version=4)
        except Exception as e:
            self.errors.append(f"{fname} is not a valid notebook: {e}")

    def _check_python_syntax(self, fname: str):
        path = self.lab_dir / fname
        if not path.exists():
            return
        try:
            ast.parse(path.read_text(encoding="utf-8"))
        except SyntaxError as e:
            self.errors.append(f"Syntax error in {fname}: {e}")

    def _check_metadata(self):
        meta_path = self.lab_dir / "metadata.json"
        if not meta_path.exists():
            return
        try:
            meta = json.loads(meta_path.read_text())
            required_keys = {"assignment_id", "topic", "difficulty", "total_points"}
            missing = required_keys - set(meta.keys())
            if missing:
                self.warnings.append(f"metadata.json missing keys: {missing}")
        except json.JSONDecodeError as e:
            self.errors.append(f"metadata.json is invalid JSON: {e}")

    def _check_start_end_markers(self):
        nb_path = self.lab_dir / "assignment.ipynb"
        if not nb_path.exists():
            return
        import nbformat
        try:
            nb = nbformat.read(str(nb_path), as_version=4)
            start_count = sum(
                1 for c in nb.cells
                if c.cell_type == "code" and "### START CODE HERE ###" in c.source
            )
            if start_count == 0:
                self.warnings.append("No START CODE HERE markers found in assignment.ipynb")
        except Exception:
            pass

    def print_report(self) -> None:
        result = self.validate_lab()
        from rich.console import Console
        from rich.table import Table

        console = Console()
        status = "[green]VALID[/green]" if result["valid"] else "[red]INVALID[/red]"
        console.print(f"\n  Lab validation: {status}\n")

        if result["errors"]:
            console.print("  [red]Errors:[/red]")
            for e in result["errors"]:
                console.print(f"    [red]✗[/red] {e}")

        if result["warnings"]:
            console.print("  [yellow]Warnings:[/yellow]")
            for w in result["warnings"]:
                console.print(f"    [yellow]![/yellow] {w}")

        if not result["errors"] and not result["warnings"]:
            console.print("  [green]✓[/green] All checks passed")
