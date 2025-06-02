from summarizer_agent import SummarizerAgent, SummaryTone

def test_single_summary():
    agent = SummarizerAgent()
    summary = agent.generate_summary(
        "Refactor release module to support multi-source inputs",
        SummaryTone.DEV
    )
    print("[DEV]", summary)
    assert summary and "Refactor" in summary

def test_exec_summary():
    agent = SummarizerAgent()
    summary = agent.generate_summary(
        "Refactor release module to support multi-source inputs",
        SummaryTone.EXEC
    )
    print("[EXEC]", summary)
    assert summary and "Refactor" in summary

def test_sassy_summary():
    agent = SummarizerAgent()
    summary = agent.generate_summary(
        "Refactor release module to support multi-source inputs",
        SummaryTone.SASSY
    )
    print("[SASSY]", summary)
    assert summary and "Refactor" in summary

if __name__ == "__main__":
    test_single_summary()
    test_exec_summary()
    test_sassy_summary()
