# Meta AI API 

> Fork of [meta-ai-api](https://github.com/Strvm/meta-ai-api) with support for tool-calling

A Python package for interacting with the Meta AI API, including authentication, messaging, and tool-call capabilities.

---

## Features
- Normal Text based chat
- Tool-call support for advanced integrations

---

## Installation

```bash
pip install meta_ai_api_tool_call
```

---

## Usage

### Basic Example
```python
from meta_ai_api_tool_call import MetaAI

# For unauthenticated (public) access
ai = MetaAI()
response = ai.prompt("Hello Meta!")
print(response)

# For authenticated access (recommended for full features)
ai = MetaAI(fb_email="your_fb_email", fb_password="your_fb_password")
response = ai.prompt("Hello with login!")
print(response)
```

### Tool Call Example
```python
from meta_ai_api_tool_call import MetaAI

def add(a: int, b: int) -> int:
    """Adds two numbers."""
    return a + b

ai = MetaAI()
tools = [add]
response = ai.prompt("Use the add tool to add 2 and 3", tools=tools)
print(response)
```

---


## Contributing
Contributions are welcome! Please open issues or pull requests on [GitHub](https://github.com/mr-destructive/meta_ai_api_tool_call).

---

## License

Follow the [meta-ai](https://www.meta.ai/) and Meta's [terms and policies](https://www.facebook.com/policies_center/) for usage.
---

## Disclaimer
This project is not affiliated with Meta, Facebook, or their partners. Use at your own risk and comply with all applicable terms of service.
