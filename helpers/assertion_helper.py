import re
import json

import allure

from tests.api.models import Pet


def assert_pet_response_matches_expected(response, valid_pet_full):
    with allure.step("Assert pet created successfully"):
        assert response.status_code == 200, \
            f"Expected 200, got {response.status_code}"

        json_data = response.json()
        actual_pet = Pet(**json_data)
        expected_pet = Pet(**valid_pet_full)

        allure.attach(json.dumps(json_data, indent=2), name="Actual Pet",
                      attachment_type=allure.attachment_type.JSON)
        allure.attach(json.dumps(valid_pet_full, indent=2), name="Expected Pet",
                      attachment_type=allure.attachment_type.JSON)

        assert actual_pet == expected_pet, "Response body does not match expected pet"


def assert_pet_creation_failed_bad_request(response):
    with allure.step("Assert pet creation failed bad request"):
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"


def assert_pet_deleted(response):
    with allure.step("Verify that pet is deleted (200)"):
        assert response.status_code == 200, \
            f"Expected 200, got {response.status_code}"
        assert response.text == "Pet deleted", \
            f"Expected body 'Pet deleted', got '{response.text}'"


def assert_pet_not_found(response):
    with allure.step("Verify that pet is not found (404)"):
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"

        response_text = response.text.strip().lower()
        expected_messages = ["pet not found", "http 404 not found"]
        assert any(msg in response_text for msg in expected_messages), \
            f"Response body does not contain any expected message: {response.text}"


def assert_pet_invalid_pet_id_format(response):
    with allure.step("Verify that format of pet id is invalid (400)"):
        assert response.status_code == 400, \
            f"Expected 400, got {response.status_code}"

        assert "input error: couldn't convert" in response.text.lower(), \
            f"Response body does not contain 'input error: couldn't convert': {response.text}"


def assert_pets_status_success(response, status_set, test_pet_list):
    with (allure.step(f'Verify that pets with status in {status_set} (200)')):
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        json_data = response.json()

        assert len(json_data) >= len(test_pet_list), \
            f"Expected at least {len(test_pet_list)} pet(s) in response, but got len(json_data) pet(s)"

        pets = [Pet(**p) for p in json_data]

        for pet in pets:
            assert pet.status in status_set, f"Expected status in {status_set}, got {pet.status}"

        for test_pet_status in test_pet_list:
            actual_pet = next((pet for pet in pets if pet.id == test_pet_status['id']), None)
            assert actual_pet is not None, (
                f"Pet with id={test_pet_status['id']} not found in response. "
                "Note: this is a limitation of the test server; on production this cannot happen."
            )

            assert actual_pet.model_dump() == test_pet_status, (
                f"Pet data mismatch for id={test_pet_status['id']}:\n"
                f"Expected: {test_pet_status}\n"
                f"Actual:   {actual_pet.model_dump()}"
            )


def assert_find_pet_invalid_status(response, status):
    with allure.step("Verify that status is invalid (400)"):
        assert response.status_code == 400, \
            f"Expected 400, got {response.status_code}"

        assert f"Input error: query parameter `status value `{status}` is not in the allowable values `[available, pending, sold]`".lower() in response.text.lower(), \
            f"Response body does not contain 'Input error: query parameter `status value ...' : {response.text}"


def assert_find_pet_no_status_param(response):
    with allure.step("Verify that status is invalid (400)"):
        assert response.status_code == 400, \
            f"Expected 400, got {response.status_code}"

        assert f"Input error: missing required query parameter `status`".lower() in response.text.lower(), \
            f"Response body does not contain 'Input error: missing required query parameter `status`' : {response.text}"


