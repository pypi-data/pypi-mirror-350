# Heroku MIA SDK for Python

A Python SDK for Heroku's Managed Inference API (MIA), providing easy access to AI models through a LangChain-compatible interface.

## 🚀 Quick Start

### Installation

```bash
pip install heroku-mia-sdk
```

### Basic Usage

```python
import os
from heroku_mia_sdk import HerokuMia

# Set your environment variables
os.environ["HEROKU_API_KEY"] = "your-api-key"
os.environ["INFERENCE_MODEL_ID"] = "claude-3-7-sonnet"
os.environ["INFERENCE_URL"] = "https://us.inference.heroku.com"

# Create client and send message
client = HerokuMia()
response = client.invoke("What is the capital of France?")
print(response.content)
```

## 📋 Features

- **LangChain Compatible**: Works seamlessly with LangChain ecosystem
- **Streaming Support**: Real-time response streaming
- **Tool Calling**: Function calling capabilities
- **Async Support**: Full async/await support
- **Type Safe**: Built with Pydantic for type safety

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `HEROKU_API_KEY` | Your Heroku API key | Yes |
| `INFERENCE_MODEL_ID` | Model to use (e.g., `claude-3-7-sonnet`) | Yes |
| `INFERENCE_URL` | Inference endpoint URL | Yes |

### Getting Your API Key

1. Log in to your Heroku account
2. Navigate to Account Settings
3. Generate an API key
4. Use the format: `inf-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`

## 📖 Examples

### Basic Chat

```python
from heroku_mia_sdk import HerokuMia

client = HerokuMia()
response = client.invoke("Hello, how are you?")
print(response.content)
```

### Streaming Chat

```python
from heroku_mia_sdk import HerokuMia

client = HerokuMia()
for chunk in client.stream("Tell me a story"):
    print(chunk.content, end="", flush=True)
```

### Chat with Tools

```python
from heroku_mia_sdk import HerokuMia
from langchain_core.tools import tool

@tool
def get_weather(city: str) -> str:
    """Get weather for a city."""
    return f"The weather in {city} is sunny and 25°C"

client = HerokuMia()
client = client.bind_tools([get_weather])
response = client.invoke("What's the weather in Paris?")
```

### Multiple Messages

```python
from heroku_mia_sdk import HerokuMia
from langchain_core.messages import HumanMessage, SystemMessage

client = HerokuMia()
messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="What is Python?")
]
response = client.invoke(messages)
print(response.content)
```

## 🛠️ Development

### Local Installation

```bash
git clone https://github.com/heroku/heroku-mia-sdk-python
cd heroku-mia-sdk-python/python
pip install -e .
```

### Running Examples

```bash
# Set environment variables
export HEROKU_API_KEY="your-api-key"
export INFERENCE_MODEL_ID="claude-3-7-sonnet"
export INFERENCE_URL="https://us.inference.heroku.com"

# Run examples
python examples/example_chat_basic.py
python examples/example_chat_streaming.py
python examples/example_chat_tools.py
```

### Development Dependencies

```bash
pip install -e ".[dev]"
```

## 📚 API Reference

### HerokuMia Class

The main client class for interacting with Heroku's Managed Inference API.

#### Methods

- `invoke(input)` - Send a message and get response
- `stream(input)` - Stream response chunks
- `bind_tools(tools)` - Bind tools for function calling
- `with_config(config)` - Configure client settings

#### Parameters

- `model_id` (str): Model identifier
- `api_key` (str): Heroku API key  
- `base_url` (str): API base URL
- `temperature` (float): Response randomness (0.0-1.0)
- `max_tokens` (int): Maximum response tokens

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

## 🆘 Support

- [GitHub Issues](https://github.com/heroku/heroku-mia-sdk-python/issues)
- [Heroku Support](https://help.heroku.com/)

## 🔗 Related

- [Heroku Platform](https://heroku.com)
- [LangChain](https://langchain.com)
- [Heroku AI Documentation](https://devcenter.heroku.com/categories/ai)

