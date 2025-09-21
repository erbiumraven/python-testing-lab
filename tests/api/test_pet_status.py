import allure
import pytest

from fixtures.pet_fixtures import (
    all_statuses_pets,
    pet_with_status
)

from helpers.api_helper import get_with_allure

from helpers.assertion_helper import (
    assert_find_pet_invalid_status,
    assert_find_pet_no_status_param,
    assert_pets_status_success
)


@allure.feature("Pet API")
@allure.story("Get Pet by Status")
@pytest.mark.pet_status
class TestFindPetByStatus:

    @allure.description("Find pets by a single valid status returns matching pets.")
    def test_find_pets_by_status(self, session, pet_status_url, pet_with_status):
        status = pet_with_status["status"]
        url = f"{pet_status_url}?status={status}"
        response = get_with_allure(session, url)
        assert_pets_status_success(response, {status}, [pet_with_status])

    @allure.description("Find pets by multiple valid statuses returns pets for each status.")
    def test_find_pets_multiple_status(self, session, pet_status_url, all_statuses_pets):
        statuses = {pet["status"] for pet in all_statuses_pets}
        param = ",".join(statuses)
        url = f"{pet_status_url}?status={param}"
        response = get_with_allure(session, url)
        assert_pets_status_success(response, statuses, all_statuses_pets)

    @allure.description("Find pets with an invalid status value returns 400.")
    def test_find_pets_invalid_status(self, session, pet_status_url):
        status = "unknown"
        url = f"{pet_status_url}?status={status}"
        response = get_with_allure(session, url)
        assert_find_pet_invalid_status(response, status)

    @allure.description("Find pets with empty status value returns 400.")
    def test_find_pets_empty_status(self, session, pet_status_url):
        status = ""
        url = f"{pet_status_url}?status={status}"
        response = get_with_allure(session, url)
        assert_find_pet_invalid_status(response, status)

    @allure.description("Find pets without status query parameter returns 400.")
    def test_find_pets_no_status_param(self, session, pet_status_url):
        response = get_with_allure(session, pet_status_url)
        assert_find_pet_no_status_param(response)
