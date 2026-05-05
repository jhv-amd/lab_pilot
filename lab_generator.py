#!/usr/bin/env python3
"""
Lab Generator CLI

Generate complete ML lab kits from a single command.

Usage:
    python lab_generator.py create --topic "Churn Prediction" --course machine_learning \\
        --dataset telco_churn --difficulty intermediate --output ./labs/churn
    python lab_generator.py list --templates
    python lab_generator.py list --datasets
    python lab_generator.py validate ./labs/churn
    python lab_generator.py interactive
"""

import sys
from pathlib import Path

import click
import yaml
from rich.console import Console
from rich.table import Table

console = Console()

CONFIG_DIR = Path(__file__).parent / "config"
DATASETS_DIR = Path(__file__).parent / "datasets"

GENERATOR_MAP = {
    "machine_learning": "classification",
    "regression": "regression",
    "deep_learning": "deep_learning",
    "nlp": "nlp",
    "computer_vision": "computer_vision",
    "time_series": "time_series",
    "classification": "classification",
}


def _load_course_templates() -> dict:
    with open(CONFIG_DIR / "course_templates.yaml") as f:
        return yaml.safe_load(f) or {}


def _load_all_datasets() -> dict:
    datasets = {}
    for yaml_file in DATASETS_DIR.glob("*.yaml"):
        with open(yaml_file) as f:
            datasets.update(yaml.safe_load(f) or {})
    return datasets


def _get_generator(course: str, topic: str, dataset: str, difficulty: str, output: str, exercises_filter=None):
    gen_type = GENERATOR_MAP.get(course.lower(), "classification")

    if gen_type == "classification":
        from generators.classification_generator import ClassificationGenerator
        return ClassificationGenerator(topic, dataset, difficulty, output, course, exercises_filter)
    elif gen_type == "regression":
        from generators.regression_generator import RegressionGenerator
        return RegressionGenerator(topic, dataset, difficulty, output, course, exercises_filter)
    elif gen_type == "deep_learning":
        from generators.deep_learning_generator import DeepLearningGenerator
        return DeepLearningGenerator(topic, dataset, difficulty, output, course, exercises_filter)
    elif gen_type == "nlp":
        from generators.nlp_generator import NLPGenerator
        return NLPGenerator(topic, dataset, difficulty, output, course, exercises_filter)
    elif gen_type == "computer_vision":
        from generators.computer_vision_generator import ComputerVisionGenerator
        return ComputerVisionGenerator(topic, dataset, difficulty, output, course, exercises_filter)
    elif gen_type == "time_series":
        from generators.time_series_generator import TimeSeriesGenerator
        return TimeSeriesGenerator(topic, dataset, difficulty, output, course, exercises_filter)
    else:
        from generators.classification_generator import ClassificationGenerator
        return ClassificationGenerator(topic, dataset, difficulty, output, course, exercises_filter)


# ── CLI group ─────────────────────────────────────────────────────────────────

@click.group()
def cli():
    """AI-powered ML lab kit generator for university courses."""


# ── create ────────────────────────────────────────────────────────────────────

@cli.command()
@click.option("--topic", required=True, help="Lab topic, e.g. 'Customer Churn Prediction'")
@click.option("--course", required=True,
              type=click.Choice(["machine_learning", "regression", "deep_learning",
                                 "nlp", "computer_vision", "time_series", "classification"],
                                case_sensitive=False),
              help="Course type")
@click.option("--dataset", required=True, help="Dataset name (see: lab_generator.py list --datasets)")
@click.option("--difficulty", default="intermediate",
              type=click.Choice(["beginner", "intermediate", "advanced"], case_sensitive=False),
              help="Difficulty level")
@click.option("--output", required=True, help="Output directory for the generated lab")
@click.option("--exercises", default=None,
              help="Comma-separated list of exercise function names to include")
def create(topic, course, dataset, difficulty, output, exercises):
    """Generate a complete lab kit."""
    exercises_filter = [e.strip() for e in exercises.split(",")] if exercises else None

    console.print(f"\n  [bold blue]AI Lab Generator[/bold blue]")
    console.print(f"  Topic:      {topic}")
    console.print(f"  Course:     {course}")
    console.print(f"  Dataset:    {dataset}")
    console.print(f"  Difficulty: {difficulty}")
    console.print(f"  Output:     {output}\n")

    try:
        generator = _get_generator(course, topic, dataset, difficulty, output, exercises_filter)
        summary = generator.generate_all()
    except Exception as e:
        console.print(f"  [red]✗ Generation failed: {e}[/red]")
        raise SystemExit(1)

    console.print()
    for f in summary["files"]:
        console.print(f"  [green]✓[/green] {f}")

    console.print(f"\n  [bold green]Lab ready![/bold green]  {summary['output_dir']}")
    console.print(f"  {summary['exercises']} exercises  ·  {summary['elapsed_seconds']}s\n")


