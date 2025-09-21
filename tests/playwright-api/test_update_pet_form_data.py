import allure
import pytest

from playwright.sync_api import APIRequestContext

from fixtures.pet_fixtures import test_pet
from fixtures.pet_playwright_fixtures import api_request_context
from helpers.api_helper import playwright_post_with_allure
from helpers.assertion_helper import (
    assert_updated_pet_matches_expected,
    assert_update_pet_missing_name_param_fails
)


@allure.feature("Pet API")
@allure.story("Update Pet Form Data")
@pytest.mark.pet_update_form_data
class TestUpdatePetFormData:

    @allure.description("Update pet name and status successfully")
    def test_update_pet_name_and_status_success(self, api_request_context: APIRequestContext, test_pet):
        params = {"name": "Hoxha", "status": "sold"}

        response = playwright_post_with_allure(api_request_context, test_pet['id'], params)
        assert_updated_pet_matches_expected(response, test_pet, params)

    @allure.description("Update only pet name successfully")
    def test_update_only_pet__name_success(self, api_request_context: APIRequestContext, test_pet):
        params = {"name": "Hoxha_updated"}

        response = playwright_post_with_allure(api_request_context, test_pet['id'], params)
        assert_updated_pet_matches_expected(response, test_pet, params)

    @allure.description("Update empty pet name successfully")
    def test_update_empty_pet_name_success(self, api_request_context: APIRequestContext, test_pet):
        params = {"name": "", "status": "sold"}

        response = playwright_post_with_allure(api_request_context, test_pet['id'], params)
        assert_updated_pet_matches_expected(response, test_pet, params)

    @allure.description("Update empty pet status successfully")
    def test_update_empty_pet_status_success(self, api_request_context: APIRequestContext, test_pet):
        params = {"name": "Hoxha_updated", "status": ""}

        response = playwright_post_with_allure(api_request_context, test_pet['id'], params)
        assert_updated_pet_matches_expected(response, test_pet, params)

    @allure.description("Update fails when name parameter is missing(400)")
    def test_update_pet_missing_name_fails(self, api_request_context: APIRequestContext, test_pet):
        params = {"status": "sold"}

        response = playwright_post_with_allure(api_request_context, test_pet['id'], params)
        assert_update_pet_missing_name_param_fails(response)
