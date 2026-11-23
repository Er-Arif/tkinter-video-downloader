import unittest

from download import format_for_height, validate_youtube_url


class DownloaderTests(unittest.TestCase):
    def test_accepts_standard_and_short_urls(self):
        self.assertEqual(
            validate_youtube_url("https://www.youtube.com/watch?v=abc"),
            "https://www.youtube.com/watch?v=abc",
        )
        self.assertEqual(
            validate_youtube_url("https://youtu.be/abc"), "https://youtu.be/abc"
        )

    def test_rejects_other_domains_and_insecure_urls(self):
        for url in ("https://youtube.com.evil.example/watch", "http://youtube.com/watch", ""):
            with self.assertRaises(ValueError):
                validate_youtube_url(url)

    def test_format_selector(self):
        self.assertIn("height<=720", format_for_height(720))
        with self.assertRaises(ValueError):
            format_for_height(144)


if __name__ == "__main__":
    unittest.main()
