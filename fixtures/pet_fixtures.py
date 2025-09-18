import os
import tempfile

import pytest
import random
from helpers.api_helper import post_with_allure, delete_with_allure


def make_pet_data(
        pet_id=None,
        name="Hardy",
        status="available",
        tags=None,
        photos=None,
        include_fields=None
):
    if tags is None:
        tags = [{"id": 0, "name": "string"}]
    if photos is None:
        photos = ["https://pixabay.com/photos/pomeranian-dog-puppy-mammal-animal-8096885/"]
    if pet_id is None:
        pet_id = random.randint(100000, 999999)

    full_pet = {
        "id": pet_id,
        "name": name,
        "category": {"id": 1, "name": "Dogs"},
        "photoUrls": photos,
        "tags": tags,
        "status": status
    }

    if include_fields is None:
        return full_pet

    return {key: value for key, value in full_pet.items() if key in include_fields}


@pytest.fixture(scope="function")
def test_pet(pet_url, session):
    pet = make_pet_data()
    post_with_allure(session, f"{pet_url}", pet)
    yield pet
    delete_with_allure(session, f"{pet_url}/{pet['id']}")


@pytest.fixture(params=["available", "pending", "sold"])
def pet_with_status(pet_url, session, request):
    status = request.param
    pet_data = make_pet_data(status=status)

    post_with_allure(session, f"{pet_url}", pet_data)
    yield pet_data
    delete_with_allure(session, f"{pet_url}/{pet_data['id']}")


@pytest.fixture(scope="session")
def all_statuses_pets(pet_url, session):
    statuses = ["available", "pending", "sold"]
    pets = []

    for status in statuses:
        pet_data = make_pet_data(status=status)
        post_with_allure(session, f"{pet_url}", pet_data)
        pets.append(pet_data)

    yield pets

    for pet in pets:
        delete_with_allure(session, f"{pet_url}/{pet['id']}")


@pytest.fixture(scope="session")
def all_tags_pets(pet_url, session):
    tags = ["tag1", "tag2", "4_tag"]
    pets = []

    for i, tag in enumerate(tags):
        tag_to_add = [{"id": i, "name": tag}]
        pet_data = make_pet_data(tags=tag_to_add)
        post_with_allure(session, f"{pet_url}", pet_data)
        pets.append(pet_data)

    yield pets

    for pet in pets:
        delete_with_allure(session, f"{pet_url}/{pet['id']}")


@pytest.fixture
def pet_required_fields_only():
    return make_pet_data(include_fields=["name", "photoUrls"])


@pytest.fixture
def invalid_missing_name():
    return make_pet_data(include_fields=["id", "category", "photoUrls", "tags", "status"])


@pytest.fixture
def invalid_missing_photos():
    return make_pet_data(include_fields=["id", "name", "category", "tags", "status"])


@pytest.fixture
def invalid_empty_name():
    return make_pet_data(name="")


@pytest.fixture
def invalid_photourls_string():
    return make_pet_data(photos="string")


@pytest.fixture
def temp_data_file():
    with tempfile.NamedTemporaryFile(suffix=".webp", delete=False) as tmp_file:
        tmp_file.write(b"FakeWebPData")
        tmp_file_path = tmp_file.name

    yield tmp_file_path

    if os.path.exists(tmp_file_path):
        os.remove(tmp_file_path)
