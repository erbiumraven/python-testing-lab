import allure
from helpers.api_helper import post_with_allure
from helpers.assertion_helper import (
    assert_pet_response_matches_expected,
    assert_pet_creation_failed_bad_request
)
from fixtures.pet_fixtures import test_pet, pet_required_fields_only, invalid_missing_name, invalid_missing_photos, \
    invalid_empty_name, invalid_photourls_string


@allure.feature("Pet API")
@allure.story("Create Pet")
class TestCreatePet:

    @allure.description("Verify that a pet with all fields is successfully created.")
    def test_create_pet_with_all_fields(self, session, pet_url, test_pet):
        response = post_with_allure(session, pet_url, test_pet)
        assert_pet_response_matches_expected(response, test_pet)

    @allure.description("Verify that a pet with only mandatory fields is successfully created.")
    def test_create_pet_with_only_required_fields(self, session, pet_url, pet_required_fields_only):
        response = post_with_allure(session, pet_url, pet_required_fields_only)
        assert_pet_response_matches_expected(response, pet_required_fields_only)

    @allure.description("Verify error occurs when creating a pet without the required name field.")
    def test_create_pet_with_missing_name(self, session, pet_url, invalid_missing_name):
        response = post_with_allure(session, pet_url, invalid_missing_name)
        assert_pet_creation_failed_bad_request(response)

    @allure.description("Verify error occurs when creating a pet without the required photos field.")
    def test_create_pet_with_missing_photos(self, session, pet_url, invalid_missing_photos):
        response = post_with_allure(session, pet_url, invalid_missing_photos)
        assert_pet_creation_failed_bad_request(response)

    @allure.description("Verify error occurs when creating a pet with empty name field.")
    def test_create_pet_with_empty_name(self, session, pet_url, invalid_empty_name):
        response = post_with_allure(session, pet_url, invalid_empty_name)
        assert_pet_creation_failed_bad_request(response)

    @allure.description("Verify error occurs for invalid photoUrls field type when creating a pet.")
    def test_create_pet_with_invalid_photourls_type(self, session, pet_url, invalid_photourls_string):
        response = post_with_allure(session, pet_url, invalid_photourls_string)
        assert_pet_creation_failed_bad_request(response)
