from feedspeechback.contracts.evaluation import Scenario

RUBRICS: dict[Scenario, dict] = {
    Scenario.INTERVIEW: {
        "criteria": [
            "technical depth",
            "communication clarity",
            "structure of answers",
        ],
    },
    Scenario.JOB_MEETING: {
        "criteria": [
            "negotiation tone",
            "active listening",
            "expectation alignment",
        ],
    },
}
