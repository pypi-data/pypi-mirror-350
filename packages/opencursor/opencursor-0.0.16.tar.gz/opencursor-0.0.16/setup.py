# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['code_agent',
 'code_agent.src',
 'code_agent.tests',
 'code_agent.tests.TestEnvironment.sample']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['opencursor = code_agent.cli_entry:entry_point']}

setup_kwargs = {
    'name': 'opencursor',
    'version': '0.0.16',
    'description': 'An AI-powered code agent for workspace operations',
    'long_description': '# OpenCursor\n\nAn AI-powered code agent for workspace operations with a rich terminal UI.\n\n## Overview\n\nOpenCursor is a terminal-based AI coding assistant that helps you navigate, understand, and modify codebases. It provides both autonomous and interactive agent modes, along with direct LLM chat capabilities. The tool uses a variety of AI-powered features to help you work with code more efficiently.\n\n## Features\n\n### Core Functionality\n- **AI-powered code assistance** with autonomous and interactive modes\n- **Rich terminal UI** with syntax highlighting and markdown support\n- **File context management** to focus on relevant files\n- **Repository exploration** and visualization\n- **Web search integration** for up-to-date information\n- **Code editing and terminal command execution** capabilities\n\n### Agent Modes\n- **Autonomous Mode**: Agent works step-by-step without user interaction\n- **Interactive Mode**: Agent performs one tool call at a time, waiting for user input\n- **Chat Mode**: Direct conversation with the LLM without using tools\n\n### Tools\n- **File Operations**: Read, edit, list, search, and delete files\n- **Code Analysis**: Semantic search, grep search, and code usage analysis\n- **Terminal Operations**: Execute terminal commands\n- **Web Tools**: Search the web and fetch webpage content\n\n## Installation\n\n### Using pip (recommended)\n\n```bash\npip install -U opencursor\n```\n\n### Using Poetry\n\n```bash\n# Clone the repository\ngit clone https://github.com/santhoshkammari/OpenCursor.git\ncd OpenCursor\n\n# Install with Poetry\npoetry install\n```\n\n## Usage\n\nOnce installed, you can use OpenCursor from the command line:\n\n```bash\n# Basic usage\nopencursor\n\n# Specify a workspace directory\nopencursor -w /path/to/workspace\n\n# Use a different model\nopencursor -m "gpt-4"\n\n# Start with an initial query\nopencursor -q "Create a simple Flask app"\n```\n\n### Command-line Options\n\n- `-w, --workspace`: Path to the workspace directory (default: current directory)\n- `-q, --query`: Initial query to process\n- `-m, --model`: LLM model to use (default: qwen3_14b_q6k:latest)\n- `-H, --host`: Ollama API host URL (default: http://192.168.170.76:11434)\n- `--no-thinking`: Disable thinking process in responses\n\n## Commands\n\nOpenCursor provides several commands that you can use within the application:\n\n- `/agent <message>`: Send a message to the agent (autonomous mode)\n- `/interactive <message>`: Send a message to the agent (interactive mode)\n- `/chat <message>`: Chat with the LLM directly (no tools)\n- `/add <filepath>`: Add a file to the chat context\n- `/drop <filepath>`: Remove a file from the chat context\n- `/clear`: Clear all files from the chat context\n- `/repomap`: Show a map of the repository\n- `/focus <filepath>`: Focus on a specific file\n- `/diff <filepath>`: Show git diff for a file with syntax highlighting\n- `/help`: Show help information\n- `/exit`: Exit the application\n\nYou can also use shortcuts:\n- `@filepath` to quickly add a file to the context\n\n\n## Development\n\n### Project Structure\n\n```\nopencursor/\n├── code_agent/\n│   ├── src/\n│   │   ├── app.py         # Main application with UI\n│   │   ├── agent.py       # Agent implementation\n│   │   ├── llm.py         # LLM client\n│   │   ├── tools.py       # Tool implementations\n│   │   ├── prompts.py     # System prompts\n│   │   ├── tool_playwright.py  # Web search tools\n│   │   └── tool_browser.py     # Browser tools\n│   ├── cli_entry.py       # CLI entry point\n│   └── __init__.py\n├── pyproject.toml         # Poetry configuration\n├── requirements.txt       # Dependencies\n└── README.md\n```\n\n### Core Components\n\n1. **OpenCursorApp**: Main application class that handles the UI and command processing\n2. **CodeAgent**: Handles autonomous and interactive modes, manages tool execution\n3. **LLMClient**: Interacts with the Ollama API, manages conversation history\n4. **Tools**: Implements various tools for file operations, code analysis, etc.\n\n### Setting Up Development Environment\n\n```bash\n# Clone the repository\ngit clone https://github.com/santhoshkammari/OpenCursor.git\ncd OpenCursor\n\n# Install dependencies\npip install -e .\n# or with poetry\npoetry install\n\n# Run the application\npython -m code_agent.cli_entry\n```\n\n## Dependencies\n\n- Python 3.11+\n- Rich: Terminal UI and formatting\n- Ollama: LLM API client\n- Prompt_toolkit: Command completion and input handling\n- Playwright: Web search functionality\n- SentenceTransformer: Semantic code search\n\n## License\n\nMIT\n\n## Contributing\n\nContributions are welcome! Please feel free to submit a Pull Request.\n\n1. Fork the repository\n2. Create your feature branch (`git checkout -b feature/amazing-feature`)\n3. Commit your changes (`git commit -m \'Add some amazing feature\'`)\n4. Push to the branch (`git push origin feature/amazing-feature`)\n5. Open a Pull Request',
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
