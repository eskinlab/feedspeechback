# feedspeechback — serverless MVP

AI feedback on recorded speech, as one serverless GPU job:

```
python cli.py  →  Nebius Serverless Job (WhisperX + pyannote)
                        →  Nebius AI Studio LLM  →  report.md in the bucket
```

```
├── pyproject.toml     boto3 for the CLI; heavy job deps in the "job" group
├── uv.lock
├── Dockerfile         CUDA runtime + ffmpeg + uv sync --only-group job
├── cli.py             laptop: submit / status / fetch
│
└── app/               runs inside the container (python -m app.main)
    ├── main.py        entrypoint (argparse)
    ├── pipeline.py    extract -> transcribe -> diarize -> metrics -> evaluate -> report
    ├── config.py      all env-var knobs in one place
    ├── media/
    │   └── extractor.py    any audio/video -> 16 kHz mono WAV (ffmpeg)
    ├── transcription/
    │   └── whisperx.py     WhisperX transcribe + align
    ├── diarization/
    │   └── pyannote.py     speaker diarization (needs HF_TOKEN)
    ├── metrics/
    │   └── analyzer.py     wpm, pauses, talk-time share
    ├── llm/
    │   ├── client.py       Nebius AI Studio call
    │   └── prompts.py      rubrics + prompt template
    └── reporting/
        └── markdown.py     report.md rendering
```

The Temporal-based pipeline lives on `main`.

## Setup (once)

1. Configure the `nebius` CLI; create an Object Storage bucket and S3 keys.
2. Get a Nebius AI Studio API key and an HF token (accept the licenses for
   `pyannote/speaker-diarization-3.1` and `pyannote/segmentation-3.0`).
3. Build and push the image (from WSL or CI):
   `docker build -t <registry>/feedspeechback-job:dev . && docker push <registry>/feedspeechback-job:dev`
4. `cp .env.example .env`, fill it in, load it into your shell.

## Use

```sh
uv sync   # installs boto3 for the CLI (heavy job deps stay in Docker)

uv run cli.py submit talk.wav --scenario interview   # prints <id>
uv run cli.py status <id>                            # until it says done
uv run cli.py fetch <id>                             # -> <id>-report.md
```
