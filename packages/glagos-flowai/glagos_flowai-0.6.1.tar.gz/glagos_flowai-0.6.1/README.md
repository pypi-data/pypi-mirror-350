# FlowAI

FlowAI is a Python-based CLI tool that helps developers streamline their development workflow by automating common tasks using LLMs (Language Learning Models).

## Features

- Generate detailed commit messages from git diffs
- Create comprehensive pull request descriptions
- Perform automated code reviews
- Interactive chat mode with streaming support
- Web search capability with Gemini models
- Thinking mode for Gemini 2.5 models
- Support for multiple LLM providers:
  - OpenAI
  - Anthropic
  - Groq
  - Gemini
  - Ollama
- Cross-platform compatibility (Windows, Mac, Linux)
- Markdown rendering in terminal
- Streaming responses for real-time feedback
- Configurable output formatting per command

## Command System

FlowAI uses a powerful command system to automate common tasks. Commands are defined in `~/flowai-prompts/prompt-index.txt` and can be customized to your needs.

### Command Features
- Pre-configured context gathering
- Template-based prompts
- Interactive user input
- Platform-specific variants (Windows/Unix)
- Configurable output formatting:
  - `markdown` - Rich formatted output (default)
  - `raw` - Plain text output (ideal for commit messages, PR descriptions)

### Example Commands
```bash
# Generate a commit message for staged changes (raw output)
flowai --command staged-commit-message

# Review code changes (markdown formatted)
flowai --command staged-code-review

# Create PR description (raw output)
flowai --command pull-request
```

## Chat Mode Features

FlowAI's chat mode is a powerful way to interact with the AI assistant. You can:

1. Start a direct chat session:
```bash
flowai --chat
```

2. Turn any command into a chat session by adding `--chat`:
```bash
# Start with a code review and continue chatting about it
flowai --command staged-code-review --chat

# Generate a commit message and discuss it
flowai --command staged-commit-message --chat

# Create a PR description and refine it through chat
flowai --command pull-request --chat
```

When using `--chat` with a command, FlowAI will:
1. Execute the command normally first
2. Use the command's output as context for a new chat session
3. Allow you to discuss, refine, or ask questions about the output
4. Keep the original context (e.g., git diff, code changes) available for reference

### Chat Features
- Stream mode toggle (`/stream`, `/stream on`, `/stream off`)
- Web search capability with Gemini models
- Thinking mode for Gemini 2.5 models
- Token usage tracking
- Real-time response streaming
- Command system for common operations
- Chat history persistence
- Markdown rendering
- Loading indicators with timing information

### Chat Commands
- `/help` - Show available commands
- `/quit` - Exit chat mode
- `/clear` - Clear chat history
- `/stream` - Toggle stream mode
- `/stream on` - Enable stream mode
- `/stream off` - Disable stream mode
- `/save` - Save the entire chat session to a markdown file
- `/save last` - Save only the last response
- `/add-file <path>` - Upload and cache a file (Gemini 1.5+ models only)
- `/list-files` - Show all files cached in this session

## Known Issues

We are actively working on fixing several issues in the chat mode:
- Ctrl+C handling may not work correctly in some scenarios
- Status display (tokens and stream mode) may not show correctly in some terminals
- Double "Generating response..." message may appear
- Some formatting issues with streamed responses
- Terminal compatibility issues with certain commands

Please check our [TODO.md](TODO.md) file for a complete list of issues being tracked.

## Installation

```bash
pip install flowai
```

## Configuration

Run the initial setup:
```bash
flowai --init
```

This will guide you through:
1. Setting up API keys
2. Choosing your default model
3. Configuring stream mode preferences

## Usage

### Basic Commands
```bash
# Start chat mode
flowai --chat

# pipe output into flowai as context
git diff | flowai "summarise these changes in 1 paragraph"

# ask any question
flowai "how do i do a git rebase? Is it dangerous? Be concise"

# Generate commit message for staged changes (raw output)
flowai --command staged-commit-message

# Review staged changes (markdown formatted)
flowai --command staged-code-review

# Get help (markdown formatted)
flowai --command help

# Get specific help on any flowai feature
flowai --command help "how do i create a custom command that will work in windows and unix style platforms?"

# Use web search (only works with Gemini models)
flowai --web-search "What are the latest developments in quantum computing?"

# Enable thinking mode for Gemini 2.5 models
flowai --model gemini/gemini-2.5-pro --thinking-budget 2048 "Analyze this code for security issues"
```

