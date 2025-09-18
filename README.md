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

## Allure report
```bash
allure generate allure-results -o allure-report --clean
allure open allure-report
```