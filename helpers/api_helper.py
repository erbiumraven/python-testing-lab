import urllib
import allure
import json


def _allure_request(session, method, url, payload=None, step_name=None):
    path = urllib.parse.urlparse(url).path

    with allure.step(step_name or f"{method.upper()} {path}"):
        request_info = {"headers": dict(session.headers)}
        if payload:
            request_info["body"] = payload
        allure.attach(
            json.dumps(request_info, indent=2),
            name="Request",
            attachment_type=allure.attachment_type.JSON
        )

        response = getattr(session, method)(url, json=payload if payload else None)

        try:
            body = response.json()
        except Exception:
            body = response.text

        response_info = {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "body": body
        }
        allure.attach(
            json.dumps(response_info, indent=2),
            name="Response",
            attachment_type=allure.attachment_type.JSON
        )

        return response


def post_with_allure(session, url, payload):
    return _allure_request(session, "post", url, payload)


def get_with_allure(session, url):
    return _allure_request(session, "get", url)


def delete_with_allure(session, url):
    return _allure_request(session, "delete", url)


def put_with_allure(session, url, payload):
    return _allure_request(session, "put", url, payload)


def upload_post_with_allure(session, url, data):
    path = urllib.parse.urlparse(url).path

    with allure.step(f"POST {path}"):
        request_info = {
            "headers": dict(session.headers),
        }

        allure.attach(
            json.dumps(request_info, indent=2),
            name="Request",
            attachment_type=allure.attachment_type.JSON
        )

        response = session.post(url, data=data)

        try:
            body = response.json()
        except Exception:
            body = response.text

        response_info = {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "body": body
        }
        allure.attach(
            json.dumps(response_info, indent=2),
            name="Response",
            attachment_type=allure.attachment_type.JSON
        )

    return response


def build_pet_upload_file_url(pet_url: str, pet_id: str = None, metadata: str = None) -> str:
    pet_segment = pet_id if pet_id else ""
    url = f"{pet_url}/{pet_segment}/uploadImage"
    if metadata is not None:
        url += f"?additionalMetadata={metadata}"
    return url
