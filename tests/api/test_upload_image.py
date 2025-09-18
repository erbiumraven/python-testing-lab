import allure
import pytest

from fixtures.pet_fixtures import (
    test_pet,
    temp_data_file
)
from helpers.api_helper import (
    build_pet_upload_file_url,
    upload_post_with_allure,
    post_with_allure
)
from helpers.assertion_helper import (
    assert_file_successfully_uploaded,
    assert_upload_failed_no_file,
    assert_upload_failed_unsupported_content_type,
    assert_pet_not_found,
    assert_upload_failed_convert_id_error
)


@allure.feature("Pet API")
@allure.story("Upload image")
class TestUploadImage:

    @pytest.mark.parametrize("metadata", [
        "",
        "12345",
        "abcDEF",
        "with space",
        "special_!@#$%^&*()",
        "meta=param&flag=true",
        "тест",
        "犬",
        "emoji_😊🔥",
        "long" * 50
    ])
    @allure.description("Verify that uploading a file with metadata value succeeds")
    def test_upload_pet_file_with_metadata_succeeds(self, octet_stream_session, pet_url, test_pet, temp_data_file,
                                                    metadata):
        pet_id = test_pet["id"]
        upload_url = build_pet_upload_file_url(pet_url, pet_id=pet_id, metadata=metadata)

        with open(temp_data_file, "rb") as file:
            response = upload_post_with_allure(octet_stream_session, upload_url, file)

        assert_file_successfully_uploaded(response, pet_id)

    @allure.description("Verify that uploading a file without metadata parameter succeeds")
    def test_upload_file_without_metadata_succeeds(self, octet_stream_session, pet_url, test_pet, temp_data_file):
        pet_id = test_pet["id"]
        upload_url = build_pet_upload_file_url(pet_url, pet_id=pet_id, metadata=None)

        with open(temp_data_file, "rb") as file:
            response = upload_post_with_allure(octet_stream_session, upload_url, file)

        assert_file_successfully_uploaded(response, pet_id)

    @allure.description("Verify that uploading without a file fails with 400 error")
    def test_upload_without_file_fails(self, octet_stream_session, pet_url, test_pet):
        upload_url = build_pet_upload_file_url(pet_url, pet_id=test_pet["id"], metadata="metadata")
        response = post_with_allure(octet_stream_session, upload_url, payload=None)
        assert_upload_failed_no_file(response)

    @allure.description("Verify upload with wrong content type fails with 415 error")
    def test_upload_with_wrong_content_type_failed(self, session, pet_url, test_pet, temp_data_file):
        upload_url = build_pet_upload_file_url(pet_url, pet_id=test_pet["id"], metadata="metadata")

        with open(temp_data_file, "rb") as file:
            response = upload_post_with_allure(session, upload_url, file)

        assert_upload_failed_unsupported_content_type(response)

    @allure.description("Verify upload without content type fails")
    def test_upload_without_content_type_failed(self, session_no_content_type, pet_url, test_pet, temp_data_file):
        upload_url = build_pet_upload_file_url(pet_url, pet_id=test_pet["id"], metadata="metadata")

        with open(temp_data_file, "rb") as file:
            response = upload_post_with_allure(session_no_content_type, upload_url, file)

        assert response.status_code == 400

    @allure.description("Verify that uploading file for non-existing pet fails with 404 error")
    def test_upload_file_for_non_existing_pet_fails(self, octet_stream_session, pet_url, temp_data_file):
        upload_url = build_pet_upload_file_url(pet_url, pet_id="66767676", metadata="metadata")

        with open(temp_data_file, "rb") as file:
            response = upload_post_with_allure(octet_stream_session, upload_url, file)

        assert_pet_not_found(response)

    @allure.description("Verify that uploading file for invalid pet ID fails with input conversion error")
    def test_upload_file_with_invalid_pet_id_fails(self, octet_stream_session, pet_url, temp_data_file):
        pet_id = "dog"
        upload_url = build_pet_upload_file_url(pet_url, pet_id=pet_id, metadata="metadata")

        with open(temp_data_file, "rb") as file:
            response = upload_post_with_allure(octet_stream_session, upload_url, file)

        assert_upload_failed_convert_id_error(response, pet_id)

    @allure.description("Verify that uploading file with empty pet ID fails")
    def test_upload_file_with_empty_pet_id_fails(self, octet_stream_session, pet_url, temp_data_file):
        upload_url = build_pet_upload_file_url(pet_url, pet_id="", metadata="metadata")

        with open(temp_data_file, "rb") as file:
            response = upload_post_with_allure(octet_stream_session, upload_url, file)

        assert_pet_not_found(response)
