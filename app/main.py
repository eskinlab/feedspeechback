"""Job entrypoint — what the container runs inside Nebius Serverless AI.

    python3 -m app.main --input /mnt/data/input/<id>/talk.mp4 \
        --scenario interview --output-dir /mnt/data/output/<id>
"""

import argparse

from app import pipeline
from app.llm.prompts import RUBRICS


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input", required=True, help="media file — video or audio; audio is extracted"
    )
    parser.add_argument("--scenario", choices=sorted(RUBRICS), default="interview")
    parser.add_argument("--output-dir", default="/mnt/data/output")
    args = parser.parse_args()

    print(pipeline.run(args.input, args.scenario, args.output_dir))


if __name__ == "__main__":
    main()