def assert_pet_tags_success(response, tag_names, all_tags_pets):
    with allure.step(f'Verify that pets with tags {tag_names} (200)'):
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        json_data = response.json()
        assert len(json_data) >= len(
            all_tags_pets), f"Expected at least {len(all_tags_pets)} pets in response, but got {len(json_data)} pets"

        pets = [Pet(**p) for p in json_data]

        tag_to_pets = {tag: 0 for tag in tag_names}

        for pet in pets:
            pet_tag_names = {tag.name for tag in getattr(pet, "tags", [])}

            assert pet_tag_names & tag_names, (
                f"Pet id={pet.id} has no tags from expected tag_names: {tag_names}. "
                f"Actual pet tags: {pet_tag_names}"
            )

            for tag in tag_names:
                if tag in pet_tag_names:
                    tag_to_pets[tag] += 1

        for tag, count in tag_to_pets.items():
            assert count > 0, f"No pet found with tag '{tag}'"


def assert_find_pet_no_tags_param(response):
    with allure.step("Verify that tags is invalid (400)"):
        assert response.status_code == 400, \
            f"Expected 400, got {response.status_code}"

        assert f"Input error: missing required query parameter `tags`".lower() in response.text.lower(), \
            f"Response body does not contain 'Input error: missing required query parameter `tags`' : {response.text}"


def assert_method_not_allowed(response):
    with allure.step("Verify that method is not allowed error (405)"):
        assert response.status_code == 405, \
            f"Expected 405, got {response.status_code}"

        assert "method not allowed" in response.text.lower(), \
            f"Response body does not contain 'method not allowed': {response.text}"


def assert_invalid_pet_id_format(response):
    with allure.step("Verify that error occurred where pet id format is invalid (400)"):
        assert response.status_code == 400, \
            f"Expected 400, got {response.status_code}"

        assert "invalid petid format" in response.text.lower(), \
            f"Response body does not contain 'invalid petid format': {response.text}"


def assert_return_empty_list_for_nonexistent_tags(response):
    with allure.step("Verify that empty list of pets returns where no pets found by tags (200)"):
        assert response.status_code == 200
        assert response.json() == []


def assert_error_occurred_for_empty_tag(response):
    with allure.step("Verify that error occurred where tag is empty (400)"):
        assert response.status_code == 400, f"Expected status code 400, but got {response.status_code}"

        assert "no tags provided. try again?" in response.text.lower(), (
            f"Expected error message 'No tags provided. Try again?' in response body, "
            f"but got: {response.text}")


def assert_file_successfully_uploaded(response, pet_id):
    with allure.step("Verify that file was uploaded successfully"):
        assert response.status_code == 200, \
            f"Expected 200, got {response.status_code}"

        data = response.json()
        assert data["id"] == pet_id

        assert isinstance(data["photoUrls"], list)
        assert len(data["photoUrls"]) > 0
        assert re.match(r"^/tmp/inflector\d+\.tmp$", data["photoUrls"][-1])


def assert_upload_failed_no_file(response):
    expected_text = "No file uploaded"
    with allure.step("Verify upload without file fails"):
        assert response.status_code == 400, f"Expected status 400, got {response.status_code}"
        assert expected_text.lower() in response.text.strip().lower(), \
            f"Expected '{expected_text}' to be in response, got '{response.text.strip()}'"


def assert_upload_failed_unsupported_content_type(response):
    expected_text = "HTTP 415 Unsupported Media Type"
    with allure.step("Verify upload fails with unsupported content type"):
        assert response.status_code == 415, f"Expected status 415, got {response.status_code}"
        assert expected_text.lower() in response.text.strip().lower(), \
            f"Expected '{expected_text}' to be in response, got '{response.text.strip()}'"


def assert_upload_failed_convert_id_error(response, pet_id):
    expected_text = f"Input error: couldn't convert `{pet_id}` to type `class java.lang.Long`"
    with allure.step("Verify upload fails with convert id error"):
        assert response.status_code == 400, f"Expected status 400, got {response.status_code}"
        assert expected_text.lower() in response.text.strip().lower(), \
            f"Expected '{expected_text}' to be in response, got '{response.text.strip()}'"
