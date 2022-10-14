import shutil
import unittest
from pathlib import Path
from shutil import which
from subprocess import PIPE
from subprocess import Popen
from subprocess import run
from time import sleep

import toml


class TestRandomTable(unittest.TestCase):

    def test_run_app_curl_main_page_expect_same_result_as_always(self):
        # ARRANGE
        test_dir = Path(__file__).parent
        working_dir = test_dir.parent
        app_name = working_dir / "streamlit_app.py"
        streamlit_config = toml.load(working_dir / ".streamlit" / "config.toml")
        app_url = f"http://localhost:{streamlit_config['server']['port']}"
        expected_response = (
                test_dir / "assets" / "streamlit_http_get_response.html").read_text()

        # ACT
        with Popen(
                [which("poetry"), "run", which("streamlit"), "run", app_name,
                 "--server.headless",
                 "true"], cwd=working_dir, stdout=PIPE) as app:
            sleep(2)  # Wait until started.
            response = run([which("curl"), app_url], capture_output=True,
                           text=True)
            app.terminate()

        # ASSERT
        self.assertEqual(response.returncode, 0)
        self.assertEqual(response.stdout, expected_response)


if __name__ == '__main__':
    unittest.main()