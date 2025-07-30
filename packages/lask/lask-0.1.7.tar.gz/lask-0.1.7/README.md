(Still under development)

# lask

Ask LLMs right from the terminal.

Supports multiple providers like OpenAI, Anthropic, AWS Bedrock, and Azure OpenAI


## Usage
Ensure you have `OPENAI_API_KEY` in your environment variables or configure it in `~/.lask-config`, then you can use `lask` to send prompts to the LLM.

```bash
lask What movie is this quote from\? \"that still only counts as one\"
```

## Features

- Simple command-line interface to send prompts to multiple LLM providers
- Support for OpenAI, Anthropic, AWS Bedrock, and more.
- Customizable models and parameters for each provider
- Minimal dependencies (only requires the `requests` library, and `boto3` for AWS)
- Easy installation via pip
- Direct output to your terminal
- Streaming responses for real-time output

## Installation

### Using pip (recommended)

```bash
pip install lask
```

(For dev, do `pip install .`)

For a user-specific installation:

```bash
pip install --user lask
```

### From source

1. Clone the repository:
   ```bash
   git clone https://github.com/Open-Source-Lodge/lask.git
   ```

2. Navigate to the directory:
   ```bash
   cd lask
   ```

3. Install the package:
   ```bash
   pip install -e .
   ```

## Setup

Before using lask, you need to set up API keys for your preferred provider:

1. Get an API key from your chosen provider:
   - [OpenAI](https://platform.openai.com/api-keys)
   - [Anthropic](https://console.anthropic.com/)
   - AWS Bedrock (uses your AWS credentials)

2. Create a configuration file at `~/.lask-config` in INI format:

   ```ini
   [default]
   provider = openai  # Options: openai, anthropic, aws, azure

   [openai]
   # OpenAI-specific settings
   api_key = your-api-key-here
   model = gpt-4.1

   [anthropic]
   # Anthropic-specific settings
   api_key = your-api-key-here
   model = claude-3-opus-20240229

   [aws]
   # AWS Bedrock settings
   api_key = your-api-key-here
   model_id = anthropic.claude-3-sonnet-20240229-v1:0
   region = us-east-1

   [azure]
   # Azure OpenAI settings
   api_key = your-azure-api-key
   resource_name = your-resource-name
   deployment_id = your-deployment-id
   ```

   This INI configuration file allows you to set your preferred provider, API keys, and customize the models and parameters for each provider.

   An example configuration file with comments is available in the `examples/example.lask-config` file.

3. Alternatively, set the appropriate environment variable:

   **For OpenAI (default provider):**
   ```bash
   export OPENAI_API_KEY='your-api-key-here'
   ```

   **For Anthropic:**
   ```bash
   export ANTHROPIC_API_KEY='your-api-key-here'
   ```

   **For AWS Bedrock:**
   Ensure your AWS credentials are properly configured.

   **For Azure OpenAI:**
   ```bash
   export AZURE_OPENAI_API_KEY='your-api-key-here'
   ```

   To make these permanent, add the export line to your `~/.bashrc`, `~/.zshrc`, or equivalent shell configuration file.

   **Windows users** can use `set` (CMD) or `$env:` (PowerShell) instead of `export`.


## API Key Issues

If you see an error about the API key:

1. Ensure you've configured the API key in the `~/.lask-config` file
2. Alternatively, double-check that you've correctly set the appropriate environment variable for your chosen provider:
   - OpenAI: `OPENAI_API_KEY`
   - Anthropic: `ANTHROPIC_API_KEY`
   - AWS: Check your AWS credentials configuration
3. Verify your API key is valid and has enough credits


## Configuration

You can find a fully commented example configuration file in the `examples/example.lask-config` directory of this repository. Copy it to your home directory as `~/.lask-config` and customize it to your needs.

### Selecting a Provider

Set your preferred provider in the `[default]` section:

```ini
[default]
provider = openai  # Options: openai, anthropic, aws
```

### Streaming Configuration

By default, responses are streamed in real-time to your terminal. You can disable streaming in your configuration file:

```ini
[openai]
streaming = false  # Disable streaming for OpenAI

[anthropic]
streaming = false  # Disable streaming for Anthropic
```

When streaming is enabled, you'll see the response appearing in real-time as it's generated. When disabled, you'll get the complete response only after it's fully generated.

### Provider-specific Configuration

Each provider has its own section where you can set provider-specific options:

#### OpenAI

```ini
[openai]
api_key = your-openai-api-key
model = gpt-4.1
temperature = 0.7
max_tokens = 2000
streaming = true  # Enable streaming (this is the default)
```

#### Anthropic

```ini
[anthropic]
api_key = your-anthropic-api-key
model = claude-3-opus-20240229
temperature = 0.7
max_tokens = 4096
streaming = true  # Enable streaming (this is the default)
```

#### AWS Bedrock

```ini
[aws]
model_id = anthropic.claude-3-sonnet-20240229-v1:0
region = us-east-1
temperature = 0.7
max_tokens = 4096
```

#### Azure OpenAI

```ini
[azure]
api_key = your-azure-api-key
resource_name = your-resource-name
deployment_id = your-deployment-id
api_version = 2023-05-15
temperature = 0.7
max_tokens = 2000
```

## Developing

### Dependencies
This repo uses `uv` for running scripts and building the package. [uv install instruction](https://docs.astral.sh/uv/getting-started/installation/)

To install the development dependencies, run:
```bash
uv sync
```

### Build
To build the package, run:

```bash
uv build
```

### Install for development
To install the package in development mode, run:

```bash
pip install dist/lask-0.1.0-py3-none-any.whl
```

or

```bash
pip install -e .
```
With the `-e` flag, you can edit the source code and see changes immediately without reinstalling.


If you want to use AWS Bedrock, also install boto3:

```bash
pip install boto3
```
(I have not tested aws yet, so please report any issues you find)

## License

GNU General Public License v3.0 (GPL-3.0)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
