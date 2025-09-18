import allure

from helpers.api_helper import (
    delete_with_allure,
    get_with_allure
)
from fixtures.pet_fixtures import test_pet
from helpers.assertion_helper import (
    assert_pet_deleted,
    assert_pet_not_found,
    assert_pet_invalid_pet_id_format
)


@allure.feature("Pet API")
@allure.story("Delete Pet")
class TestDeletePet:

    @allure.description("Verify that pet successfully deleted.")
    def test_delete_pet_success(self, session, pet_url, test_pet):
        pet_id = test_pet['id']
        response = delete_with_allure(session, f'{pet_url}/{pet_id}')
        assert_pet_deleted(response)

        response = get_with_allure(session, f'{pet_url}/{pet_id}')
        assert_pet_not_found(response)

    @allure.description("Verify that deleting a non-existing pet returns a successful response without errors.")
    def test_delete_nonexistent_pet(self, session, pet_url):
        pet_id = 777777
        response = delete_with_allure(session, f'{pet_url}/{pet_id}')
        assert_pet_deleted(response)

        response = get_with_allure(session, f'{pet_url}/{pet_id}')
        assert_pet_not_found(response)

    @allure.description("Verify that deleting a pet with an invalid ID format returns an error response.")
    def test_delete_invalid_pet_id(self, session, pet_url):
        pet_id = "invalid_type"
        response = delete_with_allure(session, f'{pet_url}/{pet_id}')
        assert_pet_invalid_pet_id_format(response)
