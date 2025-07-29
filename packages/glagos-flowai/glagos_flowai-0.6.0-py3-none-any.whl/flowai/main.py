import typer
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.live import Live
from rich.table import Table
import questionary
from questionary import Choice
from typing import Optional, Dict, Any
import time
import sys
import re
import select
from difflib import get_close_matches
import shutil
from pathlib import Path
import os
if os.name == 'nt':  # Windows
    import msvcrt
import subprocess
import pyperclip
import importlib.resources as pkg_resources
from importlib.resources import files, as_file
import importlib.metadata
import traceback
import csv
from markdown_it import MarkdownIt
import configparser
import platform

from .config_manager import ConfigManager
from .llm_connector import LLMConnector, open_image
from .chat_manager import ChatManager
import flowai  # Import the package to access resources

app = typer.Typer(add_completion=False)
console = Console()

# Initialize markdown parser
md_parser = MarkdownIt("commonmark", {"breaks": True})

from flowai import __version__

# Global dictionary for provider URLs
provider_urls = {
    "gemini": "https://ai.google.dev/gemini-api/docs/api-key",
    "anthropic": "https://docs.anthropic.com/en/api/getting-started",
    "openai": "https://help.openai.com/en/articles/4936850-where-do-i-find-my-openai-api-key",
    "groq": "https://console.groq.com/docs/api-keys",
    "ollama": "https://www.ollama.com"
}

def get_image_from_clipboard():
    """
    Get an image from the clipboard and save it to a temporary file.

    Returns:
        str: Path to the saved image file, or None if no image was found or an error occurred
    """
    try:
        import tempfile
        from PIL import Image, ImageGrab

        # Get image from clipboard
        clipboard_image = ImageGrab.grabclipboard()

        # Check if the clipboard contains an image
        if clipboard_image is None:
            console.print("[bold red]No image found in clipboard.[/bold red]")
            return None

        if not isinstance(clipboard_image, Image.Image):
            # On macOS and Windows, ImageGrab.grabclipboard() returns an Image.Image object
            # On some platforms, it might return a file path or other data
            console.print("[bold red]Clipboard does not contain a valid image.[/bold red]")
            return None

        # Save the image to a temporary file
        fd, temp_path = tempfile.mkstemp(suffix='.png')
        os.close(fd)

        clipboard_image.save(temp_path, format='PNG')
        console.print(f"[green]Image from clipboard saved to: {temp_path}[/green]")

        # Try to get image dimensions
        width, height = clipboard_image.size
        console.print(f"[green]Dimensions: {width}x{height}[/green]")

        return temp_path
    except ImportError:
        console.print("[bold red]Error: PIL/Pillow is required for clipboard image handling. Install with 'pip install pillow'.[/bold red]")
        return None
    except Exception as e:
        console.print(f"[bold red]Error getting image from clipboard: {str(e)}[/bold red]")
        return None

def get_available_models(config):
    available_models = {}
    llm_connector = None
    try:
        llm_connector = LLMConnector(config)

        for provider in ["openai", "anthropic", "groq", "gemini", "ollama"]:
            try:
                models = llm_connector.get_available_models(provider)
                # Skip test models in listings
                if models and "Error fetching models" not in models[0] and provider != "test":
                    available_models[provider] = [f"{provider}/{model}" for model in models]
                elif provider == "ollama" and "Error fetching models" in models[0]:
                    console.print(f"[yellow]Ollama is not installed. Go to {provider_urls['ollama']} to install it.[/yellow]")
                elif "No API key set" in models[0]:
                    console.print(f"[yellow]No API key detected for {provider}. See {provider_urls[provider]} to set one.[/yellow]")
                elif "Error fetching models" in models[0]:
                    console.print(f"[red]Error fetching models for {provider}[/red]")
            except Exception as e:
                print(f"\nError while fetching {provider} models:", file=sys.stderr)
                traceback.print_exc()

    except Exception as e:
        print("\nError initializing LLM connector:", file=sys.stderr)
        traceback.print_exc()

    return available_models

def check_version():
    """Check if the installed version matches the config version and trigger updates if needed."""
    config_dir = Path.home() / ".config" / "flowai"
    version_file = config_dir / "VERSION"
    current_version = __version__

    try:
        needs_update = False
        if not version_file.exists():
            console.print("\n[bold yellow]First time running this version of FlowAI![/bold yellow]")
            console.print("[yellow]Setting up templates and documentation...[/yellow]\n")
            needs_update = True
        else:
            with open(version_file, 'r') as f:
                installed_version = f.read().strip()

            if installed_version != current_version:
                console.print(f"\n[bold yellow]FlowAI has been updated from v{installed_version} to v{current_version}![/bold yellow]")
                console.print("[yellow]Updating templates and documentation...[/yellow]\n")
                needs_update = True

        return needs_update
    except Exception as e:
        console.print(f"[yellow]Warning: Could not check version: {str(e)}[/yellow]")
        return False

def update_files():
    """Update template and documentation files without changing configuration."""
    config_dir = Path.home() / ".config" / "flowai"
    prompts_dir = Path.home() / "flowai-prompts"
    docs_dir = config_dir / "docs"

    for directory in [prompts_dir, config_dir, docs_dir]:
        directory.mkdir(parents=True, exist_ok=True)

    # Copy prompt files from the package resources
    prompt_files = ["prompt-commit-message.txt", "prompt-pull-request.txt", "prompt-code-review.txt", "prompt-index.txt", "prompt-help.txt"]
    for prompt_file in prompt_files:
        try:
            with pkg_resources.as_file(pkg_resources.files('flowai.prompts') / prompt_file) as prompt_path:
                shutil.copy(prompt_path, prompts_dir / prompt_file)
        except Exception as e:
            console.print(f"[yellow]Warning: Could not copy {prompt_file}: {str(e)}[/yellow]")

    # Copy documentation files
    try:
        docs_path = pkg_resources.files('flowai.docs')
        for doc_file in [p for p in docs_path.iterdir() if p.name.endswith('.md')]:
            with pkg_resources.as_file(doc_file) as doc_path:
                shutil.copy(doc_path, docs_dir / doc_path.name)
    except Exception as e:
        console.print(f"[yellow]Warning: Could not copy documentation files: {str(e)}[/yellow]")

    # Update version file
    try:
        with open(config_dir / "VERSION", 'w') as f:
            f.write(__version__)
    except Exception as e:
        console.print(f"[yellow]Warning: Could not write version file: {str(e)}[/yellow]")

    console.print(f"\n[bold green]Template files copied to {prompts_dir}[/bold green]")
    console.print(f"[bold green]Documentation files copied to {docs_dir}[/bold green]")

def init_config():
    """Full initialization including model selection and file updates."""
    config_manager = ConfigManager()
    config = config_manager.load_config()

    # Ensure all necessary keys are present with default values
    default_config = {
        'default_model': 'openai/gpt-3.5-turbo',
        'openai_api_key': '',
        'anthropic_api_key': '',
        'groq_api_key': '',
        'google_api_key': '',
        'ollama_base_url': 'http://localhost:11434',
        'stream_mode': 'true'
    }

    for key, value in default_config.items():
        if key not in config['DEFAULT']:
            config['DEFAULT'][key] = value

    current_model = config['DEFAULT']['default_model']
    current_stream_mode = config.getboolean('DEFAULT', 'stream_mode')

    console.print(Panel.fit(
        f"[bold green]Welcome to FlowAI {__version__}![/bold green]\n\n"
        "flowai is a CLI tool for multi-agent LLM tasks. It allows you to interact with "
        "various Language Models from different providers and NOT manage complex, multi-step tasks.\n\n"
        f"[bold blue]Current configuration:[/bold blue]\n"
        f"Model: [yellow]{current_model}[/yellow]\n"
        f"Stream mode: [yellow]{'On' if current_stream_mode else 'Off'}[/yellow]"
    ))

    available_models = get_available_models(config)

    # Prepare choices for providers with valid API keys
    provider_choices = []
    for provider, models in available_models.items():
        if models and models[0] not in [f"{provider}/No API key set", "Error fetching models"]:
            provider_choices.append(Choice(provider, value=provider))
        elif models[0] == f"{provider}/No API key set":
            console.print(f"[yellow]No API key detected for {provider}. See {provider_urls[provider]} to set one.[/yellow]")
        elif models[0] == "Error fetching models":
            console.print(f"[yellow]Error fetching models for {provider}. Please check your configuration.[/yellow]")

    if not provider_choices:
        console.print("[bold red]No models available. Please set at least one API key and try again.[/bold red]")
        for provider, url in provider_urls.items():
            console.print(f"[yellow]For {provider}, visit: {url}[/yellow]")
        return

    # First level: Select provider
    selected_provider = questionary.select(
        "Select a provider:",
        choices=provider_choices
    ).ask()

    if not selected_provider:
        console.print("[bold red]No provider selected. Exiting configuration.[/bold red]")
        return

    # Second level: Select model from the chosen provider
    model_choices = [model.split('/', 1)[1] for model in available_models[selected_provider]]
    current_model = config['DEFAULT']['default_model']
    current_model_name = current_model.split('/', 1)[1] if '/' in current_model else current_model

    selected_model = questionary.select(
        f"Select a model from {selected_provider}:",
        choices=model_choices,
        default=current_model_name if current_model_name in model_choices else model_choices[0]
    ).ask()

    if not selected_model:
        console.print("[bold red]No model selected. Exiting configuration.[/bold red]")
        return

    # When setting the default model
    default_model = f"{selected_provider}/{selected_model}"

    console.print(f"\n[bold green]Selected model: {default_model}[/bold green]")

    stream_mode = questionary.confirm("Enable stream mode by default?", default=config.getboolean('DEFAULT', 'stream_mode')).ask()

    # Update the config
    config['DEFAULT'] = {
        'default_model': default_model,
        'stream_mode': str(stream_mode).lower(),
        'openai_api_key': config.get('DEFAULT', 'openai_api_key', fallback=''),
        'anthropic_api_key': config.get('DEFAULT', 'anthropic_api_key', fallback=''),
        'groq_api_key': config.get('DEFAULT', 'groq_api_key', fallback=''),
        'google_api_key': config.get('DEFAULT', 'google_api_key', fallback=''),
        'ollama_base_url': config.get('DEFAULT', 'ollama_base_url', fallback='http://localhost:11434')
    }
    config_manager.save_config(config)
    console.print(f"\n[bold green]Configuration updated![/bold green]")

    console.print(f"Your config file is located at: {config_manager.config_file}")
    console.print("You can update these values by editing the file or by running 'flowai --init' again.")

    # Update files after configuration
    update_files()

