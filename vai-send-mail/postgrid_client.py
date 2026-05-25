import time
import requests
from dataclasses import dataclass

POSTGRID_BASE_URL = "https://print.postgrid.com/print-mail/v1"
MAX_RETRIES = 3
RETRY_BACKOFF = [1.0, 2.0, 4.0]
INTER_REQUEST_DELAY = 0.5


@dataclass
class LetterResult:
    success: bool
    letter_id: str | None = None
    pdf_url: str | None = None
    error: str | None = None


class PostGridClient:
    def __init__(self, api_key: str):
        self._api_key = api_key
        self._session = requests.Session()
        self._session.headers.update({
            "x-api-key": api_key,
            "Content-Type": "application/json",
        })
        self._last_request_time = 0.0

    @property
    def is_test_mode(self) -> bool:
        return self._api_key.startswith("test_")

    def _throttle(self):
        elapsed = time.time() - self._last_request_time
        if elapsed < INTER_REQUEST_DELAY:
            time.sleep(INTER_REQUEST_DELAY - elapsed)
        self._last_request_time = time.time()

    def create_letter(
        self,
        html_content: str,
        to_address: dict,
        from_address: dict,
        description: str = "",
    ) -> LetterResult:
        """
        Create a letter via PostGrid.
        to_address and from_address should have keys:
            firstName, lastName, addressLine1, addressLine2, city, provinceOrState, postalOrZip, country
        """
        self._throttle()

        payload = {
            "to": to_address,
            "from": from_address,
            "html": html_content,
            "description": description,
        }

        for attempt in range(MAX_RETRIES):
            try:
                resp = self._session.post(
                    f"{POSTGRID_BASE_URL}/letters",
                    json=payload,
                    timeout=30,
                )

                if resp.status_code == 200 or resp.status_code == 201:
                    data = resp.json()
                    return LetterResult(
                        success=True,
                        letter_id=data.get("id", ""),
                        pdf_url=data.get("url", ""),
                    )
                elif resp.status_code == 429:
                    if attempt < MAX_RETRIES - 1:
                        time.sleep(RETRY_BACKOFF[attempt])
                        continue
                    return LetterResult(
                        success=False,
                        error=f"Rate limited after {MAX_RETRIES} retries",
                    )
                elif resp.status_code >= 500:
                    if attempt < MAX_RETRIES - 1:
                        time.sleep(RETRY_BACKOFF[attempt])
                        continue
                    return LetterResult(
                        success=False,
                        error=f"Server error {resp.status_code}: {resp.text[:200]}",
                    )
                else:
                    return LetterResult(
                        success=False,
                        error=f"API error {resp.status_code}: {resp.text[:200]}",
                    )

            except requests.exceptions.Timeout:
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_BACKOFF[attempt])
                    continue
                return LetterResult(success=False, error="Request timed out")
            except requests.exceptions.ConnectionError:
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_BACKOFF[attempt])
                    continue
                return LetterResult(success=False, error="Connection error")

        return LetterResult(success=False, error="Max retries exceeded")


class MockPostGridClient:
    """A mock client that simulates PostGrid responses for testing without API keys."""

    def __init__(self):
        self._counter = 0

    @property
    def is_test_mode(self) -> bool:
        return True

    def create_letter(
        self,
        html_content: str,
        to_address: dict,
        from_address: dict,
        description: str = "",
    ) -> LetterResult:
        self._counter += 1
        time.sleep(0.05)

        letter_id = f"letter_mock_{self._counter:06d}"
        pdf_url = f"https://postgrid-mock.example.com/preview/{letter_id}.pdf"

        return LetterResult(
            success=True,
            letter_id=letter_id,
            pdf_url=pdf_url,
        )
