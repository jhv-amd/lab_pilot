"""Auto-generate grading rubrics from exercise specifications."""

import json
from typing import Any, Dict, List


class RubricGenerator:
    """Generate grading rubrics from exercise definitions."""

    @staticmethod
    def generate(exercises: List[Dict[str, Any]], difficulty: str) -> Dict[str, Any]:
        total = sum(ex.get("points", 0) for ex in exercises)
        items = []
        for ex in exercises:
            pts = ex.get("points", 0)
            fn = ex.get("function_name", "unknown")
            items.append({
                "exercise": ex.get("title", fn),
                "function": fn,
                "max_points": pts,
                "grading_criteria": _build_criteria(ex, difficulty),
                "partial_credit": _partial_credit(pts),
            })
        return {
            "total_points": total,
            "difficulty": difficulty,
            "items": items,
            "late_penalty": "10% per day",
            "academic_integrity_note": (
                "Solutions must be the student's own work. "
                "Sharing solutions is a violation of academic integrity policy."
            ),
        }

    @staticmethod
    def to_markdown(rubric: Dict[str, Any]) -> str:
        lines = [
            "# Grading Rubric",
            "",
            f"**Total Points:** {rubric['total_points']}  ",
            f"**Difficulty:** {rubric['difficulty']}",
            "",
            "---",
            "",
        ]
        for item in rubric["items"]:
            lines += [
                f"## {item['exercise']} ({item['max_points']} pts)",
                "",
                "| Criteria | Points |",
                "|----------|--------|",
            ]
            for criterion in item["grading_criteria"]:
                lines.append(f"| {criterion['description']} | {criterion['points']} |")
            lines += ["", "**Partial Credit:**"]
            for pc in item["partial_credit"]:
                lines.append(f"- {pc['condition']}: {pc['points']} pts")
            lines.append("")
        lines += [
            "---",
            "",
            f"*{rubric['academic_integrity_note']}*",
        ]
        return "\n".join(lines)


def _build_criteria(ex: Dict, difficulty: str) -> List[Dict]:
    pts = ex.get("points", 10)
    fn = ex.get("function_name", "exercise")
    return [
        {"description": f"`{fn}` is defined and callable", "points": round(pts * 0.1)},
        {"description": "Returns correct type/structure", "points": round(pts * 0.2)},
        {"description": "All hidden tests pass", "points": round(pts * 0.5)},
        {"description": "Code is clean and follows PEP 8", "points": round(pts * 0.2)},
    ]


def _partial_credit(max_pts: int) -> List[Dict]:
    return [
        {"condition": "Function defined but wrong output", "points": max(1, max_pts // 5)},
        {"condition": "Correct approach but minor bug", "points": max(1, max_pts // 2)},
        {"condition": "Passes public but not hidden tests", "points": max(1, max_pts * 2 // 3)},
    ]
