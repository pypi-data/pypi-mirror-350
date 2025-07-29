# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['code_agent', 'code_agent.src', 'code_agent.tests']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['opencursor = code_agent.cli_entry:entry_point']}

setup_kwargs = {
    'name': 'opencursor',
    'version': '0.0.10',
    'description': 'An AI-powered code agent for workspace operations',
    'long_description': '# OpenCursor\n\nAn AI-powered code agent for workspace operations.\n\n## Features\n\n- Chat with an AI coding agent in autonomous or interactive mode\n- Direct LLM chat without tools\n- File context management (add, drop, clear)\n- Repository mapping\n- Focus on specific files\n- Workspace directory selection\n\n## Installation\n\n### Using Poetry (recommended)\n\n```bash\n# Clone the repository\ngit clone https://github.com/yourusername/opencursor.git\ncd opencursor\n\n# Install with Poetry\npoetry install\n```\n\n### Using pip\n\n```bash\npip install git+https://github.com/yourusername/opencursor.git\n```\n\n## Usage\n\nOnce installed, you can use OpenCursor from the command line:\n\n```bash\n# Basic usage\nopencursor -q "Create a simple Flask app"\n\n# Specify a workspace directory\nopencursor -w /path/to/workspace -q "Fix the bug in app.py"\n\n# Use a different model\nopencursor -m "gpt-4" -q "Refactor the authentication module"\n\n# Run in interactive mode\nopencursor -i -q "Create a React component"\n```\n\n### Command-line Options\n\n- `-w, --workspace`: Path to the workspace directory (default: current directory)\n- `-q, --query`: Query to process (required)\n- `-m, --model`: LLM model to use (default: qwen3_14b_q6k:latest)\n- `-H, --host`: Ollama API host URL (default: http://192.168.170.76:11434)\n- `-i, --interactive`: Run in interactive mode (one tool call at a time)\n\n## Development\n\n### Setup\n\n```bash\n# Clone the repository\ngit clone https://github.com/yourusername/opencursor.git\ncd opencursor\n\n# Install dependencies\npoetry install\n\n# Run tests\npoetry run pytest\n```\n\n### Project Structure\n\n```\nopencursor/\n├── code_agent/\n│   ├── src/\n│   │   ├── agent.py      # Main agent implementation\n│   │   ├── llm.py        # LLM client\n│   │   ├── prompts.py    # System prompts\n│   │   ├── tools.py      # Tool implementations\n│   │   └── ...\n│   ├── cli.py            # Command-line interface\n│   └── __init__.py\n├── tests/\n├── pyproject.toml\n└── README.md\n```\n\n## License\n\nMIT\n\n### UI Components\n\n- **Chat History**: Shows the conversation between you and the AI\n- **Message Input**: Type your messages here\n- **Tool Selection**: Choose which tool to use for processing your message\n- **Workspace Path**: Set the directory to work with\n- **Context Information**: Shows which files are currently in context\n- **Update Context**: Refreshes the context information\n- **Clear Chat**: Clears the chat history\n\n### Available Tools\n\n- **agent (autonomous)**: Agent works step-by-step without user interaction\n- **agent (interactive)**: Agent performs one tool call at a time, waiting for user input\n- **chat (LLM only)**: Chat with the LLM directly without using tools\n- **add file**: Add a file to the context (provide file path in message)\n- **drop file**: Remove a file from the context (provide file path in message)\n- **clear context**: Remove all files from the context\n- **repo map**: Show the files in the current workspace\n- **focus on file**: Add a file to context and show its contents\n\n## Customization\n\nYou can modify the model and host settings in the `main()` function of `gradio_ui.py`.',
    'author': 'Kammari Santhosh',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/santhosh/',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
