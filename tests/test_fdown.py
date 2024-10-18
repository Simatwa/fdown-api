import unittest
from os import remove
from fdown_api import Fdown
from fdown_api.main import Fdown, VideoLinks


class TestFdown(unittest.TestCase):

    def setUp(self):
        self.fdown = Fdown()
        self.urls = (
            "https://www.facebook.com/reel/823513456342882?mibextid=rS40aB7S9Ucbxw6v",
            "https://fb.watch/vhalCYi2ib/?mibextid=rS40aB7S9Ucbxw6v",
        )

    def test_validate_url(self):
        for url in self.urls:
            self.assertIsInstance(self.fdown.validate_url(url), str)
        self.assertFalse(self.fdown.validate_url("some random string", True))
        with self.assertRaises(ValueError) as context:
            self.fdown.validate_url("another random string")

    def test_links_generation(self):
        video_links = self.fdown.get_links(self.urls[0])
        self.assertIsInstance(video_links.duration_in_seconds, int)
        self.assertIsInstance(video_links, VideoLinks)

    def test_video_download(self):
        video_links = self.fdown.get_links(self.urls[1])
        saved_to = self.fdown.download_video(
            video_links, quiet=True, progress_bar=False
        )
        self.assertTrue(saved_to.exists())
        remove(saved_to)


if __name__ == "__main__":
    unittest.main()
