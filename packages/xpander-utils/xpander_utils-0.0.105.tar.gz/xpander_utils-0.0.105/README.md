Here's a **greatly improved** version of your README, integrating details from your `setup.py` (like updated Python version, full dependency list, extras, etc.), formatted clearly and professionally in Markdown:  

---

# xpander_utils Package Development Guide

## Overview

**`xpander_utils`** is a Python utilities SDK for [xpander.ai](https://www.xpander.ai) services.  
It provides adapters, helpers, and utilities to integrate and enhance the development of AI agents, workflows, and more.

- **Package Name:** `xpander_utils`
- **Version:** `0.0.1`
- **Author:** xpanderAI
- **Email:** dev@xpander.ai
- **License:** MIT License
- **URL:** [https://www.xpander.ai](https://www.xpander.ai)

---

## Installation 

### Install from PyPI

To use the `xpander_utils` package in your project, install it via pip:

```bash
pip install xpander-utils
```

### Install Locally (Development Mode)

If you want to contribute or modify the package, clone the repository and install it locally in editable mode:

```bash
pip install -e .
```

This allows you to make changes to the source code without reinstalling the package after each modification.

---

## Usage Example 

Here's a simple example using `SmolAgentsAdapter` to bridge between **xpander.ai** and **smolagents**:

```python
from smolagents import OpenAIServerModel, ToolCallingAgent
from xpander_utils.sdk.adapters import SmolAgentsAdapter

# API keys
llm_api_key = "{YOUR_LLM_KEY}"
xpander_api_key = "{YOUR_API_KEY}"

# Initialize Xpander agent
xpander = SmolAgentsAdapter(agent_id="{YOUR_AGENT_ID}", api_key=xpander_api_key)

# Initialize model
model = OpenAIServerModel(
    model_id="gpt-4o",
    api_key=llm_api_key
)

# Add a task to Xpander 
prompt = "get the longest tag"
xpander.add_task(input=prompt)

# Build the agent using Xpander's tools
agent = ToolCallingAgent(
    step_callbacks=[xpander.step_callback()],
    tools=xpander.get_tools(),
    model=model,
    prompt_templates={"system_prompt": xpander.get_system_prompt()}
)

# Initialize memory from Xpander
xpander.init_memory(agent=agent)

# Run the agent
result = agent.run(task=prompt, reset=False)
```

---

## Dependencies

The package requires the following libraries:

- `pydantic`
- `loguru`
- `xpander-sdk`
- `httpx`
- `aiosseclient`

### Optional / Extras

Additional functionality can be installed with extras:

| Extra        | Libraries Installed |
| ------------ | -------------------- |
| `smolagents` | `smolagents`          |
| `llama-index`| `llama_index`         |
| `chainlit`   | `chainlit`            |

Example to install with extras:

```bash
pip install "xpander-utils[smolagents]"
```

You can combine extras:

```bash
pip install "xpander-utils[smolagents,llama-index]"
```

---

## Supported Python Versions

This package officially supports **Python >= 3.12.7**.

Ensure you are using a compatible Python version for full functionality.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Development Notes

- Source code is located under the `src/` directory.
- Package discovery is handled via `find_packages(where="src")`.
- `long_description` for the package is directly pulled from `README.md`.

---

Would you also like me to suggest an even more **"pypi-publish-ready"** version that includes badges (like version, license, Python version, pypi status) at the top? 🚀  
It would look very official!  
Want me to generate it too? 🎯