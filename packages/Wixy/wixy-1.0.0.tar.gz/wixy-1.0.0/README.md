# 📦 WixyPy – Python SDK for Nest API

[![License](https://img.shields.io/github/license/N3x74/Wixy)](LICENSE)
[![PyPI](https://img.shields.io/pypi/v/wixypy.svg)](https://pypi.org/project/wixy/)
[![Python](https://img.shields.io/pypi/pyversions/wixypy)](https://pypi.org/project/wixy/)

**WixyPy** is a lightweight and modern Python SDK for communicating with the [Nest API](https://nestcode.org/).
It supports both **sync** and **async** usage automatically, offers versioned endpoints, and features error-safe JSON decoding with an elegant interface.

---

## 🚀 Features

* 🔁 Auto sync/async mode detection
* 🔑 Easy API key setup
* 🔧 Versioned endpoint routing
* ⚠️ Built-in error handling
* ⚡ Powered by `httpx`
* 🧪 Typed and clean design (Python 3.7+)

---

## 📦 Installation

```bash
pip install wixy
```

> Requires Python 3.7 or higher

---

## 🛠 Usage

### 🔸 Synchronous Example

```python
from wixy import Api

api = Api("your_api_key_here")

response = api.version(1).get("endpoint-name", {
    "param1": "value1",
    "param2": "value2"
})

print(response)
```

### 🔹 Asynchronous Example

```python
import asyncio
from wixy import Api

async def main():
    api = Api("your_api_key_here")
    response = await api.version(1).get("endpoint-name", {
        "param1": "value1",
        "param2": "value2"
    })
    print(response)

asyncio.run(main())
```

---

## 📘 Example

```python
api = Api("your_api_key")
response = api.version(1).get("ChatGPT", {"q": "Hello"})

if response["status_code"] == 200:
    print("Result:", response["body"].get("detail", {}).get("data", "No result"))
else:
    print("Error:", response.get("error", "Unknown error"))
```

---

## 📥 Response Format

### ✅ On success:
```python
{
    "status_code": 200,
    "body": { ...parsed JSON... }
}
```

### ❌ On failure:
If the error response is JSON:
```python
{
    "status_code": 400,
    "body": { ...error details... },
    "error": "Httpx exception message"
}
```

If the error is plain text:
```python
{
    "status_code": 500,
    "body": "Server Error",
    "error": "Httpx exception message"
}
```

---

## 📚 API Versioning

To target a specific API version:

```python
api.version(1).get("endpoint")
api.version(2).get("another-endpoint")
```

Internally, the version changes the request path to:
```
https://open.nestcode.org/apis-{version}/{endpoint}
```

---

## ✅ Requirements

- Python 3.7
- httpx 0.27

---

## 📄 License

This project is open-sourced under the [MIT license](LICENSE).

---

## 🔗 Links

- 🧠 Nest API: [https://nestcode.org/](https://nestcode.org/)
- 📦 PyPI: [https://pypi.org/project/wixy/](https://pypi.org/project/wixy/)
- 🧑‍💻 Author: [@N3x74](https://github.com/N3x74)
- ☁️ telegram: [@N3x74](https://t.me/N3x74)
