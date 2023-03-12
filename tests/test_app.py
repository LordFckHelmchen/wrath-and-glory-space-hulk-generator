import unittest
from pathlib import Path
from shutil import which
from subprocess import PIPE
from subprocess import Popen
from subprocess import run
from time import sleep

import toml


class TestApp(unittest.TestCase):
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
        streamlit_args = ["--server.headless", "true"]
        curl = which("curl")
        # Sometime setup takes longer, and we retry to get the connection.
        curl_args = ["--raw", "--retry-connrefused", "--retry", "2", "--show-error", "--silent"]

        # ACT
        with Popen([poetry, "run", "streamlit", "run", app_name, *streamlit_args], cwd=working_dir, stdout=PIPE) as app:
            sleep(2)  # Give it some time to start, if taken longer, curl will take care of retries.
            response = run([curl, app_url, *curl_args], capture_output=True, text=True)
            app.terminate()

        # ASSERT
        with self.subTest(i="Successfully returns with 0"):
            actual_return_code = response.returncode
            msg = f"\ncurl error '{response.stderr}'"
            self.assertEqual(actual_return_code, 0, msg=msg)
            if actual_return_code == 0 and response.stderr != "":
                print(f"Although the test passed, something went wrong:\n    '{response.stderr}'")
        with self.subTest(i="Response contains correct html"):
            actual_html = response.stdout
            (test_dir / f"generated_{expected_html_file.name}").write_text(actual_html)
            self.assertEqual(actual_html, expected_html)


if __name__ == "__main__":
    unittest.main()
