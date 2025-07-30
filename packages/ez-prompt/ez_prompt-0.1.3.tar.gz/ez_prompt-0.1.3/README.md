# ezprompt

An easy-to-use library for creating and sending prompts to various LLMs.

## Features (Planned)

- Simple prompt definition using Markdown and Jinja templating.
- Automatic input validation against prompt templates.
- Model selection from a wide range of providers.
- Context length validation with suggestions for suitable models.
- Cost estimation before sending prompts.
- Up-to-date model information (context size, pricing).
- Asynchronous support for concurrent prompt execution.

## Installation

```bash
pip install ez-prompt
```

## Basic Usage

See the supported models by running:

```python
from ez_prompt import list_models

list_models()
```

Then, create a template, choose your model, provide an API key, format and send. Sending is asynchronous by default.

```python
import asyncio
from ez_prompt import Prompt

async def main():
    # Define a prompt template (details TBD)
    prompt_template = """
    Translate the following text from {{ source_lang }} to {{ target_lang }}:

    {{ text }}
    """

    # Initialize the prompt
    my_prompt = Prompt(
        template=prompt_template,
        model="gpt-3.5-turbo",
        api_key="your_api_key"
    )

    # Format the prompt with inputs
    my_prompt.format(
        inputs={"source_lang": "English", "target_lang": "French", "text": "Hello, world!"},
    )

    # Send the prompt
    response = await my_prompt.send()
    print(f"Model response: {response}")

if __name__ == "__main__":
    # Required environment variables (e.g., OPENAI_API_KEY)
    # Set them according to the model provider you use.
    asyncio.run(main())

```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
