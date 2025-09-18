import allure

from helpers.api_helper import get_with_allure
from fixtures.pet_fixtures import test_pet
from helpers.assertion_helper import (
    assert_pet_response_matches_expected,
    assert_pet_not_found,
    assert_method_not_allowed,
    assert_invalid_pet_id_format
)


@allure.feature("Pet API")
@allure.story("Get Pet by ID")
class TestGetPetById:

    @allure.description("Get pet by valid ID returns 200 and correct pet data.")
    def test_get_pet_by_id(self, session, pet_url, test_pet):
        response = get_with_allure(session, f'{pet_url}/{test_pet["id"]}')
        assert_pet_response_matches_expected(response, test_pet)

    @allure.description("Get pet by non-existing ID returns 404.")
    def test_get_pet_by_id_not_found(self, session, pet_url):
        response = get_with_allure(session, f'{pet_url}/9966990')
        assert_pet_not_found(response)

    @allure.description("Get pet by invalid ID format returns 400.")
    def test_get_pet_by_invalid_id_string(self, session, pet_url):
        response = get_with_allure(session, f'{pet_url}/dobby_45_a')
        assert_invalid_pet_id_format(response)

    @allure.description("Get pet without ID returns 405.")
    def test_get_pet_empty_id(self, session, pet_url):
        response = get_with_allure(session, f'{pet_url}/')
        assert_method_not_allowed(response)
