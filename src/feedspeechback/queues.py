"""Temporal task queue names, shared by the scheduling side (API, workflows)
and the polling side (workers). Task queues are created implicitly on first
use, so a mismatched name hangs silently until the activity timeout — always
route through these constants, never a string literal.

Import-light on purpose: this module is imported into the workflow sandbox.
"""

DEFAULT_QUEUE = "default-queue"
TRANSCRIPTION_QUEUE = "transcription-queue"
DIARIZATION_QUEUE = "diarization-queue"
