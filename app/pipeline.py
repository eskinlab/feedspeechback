"""The pipeline: extract -> transcribe -> diarize -> metrics -> evaluate -> report."""

import shutil
import tempfile
from pathlib import Path

from app import config
from app.diarization import pyannote
from app.llm import client
from app.media import extractor
from app.metrics import analyzer
from app.reporting import markdown
from app.transcription import whisperx


def run(media_path: str, scenario: str, output_dir: str) -> Path:
    audio_path = extractor.extract_audio(media_path)
    result = whisperx.transcribe(audio_path)
    if config.HF_TOKEN:
        result = pyannote.diarize(audio_path, result)

    metrics = analyzer.analyze(result["segments"])
    transcript = " ".join(seg["text"].strip() for seg in result["segments"])
    evaluation = client.evaluate(transcript, scenario, metrics)
    report = markdown.render(result, evaluation, metrics, scenario)

    # Write locally first, then move into the bucket mount — no partial files.
    with tempfile.NamedTemporaryFile(
        "w", suffix=".md", delete=False, encoding="utf-8"
    ) as tmp:
        tmp.write(report)
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    report_path = out_dir / "report.md"
    shutil.move(tmp.name, report_path)
    return report_path
