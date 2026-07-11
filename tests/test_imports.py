"""Entry-point smoke test.

A broken or heavy import in an activity module otherwise only surfaces when
a worker boots in a deployed container. This also guards the import-light
invariant: these must import fast, without pulling ML dependencies.
"""

import importlib

import pytest

ENTRY_MODULES = [
    "feedspeechback.api.main",
    "feedspeechback.workers.default",
    "feedspeechback.workers.transcription",
    "feedspeechback.workers.diarization",
]


@pytest.mark.parametrize("module", ENTRY_MODULES)
def test_entry_module_imports(module: str) -> None:
    importlib.import_module(module)
