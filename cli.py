"""Submit a recording to a Nebius serverless job and fetch the report.

    python cli.py submit talk.wav --scenario interview   # prints <id>
    python cli.py status <id>
    python cli.py fetch <id>                             # -> <id>-report.md

Needs: `pip install boto3`, a configured `nebius` CLI, and the env vars
from .env.example (bucket, S3 credentials, image, API keys).
"""

import argparse
import json
import os
import subprocess
import uuid
from pathlib import Path


def env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise SystemExit(f"Set {name} (see .env.example)")
    return value


def s3():
    import boto3

    return boto3.client(
        "s3",
        endpoint_url=os.environ.get(
            "S3_ENDPOINT", "https://storage.eu-north1.nebius.cloud"
        ),
    )


def nebius(*args: str) -> str:
    return subprocess.run(
        ["nebius", *args], capture_output=True, text=True, check=True
    ).stdout


def submit(args: argparse.Namespace) -> None:
    job_id = uuid.uuid4().hex[:12]
    bucket = env("BUCKET")
    key = f"input/{job_id}/{Path(args.input).name}"
    s3().upload_file(args.input, bucket, key)

    env_flags = ["--env", f"NEBIUS_API_KEY={env('NEBIUS_API_KEY')}"]
    for name in ("HF_TOKEN", "WHISPER_MODEL"):  # optional; forwarded when set
        if os.environ.get(name):
            env_flags += ["--env", f"{name}={os.environ[name]}"]

    nebius(
        "ai", "job", "create",
        "--name", f"feedspeechback-{job_id}",
        "--image", env("JOB_IMAGE"),
        "--container-command", "python3",
        f"--args=-m app.main --input /mnt/data/{key} "
        f"--scenario {args.scenario} --output-dir /mnt/data/output/{job_id}",
        "--volume", f"s3://{bucket}:/mnt/data:rw",
        *env_flags,
        "--platform", "gpu-l40s-a",
        "--preset", "1gpu-8vcpu-32gb",
        "--timeout", "1h",
    )
    print(job_id)


def status(args: argparse.Namespace) -> None:
    out = nebius(
        "ai", "job", "get-by-name",
        "--name", f"feedspeechback-{args.id}",
        "--format", "json",
    )
    print(json.loads(out).get("status", {}).get("phase", "unknown"))


def fetch(args: argparse.Namespace) -> None:
    target = f"{args.id}-report.md"
    s3().download_file(env("BUCKET"), f"output/{args.id}/report.md", target)
    print(target)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(required=True)

    p = sub.add_parser("submit", help="upload a video/audio file and launch the job")
    p.add_argument("input", help="media file — video or audio")
    p.add_argument(
        "--scenario", choices=["interview", "job_meeting"], default="interview"
    )
    p.set_defaults(fn=submit)

    p = sub.add_parser("status", help="print the job phase")
    p.add_argument("id")
    p.set_defaults(fn=status)

    p = sub.add_parser("fetch", help="download the finished report")
    p.add_argument("id")
    p.set_defaults(fn=fetch)

    args = parser.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
