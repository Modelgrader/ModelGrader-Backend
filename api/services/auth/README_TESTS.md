# Auth Service Unit Tests

This document describes the comprehensive unit tests created for the Auth Service module.

## Test Coverage

The test suite covers three main areas:

### 1. Abstract Base Class Tests (`TestAuthService`)
- Validates that `AuthService` cannot be instantiated directly
- Ensures abstract methods are properly defined

### 2. Implementation Tests (`TestAuthServiceImpl`)
- **Initialization Tests**: Verifies proper setup of dependencies
- **Token Verification Tests**: Comprehensive testing of `verifyToken()` method
- **Account Retrieval Tests**: Thorough testing of `getAccountByToken()` method

### 3. Integration Tests (`TestAuthServiceIntegration`)
- Real database interactions
- End-to-end functionality validation

## Test Scenarios Covered

### Valid Token Tests
- ✅ Valid, non-expired tokens
- ✅ Tokens expiring exactly at current time (edge case)

### Invalid Token Tests
- ✅ Expired tokens
- ✅ Non-existent tokens
- ✅ `None` token values
- ✅ Empty string tokens

### Error Handling Tests
- ✅ `Account.DoesNotExist` exceptions
- ✅ Database connection issues (via mocking)

### Dependency Interaction Tests
- ✅ `AuthRepository.getByToken()` method calls
- ✅ `model_to_dict()` function usage
- ✅ `time()` function mocking for consistent testing

## Running the Tests

### Option 1: Using Django's Test Runner
```bash
cd /Users/kanon.che/Documents/ModelGrader-Backend
python manage.py test api.services.auth.test_auth_service
```

### Option 2: Using the Custom Test Runner
```bash
cd /Users/kanon.che/Documents/ModelGrader-Backend
python run_auth_tests.py
```

### Option 3: Running Specific Test Classes
```bash
# Run only unit tests (no database)
python manage.py test api.services.auth.test_auth_service.TestAuthService

# Run only implementation tests
python manage.py test api.services.auth.test_auth_service.TestAuthServiceImpl

# Run only integration tests
python manage.py test api.services.auth.test_auth_service.TestAuthServiceIntegration
```

## Test Structure

```
api/services/auth/
├── auth_service.py          # Implementation under test
├── test_auth_service.py     # Unit tests
└── README_TESTS.md         # This documentation
```

## Mock Objects and Dependencies

The tests use comprehensive mocking to isolate the unit under test:

- **AuthRepository**: Mocked to control database responses
- **time()**: Mocked for consistent time-based testing
- **model_to_dict()**: Mocked to verify proper usage
- **Account model**: Real instances used in controlled scenarios

## Test Data

Test accounts are created with various expiration states:
- Valid tokens (expire in future)
- Expired tokens (expired in past)
- Edge case tokens (expire exactly at test time)

## Expected Test Results

All tests should pass when the auth service is functioning correctly. The test suite includes:

- **19 unit tests** for the implementation
- **6 integration tests** for database interactions
- **3 abstract class validation tests**

**Total: 28 test cases**

## Maintenance

When modifying the auth service:

1. Run the test suite before changes
2. Update tests if interface changes
3. Add new tests for new functionality
4. Ensure all tests pass after modifications

## Dependencies

Required packages for testing:
- `django`
- `unittest` (built-in)
- `unittest.mock` (built-in)

The tests are designed to be self-contained and not require external services or specific database states.