### Advanced Features

#### Web Search
FlowAI supports web search capabilities with Google's Gemini models, allowing you to access up-to-date information from the internet.

```bash
# Enable web search (only works with Gemini models)
flowai --web-search "What are the latest developments in quantum computing?"

# Use in chat mode
flowai --chat --web-search

# Combine with commands
flowai --command help --web-search "What are the latest features in FlowAI?"
```

When web search is enabled:
- The current date and time are included in the prompt
- The AI will cite its sources in a dedicated "Sources" section
- Citations include webpage titles and URLs
- Only works with Gemini models (automatically disabled for other models)

#### Thinking Mode (Gemini 2.5 Models)
Gemini 2.5 models support a "thinking mode" that allows the AI to perform more thorough reasoning before responding.

```bash
# Enable thinking mode with a specific budget (1024+ recommended)
flowai --model gemini/gemini-2.5-pro --thinking-budget 2048 "Analyze this code for security issues"

# Use in chat mode
flowai --chat --thinking-budget 2048

# Combine with commands
flowai --command code-review --thinking-budget 2048
```

Thinking mode:
- Allows the AI to perform more thorough reasoning
- Higher budgets (1024+) enable more complex thinking
- Setting to 0 disables thinking mode
- Status is displayed in the terminal output
- Only works with Gemini 2.5 models

#### Image Generation
FlowAI supports generating images using Google's Gemini models. You can create images from text prompts and refine them interactively.

```bash
# Basic image generation
flowai --create-image "A futuristic spaceship hovering over the surface of Mars"

# Use a reference image to guide generation
flowai --create-image "A futuristic spaceship hovering over the surface of Mars" --reference-image path/to/image.jpg

# Use an image from clipboard as reference
flowai --create-image "A futuristic spaceship hovering over the surface of Mars" --reference-from-clipboard

# Enter interactive chat mode to refine the image
flowai --create-image "A futuristic spaceship hovering over the surface of Mars" --chat
```

You can also provide a reference image without explicitly using the `--create-image` flag:
```bash
# These automatically enable image generation mode
flowai --reference-image path/to/image.jpg "A futuristic spaceship hovering over the surface of Mars"
flowai --reference-from-clipboard "A futuristic spaceship hovering over the surface of Mars"
```

In interactive chat mode, you can:
- Type refinement instructions to modify the current image
- Use `/help` to see available commands
- Use `/reference <path>` to set a new reference image
- Use `/clipboard` to use clipboard image as reference
- Type `/quit` to exit chat mode

For more details, see [Image Generation Guide](flowai/docs/image_generation.md).

#### File Upload and Caching
FlowAI can upload PDF, image, or text files to Google Gemini 2.5 and cache them for a chat session.

```bash
# Upload a file and immediately ask a question
flowai --files report.pdf "summarise this file"

# Start a chat session with cached files
flowai --files notes.txt --chat
```

While chatting you can add more files using `/add-file <path>` and list cached files with `/list-files`.

**Note:** Files smaller than 1024 tokens are uploaded directly (not cached) but work identically. The system automatically chooses the best method.

### Output Formatting
Commands can be configured to output in either markdown or raw format:
- Markdown format: Rich text with formatting, ideal for reviews and documentation
- Raw format: Plain text, perfect for commit messages and PR descriptions

You can:
1. Set format per command in `prompt-index.txt`
2. Override with `--no-markdown` flag
3. Default to markdown if not specified

### Chat Commands
- `/help` - Show available commands
- `/quit` - Exit chat mode
- `/clear` - Clear chat history
- `/stream` - Toggle stream mode
- `/stream on` - Enable stream mode
- `/stream off` - Disable stream mode
- `/save` - Save the entire chat session to a markdown file
- `/save last` - Save only the last response
- `/add-file <path>` - Upload and cache a file (Gemini 1.5+ models only)
- `/list-files` - Show all files cached in this session

## Contributing

Please see our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

## License

MIT License - see [LICENSE](LICENSE) for details