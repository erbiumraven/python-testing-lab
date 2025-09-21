from typing import Generator

import pytest
from playwright.sync_api import Playwright, APIRequestContext


@pytest.fixture(scope="session")
def api_request_context(
        playwright: Playwright,
        pet_url
) -> Generator[APIRequestContext, None, None]:
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    request_context = playwright.request.new_context(
        base_url=f"{pet_url}/",
        extra_http_headers=headers
    )
    yield request_context
    request_context.dispose()
