# Installation

## Prerequisites

- Python 3.8+
- An OpenAI API key

## Install with pip

```bash
pip install openai-toolchain
```

## Install from source

1. Clone the repository:

   ```bash
   git clone https://github.com/bemade/openai-toolchain.git
   cd openai-toolchain
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install with development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

## Verify Installation

```python
import openai_toolchain
print(openai_toolchain.__version__)
```

## Configuration

Set your OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY='your-api-key-here'
```

Or pass it when initializing the client:

```python
from openai_toolchain import OpenAIClient

client = OpenAIClient(api_key="your-api-key-here")
```

## Next Steps

- [Tutorial](tutorial.md) - Learn how to use OpenAI Toolchain
- [API Reference](reference/) - Detailed API documentation
