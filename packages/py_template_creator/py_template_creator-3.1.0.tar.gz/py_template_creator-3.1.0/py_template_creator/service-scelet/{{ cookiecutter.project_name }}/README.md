# {{ cookiecutter.project_name }}

This document provides steps to set up, start, and test the **{{ cookiecutter.project_name }}**.

## **Setup Service**

1. Navigate to the `{{ cookiecutter.project_name }}` directory:
   ```bash
   cd {{ cookiecutter.project_name }}
   ```

2. Install the required packages for the project:
   ```bash
   make env
   ```

---

## **Start Service**

1. **Stop Docker Container for This Service**  
   Ensure the Docker container for the {{ cookiecutter.project_name }} is stopped:
   ```bash
   cd <project root>
   docker-compose stop {{ cookiecutter.project_name }}
   ```

2. **Start the Service in the Virtual Environment**  
   Run the service locally:
   ```bash
   cd {{ cookiecutter.project_name }}
   make run
   ```

---

## **Run Tests**

1. Run all tests:
   ```bash
   make test
   ```

2. Run all tests in a specific file:
   ```bash
   make test module="package/tests/test_health.py"
   ```

3. Run a single test in a specific file:
   ```bash
   make test module="package/tests/test_health.py::HealthTest::test_health"
   ```

---