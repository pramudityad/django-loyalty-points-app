# Running Tests with Docker

This guide covers how to run the test suite for the Loyalty Points System within the Docker environment.

## Prerequisites

- Docker and Docker Compose installed and configured
- The application containers should be running (via `docker-compose up -d`)

## Running the Test Suite

### Run All Tests

To run the entire test suite:

```bash
docker-compose exec loyalty_web pytest
```

### Run Tests with Coverage Report

To generate a coverage report:

```bash
docker-compose exec loyalty_web pytest --cov=. --cov-report=term-missing --cov-report=html
```

This will:
- Run all tests
- Generate a terminal coverage report showing missing lines
- Create an HTML coverage report in the `htmlcov` directory

To view the HTML coverage report, you'll need to access the files from the container:

```bash
# Copy the coverage report from the container to your local machine
docker cp loyalty_web:/app/htmlcov ./htmlcov

# Then open htmlcov/index.html in your browser
```

### Run Tests for Specific Apps

To test only a particular app:

```bash
# Test users app
docker-compose exec loyalty_web pytest users/

# Test points app
docker-compose exec loyalty_web pytest points/

# Test transactions app
docker-compose exec loyalty_web pytest transactions/

# Test vouchers app
docker-compose exec loyalty_web pytest vouchers/
```

### Run a Specific Test File

To run tests from a specific file:

```bash
docker-compose exec loyalty_web pytest users/test_users_models.py
```

### Run a Specific Test Class or Method

```bash
# Run a specific test class
docker-compose exec loyalty_web pytest users/test_users_models.py::TestUserModel

# Run a specific test method
docker-compose exec loyalty_web pytest users/test_users_models.py::TestUserModel::test_update_membership_status_gold
```

## Test Configuration

The test configuration is defined in `pytest.ini`, which includes:

- Minimum coverage threshold (80%)
- Path settings
- Warning filters

## Troubleshooting Test Issues

### Database-Related Test Issues

If you encounter database-related issues during testing:

```bash
# Reset the test database
docker-compose exec loyalty_db psql -U loyalty_user -d loyalty_db -c "DROP DATABASE test_loyalty_db;"
```

Django's test runner will recreate the test database as needed.

### Missing Test Dependencies

If tests fail due to missing dependencies:

1. Add the required packages to `requirements.txt`
2. Rebuild the container:
   ```bash
   docker-compose build loyalty_web
   docker-compose up -d
   ```

### Warehouse Database Mock

The tests use mocking to simulate warehouse database operations. If you see issues related to the warehouse database during testing, check that the mocking is properly configured in the test files.

## Continuous Integration

To integrate these tests into a CI/CD pipeline, you can use this command:

```bash
docker-compose run --rm loyalty_web pytest --cov=. --cov-report=xml --cov-fail-under=80
```

This will:
- Run the tests in a temporary container
- Generate a coverage XML report (compatible with most CI systems)
- Fail if coverage is below 80%

## Adding New Tests

When adding new tests:

1. Create test files following the naming convention (`test_*.py`)
2. Place them in the appropriate app directory
3. Ensure they use the fixtures defined in `conftest.py` where appropriate
4. Run the specific test file to verify it works:
   ```bash
   docker-compose exec loyalty_web pytest path/to/your/new_test_file.py -v
   ```