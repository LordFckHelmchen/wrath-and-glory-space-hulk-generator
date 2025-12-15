import sys
import unittest
from pathlib import Path
from shutil import which
from subprocess import PIPE
from subprocess import Popen
from subprocess import run
from time import sleep

import toml


def get_executable(name: str) -> Path:
    if (executable := which(name)) is not None:
        executable = Path(executable)
        if executable.exists():
            return executable

    # This can happen if the dependencies for uv/curl are not available or the PATH isn't properly set up.
    # Try adding ~/.uv/bin/uv if this fails for uv.
    msg = f"Couldn't find executable for '{name}'! sys.path contained the following entries:\n" + "\n".join(sys.path)
    raise OSError(msg)


class TestApp(unittest.TestCase):
    def test_run_app_curl_main_page_expect_same_result_as_always(self) -> None:
        # ARRANGE
        test_dir = Path(__file__).parent
        working_dir = test_dir.parent
        streamlit_config = toml.load(working_dir / ".streamlit" / "config.toml")
        app_url = f"http://localhost:{streamlit_config['server']['port']}"
        expected_html_file = test_dir / "assets" / "streamlit_http_get_response.html"
        expected_html = expected_html_file.read_text()
        actual_html_file = test_dir / f"generated_{expected_html_file.name}"
        actual_html_file.unlink(missing_ok=True)
        uv = get_executable("uv")
        app = (uv, "run", "streamlit", "run", working_dir / "streamlit_app.py", "--server.headless", "true")

        # Set up curl command to app
        max_retries = 9
        retry_wait_in_sec = 2
        curl_cmd = (get_executable("curl"), app_url, "--raw", "--show-error", "--silent", "--output", actual_html_file)

        def curl_app() -> int:
            sleep(retry_wait_in_sec)  # Always wait to be ready.
            response = run(curl_cmd, check=False, stderr=PIPE, text=True, timeout=retry_wait_in_sec)
            if response.stderr:
                print(f"Curl had difficulties: '{response.stderr}'")
            return response.returncode

        # ACT
        with Popen(app, cwd=working_dir) as app:
            try_id = 1
            while (actual_return_code := curl_app()) != 0 and try_id <= max_retries:
                print(f"Couldn't get a response from the app on try {try_id}/{max_retries}. Retrying...")
                try_id += 1
            app.terminate()

        # ASSERT
        with self.subTest(i="Successfully returns with 0"):
            assert actual_return_code == 0
        with self.subTest(i="Response contains correct html"):
            actual_html = actual_html_file.read_text()
            assert actual_html == expected_html


if __name__ == "__main__":
    unittest.main()
