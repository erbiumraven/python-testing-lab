# python-testing-lab
A learning repository for practicing test automation with Python.

## Requirements

- **Python 3.11+** – required only when running tests directly on the host machine  
- **Java 21+** – required only to run tests on the host  
- **Allure CLI** – required only when running tests on the host for generating reports  
- **Docker & Docker Compose** – required only when running tests inside Docker

**Note:** Some tools are only needed if you run tests directly on your host machine. When running tests inside Docker, Python, Java, and Allure CLI are not required on your host. It is recommended to run tests in Docker, as it ensures a consistent environment, avoids dependency conflicts, 
and allows running tests both locally and on remote hosts without manual setup.

## Environment Variables
**PET_BASE_URL** – The base URL of the Petstore API that tests will target.
- If you are running tests against a remote host (like the official Swagger Petstore), set it to the remote API URL.
- If you are running tests locally with your own server, set it to your local server URL.

Example:
```bash
export PET_BASE_URL=https://petstore3.swagger.io/api/v3 # REMOTE HOST
export PET_BASE_URL=http://localhost:8080/api/v3 # LOCAL HOST
```
## Running Tests
### 1. Run tests on a remote host using your local Python environment
- Requires Python, pip, virtual environment etc installed locally.
- Tests will hit the remote API specified by https://petstore3.swagger.io/api/v3.
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

pytest
```
**Note:** **PET_BASE_URL** is optional here.
- If not set or left empty, the tests will default to the remote host: https://petstore3.swagger.io/api/v3.
- You only need to set it if you want to override the default, e.g., for a local server or a different remote host.


### 2. Run tests on a local server using your local Python environment
- Requires Python, pip, virtual environment etc installed locally.
- Tests will hit the local API specified by https://localhost:8080/api/v3.
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

java -jar ./server/pethhttpserver.jar # to run server on localhost
export PET_BASE_URL="http://localhost:8080/api/v3"

pytest
```

### 3. Run tests on a remote host using Docker
- Executes the test suite inside a Docker container against the remote API host.
- No local server is required; **PET_BASE_URL** defaults to the remote host.
```bash
./run_test.sh
```

### 4. Run tests on a local server using Docker
- Executes the test suite inside a Docker container against the local API host.
- A local server is required; **PET_BASE_URL** defaults to the local host.
```bash
./run_test.sh local
```

### 5. Run tests by filter
Each test class is designed to validate a specific API endpoint. To facilitate selective execution, custom pytest markers are applied to each class, enabling tests to be filtered and executed according to the targeted endpoint.
```text
    pet_create: Tests for POST /pet
    pet_delete: Tests for DELETE /pet/{petId}
    pet_get: Tests for GET /pet/{petId}
    pet_status: Tests for GET /pet/findByStatus
    pet_tags: Tests for GET /pet/findByTags
    pet_update: Tests for PUT /pet
    pet_update_form_data: Tests for POST /pet/{petId}
    pet_upload_image: Tests for POST /pet/{petId}/uploadImage
```

To execute only tests for a specific endpoint, use the `-m` option with pytest:

```bash
# Run all tests for POST /pet
pytest -m pet_create

# Run all tests for DELETE /pet/{petId}
pytest -m pet_delete

# Run tests for multiple endpoints (logical OR)
pytest -m "pet_create or pet_update"

# Run tests for all endpoints except a specific one (logical NOT)
pytest -m "not pet_upload_image"
```

In addition to using markers, pytest allows you to run tests selectively by specifying the **class name** or **method name**.

```bash
# Run a specific test method in any class
pytest -k test_create_pet_success

# Run a specific test method in a specific class
pytest -k "TestCreatePet and test_create_pet_success"

# Run multiple test methods across classes
pytest -k "test_create_pet_success or test_create_pet_missing_name"

# Run methods matching multiple conditions in a single class
pytest -k "TestCreatePet and (test_create_pet_success or test_create_pet_validation_error)"

# or

# To run all the tests within a specific test class, you use the following syntax:
pytest tests/api/test_create_pet.py::TestCreatePet

# To run a single test method within a class, you extend the previous syntax to include the method name:
pytest tests/api/test_create_pet.py::TestCreatePet::test_create_pet_with_missing_name
```

## Allure report
```bash
allure generate allure-results -o allure-report --clean
allure open allure-report
```