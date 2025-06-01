import unittest
from summarizer_agent import SummarizerAgent, SummaryTone

class TestSummarizerAgent(unittest.TestCase):
    def setUp(self):
        self.agent = SummarizerAgent()
        self.test_input = "Refactor release module to support multi-source inputs"

    def test_generate_summary_dev(self):
        summary = self.agent.generate_summary(self.test_input, SummaryTone.DEV)
        self.assertIsInstance(summary, str)
        self.assertGreater(len(summary), 0)
        print("\n[DEV]", summary)

    def test_generate_summary_exec(self):
        summary = self.agent.generate_summary(self.test_input, SummaryTone.EXEC)
        self.assertIsInstance(summary, str)
        self.assertGreater(len(summary), 0)
        print("\n[EXEC]", summary)

    def test_generate_summary_sassy(self):
        summary = self.agent.generate_summary(self.test_input, SummaryTone.SASSY)
        self.assertIsInstance(summary, str)
        self.assertGreater(len(summary), 0)
        print("\n[SASSY]", summary)

if __name__ == '__main__':
    unittest.main()