def is_input_available():
    if os.name == 'nt':  # Windows
        return msvcrt.kbhit()
    else:  # Unix-based systems (Mac, Linux)
        return select.select([sys.stdin], [], [], 0.0)[0]

def generate_status_table(elapsed_time):
    table = Table.grid(padding=(0, 1))
    table.add_row(
        "[bold green]Generating response...",
        f"[bold blue]Elapsed time: {elapsed_time:.3f}s"
    )
    return table

def parse_prompt_index():
    """Parse the prompt index file using proper CSV parsing to handle commas in values."""
    prompts_dir = Path.home() / "flowai-prompts"
    index_file = prompts_dir / "prompt-index.txt"

    if not index_file.exists():
        raise ValueError("Prompt index file not found. Please run 'flowai --init' to set up the prompts directory.")

    commands = {}
    with open(index_file, 'r') as f:
        # Use csv module to properly handle commas within fields
        reader = csv.DictReader(f)
        for row in reader:
            label = row['label']
            # Handle platform-specific commands
            if ':' in label:
                platform, cmd = label.split(':', 1)
                # Check for valid platform prefixes
                if platform not in ['win', 'unix']:
                    console.print(f"[yellow]Warning: Invalid platform prefix '{platform}' in command '{label}'. Valid prefixes are 'win:' and 'unix:'.[/yellow]")
                    continue
                # Skip if not for current platform
                if platform == 'win' and os.name != 'nt':
                    continue
                if platform == 'unix' and os.name == 'nt':
                    continue
                # Store without platform prefix
                label = cmd

            # Replace ~ with actual home directory in prompt file path
            prompt_file = row['prompt_file'].replace('~', str(Path.home()))

            # Replace ~ with %USERPROFILE% in context command for Windows
            context_command = row['context_command']
            if os.name == 'nt':
                context_command = context_command.replace('~', '%USERPROFILE%')
            else:
                context_command = context_command.replace('~', str(Path.home()))

            # Get format value if it exists, validate it
            format_value = row.get('format', '').lower()
            if format_value and format_value not in ['raw', 'markdown']:
                console.print(f"[yellow]Warning: Invalid format value '{format_value}' in command '{label}'. Valid values are 'raw' or 'markdown'.[/yellow]")
                format_value = ''

            # Get user_input value if it exists
            user_input = row.get('user_input', '').strip()

            commands[label] = {
                'description': row['description'],
                'context_command': context_command,
                'prompt_file': prompt_file,
                'format': format_value,
                'user_input': user_input
            }
    return commands

def handle_user_prompts(command_str):
    """Extract user prompts from command string and get user input."""
    prompt_pattern = r'\[(.*?)\]'
    matches = re.finditer(prompt_pattern, command_str)

    for match in matches:
        prompt_text = match.group(1)
        user_input = questionary.text(f"{prompt_text}: ").ask()
        if user_input is None:
            raise typer.Abort()
        command_str = command_str.replace(f"[{prompt_text}]", user_input)

    # Show the command that will be run
    if command_str:
        console.print(f"\n[bold blue]Running command:[/bold blue] [cyan]{command_str}[/cyan]\n")

    return command_str

def display_available_commands():
    """Display available commands in a user-friendly way using Rich."""
    try:
        commands = parse_prompt_index()

        console.print("\n[bold green]G'day! Here are the available FlowAI commands:[/bold green]\n")

        table = Table(show_header=True, header_style="bold blue", show_lines=True)
        # Set column widths: command (25%), description (35%), context (40%)
        table.add_column("Command", style="yellow", ratio=1)
        table.add_column("Description", style="white", ratio=2)
        table.add_column("Context Source", style="cyan", ratio=3)

        for cmd, info in commands.items():
            context_source = info['context_command']
            if '[' in context_source:
                # Use Rich's markup for highlighting
                context_source = re.sub(r'\[(.*?)\]', r'[yellow]\[\1][/yellow]', context_source)

            table.add_row(cmd, info['description'], context_source)

        console.print(table)
        console.print("\n[bold green]To use a command:[/bold green]")
        console.print("  flowai --command [purple]<command-name>[/purple]")
        console.print("\n[bold green]Example:[/bold green]")
        console.print("  flowai --command pull-request")
        console.print("\n[italic]Note: [yellow]Yellow[/yellow] highlights in Context Source indicate where you'll be prompted for input[/italic]\n")

    except Exception as e:
        if "Prompt index file not found" in str(e):
            console.print("[bold yellow]No commands available. Run 'flowai --init' to set up command templates.[/bold yellow]")
        else:
            raise e

def list_commands_callback(ctx: typer.Context, param: typer.CallbackParam, value: str) -> Optional[str]:
    """Callback to handle --command with no value"""
    if value is None:
        display_available_commands()
        raise typer.Exit()
    return value

def first_run_onboarding(config_manager: ConfigManager):
    """Handle first-time user onboarding with a friendly introduction and setup guidance."""
    config = config_manager.load_config()

    welcome_md = f"""# Welcome to FlowAI! 🚀

G'day! Thanks for trying out FlowAI, your AI-powered development assistant.

## What is FlowAI?

FlowAI helps you automate common development tasks using AI, such as:
- Generating detailed commit messages from your changes
- Creating comprehensive pull request descriptions
- Performing automated code reviews
- And much more!

## Getting Started

FlowAI supports multiple AI providers:
| Provider | Status | API Key Link |
|----------|---------|--------------|"""

    # Check which providers have API keys
    has_api_keys = False
    provider_status = []

    for provider, url in provider_urls.items():
        key = f"{provider}_api_key".upper()  # Environment variables are uppercase
        if provider == "ollama":
            status = "✅ No key needed" if shutil.which("ollama") else "❌ Not installed"
        else:
            # Check both config and environment variables
            has_key = bool(config.get('DEFAULT', key.lower(), fallback='')) or bool(os.environ.get(key, ''))
            status = "✅ Configured" if has_key else "❌ Not configured"
            has_api_keys = has_api_keys or has_key

        provider_status.append(f"| {provider.capitalize()} | {status} | {url} |")

    welcome_md += "\n" + "\n".join(provider_status)

    if not has_api_keys:
        welcome_md += """

## Next Steps

1. Set up at least one API key from the providers above
2. Set the API key as an environment variable:
   ```bash
   # For OpenAI
   export OPENAI_API_KEY=your_key_here

   # For Anthropic
   export ANTHROPIC_API_KEY=your_key_here

   # For Groq
   export GROQ_API_KEY=your_key_here

   # For Gemini
   export GOOGLE_API_KEY=your_key_here

   # For Ollama
   # Just install from ollama.com
   ```
3. Run `flowai --init` to configure your preferred model

## Getting Help

- Run `flowai --command help` to get help with any topic
- Run `flowai --command list` to see available commands
- Visit our documentation at https://github.com/glagol-space/flowai
"""
    else:
        welcome_md += """

Great! You already have some API keys configured. Let's set up your preferred model.
"""

    # Display the welcome message
    console.print(Markdown(welcome_md))

    if has_api_keys:
        # If they have API keys, run the init process
        console.print("\n[yellow]Running initial setup...[/yellow]")
        init_config()
    else:
        # Just update files without running init
        update_files()
        console.print("\n[yellow]Run 'flowai --init' after setting up your API keys to complete the setup.[/yellow]")

def get_shell():
    """Get the user's shell with fallbacks for containers and minimal environments."""
    # Windows doesn't use this function
    if os.name == 'nt':
        return 'cmd.exe'

    # Try environment variables in order of preference
    if 'BASH' in os.environ and os.path.exists(os.environ['BASH']):
        return os.environ['BASH']

    if 'SHELL' in os.environ and os.path.exists(os.environ['SHELL']):
        return os.environ['SHELL']

    # Common shell paths to try
    shell_paths = [
        # Mac-specific paths
        '/usr/local/bin/bash',
        '/opt/homebrew/bin/bash',
        # Standard Unix paths
        '/bin/bash',
        '/usr/bin/bash',
        '/bin/sh',
        '/usr/bin/sh'
    ]

    # Try each shell in order
    for shell in shell_paths:
        if os.path.exists(shell):
            return shell

    # If we get here, we're in real trouble
    raise ValueError("No valid shell found. Please ensure bash or sh is installed in one of these locations: " + ", ".join(shell_paths))

