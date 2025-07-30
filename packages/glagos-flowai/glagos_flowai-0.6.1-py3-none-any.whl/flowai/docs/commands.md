# Using and Creating Commands in FlowAI

G'day! This guide will help you understand and create custom commands in FlowAI. Commands are a ripper way to automate your common workflows without having to remember complex pipe operations and prompt file combinations.

FlowAI now supports advanced features like web search and thinking mode for Gemini models, which can be combined with commands for even more powerful workflows.

## Getting Help

To see all available options and commands:
```bash
flowai
# or
flowai --help
```

To see a list of available commands:
```bash
flowai --command list
```

To get help with a specific command:
```bash
flowai --command help [command-name]
```

## What Are Commands?

Commands are pre-configured combinations of:
- A context-gathering shell command
- A prompt template file
- An optional user input prompt
- An optional output format setting
- An optional user input guide
- Optional advanced features like web search and thinking mode

Instead of typing something like:
```bash
git diff -w --staged | flowai --prompt-file ~/flowai-prompts/code-review.txt "Review these changes"
```

You can simply use:
```bash
flowai --command staged-code-review
```

## Command Configuration

Commands are defined in `~/flowai-prompts/prompt-index.txt` using a CSV format:
```csv
label,description,context_command,prompt_file,format,user_input
"staged-commit-message","Generate commit message","git diff -w --staged","~/flowai-prompts/prompt-commit-message.txt","raw","Brief description of the changes (optional)"
"pull-request","Create PR description","git log [Input branch name]..HEAD","~/flowai-prompts/prompt-pull-request.txt","raw","What is the main purpose of these changes?"
"staged-code-review","Review staged changes","git diff -w --staged","~/flowai-prompts/prompt-code-review.txt","markdown",""
```

Each field serves a specific purpose:
- `label`: The command name used with `--command`
- `description`: A brief explanation shown in the command list
- `context_command`: The shell command that generates the context
- `prompt_file`: The prompt template to use
- `format`: Optional output format ('raw' or 'markdown', defaults to markdown if not specified)
- `user_input`: Optional prompt to guide user input (if no command-line prompt is provided)

## User Input Handling

Commands can handle user input in two ways:

1. Command-line prompt (takes precedence):
```bash
# Provide description directly in command
flowai --command staged-commit-message "Added new format column"
```

2. Interactive prompt (if defined and no command-line prompt):
```bash
# Will prompt: "Brief description of the changes (optional):"
flowai --command staged-commit-message
```

You can:
- Provide input directly in the command (traditional way)
- Let the command prompt you for input (if defined)
- Skip the input entirely (just press Enter when prompted)

## Platform-Specific Commands

FlowAI automatically handles platform compatibility by allowing commands to be prefixed with the target platform:
- `win:` for Windows-specific commands
- `unix:` for Unix-based systems (Mac/Linux)

For example:
```csv
"unix:help","Get help with using FlowAI","cat ~/.config/flowai/docs/*.md","~/flowai-prompts/prompt-help.txt","markdown",""
"win:help","Get help with using FlowAI","type %USERPROFILE%\\.config\\flowai\\docs\\*.md","~/flowai-prompts/prompt-help.txt","markdown",""
```

When you run a command (e.g., `flowai --command help`), FlowAI automatically selects the appropriate version for your platform. Commands without a platform prefix work on all platforms.

## Interactive Input

Commands can prompt for user input using square brackets in the `context_command`:
```csv
"blame-lines","Find who changed specific lines","git blame -L [Enter line range (e.g. 10,20)] [Enter file path]","~/flowai-prompts/blame-analysis.txt","raw",""
```

When running this command, FlowAI will:
1. Ask for the line range
2. Ask for the file path
3. Replace the bracketed text with user input
4. Run the resulting command

## Output Formatting

Commands can specify their output format using the `format` column:
- `markdown`: Format the output as markdown (default if not specified)
- `raw`: Output plain text without markdown formatting

This is useful for:
- Commands that generate structured output (use 'markdown')
- Commands that generate raw data or code (use 'raw')
- Commands where you want to control the exact formatting

Example:
```csv
"staged-commit-message","Generate commit message","git diff -w --staged","~/flowai-prompts/prompt-commit-message.txt","raw","Brief description of the changes (optional)"
"code-review","Review code changes","git diff -w","~/flowai-prompts/prompt-code-review.txt","markdown",""
```

The format setting in the command overrides the default behavior and the `--no-markdown` flag.

## Command Ideas

Here are some ripper ideas for custom commands:

### 1. Git Workflows
- `branch-summary`: Show what's been done in the current branch
  ```csv
  "branch-summary","Summarize branch changes","git log main..HEAD","~/flowai-prompts/branch-summary.txt","markdown","Focus areas to highlight (optional)"
  ```

