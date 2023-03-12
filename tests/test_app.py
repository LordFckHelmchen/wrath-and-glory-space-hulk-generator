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
        expected_html_file = test_dir / "assets" / "streamlit_http_get_response.html"
        expected_html = expected_html_file.read_text()
        poetry = which("poetry")
        curl = which("curl")

        # ACT
        with Popen(
            [poetry, "run", "streamlit", "run", app_name, "--server.headless", "true"],
            cwd=working_dir,
            stdout=PIPE,
        ) as app:
            sleep(2)  # Wait until started.
            response = run([curl, app_url], capture_output=True, text=True)
            app.terminate()

        # ASSERT
        self.assertEqual(response.returncode, 0)
        actual_html = response.stdout
        (test_dir / f"generated_{expected_html_file.name}").write_text(actual_html)
        self.assertEqual(actual_html, expected_html)


if __name__ == "__main__":
    unittest.main()