# ── list ──────────────────────────────────────────────────────────────────────

@cli.command("list")
@click.option("--templates", is_flag=True, help="List available course templates")
@click.option("--datasets", is_flag=True, help="List available datasets")
def list_cmd(templates, datasets):
    """List available templates and datasets."""
    if not templates and not datasets:
        console.print("Specify --templates or --datasets")
        return

    if templates:
        courses = _load_course_templates()
        table = Table(title="Available Course Templates", show_lines=True)
        table.add_column("Course", style="cyan")
        table.add_column("Generator")
        table.add_column("Example Topics")
        for name, cfg in courses.items():
            topics = ", ".join(cfg.get("topics", [])[:3])
            table.add_row(name, cfg.get("generator", name), topics)
        console.print(table)

    if datasets:
        all_ds = _load_all_datasets()
        table = Table(title="Available Datasets", show_lines=True)
        table.add_column("Name", style="cyan")
        table.add_column("Type")
        table.add_column("Task")
        table.add_column("Description")
        for ds_name, cfg in all_ds.items():
            table.add_row(
                ds_name,
                cfg.get("type", ""),
                cfg.get("task", ""),
                cfg.get("description", "")[:60],
            )
        console.print(table)


# ── validate ──────────────────────────────────────────────────────────────────

@cli.command()
@click.argument("lab_dir")
def validate(lab_dir):
    """Validate a generated lab kit."""
    from utils.validation import LabValidator
    validator = LabValidator(lab_dir)
    validator.print_report()
    result = validator.validate_lab()
    sys.exit(0 if result["valid"] else 1)


# ── interactive ───────────────────────────────────────────────────────────────

@cli.command()
def interactive():
    """Interactive wizard to generate a lab kit."""
    try:
        import questionary
    except ImportError:
        console.print("[red]questionary not installed. Run: pip install questionary[/red]")
        raise SystemExit(1)

    console.print("\n[bold blue]  AI Lab Generator — Interactive Mode[/bold blue]\n")

    courses = list(_load_course_templates().keys())
    course = questionary.select("Select course:", choices=courses).ask()
    if not course:
        return

    course_cfg = _load_course_templates().get(course, {})
    topics = course_cfg.get("topics", ["Custom Topic"])
    topic = questionary.select("Select topic:", choices=topics + ["Custom..."]).ask()
    if topic == "Custom...":
        topic = questionary.text("Enter your topic:").ask()
    if not topic:
        return

    all_datasets = _load_all_datasets()
    valid_datasets = course_cfg.get("datasets", list(all_datasets.keys()))
    dataset = questionary.select("Select dataset:", choices=valid_datasets).ask()
    if not dataset:
        return

    difficulty = questionary.select(
        "Difficulty level:",
        choices=["beginner", "intermediate", "advanced"],
    ).ask()
    if not difficulty:
        return

    output = questionary.text(
        "Output directory:",
        default=f"./labs/{topic.lower().replace(' ', '_')[:30]}",
    ).ask()
    if not output:
        return

    console.print()
    generator = _get_generator(course, topic, dataset, difficulty, output)
    try:
        summary = generator.generate_all()
    except Exception as e:
        console.print(f"[red]✗ Failed: {e}[/red]")
        raise SystemExit(1)

    console.print()
    for f in summary["files"]:
        console.print(f"  [green]✓[/green] {f}")
    console.print(f"\n  [bold green]Lab ready at: {summary['output_dir']}[/bold green]\n")


# ── add-exercise ──────────────────────────────────────────────────────────────

@cli.command("add-exercise")
@click.option("--lab", required=True, help="Path to existing lab directory")
@click.option("--exercise", required=True, help="Path to a custom exercise YAML spec")
def add_exercise(lab, exercise):
    """Add a custom exercise to an existing lab."""
    import json

    lab_dir = Path(lab)
    exercise_path = Path(exercise)

    if not lab_dir.exists():
        console.print(f"[red]Lab directory not found: {lab_dir}[/red]")
        raise SystemExit(1)
    if not exercise_path.exists():
        console.print(f"[red]Exercise file not found: {exercise_path}[/red]")
        raise SystemExit(1)

    with open(exercise_path) as f:
        ex_spec = yaml.safe_load(f)

    console.print(f"  Adding exercise: {ex_spec.get('title', 'Custom Exercise')}")

    # Update metadata
    meta_file = lab_dir / "metadata.json"
    if meta_file.exists():
        meta = json.loads(meta_file.read_text())
        meta["exercises"].append({
            "name": ex_spec.get("function_name", "custom"),
            "title": ex_spec.get("title", "Custom Exercise"),
            "points": ex_spec.get("points", 10),
        })
        meta_file.write_text(json.dumps(meta, indent=2))

    console.print(f"  [green]✓[/green] Exercise added. Rebuild the notebook manually or re-run `create`.")


if __name__ == "__main__":
    cli()
