# Nanoko Python API Library

This is a Python library for the Nanoko API, including both synchronous and asynchronous APIs for question bank, user, LLM, and service.

## Installation

```bash
pip install nanoko-python
```

## Usage

```python
from nanoko import Nanoko

nanoko = Nanoko(base_url="http://localhost:25324")

# Login
nanoko.user.login(username="username", password="password")

# Get user information
user = nanoko.user.me()
print(user)
```
