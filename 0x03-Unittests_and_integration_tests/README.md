# 0x03. Unittests and Integration Tests

This directory contains Python unit and integration tests as part of the **ALX Backend Specialization** program.

The goal is to gain hands-on experience with:

- Writing unit tests using `unittest`
- Using `parameterized` to simplify test cases
- Mocking functions and external dependencies
- Testing APIs and integration with external services

---

## 📁 Files

### `utils.py`
Contains utility functions including:

- `access_nested_map(nested_map, path)`: A function to access values from nested dictionaries.

### `test_utils.py`
Unit tests for functions in `utils.py`, particularly:

- `TestAccessNestedMap`: A test class that verifies `access_nested_map` works correctly using parameterized tests.

---

## 🚀 How to Run Tests

Install the dependencies:

```bash
pip install parameterized
