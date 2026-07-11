from pathlib import Path

from temporalio import activity

from feedspeechback.contracts.evaluation import EvaluationResult
from feedspeechback.contracts.report import Report

REPORTS_DIR = Path("reports")


@activity.defn
async def generate_report(evaluation: EvaluationResult) -> Report:
    activity.logger.info(f"Generating report for scenario={evaluation.scenario}")

    # TODO: render a Jinja2 HTML template from `evaluation` (score, per-criterion
    # breakdown, transcript excerpts), then convert that HTML to PDF with
    # WeasyPrint. Write both files under REPORTS_DIR.

    return Report(
        evaluation=evaluation,
        html_path=str(REPORTS_DIR / f"{evaluation.scenario}-report.html"),
        pdf_path=str(REPORTS_DIR / f"{evaluation.scenario}-report.pdf"),
    )
