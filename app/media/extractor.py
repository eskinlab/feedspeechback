"""Normalize any input media (audio or video) to 16 kHz mono WAV via ffmpeg."""

import subprocess
import tempfile
from pathlib import Path


def extract_audio(media_path: str) -> str:
    src = Path(media_path)
    if not src.exists():
        raise SystemExit(f"Input file not found: {media_path}")

    out = Path(tempfile.mkdtemp()) / (src.stem + ".wav")
    proc = subprocess.run(
        ["ffmpeg", "-y", "-i", str(src), "-vn", "-ac", "1", "-ar", "16000", str(out)],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise SystemExit(
            f"ffmpeg failed on {media_path} "
            f"(exit {proc.returncode}):\n{proc.stderr.strip()[-500:]}"
        )
    return str(out)