- `commit-suggest`: Suggest commit message for staged changes
  ```csv
  "commit-suggest","Generate commit message","git diff --staged","~/flowai-prompts/commit-message.txt","raw","Brief description of changes (optional)"
  ```

### 2. Code Analysis
- `complexity-check`: Analyze function complexity
  ```csv
  "complexity-check","Check code complexity","cat [Enter file path]","~/flowai-prompts/complexity-analysis.txt","markdown","Specific concerns to address"
  ```

- `docstring-gen`: Generate Python docstrings
  ```csv
  "docstring-gen","Generate docstrings","cat [Enter file path]","~/flowai-prompts/docstring-generator.txt","raw","Style guide to follow (e.g., Google, NumPy)"
  ```

### 3. Testing
- `test-generator`: Generate unit tests
  ```csv
  "test-generator","Create unit tests","cat [Enter source file]","~/flowai-prompts/test-generator.txt","raw","Testing framework to use"
  ```

- `test-coverage`: Analyze test coverage gaps
  ```csv
  "test-coverage","Find coverage gaps","coverage report","~/flowai-prompts/coverage-analysis.txt","markdown",""
  ```

## Tips for Creating Commands

1. **Keep It Simple**
   - Start with common tasks you do frequently
   - Use descriptive command names
   - Keep descriptions clear and concise

2. **Smart Prompting**
   - Use brackets for required user input in context commands
   - Make prompt text descriptive
   - Include examples in the prompt text
   - Use user_input for optional guidance

3. **Context is Key**
   - Ensure context commands provide enough information
   - Consider using multiple commands with pipes
   - Test commands with different inputs

4. **Reusability**
   - Make commands generic enough to reuse
   - Use parameters for flexibility
   - Document any requirements

5. **Output Format**
   - Use 'markdown' for human-readable output with structure
   - Use 'raw' for code, commit messages, or other plain text
   - Default to markdown if unsure

6. **User Input**
   - Add user_input prompts for commands that benefit from guidance
   - Make prompts optional when possible
   - Include examples in the prompt text
   - Keep prompts concise but clear

## Example Usage

Here's how to use some of the commands above:

```bash
# Generate docstrings for a Python file
flowai --command docstring-gen
# When prompted: Enter Python file: src/main.py

# Create a sprint summary
flowai --command sprint-summary
# When prompted: Days ago (e.g. 14): 7

# Analyze security implications of changes
flowai --command security-review
# When prompted: Enter branch/commit: feature/new-auth
```

Remember, you can always list available commands with:
```bash
flowai --command list
```

Or get details about a specific command with:
```bash
flowai --command help [command-name]
```

# FlowAI Commands

FlowAI supports various commands to help with your development workflow.

## Advanced Features

### Web Search

FlowAI supports web search capabilities with Google's Gemini models, allowing you to access up-to-date information from the internet.

```bash
# Enable web search with any command
flowai --command help --web-search "What is the weather currently in San Francisco?"

# Use in chat mode
flowai --chat --web-search
```

When web search is enabled:
- The current date and time are included in the system prompt
- The AI will cite its sources in a dedicated "Sources" section
- Citations include webpage titles and URLs
- Only works with Gemini models (automatically disabled for other models)

### Thinking Mode (Gemini 2.5 Models)

Gemini 2.5 models support a "thinking mode" that allows the AI to perform more thorough reasoning before responding.

```bash
# Enable thinking mode with a command
flowai --command code-review --thinking-budget 2048

# Use in chat mode
flowai --chat --thinking-budget 2048
```

Thinking mode:
- Allows the AI to perform more thorough reasoning
- Higher budgets (1024+) enable more complex thinking
- Setting to 0 disables thinking mode
- Status is displayed in the terminal output
- Only works with Gemini 2.5 models

### Chat Commands

FlowAI's interactive chat mode supports several built-in commands:

```
/quit         - Exit chat mode
/clear        - Clear chat history
/stream       - Toggle stream mode
/stream on    - Enable stream mode
/stream off   - Disable stream mode
/save         - Save the entire chat session to a markdown file
/save last    - Save only the last response
/add-file <path> - Upload and cache a file (Gemini 1.5+ models only)
/list-files   - Show all files cached in this session
/help         - Show this help message
```

## Environment Compatibility

FlowAI is designed to work across different environments:
- Regular Unix/Linux systems
- macOS
  - Works with system shells and Homebrew-installed shells
  - Supports both Intel and Apple Silicon paths
- Windows (using cmd.exe)
- Docker containers and minimal environments
  - Automatically detects available shells
  - Works with limited environment variables
  - Compatible with common container base images
  - Falls back to available shell paths if environment variables aren't set

Shell Detection:
1. Windows: Always uses cmd.exe
2. Unix/Mac:
   - Checks $BASH and $SHELL environment variables
   - Falls back to common shell paths
   - Supports both system and custom-installed shells