def handle_chat_mode(llm_connector: LLMConnector, initial_context: Optional[Dict[str, Any]] = None, no_markdown: bool = False, debug: bool = False, web_search: bool = False) -> None:
    """Handle the chat mode interaction loop"""
    # Get stream mode from config if not specified in command line
    config_stream_mode = llm_connector.config.getboolean('DEFAULT', 'stream_mode', fallback=True)
    effective_stream_mode = llm_connector.stream_mode if llm_connector.stream_mode is not None else config_stream_mode

    chat_manager = ChatManager(stream=effective_stream_mode, debug=debug)

    # Initialize chat with context but don't process it yet
    if initial_context:
        if debug:
            print("\n[#555555]Initializing chat with context...[/#555555]", file=sys.stderr)
        chat_manager.start_session(initial_context)
        # If we have context, add it as the first message but don't process it
        if 'context' in initial_context and initial_context['context']:
            chat_manager.add_message("system", initial_context['context'])
    else:
        chat_manager.start_session(None)

    # Print welcome message in a box
    console.print("\n┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
    console.print("┃                                FlowAI Chat Mode                             ┃")
    console.print("┃                                                                             ┃")
    console.print("┃ Type your message and press Enter. Type '/help' for available commands.     ┃")
    console.print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n")

    while True:
        try:
            # Display prompt with status info using Rich markup
            console.print("")  # Add newline before prompt
            status_display = chat_manager.get_status_display()
            console.print(status_display, end="")
            # Set input color to light gray
            sys.stdout.write("\033[38;5;249m")  # ANSI color code for light gray
            user_message = input()
            sys.stdout.write("\033[0m")  # Reset color

            if debug:
                print(f"\n[#555555]User input: '{user_message}'[/#555555]", file=sys.stderr)

            # Handle chat commands
            if user_message.startswith('/add-file '):
                file_path = user_message[10:].strip()

                # Validate model supports file upload
                model = llm_connector.model
                provider, model_name = model.split('/', 1) if '/' in model else ('', model)
                # Check if it's a Gemini model and supports file upload (1.5+ models)
                if provider != 'gemini' or not any(version in model_name for version in ['2.5', '2.0', '1.5']):
                    console.print(Panel.fit(
                        "[bold red]Error: File upload is only supported with Gemini 1.5+ models![/bold red]\n\n"
                        f"Current model: {model}\n"
                        "Supported models include:\n"
                        "- gemini/gemini-2.5-pro-exp-03-25\n"
                        "- gemini/gemini-2.5-flash-preview-04-17\n"
                        "- gemini/gemini-2.0-flash-exp\n"
                        "- gemini/gemini-1.5-pro\n"
                        "- gemini/gemini-1.5-flash\n\n"
                        "Use '/quit' to exit and restart with a supported model.",
                        title="Unsupported Model",
                        border_style="red"
                    ))
                    continue

                # Validate file exists
                if not os.path.exists(file_path):
                    console.print(f"[red]Error: File '{file_path}' not found.[/red]")
                    continue
                if not os.path.isfile(file_path):
                    console.print(f"[red]Error: '{file_path}' is not a file.[/red]")
                    continue

                cache_id = llm_connector.upload_and_cache_files([file_path])
                if cache_id == "uploaded_not_cached":
                    chat_manager.context.setdefault('files', []).append(file_path)
                    console.print(f"[yellow]Added file {file_path} to session (too small for caching, using direct file upload).[/yellow]")
                elif cache_id:
                    chat_manager.context.setdefault('files', []).append(file_path)
                    console.print(f"[green]Added file {file_path} to session.[/green]")
                else:
                    console.print(f"[red]Failed to add file {file_path}.[/red]")
                continue

            if user_message.strip() == '/list-files':
                files_list = chat_manager.context.get('files', [])
                if files_list:
                    console.print("[bold cyan]Cached files in this session:[/bold cyan]")
                    for i, fp in enumerate(files_list, 1):
                        # Show file size if possible
                        try:
                            file_size = os.path.getsize(fp)
                            if file_size < 1024:
                                size_str = f"{file_size} bytes"
                            elif file_size < 1024 * 1024:
                                size_str = f"{file_size / 1024:.1f} KB"
                            else:
                                size_str = f"{file_size / (1024 * 1024):.1f} MB"
                            console.print(f"  {i}. [green]{fp}[/green] ({size_str})")
                        except OSError:
                            console.print(f"  {i}. [green]{fp}[/green] (file not accessible)")

                    if llm_connector.cache_id:
                        console.print(f"\n[dim]Cache ID: {llm_connector.cache_id}[/dim]")
                    elif llm_connector.uploaded_files:
                        console.print(f"\n[dim]Files uploaded directly (not cached): {len(llm_connector.uploaded_files)} files[/dim]")
                else:
                    console.print("[yellow]No files in this session.[/yellow]")
                    console.print("[dim]Use '/add-file <path>' to add files to the session.[/dim]")
                continue

            if not chat_manager.handle_command(user_message):
                break

            if user_message.startswith('/'):
                continue

            # Add user message to history
            chat_manager.add_message("user", user_message)

            # Get chat history for context
            messages = chat_manager.get_formatted_history()

            if debug:
                print("[#555555]Starting LLM processing with full context...[/#555555]", file=sys.stderr)
                print(f"[#555555]Number of messages in history: {len(messages)}[/#555555]", file=sys.stderr)

            # Start timing and show loading indicator
            start_time = time.time()
            console.print("\n", end="")

            response = ""
            loading_live = None
            try:
                if not chat_manager.stream:
                    loading_live = Live(generate_status_table(0), refresh_per_second=10, transient=True)
                    loading_live.start()

                if debug:
                    print("[#555555]Sending request to LLM...[/#555555]", file=sys.stderr)

                for chunk in llm_connector.chat_completion(messages=messages, stream=chat_manager.stream):
                    response += chunk
                    if chat_manager.stream:
                        sys.stdout.write(chunk)
                        sys.stdout.flush()
                    elif loading_live:
                        elapsed_time = time.time() - start_time
                        loading_live.update(generate_status_table(elapsed_time))

                # Check for image data in the response
                image_data_pattern = r'\[IMAGE_DATA_(\d+)\]\nMIME-Type: (.*?)\nPath: (.*?)\n\[/IMAGE_DATA_\1\]'
                image_matches = re.findall(image_data_pattern, response)
                if image_matches:
                    console.print("\n[bold green]Images detected in response:[/bold green]")
                    for idx, mime_type, path in image_matches:
                        console.print(f"[green]Image {idx}: {mime_type}[/green]")
                        console.print(f"[green]Saved to: {path}[/green]")

                        # Try to get image dimensions
                        try:
                            from PIL import Image
                            image = Image.open(path)
                            width, height = image.size
                            console.print(f"[green]Dimensions: {width}x{height}[/green]")
                            # Open the image automatically
                            open_image(image_path)
                        except ImportError:
                            console.print("[yellow]PIL/Pillow not installed. Cannot get image dimensions.[/yellow]")
                        except Exception as e:
                            console.print(f"[yellow]Could not get image dimensions: {str(e)}[/yellow]")

                    # Remove image data markers from the response
                    response = re.sub(image_data_pattern, '', response)

                if debug:
                    elapsed_time = time.time() - start_time
                    print(f"[#555555]LLM processing completed in {elapsed_time:.3f}s[/#555555]", file=sys.stderr)
            finally:
                if loading_live:
                    loading_live.stop()

            if chat_manager.stream:
                sys.stdout.write("\n")
                sys.stdout.flush()

            # Add assistant response to history
            chat_manager.add_message("assistant", response)

            # Update token counts in chat manager (set instead of add)
            chat_manager.total_input_tokens = llm_connector.input_tokens
            chat_manager.total_output_tokens = llm_connector.output_tokens

            if debug:
                print(f"[#555555]Token usage - Input: {llm_connector.input_tokens}, Output: {llm_connector.output_tokens}[/#555555]", file=sys.stderr)

            # Display response if not streaming
            if not chat_manager.stream:
                if no_markdown:
                    console.print(response)
                else:
                    console.print(Markdown(response))

        except KeyboardInterrupt:
            console.print("\n[yellow]Chat interrupted. Type '/quit' to exit or continue chatting.[/yellow]")
            continue
        except Exception as e:
            console.print(f"\n[bold red]Error:[/bold red] {str(e)}")
            continue

def display_available_models(config):
    """Display all available models from all providers"""
    print("Available models:")
    models = get_available_models(config)
    for provider, provider_models in models.items():
        print(f"\n{provider.capitalize()}:")
        if provider_models and provider_models[0] not in ["No API key set", "Error fetching models"]:
            for model in provider_models:
                print(f"  {model}")

    print("\nProviders with missing API keys or errors:")
    for provider, url in provider_urls.items():
        if provider not in models or models[provider][0] in [f"{provider}/No API key set", "Error fetching models"]:
            print(f"{provider.capitalize()}: {url}")

def display_status(config):
    """Display current FlowAI status"""
    current_model = config.get('DEFAULT', 'default_model', fallback='Not set')
    current_stream_mode = config.getboolean('DEFAULT', 'stream_mode', fallback=True)
    status_text = f"Current FlowAI Status\n\nModel: {current_model}\nStream mode: {'On' if current_stream_mode else 'Off'}"

    # Add thinking budget info for Gemini 2.5 models
    if "gemini" in current_model and "2.5" in current_model:
        thinking_budget = config.get('DEFAULT', 'thinking_budget', fallback='0')
        thinking_status = "enabled" if int(thinking_budget) > 0 else "disabled"
        status_text += f"\nThinking mode: {thinking_status} (budget: {thinking_budget})"

    # Add image generation info
    if "gemini" in current_model:
        status_text += f"\nImage generation: supported (use --create-image to generate images)"
        status_text += f"\nImage chat mode: supported (use --create-image --chat for interactive image refinement)"
    else:
        status_text += f"\nImage generation: not supported with current model (use a Gemini model with --create-image)"

    print(status_text)

def extract_from_json_error(error_message, key):
    """
    Extract a value from a JSON-like error message string.
    Args:
        error_message: The error message containing JSON data
        key: The JSON key to extract (e.g., "message", "retryDelay")
    Returns:
        The extracted value if found, None otherwise
    """
    try:
        import re
        import json

        # Try to find a complete JSON object in the error message
        json_pattern = r'({[^{}]*({[^{}]*})*[^{}]*})'
        json_matches = re.findall(json_pattern, error_message)

        for match in json_matches:
            if isinstance(match, tuple):
                match = match[0]  # Take the first element if it's a tuple

            try:
                # Try to parse as JSON
                json_obj = json.loads(match)

                # Recursively search for the key
                def find_key(obj, target_key):
                    if isinstance(obj, dict):
                        if target_key in obj:
                            return obj[target_key]
                        for k, v in obj.items():
                            result = find_key(v, target_key)
                            if result is not None:
                                return result
                    elif isinstance(obj, list):
                        for item in obj:
                            result = find_key(item, target_key)
                            if result is not None:
                                return result
                    return None

                value = find_key(json_obj, key)
                if value is not None:
                    return value
            except json.JSONDecodeError:
                # Not valid JSON, try the regex approach
                pass

        # Fallback to regex pattern matching if JSON parsing fails
        pattern = fr'"{key}"\s*:\s*"([^"]+)"'
        match = re.search(pattern, error_message)
        if match:
            return match.group(1)

        return None
    except Exception:
        # If any error occurs during extraction, return None
        return None

def handle_image_chat_mode(config: configparser.ConfigParser, model: str, initial_prompt: str,
                          initial_image_path: str, no_markdown: bool = False, debug: bool = False,
                          reference_image_path: Optional[str] = None) -> None:
    """
    Handle interactive image chat mode that uses direct Google GenAI SDK instead of LiteLLM.
    This is a special version of chat mode specifically for image generation and refinement.

    Args:
        config: The FlowAI configuration
        model: The image generation model to use
        initial_prompt: The initial prompt that generated the first image
        initial_image_path: Path to the initially generated image
        no_markdown: Whether to disable markdown rendering
        debug: Whether to enable debug mode
        reference_image_path: Optional path to a reference image used for the initial generation
    """
    from PIL import Image
    from google import genai
    from google.genai import types
    import tempfile

    google_key = config.get('DEFAULT', 'google_api_key', fallback='')
    if not google_key:
        console.print("[bold red]Google API key is required for image chat mode.[/bold red]")
        return

    # Initialize Google GenAI client
    client = genai.Client(api_key=google_key)
    model_name = model.split('/', 1)[1] if '/' in model else model

    # Get initial image dimensions
    try:
        image = Image.open(initial_image_path)
        width, height = image.size
    except Exception as e:
        console.print(f"[yellow]Could not get image dimensions: {str(e)}[/yellow]")
        width, height = "unknown", "unknown"

    # Print welcome message
    console.print("\n┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
    console.print("┃                       FlowAI Image Generation Chat Mode                      ┃")
    console.print("┃                                                                             ┃")
    console.print("┃ Type refinements to your image and press Enter. Type '/quit' to exit.       ┃")
    console.print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n")

    # Initialize chat history with reference image info if applicable
    reference_info = ""
    if reference_image_path:
        try:
            ref_image = Image.open(reference_image_path)
            ref_width, ref_height = ref_image.size
            reference_info = f" A reference image (dimensions: {ref_width}x{ref_height}) was also provided at {reference_image_path}."
        except Exception as e:
            console.print(f"[yellow]Could not get reference image dimensions: {str(e)}[/yellow]")
            reference_info = f" A reference image was also provided at {reference_image_path}."

    history = [
        {"role": "system", "content": f"You are a helpful image generation assistant. The user has just created an image with the prompt: '{initial_prompt}'. The image dimensions are {width}x{height} and it's saved at {initial_image_path}.{reference_info}"},
        {"role": "user", "content": initial_prompt},
        {"role": "assistant", "content": f"I've generated an image based on your prompt. The image has been saved to {initial_image_path}. Let me know if you'd like any changes or refinements to this image."}
    ]

    # Keep track of the images generated through this session
    current_image_path = initial_image_path
    reference_image = reference_image_path

    # Display initial response
    console.print(f"[green]Initial image generated from: '{initial_prompt}'[/green]")
    console.print(f"[green]Image saved to: {initial_image_path}[/green]")
    if reference_image:
        console.print(f"[green]Reference image used: {reference_image}[/green]")
    console.print("[yellow]You can now refine the image with additional prompts.[/yellow]\n")
    console.print("[cyan]Tips for better refinements:[/cyan]")
    console.print("- Clearly specify what elements to KEEP from the original image")
    console.print("- Be specific about what you want to ADD or CHANGE")
    console.print("- For small changes, try phrases like 'Make a small adjustment to...'")
    console.print("- For better continuity, use phrases like 'Same exact scene but with...'")

    while True:
        try:
            # Display prompt with nice formatting
            console.print("\n[bold cyan]Image refinement[/bold cyan] > ", end="")
            # Set input color to light gray
            sys.stdout.write("\033[38;5;249m")  # ANSI color code for light gray
            user_message = input()
            sys.stdout.write("\033[0m")  # Reset color

            # Handle special commands
            if user_message.lower() in ['/quit', '/exit', '/q']:
                console.print("[yellow]Exiting image chat mode.[/yellow]")
                break

            if user_message.lower() in ['/help', '/?']:
                console.print("\n[bold]Available commands:[/bold]")
                console.print("  /quit or /exit - Exit image chat mode")
                console.print("  /help - Show this help message")
                console.print("  /reference <path> - Use a new reference image for the next generation")
                console.print("  /clipboard - Use an image from clipboard as reference for the next generation")
                continue

            # Handle setting a new reference image
            if user_message.lower().startswith('/reference '):
                new_reference_path = user_message[11:].strip()
                try:
                    # Check if the file exists and is an image
                    Image.open(new_reference_path)
                    reference_image = new_reference_path
                    console.print(f"[green]Set reference image to: {reference_image}[/green]")
                except Exception as e:
                    console.print(f"[bold red]Error setting reference image: {str(e)}[/bold red]")
                continue

            # Handle clipboard reference image
            if user_message.lower() == '/clipboard':
                try:
                    clipboard_path = get_image_from_clipboard()
                    if clipboard_path:
                        reference_image = clipboard_path
                        console.print(f"[green]Set reference image from clipboard: {reference_image}[/green]")
                except Exception as e:
                    console.print(f"[bold red]Error getting image from clipboard: {str(e)}[/bold red]")
                continue

            if not user_message.strip():
                continue

            # Add user message to history
            history.append({"role": "user", "content": user_message})

            # Start timing and show loading indicator
            start_time = time.time()
            console.print("\n[yellow]Generating new image based on your refinements...[/yellow]")

            # Load the current image for inclusion in the prompt
            current_image = Image.open(current_image_path)

            # Create a refinement prompt that is more explicit about preservation
            refinement_instruction = (
                f"I want to refine this image. This is the original image that was generated from "
                f"the prompt: '{initial_prompt}'. Please maintain the core visual elements and style "
                f"of the original image, while making the following specific changes: {user_message}"
            )

            try:
                # Generate content with image response using direct Google API
                # Include the current image in the prompt to provide visual context
                try:
                    contents = []

                    # Include reference image if available
                    if reference_image:
                        try:
                            ref_img = Image.open(reference_image)
                            contents.append(ref_img)
                            # Adjust the instruction to mention the reference image
                            refinement_instruction = (
                                f"I want to refine this image. I've provided a reference image for styling or content guidance. "
                                f"This is the original image that was generated from the prompt: '{initial_prompt}'. "
                                f"Please maintain the core visual elements and style of the original image, while using the reference image "
                                f"as inspiration for making the following specific changes: {user_message}"
                            )
                        except Exception as e:
                            console.print(f"[yellow]Warning: Could not load reference image: {str(e)}[/yellow]")

                    # Add current image and instruction
                    contents.append(current_image)
                    contents.append(refinement_instruction)

                    response = client.models.generate_content(
                        model=model_name,
                        contents=contents,
                        config=types.GenerateContentConfig(
                            response_modalities=['TEXT', 'IMAGE']
                        )
                    )
                except Exception as google_api_error:
                    # Handle specific Google API errors
                    error_message = str(google_api_error)
                    if "Response modalities" in error_message:
                        console.print("[bold red]Error:[/bold red] The model does not support the requested image generation configuration.")
                    elif "rate limit" in error_message.lower() or "quota" in error_message.lower():
                        console.print("[bold red]Rate limit exceeded.[/bold red] You've hit Google's API rate limits.")
                    elif "permission" in error_message.lower() or "credentials" in error_message.lower():
                        console.print("[bold red]Authentication error.[/bold red] Please check your Google API key.")
                    else:
                        # General API error
                        console.print(f"[bold red]Google API Error:[/bold red] {error_message}")

                    if debug:
                        traceback.print_exc()

                    # Add the error to history
                    history.append({"role": "assistant", "content": f"I encountered an error while trying to generate a new image: {error_message}. Please try a different refinement."})
                    continue

                image_path = None
                text_response = ""

                # Process the response to extract image and text
                if hasattr(response, 'candidates') and response.candidates and len(response.candidates) > 0:
                    candidate = response.candidates[0]
                    if hasattr(candidate, 'content') and candidate.content:
                        content = candidate.content
                        if hasattr(content, 'parts') and content.parts:
                            for part in content.parts:
                                # Extract text content
                                if hasattr(part, 'text') and part.text is not None:
                                    text_response += part.text

                                # Extract image content
                                if hasattr(part, 'inline_data') and part.inline_data:
                                    inline_data = part.inline_data
                                    if (hasattr(inline_data, 'mime_type') and
                                        inline_data.mime_type is not None and
                                        inline_data.mime_type.startswith('image/') and
                                        hasattr(inline_data, 'data') and
                                        inline_data.data is not None):
                                        mime_type = inline_data.mime_type
                                        image_data = inline_data.data

                                        # Save the image to a temporary file
                                        ext = mime_type.split('/')[-1]
                                        fd, temp_path = tempfile.mkstemp(suffix=f'.{ext}')
                                        os.close(fd)

                                        # Write the image data to the file
                                        with open(temp_path, 'wb') as f:
                                            f.write(image_data)

                                        image_path = temp_path

                elapsed_time = time.time() - start_time

                # Display the results
                if image_path:
                    console.print(f"[green]New image generated in {elapsed_time:.2f}s![/green]")
                    console.print(f"[green]Image saved to: {image_path}[/green]")

                    # Update the current image path for the next refinement
                    current_image_path = image_path

                    # Try to get image dimensions and open the image
                    try:
                        image = Image.open(image_path)
                        width, height = image.size
                        console.print(f"[green]Dimensions: {width}x{height}[/green]")
                        # Open the image automatically
                        open_image(image_path)
                    except Exception as e:
                        console.print(f"[yellow]Could not open image: {str(e)}[/yellow]")

                    # Add assistant response to history
                    if text_response:
                        console.print("\n[cyan]Model response:[/cyan]")
                        if no_markdown:
                            console.print(text_response)
                        else:
                            console.print(Markdown(text_response))

                        ref_note = " I used your reference image as a guide." if reference_image else ""
                        history.append({"role": "assistant", "content": f"{text_response}\n\nI've generated a new image based on your refinement.{ref_note} The image has been saved to {image_path}."})
                    else:
                        # Default response if no text was provided
                        ref_note = " I used your reference image as a guide." if reference_image else ""
                        default_response = f"I've generated a new image based on your refinement.{ref_note} The image has been saved to {image_path}."
                        console.print(f"\n[cyan]Model response:[/cyan] {default_response}")
                        history.append({"role": "assistant", "content": default_response})

                    # Provide guidance for the next refinement
                    console.print("\n[yellow]For your next refinement, try being specific about what elements to keep and what to change.[/yellow]")
                else:
                    # No image was generated, display the text response if any
                    console.print("[yellow]No image was generated.[/yellow]")
                    if text_response:
                        console.print("\n[cyan]Model response:[/cyan]")
                        if no_markdown:
                            console.print(text_response)
                        else:
                            console.print(Markdown(text_response))
                        history.append({"role": "assistant", "content": text_response})
                    else:
                        console.print("[red]No response received from the model.[/red]")
                        history.append({"role": "assistant", "content": "I couldn't generate a new image based on your request. Please try a different refinement."})

            except Exception as e:
                console.print(f"[bold red]Error generating image:[/bold red] {str(e)}")
                if debug:
                    traceback.print_exc()
                history.append({"role": "assistant", "content": f"I encountered an error while trying to generate a new image: {str(e)}. Please try a different refinement."})

        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted. Type '/quit' to exit or continue refining.[/yellow]")
            continue
        except Exception as e:
            console.print(f"\n[bold red]Error:[/bold red] {str(e)}")
            if debug:
                traceback.print_exc()
            continue

@app.command(help="""FlowAI - AI-powered development assistant

A powerful CLI tool that helps streamline your development workflow using AI.

After setting up your API keys, you'll have access to an advanced help system:

    flowai --command help "your question here"

For example, try these questions:

    flowai --command help "how do I use FlowAI for code reviews?"

    flowai --command help "what's the best way to generate commit messages?"

    flowai --command help "explain the different context options"

The AI will provide detailed, contextual help based on your specific questions!""")
def main(
    model: Optional[str] = typer.Option(None, help="Specify the LLM model to use"),
    list_models: bool = typer.Option(False, "--list-models", help="List available models for all providers"),
    init: bool = typer.Option(False, "--init", help="Initialize FlowAI configuration"),
    status: bool = typer.Option(False, "--status", help="Show current model and settings"),
    stream: Optional[bool] = typer.Option(None, "--stream/--no-stream", "-S/-s", help="Stream mode: -S to enable, -s to disable"),
    context_file: Optional[str] = typer.Option(None, "--context-file", "-c", help="Path to a context file for global context"),
    debug: bool = typer.Option(False, "--debug", "-d", help="Enable debug mode to display prompts"),
    version: bool = typer.Option(False, "--version", help="Show the version of FlowAI"),
    prompt_file: Optional[str] = typer.Option(None, "--prompt-file", "-p", help="Path to a file containing a detailed prompt"),
    select_prompt_file: bool = typer.Option(False, "--select-prompt-file", help="Select a prompt file from the flowai-prompts directory"),
    context_shell_command: Optional[str] = typer.Option(None, "--context-shell-command", help="Shell command to generate context"),
    context_from_clipboard: bool = typer.Option(False, "--context-from-clipboard", help="Set context from the system clipboard"),
    files: Optional[str] = typer.Option(None, "--files", help="Comma-separated list of files to upload and cache for Gemini"),
    no_markdown: bool = typer.Option(False, "--no-markdown", help="Return the response without Markdown formatting"),
    command: Optional[str] = typer.Option(None, "--command", help="Command to run (use '--command list' to see available commands)"),
    chat: bool = typer.Option(False, "--chat", help="Start or continue a chat session after command execution"),
    web_search: bool = typer.Option(False, "--web-search", help="Enable web search capability (only supported by some models)"),
    thinking_budget: int = typer.Option(0, "--thinking-budget", help="Set thinking budget for Gemini 2.5 models (0 to disable thinking, 1024+ to enable)"),
    create_image: bool = typer.Option(False, "--create-image", help="Generate an image using the provided prompt. Add --chat to enter a specialized interactive mode where you can refine the image with additional prompts. Use --reference-image to provide a reference image for guided generation."),
    reference_image: Optional[str] = typer.Option(None, "--reference-image", "-r", help="Path to a reference image file to guide image generation. Used with --create-image to provide visual direction."),
    reference_from_clipboard: bool = typer.Option(False, "--reference-from-clipboard", help="Use an image from the clipboard as a reference for image generation. Used with --create-image."),
    prompt: Optional[str] = typer.Argument(None, help="The prompt to send to the LLM (optional if --prompt-file or --select-prompt-file is used)")
):
    """Main entry point for the FlowAI CLI"""
    try:
        # Handle broken pipe errors gracefully
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)

        # Automatically enable create_image mode if reference images are provided
        if (reference_image or reference_from_clipboard) and not create_image:
            console.print("[yellow]Reference image specified without --create-image. Automatically enabling image generation mode.[/yellow]")
            create_image = True

        # Initialize variables
        context = ""
        file_prompt = ""
        system_prompt = ""
        full_prompt = ""
        initial_context = None

        # Initialize config
        config_manager = ConfigManager()
        config = config_manager.load_config()

        # Get stream mode from config if not specified in command line
        default_stream = config.getboolean('DEFAULT', 'stream_mode', fallback=True)
        stream_mode = stream if stream is not None else default_stream

        # Check for first-time run
        config_dir = Path.home() / ".config" / "flowai"
        version_file = config_dir / "VERSION"
        if not version_file.exists():
            first_run_onboarding(config_manager)
            if not config_manager.config_exists():
                console.print("\n[yellow]Please run 'flowai --init' after setting up your API keys to start using FlowAI.[/yellow]")
                return

        # Handle early returns for simple commands
        if version:
            print(f"FlowAI version {__version__}")
            return

        if init:
            init_config()
            return

        if list_models:
            display_available_models(config)
            return

        if status:
            display_status(config)
            return

        # Check for stdin content
        if not sys.stdin.isatty():
            if debug:
                print("\n[#555555]Reading content from stdin...[/#555555]", file=sys.stderr)
            context = sys.stdin.read().strip()
            # If we have context but no other arguments, show error unless chat mode is explicitly requested
            if not any([prompt, prompt_file, select_prompt_file, command, list_models, init, status, version]):
                if not chat:
                    console.print(Panel.fit(
                        "[bold red]Error: Context provided without prompt or chat mode![/bold red]\n\n"
                        "When providing context (via pipe, file, or command), you must either:\n"
                        "1. Specify a prompt/command to process the context\n"
                        "2. Use --chat to discuss the context interactively\n\n"
                        "Examples:\n"
                        "  git diff | flowai --chat\n"
                        "  git diff | flowai \"summarize these changes\"\n"
                        "  git diff | flowai --command review",
                        title="Invalid Usage",
                        border_style="red"
                    ))
                    raise typer.Exit(code=1)
                chat = True
            # Reopen stdin for interactive use if needed
            if chat:
                try:
                    sys.stdin.close()
                    sys.stdin = open('/dev/tty')
                except Exception as e:
                    print(f"\nWarning: Could not reopen terminal for interactive use. Chat mode may not be available.", file=sys.stderr)

        # Validate --files argument requirements
        if files:
            # Validate that either --chat or a prompt is provided when using --files
            if not chat and not any([prompt, prompt_file, select_prompt_file, command]):
                console.print(Panel.fit(
                    "[bold red]Error: --files requires either --chat or a prompt![/bold red]\n\n"
                    "When using --files, you must either:\n"
                    "1. Provide a prompt to process the files\n"
                    "2. Use --chat to discuss the files interactively\n\n"
                    "Examples:\n"
                    "  flowai --files document.pdf \"summarize this file\"\n"
                    "  flowai --files document.pdf --chat",
                    title="Invalid Usage",
                    border_style="red"
                ))
                raise typer.Exit(code=1)

        # Handle direct chat mode
        if chat and not any([prompt, prompt_file, select_prompt_file, command, list_models, init, status, version]):
            if not config_manager.config_exists():
                raise ValueError("No configuration file found. Please run 'flowai --init' to set up FlowAI.")

            model = model or config.get('DEFAULT', 'default_model')
            if not model:
                raise ValueError("No valid model set. Please run 'flowai --init' or use --model to set a model.")

            # Convert model format if needed (from old ':' format to new '/' format)
            if ':' in model and '/' not in model:
                provider, model_name = model.split(':', 1)
                model = f"{provider}/{model_name}"

            # Validate model for file upload if files are provided
            if files:
                provider, model_name = model.split('/', 1) if '/' in model else ('', model)
                # Check if it's a Gemini model and supports file upload (2.0+ models)
                if provider != 'gemini' or not any(version in model_name for version in ['2.5', '2.0', '1.5']):
                    console.print(Panel.fit(
                        "[bold red]Error: File upload is only supported with Gemini 1.5+ models![/bold red]\n\n"
                        f"Current model: {model}\n"
                        "Supported models include:\n"
                        "- gemini/gemini-2.5-pro-exp-03-25\n"
                        "- gemini/gemini-2.5-flash-preview-04-17\n"
                        "- gemini/gemini-2.0-flash-exp\n"
                        "- gemini/gemini-1.5-pro\n"
                        "- gemini/gemini-1.5-flash\n\n"
                        "Please use --model to specify a supported model.",
                        title="Unsupported Model",
                        border_style="red"
                    ))
                    raise typer.Exit(code=1)

            llm_connector = LLMConnector(
                config=config,
                model=model,
                system_prompt=config_manager.get_system_prompt(),
                stream_mode=stream_mode,
                web_search=web_search,
                thinking_budget=thinking_budget
            )

            # Set create_image_mode flag when using --create-image
            if create_image:
                llm_connector.create_image_mode = True

            # Set debug flag when using --debug
            if debug:
                llm_connector.debug = True

            # Check if web search is requested but not supported
            if web_search and not llm_connector.supports_web_search():
                console.print("[yellow]Warning: Web search is only supported by Google models. Your request will proceed without web search.[/yellow]")

            # Create initial context with stdin content or context file if available
            initial_context = {
                'input_tokens': 0,
                'output_tokens': 0
            }

            if context:
                initial_context['context'] = context
                initial_context['last_command'] = "Chat with context from stdin"

            if context_file:
                try:
                    with open(context_file, 'r') as f:
                        context = f.read().strip()
                    initial_context['context'] = context
                    initial_context['last_command'] = f'Reading context from file: {context_file}'
                except FileNotFoundError:
                    console.print(f"[bold red]Error: Context file '{context_file}' not found.[/bold red]")
                    raise typer.Exit(code=1)
                except IOError:
                    console.print(f"[bold red]Error: Unable to read context file '{context_file}'.[/bold red]")
                    raise typer.Exit(code=1)

            if files:
                # Validate files exist before attempting upload
                file_list = [p.strip() for p in files.split(',') if p.strip()]
                for file_path in file_list:
                    if not os.path.exists(file_path):
                        console.print(f"[bold red]Error: File '{file_path}' not found.[/bold red]")
                        raise typer.Exit(code=1)
                    if not os.path.isfile(file_path):
                        console.print(f"[bold red]Error: '{file_path}' is not a file.[/bold red]")
                        raise typer.Exit(code=1)

                cache_id = llm_connector.upload_and_cache_files(file_list)
                if cache_id == "uploaded_not_cached":
                    initial_context['files'] = file_list
                    console.print(f"[yellow]Successfully uploaded {len(file_list)} file(s) (too small for caching, using direct file upload).[/yellow]")
                elif cache_id:
                    initial_context['files'] = file_list
                    console.print(f"[green]Successfully uploaded and cached {len(file_list)} file(s).[/green]")
                else:
                    console.print("[red]Failed to upload files.[/red]")
                    raise typer.Exit(code=1)

            handle_chat_mode(llm_connector, initial_context, no_markdown, debug, web_search)
            return

        # Show help if no input is provided and not in chat mode
        if not any([prompt, prompt_file, select_prompt_file, command, list_models, init, status, version, chat]):
            console.print("[blue]No command detected. type 'flowai --help' for more information...[/blue]\n")
            raise typer.Exit()

        # Check for version updates (only if not first run)
        if check_version():
            update_files()  # Update files, but don't return - continue with the command
            console.print("[green]Update complete![/green]\n")

        if version:
            print(f"FlowAI version: {__version__}")
            return

        if not config_manager.config_exists():
            raise ValueError("No configuration file found. Please run 'flowai --init' to set up FlowAI.")

        config = config_manager.load_config()
        system_prompt = config_manager.get_system_prompt()

        if status:
            current_model = config.get('DEFAULT', 'default_model', fallback='Not set')
            current_stream_mode = config.getboolean('DEFAULT', 'stream_mode', fallback=True)
            print(f"Current FlowAI Status\n\nModel: {current_model}\nStream mode: {'On' if current_stream_mode else 'Off'}")
            return

        if list_models:
            print("Available models:")
            models = get_available_models(config)
            for provider, provider_models in models.items():
                print(f"\n{provider.capitalize()}:")
                if provider_models and provider_models[0] not in ["No API key set", "Error fetching models"]:
                    for model in provider_models:
                        print(f"  {model}")

            print("\nProviders with missing API keys or errors:")
            for provider, url in provider_urls.items():
                if provider not in models or models[provider][0] in [f"{provider}/No API key set", "Error fetching models"]:
                    print(f"{provider.capitalize()}: {url}")
            return

        # Handle command listing and execution
        if command == "list":
            display_available_commands()
            return
        elif command:
            commands = parse_prompt_index()
            if command not in commands:
                console.print(f"\n[bold red]Unknown command: {command}[/bold red]\n")
                display_available_commands()
                raise typer.Exit(code=1)

            cmd_info = commands[command]

            # Set default help prompt if using help command without a prompt
            if command == "help" and not prompt:
                prompt = """Please provide a concise overview of FlowAI. Include:
1. What the program does and its main features
2. Available command-line switches and their usage
3. Common use cases and example commandsp"""

            # Handle any user prompts in the context command
            context_shell_command = handle_user_prompts(cmd_info['context_command'])
            prompt_file = cmd_info['prompt_file']

            # Override any existing prompt file or context command
            if prompt_file:
                prompt_file = prompt_file
            if context_shell_command:
                context_shell_command = context_shell_command

            # Override no_markdown based on command format if specified
            if cmd_info['format']:
                no_markdown = cmd_info['format'] == 'raw'

            # If no prompt provided but command has user_input defined, prompt the user
            if not prompt and cmd_info['user_input']:
                user_response = questionary.text(f"{cmd_info['user_input']}: ").ask()
                if user_response:  # Only use the response if user provided one
                    prompt = user_response

        # Check for prompt or prompt file first
        if not (prompt or prompt_file or select_prompt_file or command):
            raise ValueError("No prompt provided. Please provide a prompt, use --prompt-file, --select-prompt-file, or --command.")

        # Only validate configuration if we're not listing models or showing version/status
        if not (list_models or version or status):
            is_valid, error_message = config_manager.validate_config()
            if not is_valid:
                raise ValueError(f"Configuration error: {error_message}\nPlease run 'flowai --init' to reconfigure FlowAI.")

        model = model or config.get('DEFAULT', 'default_model')
        if not model:
            raise ValueError("No valid model set. Please run 'flowai --init' or use --model to set a model.")

        # Convert model format if needed (from old ':' format to new '/' format)
        if ':' in model and '/' not in model:
            provider, model_name = model.split(':', 1)
            model = f"{provider}/{model_name}"
        elif '/' not in model:
            raise ValueError("Invalid model format. Model should be in format 'provider/model_name'.")

        provider, model_name = model.split('/', 1)

        # Handle image generation request
        if create_image:
            # Make sure context_from_clipboard is processed immediately for image creation
            if context_from_clipboard and not context:
                try:
                    context = pyperclip.paste()
                    console.print("[green]Context loaded from clipboard for image generation.[/green]")
                    if debug:
                        print("\n[#555555]Context from clipboard for image generation:[/#555555]", file=sys.stderr)
                        print(f"[#555555]{context}[/#555555]", file=sys.stderr)
                except Exception as e:
                    console.print(f"[bold red]Error reading from clipboard: {str(e)}[/bold red]")

            # Process context file immediately if provided
            if context_file and not context:
                try:
                    with open(context_file, 'r') as f:
                        context = f.read().strip()
                    console.print(f"[green]Context loaded from file: {context_file}[/green]")
                    if debug:
                        print("\n[#555555]Context from file for image generation:[/#555555]", file=sys.stderr)
                        print(f"[#555555]{context}[/#555555]", file=sys.stderr)
                except FileNotFoundError:
                    console.print(f"[bold red]Error: Context file '{context_file}' not found.[/bold red]")
                    raise typer.Exit(code=1)
                except Exception as e:
                    console.print(f"[bold red]Error reading context file: {str(e)}[/bold red]")
                    raise typer.Exit(code=1)

            # Print debug information about context
            if debug and context:
                print("\n[#555555]Context for image generation (before processing):[/#555555]", file=sys.stderr)
                print(f"[#555555]{context}[/#555555]", file=sys.stderr)

            # Default image generation model is gemini/gemini-2.0-flash-preview-image-generation
            default_image_model = "gemini/gemini-2.0-flash-preview-image-generation"

            # If user specified their own model, respect it but show a warning
            if model and model != config.get('DEFAULT', 'default_model'):
                console.print(f"[yellow]Warning: Using user-specified model '{model}' for image generation.[/yellow]")
                console.print("[yellow]This might not work as expected as image generation is currently optimized for Gemini models.[/yellow]")
            else:
                # Set the model to the default image generation model
                model = default_image_model
                console.print(f"[yellow]Using default image generation model: {model}[/yellow]")

            # Ensure we have a prompt for image generation
            if not prompt:
                console.print("[bold red]Error: Image generation requires a prompt.[/bold red]")
                raise typer.Exit(code=1)

            # Acknowledge chat mode if requested
            if chat:
                console.print("[yellow]Image generation will be followed by interactive chat mode for refinements.[/yellow]")

            # Initialize Google GenAI client
            google_key = config.get('DEFAULT', 'google_api_key', fallback='')
            if not google_key:
                console.print("[bold red]No Google API key found in configuration. Image generation requires a Google API key.[/bold red]")
                raise typer.Exit(code=1)

            # Print masked API key for debugging
            if debug:
                # Show first 4 and last 4 chars of the key
                if len(google_key) > 8:
                    masked_key = google_key[:4] + '*' * (len(google_key) - 8) + google_key[-4:]
                else:
                    masked_key = '*' * len(google_key)
                print(f"[#555555]Using Google API key: {masked_key}[/#555555]", file=sys.stderr)

            try:
                from google import genai
                from google.genai import types
                import base64
                import tempfile
                from PIL import Image

                client = genai.Client(api_key=google_key)
                model_name = model.split('/', 1)[1] if '/' in model else model

                # Process reference image if provided
                reference_image_path = None
                if reference_image:
                    try:
                        # Verify the reference image exists and is valid
                        Image.open(reference_image)
                        reference_image_path = reference_image
                        console.print(f"[green]Using reference image: {reference_image_path}[/green]")
                    except Exception as e:
                        console.print(f"[yellow]Warning: Could not use reference image file: {str(e)}[/yellow]")
                elif reference_from_clipboard:
                    # Get image from clipboard
                    clipboard_image_path = get_image_from_clipboard()
                    if clipboard_image_path:
                        reference_image_path = clipboard_image_path
                        console.print(f"[green]Using reference image from clipboard: {reference_image_path}[/green]")

                # Prepare the contents for the API call
                contents = []

                # Add reference image if available
                if reference_image_path:
                    try:
                        ref_img = Image.open(reference_image_path)
                        contents.append(ref_img)
                        # Augment the prompt to include reference to the image
                        contents.append(prompt)
                    except Exception as e:
                        console.print(f"[yellow]Warning: Could not load reference image: {str(e)}[/yellow]")
                        # Fall back to just the prompt
                        contents = prompt
                else:
                    # No reference image, just use the prompt
                    contents = prompt

                # Add context if available
                if context:
                    if isinstance(contents, str):
                        contents = [
                            f"""
                            <context>
                            {context}
                            </context>
                            """
                        ]
                    # Add context as the scene to illustrate
                    contents.append(prompt)

                if debug:
                    print("\n[#555555]Image Generation Request:[/#555555]", file=sys.stderr)
                    print("[#555555]Contents:[/#555555]", file=sys.stderr)
                    # Check if contents is a string or a list before iterating
                    if isinstance(contents, str):
                        print(f"[#555555]Content: {contents}[/#555555]", file=sys.stderr)
                    else:
                        for i, content in enumerate(contents):
                            if isinstance(content, Image.Image):
                                print(f"[#555555]Content {i}: [Image][/#555555]", file=sys.stderr)
                            else:
                                print(f"[#555555]Content {i}: {content}[/#555555]", file=sys.stderr)
                    if context:
                        print("\n[#555555]Context:[/#555555]", file=sys.stderr)
                        print(f"[#555555]{context}[/#555555]", file=sys.stderr)

                # Generate content with image response
                response = client.models.generate_content(
                    model=model_name,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        response_modalities=['TEXT', 'IMAGE']
                    )
                )

                # Process the response
                if hasattr(response, 'candidates') and response.candidates:
                    candidate = response.candidates[0]
                    if hasattr(candidate, 'content') and candidate.content:
                        content = candidate.content
                        if hasattr(content, 'parts') and content.parts:
                            for part in content.parts:
                                if hasattr(part, 'inline_data') and part.inline_data:
                                    inline_data = part.inline_data
                                    if hasattr(inline_data, 'mime_type') and inline_data.mime_type.startswith('image/'):
                                        mime_type = inline_data.mime_type
                                        image_data = inline_data.data

                                        console.print(f"[green]Image generated! MIME type: {mime_type}[/green]")

                                        # Save the image to a temporary file
                                        ext = mime_type.split('/')[-1]
                                        fd, temp_path = tempfile.mkstemp(suffix=f'.{ext}')
                                        os.close(fd)

                                        # Write the image data to the file
                                        with open(temp_path, 'wb') as f:
                                            if isinstance(image_data, str):
                                                image_data = base64.b64decode(image_data)
                                            f.write(image_data)

                                        console.print(f"[green]Image saved to: {temp_path}[/green]")

                                        # Try to get image dimensions
                                        width, height = None, None
                                        try:
                                            image = Image.open(temp_path)
                                            width, height = image.size
                                            console.print(f"[green]Dimensions: {width}x{height}[/green]")
                                            # Open the image automatically
                                            open_image(temp_path)
                                        except Exception as e:
                                            console.print(f"[yellow]Could not get image dimensions: {str(e)}[/yellow]")

                                        # Create initial context with image information
                                        initial_context = {
                                            'last_command': f'Generated image: {temp_path}',
                                            'last_prompt': prompt,
                                            'input_tokens': 0,
                                            'output_tokens': 0,
                                            'image_path': temp_path,
                                            'image_mime_type': mime_type,
                                            'context': f"Generated image is saved at: {temp_path}. I can create variations or new images based on your requests." + (f" Image dimensions are {width}x{height}." if width and height else "")
                                        }

                                        # Enter chat mode if requested, otherwise exit
                                        if chat:
                                            console.print("\n[yellow]Entering specialized image chat mode. You can now refine your image generation through direct Google API calls.[/yellow]")

                                            try:
                                                # Use our special direct Google API chat mode for image generation
                                                handle_image_chat_mode(
                                                    config=config,
                                                    model=model,
                                                    initial_prompt=prompt,
                                                    initial_image_path=temp_path,
                                                    no_markdown=no_markdown,
                                                    debug=debug,
                                                    reference_image_path=reference_image_path
                                                )
                                            except Exception as e:
                                                console.print(f"[bold red]Error entering image chat mode: {str(e)}[/bold red]")
                                                if debug:
                                                    traceback.print_exc()
                                                console.print("[yellow]Exiting chat mode due to error.[/yellow]")

                                            # Always return after attempting image chat mode
                                            return
                                        else:
                                            # Return early since we've handled the image generation and chat is not requested
                                            return

                # If we get here, no image was found in the response
                console.print("[yellow]No image found in the response.[/yellow]")
            except Exception as e:
                console.print(f"[yellow]Error using Google GenAI for image generation: {str(e)}[/yellow]")
                if debug:
                    traceback.print_exc()

            # Always return for image generation path - never fall through to LiteLLM
            console.print("[bold red]Image generation failed. Please try again with a different prompt or configuration.[/bold red]")
            return

        # Initialize LLM connector for non-image generation paths
        llm_connector = LLMConnector(
            config=config,
            model=model,
            system_prompt=system_prompt,
            stream_mode=stream_mode,
            web_search=web_search,
            thinking_budget=thinking_budget
        )

        # Set create_image_mode flag when using --create-image
        if create_image:
            llm_connector.create_image_mode = True

        # Set debug flag when using --debug
        if debug:
            llm_connector.debug = True

        # Check if web search is requested but not supported
        if web_search and not llm_connector.supports_web_search():
            console.print("[yellow]Warning: Web search is only supported by Google models. Your request will proceed without web search.[/yellow]")

        uploaded_files = []
        if files:
            # Validate model for file upload
            provider, model_name = model.split('/', 1) if '/' in model else ('', model)
            # Check if it's a Gemini model and supports file upload (1.5+ models)
            if provider != 'gemini' or not any(version in model_name for version in ['2.5', '2.0', '1.5']):
                console.print(Panel.fit(
                    "[bold red]Error: File upload is only supported with Gemini 1.5+ models![/bold red]\n\n"
                    f"Current model: {model}\n"
                    "Supported models include:\n"
                    "- gemini/gemini-2.5-pro-exp-03-25\n"
                    "- gemini/gemini-2.5-flash-preview-04-17\n"
                    "- gemini/gemini-2.0-flash-exp\n"
                    "- gemini/gemini-1.5-pro\n"
                    "- gemini/gemini-1.5-flash\n\n"
                    "Please use --model to specify a supported model.",
                    title="Unsupported Model",
                    border_style="red"
                ))
                raise typer.Exit(code=1)

            # Validate files exist before attempting upload
            file_list = [p.strip() for p in files.split(',') if p.strip()]
            for file_path in file_list:
                if not os.path.exists(file_path):
                    console.print(f"[bold red]Error: File '{file_path}' not found.[/bold red]")
                    raise typer.Exit(code=1)
                if not os.path.isfile(file_path):
                    console.print(f"[bold red]Error: '{file_path}' is not a file.[/bold red]")
                    raise typer.Exit(code=1)

            cache_id = llm_connector.upload_and_cache_files(file_list)
            if cache_id == "uploaded_not_cached":
                uploaded_files = file_list
                console.print(f"[yellow]Successfully uploaded {len(file_list)} file(s) (too small for caching, using direct file upload).[/yellow]")
            elif cache_id:
                uploaded_files = file_list
                console.print(f"[green]Successfully uploaded and cached {len(file_list)} file(s).[/green]")
            else:
                console.print("[red]Failed to upload files.[/red]")
                raise typer.Exit(code=1)

        # Handle prompt file and command-line prompt
        file_prompt = ""
        if prompt_file:
            try:
                with open(prompt_file, 'r') as f:
                    file_prompt = f.read().strip()
                if debug:
                    print("\n[#555555]Template Prompt:[/#555555]", file=sys.stderr)
                    print(f"[#555555]{file_prompt}[/#555555]", file=sys.stderr)
            except FileNotFoundError:
                console.print(f"[bold red]Error: Prompt file '{prompt_file}' not found.[/bold red]")
                raise typer.Exit(code=1)
            except IOError:
                console.print(f"[bold red]Error: Unable to read prompt file '{prompt_file}'.[/bold red]")
                raise typer.Exit(code=1)
        elif select_prompt_file:
            if os.isatty(sys.stdin.fileno()):
                prompts_dir = Path.home() / "flowai-prompts"
                prompt_files = list(prompts_dir.glob("*.txt"))
                if not prompt_files:
                    console.print(f"[bold red]No prompt files found in {prompts_dir}.[/bold red]")
                    raise typer.Exit(code=1)
                prompt_file_choices = [Choice(str(file.name), value=str(file)) for file in prompt_files]
                selected_prompt_file = questionary.select(
                    "Select a prompt file:",
                    choices=prompt_file_choices
                ).ask()
                if not selected_prompt_file:
                    console.print("[bold red]No prompt file selected. Exiting.[/bold red]")
                    raise typer.Exit(code=1)
                with open(selected_prompt_file, 'r') as f:
                    file_prompt = f.read().strip()
                if debug:
                    print("\n[#555555]Selected Template Prompt:[/#555555]", file=sys.stderr)
                    print(f"[#555555]{file_prompt}[/#555555]", file=sys.stderr)
            else:
                console.print("[bold red]Error: --select-prompt-file requires an interactive terminal.[/bold red]")
                raise typer.Exit(code=1)

        # Show user prompt in debug mode
        if debug and prompt:
            print("\n[#555555]User Prompt:[/#555555]", file=sys.stderr)
            print(f"[#555555]{prompt}[/#555555]", file=sys.stderr)

        # Combine file prompt and command-line prompt
        full_prompt = file_prompt
        if prompt:
            # If there's a file prompt, add the user's prompt at the beginning
            # This ensures user instructions are prominent for the LLM
            if file_prompt:
                full_prompt = f"User Instructions: {prompt}\n\n{file_prompt}"
            else:
                full_prompt = prompt

        if debug:
            print("\n[#555555]System Prompt:[/#555555]", file=sys.stderr)
            print(f"[#555555]{system_prompt}[/#555555]", file=sys.stderr)

        # Check if context is required
        context_required = "{{CONTEXT}}" in full_prompt or any(keyword in full_prompt.lower() for keyword in [
            "git diff",
            "code changes",
            "analyze the changes",
            "review the code",
            "context will be provided",
            "__START_CONTEXT__"
        ])

        # Handle context_file and stdin
        if context_file:
            try:
                with open(context_file, 'r') as f:
                    context = f.read().strip()
                if debug:
                    print("\n[#555555]Context from file:[/#555555]", file=sys.stderr)
                    print(f"[#555555]{context}[/#555555]", file=sys.stderr)

                # Create initial context for chat mode
                if chat:
                    initial_context = {
                        'context': context,
                        'last_command': f'Reading context from file: {context_file}',
                        'input_tokens': 0,
                        'output_tokens': 0
                    }
            except FileNotFoundError:
                console.print(f"[bold red]Error: Context file '{context_file}' not found.[/bold red]")
                raise typer.Exit(code=1)
            except IOError:
                console.print(f"[bold red]Error: Unable to read context file '{context_file}'.[/bold red]")
                raise typer.Exit(code=1)

            # Check if stdin is also present
            if not sys.stdin.isatty():
                console.print("[bold red]Error: Cannot use both --context-file and stdin for context. Please choose one method.[/bold red]")
                raise typer.Exit(code=1)

        # Run the shell command and capture its output
        if context_shell_command:
            try:
                if os.name == 'nt':  # Windows
                    context_bytes = subprocess.check_output(f'cmd.exe /c "{context_shell_command}"', shell=True)
                else:  # Unix-based systems
                    shell = get_shell()
                    context_bytes = subprocess.check_output(f"{shell} -c '{context_shell_command}'", shell=True)

                # Try to decode with UTF-8 first, fallback to latin-1 (which always works but might not be correct)
                try:
                    context = context_bytes.decode('utf-8').strip()
                except UnicodeDecodeError:
                    # Fallback to latin-1 which can decode any byte sequence
                    context = context_bytes.decode('latin-1').strip()
                    console.print("[yellow]Warning: Command output contained non-UTF-8 characters. Fallback encoding used.[/yellow]")

                if debug:
                    print("\n[#555555]Context from command:[/#555555]", file=sys.stderr)
                    print(f"[#555555]{context}[/#555555]", file=sys.stderr)
            except subprocess.CalledProcessError as e:
                console.print(f"[bold red]Error: Failed to run shell command '{context_shell_command}'.[/bold red]")
                console.print(f"[bold red]{e.output.decode('latin-1', errors='replace') if hasattr(e, 'output') else str(e)}[/bold red]")
                if debug:
                    traceback.print_exc()
                raise typer.Exit(code=1)
            except Exception as e:
                console.print(f"[bold red]Error: {str(e)}[/bold red]")
                if debug:
                    traceback.print_exc()
                raise typer.Exit(code=1)

        # Set context from clipboard if --context-from-clipboard is provided
        if context_from_clipboard:
            context = pyperclip.paste()
            if debug:
                print("\n[#555555]Context from clipboard:[/#555555]", file=sys.stderr)
                print(f"[#555555]{context}[/#555555]", file=sys.stderr)

        # Check if context is required but missing
        if context_required and not context:
            console.print(Panel.fit(
                "[bold red]Error: This prompt requires context, but no context was provided![/bold red]\n\n"
                "You can provide context in several ways:\n\n"
                "[bold blue]1. Pipe content directly:[/bold blue]\n"
                "   git diff -w | flowai --prompt-file ~/flowai-prompts/prompt-commit-message.txt\n\n"
                "[bold blue]2. Use a context file:[/bold blue]\n"
                "   flowai --context-file changes.diff --prompt-file ~/flowai-prompts/prompt-commit-message.txt\n\n"
                "[bold blue]3. Use a shell command:[/bold blue]\n"
                "   flowai --context-shell-command \"git diff -w\" --prompt-file ~/flowai-prompts/prompt-commit-message.txt\n\n"
                "[bold blue]4. Use clipboard content:[/bold blue]\n"
                "   flowai --context-from-clipboard --prompt-file ~/flowai-prompts/prompt-commit-message.txt\n",
                title="Context Required",
                border_style="red"
            ))
            raise typer.Exit(code=1)

        # Add context to prompt
        if context:
            if debug:
                print("\n[#555555]Adding context to prompt...[/#555555]", file=sys.stderr)
            if "{{CONTEXT}}" in full_prompt:
                full_prompt = full_prompt.replace("{{CONTEXT}}", context)
            else:
                # If no {{CONTEXT}} tag is found, append the context
                full_prompt = f"{full_prompt}\n\n__START_CONTEXT__\n{context}\n__END_CONTEXT__"

            if debug:
                print("\n[#555555]Context:[/#555555]", file=sys.stderr)
                print(f"[#555555]{context}[/#555555]", file=sys.stderr)

        if debug:
            print("\n[#555555]Final Prompt to LLM:[/#555555]", file=sys.stderr)
            print(f"[#555555]{full_prompt}[/#555555]", file=sys.stderr)

        start_time = time.time()
        full_response = ""
        image_data_pattern = r'\[IMAGE_DATA_(\d+)\]\nMIME-Type: (.*?)\nPath: (.*?)\n\[/IMAGE_DATA_\1\]'

        if stream:
            response_text = ""
            for chunk in llm_connector.send_prompt(prompt=full_prompt, debug=debug):
                response_text += chunk
                sys.stdout.write(chunk)
                sys.stdout.flush()

            # Check for image data in the response
            image_matches = re.findall(image_data_pattern, response_text)
            if image_matches:
                console.print("\n[bold green]Images detected in response:[/bold green]")
                for idx, mime_type, path in image_matches:
                    console.print(f"[green]Image {idx}: {mime_type}[/green]")
                    console.print(f"[green]Saved to: {path}[/green]")

                    # Try to get image dimensions
                    try:
                        from PIL import Image
                        image = Image.open(path)
                        width, height = image.size
                        console.print(f"[green]Dimensions: {width}x{height}[/green]")
                    except ImportError:
                        console.print("[yellow]PIL/Pillow not installed. Cannot get image dimensions.[/yellow]")
                    except Exception as e:
                        console.print(f"[yellow]Could not get image dimensions: {str(e)}[/yellow]")

            sys.stdout.write("\n")
            sys.stdout.flush()
        else:
            with Live(generate_status_table(0), refresh_per_second=10, transient=not debug) as live:
                for chunk in llm_connector.send_prompt(prompt=full_prompt, debug=debug):
                    full_response += chunk
                    elapsed_time = time.time() - start_time
                    live.update(generate_status_table(elapsed_time))

                # Check for image data in the response
                image_matches = re.findall(image_data_pattern, full_response)
                if image_matches:
                    console.print("\n[bold green]Images detected in response:[/bold green]")
                    for idx, mime_type, path in image_matches:
                        console.print(f"[green]Image {idx}: {mime_type}[/green]")
                        console.print(f"[green]Saved to: {path}[/green]")

                        # Try to get image dimensions
                        try:
                            from PIL import Image
                            image = Image.open(path)
                            width, height = image.size
                            console.print(f"[green]Dimensions: {width}x{height}[/green]")
                        except ImportError:
                            console.print("[yellow]PIL/Pillow not installed. Cannot get image dimensions.[/yellow]")
                        except Exception as e:
                            console.print(f"[yellow]Could not get image dimensions: {str(e)}[/yellow]")

                # Remove image data markers from the response
                full_response = re.sub(image_data_pattern, '', full_response)

        elapsed_time = time.time() - start_time
        if debug:
            print(f"[bold blue]Total response time:[/bold blue] {elapsed_time:.3f}s", file=sys.stderr)
            print("[bold green]Response:[/bold green]\n", file=sys.stderr)
        if no_markdown:
            sys.stdout.write(full_response)
            sys.stdout.flush()
        else:
            # Process the response to ensure proper markdown formatting
            lines = full_response.splitlines()
            formatted_lines = []
            in_list = False

            for line in lines:
                line = line.rstrip()
                # Handle bullet points
                if line.strip().startswith('•'):
                    if not in_list:
                        formatted_lines.append('')  # Add space before list starts
                        in_list = True
                    formatted_lines.append(line.replace('•', '*'))
                else:
                    # If we're leaving a list, add extra space
                    if in_list and line.strip():
                        formatted_lines.append('')
                        in_list = False
                    # Add paragraphs with proper spacing
                    if line.strip():
                        formatted_lines.append(line)
                    elif formatted_lines and formatted_lines[-1] != '':
                        formatted_lines.append('')

            # Ensure proper spacing at the end
            if formatted_lines and formatted_lines[-1] != '':
                formatted_lines.append('')

            formatted_response = '\n'.join(formatted_lines)
            md = Markdown(formatted_response, justify="left")
            console.print(md)

        # Print model and token usage to stderr only if not entering chat mode
        if not chat:
            if debug:
                from rich.console import Console
                stderr_console = Console(file=sys.stderr)
                stderr_console.print(f"[dim]Token usage - Input: {llm_connector.input_tokens}, Output: {llm_connector.output_tokens}[/dim]")
            thinking_info = ""
            if "gemini" in llm_connector.model and "2.5" in llm_connector.model:
                thinking_status = "enabled" if llm_connector.thinking_mode else "disabled"
                thinking_info = f" | Thinking mode: {thinking_status} (budget: {llm_connector.thinking_budget})"
            from rich.console import Console
            stderr_console = Console(file=sys.stderr)
            stderr_console.print(f"\n\n[dim]Model used: {llm_connector.model} | Input tokens: {llm_connector.input_tokens} | Output tokens: {llm_connector.output_tokens}{thinking_info} | Elapsed time: {elapsed_time:.3f}s[/dim]")

        # Handle chat mode
        if chat:
            if debug:
                print("\n[#555555]Starting chat mode...[/#555555]", file=sys.stderr)

            # Create initial context if we don't have one yet
            if not initial_context:
                initial_context = {
                    'input_tokens': llm_connector.input_tokens,
                    'output_tokens': llm_connector.output_tokens
                }
                if context:
                    initial_context['context'] = context
                if prompt:
                    initial_context['prompt'] = prompt
                if full_prompt:
                    initial_context['full_prompt'] = full_prompt
                if 'response' in locals():
                    initial_context['last_response'] = response
                if uploaded_files:
                    initial_context['files'] = uploaded_files

            if debug and initial_context:
                print("[#555555]With initial context:[/#555555]", file=sys.stderr)
                print(f"[#555555]{initial_context}[/#555555]", file=sys.stderr)

            handle_chat_mode(llm_connector, initial_context, no_markdown, debug, web_search)
            return

    except Exception as e:
        # Handle error display more elegantly
        error_message = str(e)
        error_type = type(e).__name__

        # Check for LiteLLM specific errors
        if "litellm" in error_type.lower() or "litellm" in error_message.lower():
            # Special handling for rate limit errors
            if "RateLimitError" in error_type or "rate limit" in error_message.lower():
                console.print("[bold red]Rate limit exceeded.[/bold red] Please wait before making another request.")

                # Extract useful information using our utility function
                api_message = extract_from_json_error(error_message, "message")
                if api_message:
                    console.print(f"[red]API Message:[/red] {api_message}")

                retry_delay = extract_from_json_error(error_message, "retryDelay")
                if retry_delay:
                    console.print(f"[yellow]Recommended: Wait {retry_delay} before trying again.[/yellow]")

                # Check for quota details
                quota_metric = extract_from_json_error(error_message, "quotaMetric")
                if quota_metric:
                    console.print(f"[yellow]Quota metric: {quota_metric}[/yellow]")

                # Provide a tip for free tier users
                if "gemini" in error_message.lower() and "free" in error_message.lower():
                    console.print("[yellow]Tip: Google Gemini free tier has strict rate limits. Consider using a different model or provider.[/yellow]")

                # Skip printing full error details, even in debug mode
                if debug:
                    console.print("\n[dim]Use --debug flag to see the full error trace.[/dim]")
                return
            else:
                # Handle other LiteLLM errors
                # Try to extract a cleaner message
                clean_message = error_message
                if ": " in error_message:
                    clean_message = error_message.split(": ")[-1]

                console.print(f"[bold red]LLM Error:[/bold red] {clean_message}")
        # Check for common error types across different LLM providers
        elif "api key" in error_message.lower() or "authentication" in error_message.lower():
            console.print("[bold red]Authentication error.[/bold red] Please check your API key.")
        elif "too many tokens" in error_message.lower() or "maximum context" in error_message.lower():
            console.print("[bold red]Too much content for the model to process.[/bold red] Try reducing your input or using a model with larger context.")
        elif "not found" in error_message.lower() and "model" in error_message.lower():
            console.print("[bold red]Model not found.[/bold red] Please check the model name and ensure it's available.")
        elif "unsupported" in error_message.lower():
            console.print("[bold red]Unsupported operation.[/bold red] " + error_message)
        elif "timeout" in error_message.lower():
            console.print("[bold red]Request timed out.[/bold red] Please try again later.")
        else:
            # Extract just the error message without the traceback for general errors
            if ": " in error_message:
                error_type, clean_message = error_message.split(": ", 1)
                console.print(f"[bold red]Error ({error_type}):[/bold red] {clean_message}")
            else:
                console.print(f"[bold red]Error:[/bold red] {error_message}")

        # Only show the full traceback in debug mode
        if debug:
            console.print("\n[dim]Full error details:[/dim]")
            traceback.print_exc()

if __name__ == "__main__":
    app()
