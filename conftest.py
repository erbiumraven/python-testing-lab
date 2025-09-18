import os
import pytest
import requests

from config import DEFAULT_PET_BASE_URL


@pytest.fixture(scope="session", autouse=True)
def allure_environment(base_url):
    os.makedirs("allure-results", exist_ok=True)
    env_file = os.path.join("allure-results", "environment.properties")
    os_name = os.getenv("OS_NAME", "macOS")

    with open(env_file, "w") as f:
        f.write(f"BaseURL={base_url}\n")
        f.write(f"OS={os_name}\n")


@pytest.fixture(scope="session")
def base_url():
    return os.environ.get("PET_BASE_URL") or DEFAULT_PET_BASE_URL


@pytest.fixture(scope="session")
def pet_url(base_url):
    return f"{base_url}/pet"


@pytest.fixture(scope="session")
def pet_status_url(base_url):
    return f"{base_url}/pet/findByStatus"


@pytest.fixture(scope="session")
def pet_tags_url(base_url):
    return f"{base_url}/pet/findByTags"


def create_session(default_headers=None) -> requests.Session:
    s = requests.Session()
    headers = {"Accept": "application/json"}
    if default_headers:
        headers.update(default_headers)
    s.headers.update(headers)
    return s

@pytest.fixture(scope="session")
def session():
    return create_session({"Content-Type": "application/json"})

@pytest.fixture(scope="session")
def octet_stream_session():
    return create_session({"Content-Type": "application/octet-stream"})

@pytest.fixture(scope="session")
def session_no_content_type():
    return create_session()
