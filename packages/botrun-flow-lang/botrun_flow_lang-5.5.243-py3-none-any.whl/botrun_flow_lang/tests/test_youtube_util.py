import unittest

from botrun_flow_lang.langgraph_agents.agents.util.youtube_util import (
    get_youtube_transcript,
)


class TestYouTubeUtil(unittest.TestCase):
    def test_get_youtube_transcript(self):
        """Test getting transcript from a YouTube video"""
        url = "https://www.youtube.com/watch?v=WEBiebbeNCA"
        transcript = get_youtube_transcript(url)

        # Check that we got a response
        self.assertIsNotNone(transcript)

        # Check that it's a string
        self.assertIsInstance(transcript, str)

        # Check that it's not an error message
        self.assertFalse(transcript.startswith("Error:"))

        # Check that we got some content
        self.assertGreater(len(transcript), 0)


if __name__ == "__main__":
    unittest.main()
