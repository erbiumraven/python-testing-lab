import allure
import pytest

from fixtures.pet_fixtures import (
    all_tags_pets,
    test_pet
)

from helpers.api_helper import get_with_allure

from helpers.assertion_helper import (
    assert_error_occurred_for_empty_tag,
    assert_find_pet_no_tags_param,
    assert_pet_tags_success,
    assert_return_empty_list_for_nonexistent_tags
)


@allure.feature("Pet API")
@allure.story("Get Pet by Tags")
@pytest.mark.pet_tags
class TestFindPetByTag:

    @allure.description("Find pets by multiple tags returns all matching pets.")
    def test_find_pets_multiple_tags(self, session, pet_tags_url, all_tags_pets):
        tag_names = {tag["name"] for pet in all_tags_pets for tag in pet.get("tags", [])}
        tags = ",".join(tag_names)

        url = f"{pet_tags_url}?tags={tags}"
        response = get_with_allure(session, url)
        assert_pet_tags_success(response, tag_names, all_tags_pets)

    @allure.description("Find pets by a single tag returns all matching pets")
    def test_find_pets_single_tag(self, session, pet_tags_url, test_pet):
        first_tag = test_pet["tags"][0]["name"]
        url = f"{pet_tags_url}?tags={first_tag}"
        response = get_with_allure(session, url)
        assert_pet_tags_success(response, {first_tag}, [test_pet])

    @allure.description("Searching by nonexistent tag returns an empty list.")
    def test_find_pets_by_tag_not_found(self, session, pet_tags_url):
        url = f"{pet_tags_url}?tags=erbium_65)"
        response = get_with_allure(session, url)
        assert_return_empty_list_for_nonexistent_tags(response)

    @allure.description("Searching by empty tag returns an error.")
    def test_find_pets_by_empty_tag(self, session, pet_tags_url):
        response = get_with_allure(session, f"{pet_tags_url}?tags=")
        assert_error_occurred_for_empty_tag(response)

    @allure.description("Request without tags parameter returns an error.")
    def test_find_pets_no_tags_param(self, session, pet_tags_url):
        response = get_with_allure(session, pet_tags_url)
        assert_find_pet_no_tags_param(response)
