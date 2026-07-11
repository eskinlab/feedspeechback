# feedspeechback

AI feedback on recorded speech. Upload an interview or job-meeting recording,
get a scored evaluation report. Built on [Temporal](https://temporal.io/) —
the pipeline (transcribe ∥ diarize → align → evaluate → report) runs as a
durable workflow across dedicated workers.

> Early stage: the pipeline wiring is real, the ML steps are stubs.

## Run

```sh
cp .env.example .env   # then edit the placeholder values
docker compose up --build
```

| Service | URL |
|---|---|
| API | http://localhost:8001 |
| Temporal UI | http://localhost:8081 |

## API

```sh
# submit a recording for a scenario (interview or job-meeting)
curl -X POST localhost:8001/interview \
  -H "Content-Type: application/json" \
  -d '{"audio_path": "meeting.wav"}'
# -> {"workflow_id": "interview-meeting.wav"}

# poll for the result
curl localhost:8001/interview/interview-meeting.wav
# -> {"status": "running"} ... then {"status": "completed", "result": {...}}
```

## Layout

```
src/feedspeechback/
├── api/         FastAPI — HTTP surface
├── workflows/   Temporal workflows (orchestration only)
├── activities/  Temporal activities — thin, import-light adapters
├── contracts/   Pydantic models crossing the workflow↔activity wire
├── services/    business logic, framework-free (swappable providers)
└── workers/     process entrypoints: default, transcription, diarization
```

Dependencies point one way: `workers/api → workflows → activities → services → contracts`.

## Development

```sh
uv sync --all-groups   # install incl. dev tools
uv run pytest          # first run downloads the Temporal test server
uv run ruff check .
uv run ruff format .
```

Configuration is via environment variables — see [.env.example](.env.example).
