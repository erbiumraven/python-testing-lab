import allure
import pytest

from fixtures.pet_fixtures import test_pet

from helpers.api_helper import get_with_allure, put_with_allure

from helpers.assertion_helper import (
    assert_pet_not_found,
    assert_pet_response_matches_expected
)


@allure.feature("Pet API")
@allure.story("Update Pet")
@pytest.mark.pet_update
class TestUpdatePet:

    @allure.description("Update existing pet with new data and verify changes")
    def test_update_pet_success(self, session, pet_url, test_pet):
        test_pet['name'] = "Brown"
        test_pet['category'] = {"id": 2, "name": "Cats"}
        test_pet['tags'] = [{"id": 0, "name": "tag_b"}]
        test_pet['photoUrls'] = ["https://pixabay.com/photos/cat12"]
        test_pet['status'] = "pending"

        put_response = put_with_allure(session, pet_url, test_pet)
        assert_pet_response_matches_expected(put_response, test_pet)

        get_response = get_with_allure(session, f'{pet_url}/{test_pet["id"]}')
        assert_pet_response_matches_expected(get_response, test_pet)

    @allure.description("Updating pet with empty ID should return 400.")
    def test_update_pet_empty_id_fail(self, session, pet_url, test_pet):
        test_pet['id'] = ""
        response = put_with_allure(session, pet_url, test_pet)
        assert response.status_code == 400

    @allure.description("Updating pet with non-existing ID should return not found.")
    def test_update_pet_non_existing_id_fail(self, session, pet_url, test_pet):
        test_pet['id'] = "7777777777"
        response = put_with_allure(session, pet_url, test_pet)
        assert_pet_not_found(response)

    @allure.description("Updating pet with invalid type for name should fail.")
    def test_update_pet_invalid_type_fail(self, session, pet_url, test_pet):
        test_pet['name'] = 327846
        response = put_with_allure(session, pet_url, test_pet)
        assert response.status_code == 400
