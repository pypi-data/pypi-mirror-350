import os
import anthropic
from openai import OpenAI
from groq import Groq
from google import genai
from google.genai import types
import requests
import json
from typing import Generator, List, Dict, Optional
import traceback
import sys
import configparser
import time
import base64
from io import BytesIO
from litellm import completion, completion_cost, token_counter
import platform
import subprocess

# Suppress Google API and gRPC logging
os.environ['GRPC_VERBOSITY'] = 'ERROR'
os.environ['GLOG_minloglevel'] = '2'
os.environ['GRPC_PYTHON_LOG_LEVEL'] = 'ERROR'
os.environ['GRPC_TRACE'] = 'none'
os.environ['GRPC_VERBOSITY'] = 'NONE'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def open_image(image_path):
    system = platform.system().lower()
    try:
        if system == 'darwin':  # macOS
            subprocess.run(['open', image_path])
        elif system == 'windows':
            os.startfile(image_path)  # Windows default
        else:  # Linux
            viewers = ['eog', 'gwenview', 'feh', 'xdg-open']
            for viewer in viewers:
                try:
                    subprocess.run([viewer, image_path])
                    break
                except FileNotFoundError:
                    continue
    except Exception as e:
        print(f"Could not open image viewer: {str(e)}", file=sys.stderr)

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

class LLMConnector:
    def __init__(self, config, model=None, system_prompt=None, stream_mode=True, web_search=False, thinking_budget=0):
        self.config = config
        self.model = model or config.get('DEFAULT', 'default_model', fallback='')
        self.system_prompt = system_prompt or 'You are a helpful assistant with a cheerful disposition.'
        self.input_tokens = 0
        self.output_tokens = 0
        self.stream_mode = stream_mode
        self.web_search = web_search
        self.thinking_budget = thinking_budget
        self.thinking_mode = thinking_budget > 0
        self.create_image_mode = False  # Add this flag to track if we're in image creation mode
        self.debug = False  # Default to False, will be set by main.py when --debug is used

        # Cache management
        self.cached_files = []  # Track uploaded files (path, uri)
        self.cache_id = None    # ID of the current cached content
        self.uploaded_files = []  # Track uploaded file objects for small files that can't be cached

        # Skip API key setup for test model
        if not self.model.startswith('test:'):
            self.setup_api_keys()

            # Initialize clients only if we have API keys
            openai_key = self.config.get('DEFAULT', 'openai_api_key', fallback='')
            self.openai_client = OpenAI(api_key=openai_key) if openai_key else None

            anthropic_key = self.config.get('DEFAULT', 'anthropic_api_key', fallback='')
            self.anthropic_client = anthropic.Anthropic(api_key=anthropic_key) if anthropic_key else None

            groq_key = self.config.get('DEFAULT', 'groq_api_key', fallback='')
            self.groq_client = Groq(api_key=groq_key) if groq_key else None

            google_key = self.config.get('DEFAULT', 'google_api_key', fallback='')
            if google_key:
                client = genai.Client(api_key=google_key)
                self.google_client = client
            else:
                self.google_client = None

    def setup_api_keys(self):
        for key in ['openai_api_key', 'anthropic_api_key', 'groq_api_key', 'google_api_key']:
            if key not in self.config['DEFAULT'] or not self.config['DEFAULT'][key]:
                self.config['DEFAULT'][key] = os.environ.get(key.upper(), '')
            # Set environment variables for LiteLLM
            env_var_name = key.upper()
            api_key_value = self.config['DEFAULT'][key]
            os.environ[env_var_name] = api_key_value
            # Also set GEMINI_API_KEY if GOOGLE_API_KEY is set, as LiteLLM might prefer it
            if env_var_name == 'GOOGLE_API_KEY' and api_key_value:
                os.environ['GEMINI_API_KEY'] = api_key_value

    def get_available_models(self, provider) -> List[str]:
        if provider == "openai":
            return self.get_openai_models()
        elif provider == "anthropic":
            return self.get_anthropic_models()
        elif provider == "ollama":
            return self.get_ollama_models()
        elif provider == "groq":
            return self.get_groq_models()
        elif provider == "gemini":
            return self.get_google_models()
        else:
            return [f"Unsupported provider: {provider}"]

    def get_openai_models(self) -> List[str]:
        if not self.config.get('DEFAULT', 'openai_api_key'):
            return ["No API key set"]
        if not self.openai_client:
            return ["Error: OpenAI client not initialized"]
        try:
            openai_models = self.openai_client.models.list()
            return [model.id for model in openai_models.data if model.id.startswith("gpt")]
        except Exception as e:
            print(f"Error fetching OpenAI models: {str(e)}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            return ["Error fetching models"]

    def get_anthropic_models(self) -> List[str]:
        """Get available Anthropic models"""
        if not self.config.get('DEFAULT', 'anthropic_api_key'):
            return ["No API key set"]
        try:
            models = self.anthropic_client.models.list()
            sorted_models = sorted([model.id for model in models.data])
            return sorted_models
        except Exception as e:
            print(f"Error fetching Anthropic models: {str(e)}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            return ["Error fetching models"]

    def get_ollama_models(self) -> List[str]:
        # Read the base URL from config, falling back to the default
        ollama_base_url = self.config.get('DEFAULT', 'ollama_base_url', fallback='http://localhost:11434')
        ollama_tags_url = f"{ollama_base_url}/api/tags"
        try:
            # Add a timeout (e.g., 5 seconds) to prevent hanging
            response = requests.get(ollama_tags_url, timeout=5)
            # Raise an HTTPError for bad responses (4xx or 5xx)
            response.raise_for_status()

            ollama_models = response.json().get('models', [])
            return [model['name'] for model in ollama_models]

        except requests.exceptions.ConnectionError:
            # Specifically handle connection errors (server down, wrong address/port)
            print(f"Error: Could not connect to Ollama server at {ollama_base_url}. Please ensure it is running.", file=sys.stderr)
            return ["Ollama server not reachable"] # Return a more specific status
        except requests.exceptions.Timeout:
            # Handle timeouts
            print(f"Error: Connection to Ollama server at {ollama_base_url} timed out.", file=sys.stderr)
            return ["Ollama connection timed out"]
        except requests.exceptions.RequestException as e:
            # Handle other request errors (like HTTP errors from raise_for_status)
            print(f"Error fetching Ollama models: {str(e)}", file=sys.stderr)
            return ["Error fetching models"]
        except Exception as e:
            # Catch any other unexpected errors (e.g., JSON decoding)
            print(f"Unexpected error fetching Ollama models: {str(e)}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            return ["Unexpected error fetching models"]

    def get_groq_models(self) -> List[str]:
        if not self.config.get('DEFAULT', 'groq_api_key'):
            return ["No API key set"]
        try:
            groq_models = self.groq_client.models.list()
            return [model.id for model in groq_models.data]
        except Exception as e:
            print(f"Error fetching Groq models: {str(e)}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            return ["Error fetching models"]

    def get_google_models(self) -> List[str]:
        if not self.config.get('DEFAULT', 'google_api_key'):
            return ["No API key set"]
        try:
            models = self.google_client.models.list()
            google_models = []
            for m in models:
                if 'generateContent' in m.supported_actions:
                    # Strip the 'models/' prefix from the model name
                    name = m.name.replace('models/', '')
                    google_models.append(name)
            return google_models
        except Exception as e:
            print(f"Error fetching Google models: {str(e)}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            return ["Error fetching models"]

    def send_prompt(self, prompt: str, debug: bool = False) -> Generator[str, None, None]:
        if debug:
            print(f"\n[DEBUG] Sending prompt with model: {self.model}", file=sys.stderr)

        # Store the prompt for potential use in direct API calls
        self.last_prompt = prompt

        try:
            if self.model.startswith('test:'):
                yield from self.send_prompt_test(prompt, debug)
                return

            # If we have cached content or uploaded files for Gemini models, use Google GenAI SDK directly
            provider = self.model.split('/')[0] if '/' in self.model else None
            if provider == 'gemini' and (self.cache_id or self.uploaded_files):
                yield from self._send_prompt_with_files(prompt, debug)
                return

            # Add current date and time to system prompt if web search is enabled
            system_content = self.system_prompt
            if self.web_search:
                from datetime import datetime
                current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                system_content = f"{self.system_prompt}\n\nCurrent date and time: {current_datetime}\n\nWhen using web search, you MUST include citations for your information sources. After your response, list all sources with their URLs and webpage titles in a completely new section titled 'Sources:'."
                if debug:
                    print(f"\n[DEBUG] Added current datetime to system prompt: {current_datetime}", file=sys.stderr)

            messages = [
                {"role": "user", "content": system_content},
                {"role": "user", "content": prompt}
            ]

            # Determine provider and get the correct API key
            provider = self.model.split('/')[0] if '/' in self.model else None
            api_key = None
            if provider == 'gemini':
                api_key = self.config.get('DEFAULT', 'google_api_key', fallback=None)
            elif provider == 'openai':
                api_key = self.config.get('DEFAULT', 'openai_api_key', fallback=None)
            elif provider == 'anthropic':
                api_key = self.config.get('DEFAULT', 'anthropic_api_key', fallback=None)
            elif provider == 'groq':
                api_key = self.config.get('DEFAULT', 'groq_api_key', fallback=None)
            # Add other providers as needed

            # Model name is already in the correct format
            model_to_use = self.model

            completion_args = {
                "model": model_to_use,
                "messages": messages,
                "stream": self.stream_mode
            }
            if api_key:
                completion_args["api_key"] = api_key

            # Set thinking budget for Gemini 2.5 models
            if provider == 'gemini' and '2.' in model_to_use:
                thinking_status = "enabled" if self.thinking_mode else "disabled"
                from rich.console import Console
                stderr_console = Console(file=sys.stderr)
                stderr_console.print(f"\n[dim]Gemini 2.5 thinking mode is {thinking_status} with budget: {self.thinking_budget}[/dim]")

                # Always enable image response modalities for Gemini models
                # This ensures all Gemini models can return images if they're capable
                completion_args["additional_params"] = {
                    "generationConfig": {
                        "response_modalities": ["TEXT", "IMAGE"],
                        "thinkingConfig": {
                            "thinkingBudget": self.thinking_budget
                        }
                    }
                }
            # Attach cached content if available
            if self.cache_id and provider == 'gemini':
                # For LiteLLM, we need to pass cached content in the generationConfig
                completion_args.setdefault("additional_params", {}).setdefault("generationConfig", {})["cachedContent"] = self.cache_id
                if debug:
                    print(f"\n[DEBUG] Using cached content: {self.cache_id}", file=sys.stderr)

            # Add web search capability if requested and supported
            if self.web_search and provider == 'gemini':
                completion_args["tools"] = [{"googleSearch": {}}]
                if debug:
                    print(f"\n[DEBUG] Enabling web search for {model_to_use}", file=sys.stderr)

            # Reset token counts before processing response
            self.input_tokens = 0
            self.output_tokens = 0

            # Count input tokens using token_counter
            try:
                self.input_tokens = token_counter(model=model_to_use, messages=messages)
            except Exception as e:
                # If token counting fails, use a simple word count estimate
                self.input_tokens = len(prompt.split()) + len(self.system_prompt.split())
                if debug:
                    print(f"\n[DEBUG] Token counting failed: {str(e)}. Using word count estimate.", file=sys.stderr)

            try:
                response = completion(**completion_args)
            except Exception as e:
                # More user-friendly error output
                error_message = str(e)
                error_type = type(e).__name__

                print(f"\n[DEBUG] Error message: {error_message}", file=sys.stderr)
                print(f"\n[DEBUG] Error type: {error_type}", file=sys.stderr)

                from rich.console import Console
                stderr_console = Console(file=sys.stderr)

                # Print the error details when debug is enabled
                if debug:
                    stderr_console.print(f"\n[red]Error in send_prompt:[/red] {error_type}: {error_message}")
                    traceback.print_exc(file=sys.stderr)
                else:
                    # For non-debug mode, print a simpler error message
                    stderr_console.print(f"\n[red]Error:[/red] {error_message}")

                # Special handling for rate limit errors
                if "RateLimitError" in error_type or "rate limit" in error_message.lower() or "ratelimit" in error_message.lower() or "429" in error_message:
                    stderr_console.print(f"\n[yellow]Rate limit exceeded for {provider}. Please try again later.[/yellow]")

                    # Extract and display the specific message from Google API
                    if provider == "gemini":
                        stderr_console.print("[yellow]Google Gemini has strict rate limits on free tier accounts.[/yellow]")

                        # Extract and display useful error information
                        api_message = extract_from_json_error(error_message, "message")
                        if api_message:
                            stderr_console.print(f"[yellow]API Message: {api_message}[/yellow]")

                        retry_delay = extract_from_json_error(error_message, "retryDelay")
                        if retry_delay:
                            stderr_console.print(f"[yellow]Suggested retry delay: {retry_delay}[/yellow]")

                        # Check for quota details
                        quota_metric = extract_from_json_error(error_message, "quotaMetric")
                        if quota_metric:
                            stderr_console.print(f"[yellow]Quota metric: {quota_metric}[/yellow]")

                # Try to extract useful information from JSON error messages
                if '"message"' in error_message:
                    api_message = extract_from_json_error(error_message, "message")
                    if api_message:
                        error_message = api_message

                # Return a friendly error message that doesn't expose too many technical details
                yield f"Error: {error_message}"

            # Process response

            # Collect response content
            response_content = ""
            citations = []
            image_parts = []

            if self.stream_mode:
                for chunk in response:
                    if chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        response_content += content
                        yield content

                    # Check for citations in tool calls
                    if hasattr(chunk.choices[0].delta, 'tool_calls') and chunk.choices[0].delta.tool_calls:
                        for tool_call in chunk.choices[0].delta.tool_calls:
                            if hasattr(tool_call, 'function'):
                                if hasattr(tool_call.function, 'name') and tool_call.function.name == 'googleSearch':
                                    try:
                                        import json
                                        search_results = json.loads(tool_call.function.arguments)
                                        if 'searchResults' in search_results:
                                            for result in search_results['searchResults']:
                                                citations.append(result)
                                        # Try alternative formats
                                        elif 'results' in search_results:
                                            for result in search_results['results']:
                                                citations.append(result)
                                    except Exception as e:
                                        pass

                    # Check for image parts in the response
                    if hasattr(chunk.choices[0].delta, 'additional_kwargs') and 'parts' in chunk.choices[0].delta.additional_kwargs:
                        parts = chunk.choices[0].delta.additional_kwargs['parts']
                        for part in parts:
                            if 'inline_data' in part:
                                try:
                                    inline_data = part['inline_data']
                                    mime_type = inline_data.get('mime_type', 'unknown/unknown')
                                    if mime_type.startswith('image/'):
                                        base64_data = inline_data.get('data', '')
                                        image_parts.append({
                                            'mime_type': mime_type,
                                            'data': base64_data
                                        })
                                        print(f"\n[green]Image detected in response! MIME type: {mime_type}[/green]", file=sys.stderr)
                                except Exception as e:
                                    print(f"Error processing image part: {str(e)}", file=sys.stderr)
            else:
                response_content = response.choices[0].message.content
                yield response_content

                # Check for citations in tool calls for non-streaming response
                if hasattr(response.choices[0].message, 'tool_calls') and response.choices[0].message.tool_calls:
                    print(f"\n[#555555]Found tool_calls in response: {response.choices[0].message.tool_calls}[/#555555]", file=sys.stderr)
                    for tool_call in response.choices[0].message.tool_calls:
                        print(f"\n[#555555]Processing tool_call: {tool_call}[/#555555]", file=sys.stderr)
                        if hasattr(tool_call, 'function'):
                            print(f"\n[#555555]Function: {tool_call.function}[/#555555]", file=sys.stderr)
                            if hasattr(tool_call.function, 'name') and tool_call.function.name == 'googleSearch':
                                try:
                                    import json
                                    print(f"\n[#555555]Function arguments: {tool_call.function.arguments}[/#555555]", file=sys.stderr)
                                    search_results = json.loads(tool_call.function.arguments)
                                    print(f"\n[#555555]Parsed search results: {search_results}[/#555555]", file=sys.stderr)
                                    if 'searchResults' in search_results:
                                        for result in search_results['searchResults']:
                                            citations.append(result)
                                    # Try alternative formats
                                    elif 'results' in search_results:
                                        for result in search_results['results']:
                                            citations.append(result)
                                except Exception as e:
                                    print(f"Error parsing search results: {str(e)}", file=sys.stderr)

                # Check for image parts in non-streaming response
                if hasattr(response.choices[0].message, 'additional_kwargs') and 'parts' in response.choices[0].message.additional_kwargs:
                    parts = response.choices[0].message.additional_kwargs['parts']
                    for part in parts:
                        if 'inline_data' in part:
                            try:
                                inline_data = part['inline_data']
                                mime_type = inline_data.get('mime_type', 'unknown/unknown')
                                if mime_type.startswith('image/'):
                                    base64_data = inline_data.get('data', '')
                                    image_parts.append({
                                        'mime_type': mime_type,
                                        'data': base64_data
                                    })
                                    print(f"\n[green]Image detected in response! MIME type: {mime_type}[/green]", file=sys.stderr)
                            except Exception as e:
                                print(f"Error processing image part: {str(e)}", file=sys.stderr)

            # Display citations if available and web search was used
            if self.web_search:
                # Print raw response for debugging
                if hasattr(response, 'choices') and response.choices:
                    choice = response.choices[0]

                    # Check for groundingMetadata in additional_kwargs
                    if hasattr(choice, 'message') and hasattr(choice.message, 'additional_kwargs'):
                        additional_kwargs = choice.message.additional_kwargs
                        # Extract grounding metadata if available
                        grounding_metadata = additional_kwargs.get("groundingMetadata", {})

                        # Extract citations from grounding chunks
                        for chunk in grounding_metadata.get("groundingChunks", []):
                            web = chunk.get("web", {})
                            if web:
                                citations.append({
                                    "title": web.get("title", "Source"),
                                    "url": web.get("uri", ""),
                                    "snippet": web.get("snippet", "")
                                })

                    # Tool calls are already processed in the streaming and non-streaming sections

                    # Check for tool_response field
                    if hasattr(choice, 'message') and hasattr(choice.message, 'tool_response'):
                        try:
                            if isinstance(choice.message.tool_response, dict) and 'results' in choice.message.tool_response:
                                for result in choice.message.tool_response['results']:
                                    citations.append(result)
                        except Exception as e:
                            pass

            # Process and display any detected images
            if image_parts:
                from rich.console import Console
                stderr_console = Console(file=sys.stderr)
                stderr_console.print("\n[bold green]Images detected in response:[/bold green]")

                for i, img_part in enumerate(image_parts):
                    mime_type = img_part['mime_type']
                    base64_data = img_part['data']

                    # Display image information
                    stderr_console.print(f"[green]Image {i+1}: {mime_type}[/green]")

                    # Try to decode and get image dimensions
                    try:
                        from PIL import Image
                        image_bytes = base64.b64decode(base64_data)
                        image = Image.open(BytesIO(image_bytes))
                        width, height = image.size
                        stderr_console.print(f"[green]Dimensions: {width}x{height}[/green]")

                        # Create a temporary file with the appropriate extension
                        ext = mime_type.split('/')[-1]
                        fd, temp_path = tempfile.mkstemp(suffix=f'.{ext}')
                        os.close(fd)

                        # Write the image data to the file
                        with open(temp_path, 'wb') as f:
                            f.write(image_bytes)

                        # Open the image automatically
                        open_image(temp_path)

                        # Print the path to stdout so it can be captured
                        print(f"\n\n[IMAGE_DATA_{i+1}]\nMIME-Type: {mime_type}\nPath: {temp_path}\n[/IMAGE_DATA_{i+1}]")

                    except ImportError:
                        stderr_console.print("[yellow]PIL/Pillow not installed. Cannot process image details.[/yellow]")
                    except Exception as e:
                        stderr_console.print(f"[red]Error processing image: {str(e)}[/red]")

            # Estimate output tokens by word count
            self.output_tokens = len(response_content.split())

        except Exception as e:
            if debug:
                print(f"Error: {str(e)}", file=sys.stderr)
                traceback.print_exc(file=sys.stderr)
            yield f"Error: {str(e)}"

    def chat_completion(self, messages: List[Dict[str, str]], stream: bool = True) -> Generator[str, None, None]:
        try:
            # Store messages for potential use in direct API calls
            self.messages = messages

            if self.model.startswith('test:'):
                yield from self._chat_completion_test(messages, stream)
                return

            # If we have cached content or uploaded files for Gemini models, use Google GenAI SDK directly
            provider = self.model.split('/')[0] if '/' in self.model else None
            if provider == 'gemini' and (self.cache_id or self.uploaded_files):
                yield from self._chat_completion_with_files(messages, stream)
                return

            # Add current date and time to the first system message if web search is enabled
            if self.web_search and messages and messages[0]["role"] == "system":
                from datetime import datetime
                current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                messages[0]["content"] = f"{messages[0]['content']}\n\nCurrent date and time: {current_datetime}\n\nWhen using web search, you MUST include citations for your information sources. After your response, list all sources with their webpage titles and URLs inside a bulleted list in a completely new section titled 'Sources:'."

            # Determine provider and get the correct API key
            provider = self.model.split('/')[0] if '/' in self.model else None
            api_key = None
            if provider == 'gemini':
                api_key = self.config.get('DEFAULT', 'google_api_key', fallback=None)
            elif provider == 'openai':
                api_key = self.config.get('DEFAULT', 'openai_api_key', fallback=None)
            elif provider == 'anthropic':
                api_key = self.config.get('DEFAULT', 'anthropic_api_key', fallback=None)
            elif provider == 'groq':
                api_key = self.config.get('DEFAULT', 'groq_api_key', fallback=None)
            # Add other providers as needed

            # Model name is already in the correct format
            model_to_use = self.model

            completion_args = {
                "model": model_to_use,
                "messages": messages,
                "stream": stream
            }
            if api_key:
                completion_args["api_key"] = api_key

            # Set thinking budget for Gemini 2.5 models
            if provider == 'gemini' and '2.' in model_to_use:
                thinking_status = "enabled" if self.thinking_mode else "disabled"
                from rich.console import Console
                stderr_console = Console(file=sys.stderr)
                stderr_console.print(f"\n[dim]Gemini 2.5 thinking mode is {thinking_status} with budget: {self.thinking_budget}[/dim]")

                # Always enable image response modalities for Gemini models
                # This ensures all Gemini models can return images if they're capable
                completion_args["additional_params"] = {
                    "generationConfig": {
                        "response_modalities": ["TEXT", "IMAGE"],
                        "thinkingConfig": {
                            "thinkingBudget": self.thinking_budget
                        }
                    }
                }

            # Attach cached content if available
            if self.cache_id and provider == 'gemini':
                # For LiteLLM, we need to pass cached content in the generationConfig
                completion_args.setdefault("additional_params", {}).setdefault("generationConfig", {})["cachedContent"] = self.cache_id
                if hasattr(self, 'debug') and self.debug:
                    print(f"\n[DEBUG] Using cached content in chat: {self.cache_id}", file=sys.stderr)

            # Add web search capability if requested and supported
            if self.web_search and provider == 'gemini':
                completion_args["tools"] = [{"googleSearch": {}}]

            # Reset token counts before processing response
            self.input_tokens = 0
            self.output_tokens = 0

            # Count input tokens using token_counter
            try:
                self.input_tokens = token_counter(model=model_to_use, messages=messages)
            except Exception as e:
                # If token counting fails, use a simple word count estimate
                total_words = 0
                for msg in messages:
                    if 'content' in msg and msg['content']:
                        total_words += len(msg['content'].split())
                self.input_tokens = total_words
                if hasattr(self, 'debug') and self.debug:
                    print(f"\n[DEBUG] Token counting failed: {str(e)}. Using word count estimate.", file=sys.stderr)

            try:
                response = completion(**completion_args)
            except Exception as e:
                # More user-friendly error output
                error_message = str(e)
                error_type = type(e).__name__

                from rich.console import Console
                stderr_console = Console(file=sys.stderr)

                # Print the error details when debug is enabled
                if hasattr(self, 'debug') and self.debug:
                    stderr_console.print(f"\n[red]Error in chat_completion:[/red] {error_type}: {error_message}")
                    traceback.print_exc(file=sys.stderr)
                else:
                    # For non-debug mode, print a simpler error message
                    stderr_console.print(f"\n[red]Error:[/red] {error_message}")

                # Special handling for rate limit errors
                if "RateLimitError" in error_type or "rate limit" in error_message.lower() or "ratelimit" in error_message.lower() or "429" in error_message:
                    stderr_console.print(f"\n[yellow]Rate limit exceeded for {provider}. Please try again later.[/yellow]")

                    # Extract and display the specific message from Google API
                    if provider == "gemini":
                        stderr_console.print("[yellow]Google Gemini has strict rate limits on free tier accounts.[/yellow]")

                        # Extract and display useful error information
                        api_message = extract_from_json_error(error_message, "message")
                        if api_message:
                            stderr_console.print(f"[yellow]API Message: {api_message}[/yellow]")

                        retry_delay = extract_from_json_error(error_message, "retryDelay")
                        if retry_delay:
                            stderr_console.print(f"[yellow]Suggested retry delay: {retry_delay}[/yellow]")

                        # Check for quota details
                        quota_metric = extract_from_json_error(error_message, "quotaMetric")
                        if quota_metric:
                            stderr_console.print(f"[yellow]Quota metric: {quota_metric}[/yellow]")

                # Try to extract useful information from JSON error messages
                if '"message"' in error_message:
                    api_message = extract_from_json_error(error_message, "message")
                    if api_message:
                        error_message = api_message

                # Return a friendly error message that doesn't expose too many technical details
                yield f"Error: {error_message}"

            # Debug: Print raw response structure
            if self.model.startswith('gemini/'):
                from rich.console import Console
                stderr_console = Console(file=sys.stderr)

                # Only show detailed response structure in debug mode
                if hasattr(self, 'debug') and self.debug:
                    stderr_console.print("\n[dim]Debugging Gemini response structure:[/dim]")

                    # Print response type and attributes
                    stderr_console.print(f"[dim]Response type: {type(response)}[/dim]")
                    stderr_console.print(f"[dim]Response attributes: {dir(response)}[/dim]")

                    # Try to access and print the first choice
                    if hasattr(response, 'choices') and response.choices:
                        choice = response.choices[0]
                        stderr_console.print(f"[dim]First choice type: {type(choice)}[/dim]")
                        stderr_console.print(f"[dim]First choice attributes: {dir(choice)}[/dim]")

                        # Check for message
                        if hasattr(choice, 'message'):
                            message = choice.message
                            stderr_console.print(f"[dim]Message type: {type(message)}[/dim]")
                            stderr_console.print(f"[dim]Message attributes: {dir(message)}[/dim]")

                            # Check for additional_kwargs
                            if hasattr(message, 'additional_kwargs'):
                                stderr_console.print(f"[dim]additional_kwargs: {message.additional_kwargs}[/dim]")

            # Process response

            # Collect response content
            response_content = ""
            citations = []
            image_parts = []

            if stream:
                for chunk in response:
                    if chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        response_content += content
                        yield content

                    # Check for citations in tool calls
                    if hasattr(chunk.choices[0].delta, 'tool_calls') and chunk.choices[0].delta.tool_calls:
                        for tool_call in chunk.choices[0].delta.tool_calls:
                            if hasattr(tool_call, 'function'):
                                if hasattr(tool_call.function, 'name') and tool_call.function.name == 'googleSearch':
                                    try:
                                        import json
                                        search_results = json.loads(tool_call.function.arguments)
                                        if 'searchResults' in search_results:
                                            for result in search_results['searchResults']:
                                                citations.append(result)
                                        # Try alternative formats
                                        elif 'results' in search_results:
                                            for result in search_results['results']:
                                                citations.append(result)
                                    except Exception as e:
                                        pass

                    # Add detailed debugging for response structure
                    if hasattr(chunk.choices[0].delta, 'additional_kwargs'):
                        from rich.console import Console
                        stderr_console = Console(file=sys.stderr)

                        # Only show debugging in debug mode
                        if hasattr(self, 'debug') and self.debug:
                            stderr_console.print("\n[dim]Checking for image parts in chunk...[/dim]")

                            # Debug: Print raw chunk structure
                            if self.model.startswith('gemini/'):
                                stderr_console.print(f"[dim]Chunk type: {type(chunk)}[/dim]")
                                stderr_console.print(f"[dim]Chunk attributes: {dir(chunk)}[/dim]")

                                # Print delta information
                                delta = chunk.choices[0].delta
                                stderr_console.print(f"[dim]Delta type: {type(delta)}[/dim]")
                                stderr_console.print(f"[dim]Delta attributes: {dir(delta)}[/dim]")
                                stderr_console.print(f"[dim]Delta additional_kwargs: {delta.additional_kwargs}[/dim]")

                            # Print the structure of additional_kwargs for debugging
                            additional_kwargs = chunk.choices[0].delta.additional_kwargs
                            stderr_console.print(f"[dim]additional_kwargs keys: {list(additional_kwargs.keys())}[/dim]")

                            # Check for parts in additional_kwargs
                            if 'parts' in additional_kwargs:
                                parts = additional_kwargs['parts']
                                stderr_console.print(f"[dim]Found {len(parts)} parts[/dim]")

                                for i, part in enumerate(parts):
                                    stderr_console.print(f"[dim]Part {i+1} keys: {list(part.keys())}[/dim]")

                                    # Check for inline_data
                                    if 'inline_data' in part:
                                        try:
                                            inline_data = part['inline_data']
                                            stderr_console.print(f"[dim]inline_data keys: {list(inline_data.keys())}[/dim]")

                                            mime_type = inline_data.get('mime_type', 'unknown/unknown')
                                            if mime_type.startswith('image/'):
                                                image_data = inline_data.get('data', '')
                                                image_parts.append({
                                                    'mime_type': mime_type,
                                                    'data': image_data
                                                })
                                                stderr_console.print(f"[green]Image detected in response! MIME type: {mime_type}[/green]")
                                        except Exception as e:
                                            stderr_console.print(f"[red]Error processing inline_data: {str(e)}[/red]")

                                    # Check for other image-related fields
                                    if 'text' in part:
                                        stderr_console.print(f"[dim]Part contains text: {part['text'][:30]}...[/dim]")

                            # Check for other possible image structures
                            if 'content' in additional_kwargs:
                                content = additional_kwargs['content']
                                stderr_console.print(f"[dim]Found content field with type: {type(content)}[/dim]")

                                if isinstance(content, list):
                                    for i, item in enumerate(content):
                                        if isinstance(item, dict):
                                            stderr_console.print(f"[dim]Content item {i+1} keys: {list(item.keys())}[/dim]")

                                            # Check for image/inline_data in content items
                                            if 'type' in item and item['type'] == 'image':
                                                try:
                                                    if 'source' in item:
                                                        source = item['source']
                                                        if 'data' in source and 'mime_type' in source:
                                                            mime_type = source['mime_type']
                                                            image_data = source['data']
                                                            image_parts.append({
                                                                'mime_type': mime_type,
                                                                'data': image_data
                                                            })
                                                            stderr_console.print(f"[green]Image detected in content! MIME type: {mime_type}[/green]")
                                                except Exception as e:
                                                    stderr_console.print(f"[red]Error processing content item: {str(e)}[/red]")
            else:
                response_content = response.choices[0].message.content
                yield response_content

                # Check for citations in tool calls for non-streaming response
                if hasattr(response.choices[0].message, 'tool_calls') and response.choices[0].message.tool_calls:
                    for tool_call in response.choices[0].message.tool_calls:
                        if hasattr(tool_call, 'function'):
                            if hasattr(tool_call.function, 'name') and tool_call.function.name == 'googleSearch':
                                try:
                                    import json
                                    search_results = json.loads(tool_call.function.arguments)
                                    if 'searchResults' in search_results:
                                        for result in search_results['searchResults']:
                                            citations.append(result)
                                    # Try alternative formats
                                    elif 'results' in search_results:
                                        for result in search_results['results']:
                                            citations.append(result)
                                except Exception as e:
                                    pass

                # Add detailed debugging for non-streaming response
                if hasattr(response.choices[0].message, 'additional_kwargs'):
                    from rich.console import Console
                    stderr_console = Console(file=sys.stderr)

                    # Only show debugging in debug mode
                    if hasattr(self, 'debug') and self.debug:
                        stderr_console.print("\n[dim]Checking for image parts in non-streaming response...[/dim]")

                        # Print the structure of additional_kwargs for debugging
                        additional_kwargs = response.choices[0].message.additional_kwargs
                        stderr_console.print(f"[dim]additional_kwargs keys: {list(additional_kwargs.keys())}[/dim]")

                        # Check for parts in additional_kwargs
                        if 'parts' in additional_kwargs:
                            parts = additional_kwargs['parts']
                            stderr_console.print(f"[dim]Found {len(parts)} parts[/dim]")

                            for i, part in enumerate(parts):
                                stderr_console.print(f"[dim]Part {i+1} keys: {list(part.keys())}[/dim]")

                                # Check for inline_data
                                if 'inline_data' in part:
                                    try:
                                        inline_data = part['inline_data']
                                        stderr_console.print(f"[dim]inline_data keys: {list(inline_data.keys())}[/dim]")

                                        mime_type = inline_data.get('mime_type', 'unknown/unknown')
                                        if mime_type.startswith('image/'):
                                            image_data = inline_data.get('data', '')
                                            image_parts.append({
                                                'mime_type': mime_type,
                                                'data': image_data
                                            })
                                            stderr_console.print(f"[green]Image detected in response! MIME type: {mime_type}[/green]")
                                    except Exception as e:
                                        stderr_console.print(f"[red]Error processing inline_data: {str(e)}[/red]")

                                # Check for other image-related fields
                                if 'text' in part:
                                    stderr_console.print(f"[dim]Part contains text: {part['text'][:30]}...[/dim]")

                        # Check for other possible image structures
                        if 'content' in additional_kwargs:
                            content = additional_kwargs['content']
                            stderr_console.print(f"[dim]Found content field with type: {type(content)}[/dim]")

                            if isinstance(content, list):
                                for i, item in enumerate(content):
                                    if isinstance(item, dict):
                                        stderr_console.print(f"[dim]Content item {i+1} keys: {list(item.keys())}[/dim]")

                                        # Check for image/inline_data in content items
                                        if 'type' in item and item['type'] == 'image':
                                            try:
                                                if 'source' in item:
                                                    source = item['source']
                                                    if 'data' in source and 'mime_type' in source:
                                                        mime_type = source['mime_type']
                                                        image_data = source['data']
                                                        image_parts.append({
                                                            'mime_type': mime_type,
                                                            'data': image_data
                                                        })
                                                        stderr_console.print(f"[green]Image detected in content! MIME type: {mime_type}[/green]")
                                            except Exception as e:
                                                stderr_console.print(f"[red]Error processing content item: {str(e)}[/red]")

            # Display citations if available and web search was used
            if self.web_search:
                # Extract citations from response
                if hasattr(response, 'choices') and response.choices:
                    choice = response.choices[0]

                    # Check for groundingMetadata in additional_kwargs
                    if hasattr(choice, 'message') and hasattr(choice.message, 'additional_kwargs'):
                        additional_kwargs = choice.message.additional_kwargs

                        # Extract grounding metadata if available
                        grounding_metadata = additional_kwargs.get("groundingMetadata", {})

                        # Extract citations from grounding chunks
                        for chunk in grounding_metadata.get("groundingChunks", []):
                            web = chunk.get("web", {})
                            if web:
                                citations.append({
                                    "title": web.get("title", "Source"),
                                    "url": web.get("uri", ""),
                                    "snippet": web.get("snippet", "")
                                })

                    # Tool calls are already processed in the streaming and non-streaming sections

                    # Check for tool_response field
                    if hasattr(choice, 'message') and hasattr(choice.message, 'tool_response'):
                        try:
                            if isinstance(choice.message.tool_response, dict) and 'results' in choice.message.tool_response:
                                for result in choice.message.tool_response['results']:
                                    citations.append(result)
                        except Exception as e:
                            pass

            # Process and display any detected images
            if image_parts:
                from rich.console import Console
                stderr_console = Console(file=sys.stderr)
                stderr_console.print("\n[bold green]Images detected in response:[/bold green]")

                for i, img_part in enumerate(image_parts):
                    mime_type = img_part['mime_type']
                    image_data = img_part['data']

                    # Display image information
                    stderr_console.print(f"[green]Image {i+1}: {mime_type}[/green]")

                    # Save the image to a temporary file
                    import tempfile
                    import os

                    try:
                        # Create a temporary file with the appropriate extension
                        ext = mime_type.split('/')[-1]
                        fd, temp_path = tempfile.mkstemp(suffix=f'.{ext}')
                        os.close(fd)

                        # Write the image data to the file
                        with open(temp_path, 'wb') as f:
                            # If the data is a string (base64), decode it first
                            if isinstance(image_data, str):
                                image_data = base64.b64decode(image_data)
                            # Write the binary data
                            f.write(image_data)

                        stderr_console.print(f"[green]Image saved to: {temp_path}[/green]")

                        # Try to get image dimensions
                        try:
                            from PIL import Image
                            image = Image.open(temp_path)
                            width, height = image.size
                            stderr_console.print(f"[green]Dimensions: {width}x{height}[/green]")
                        except ImportError:
                            stderr_console.print("[yellow]PIL/Pillow not installed. Cannot get image dimensions.[/yellow]")
                        except Exception as e:
                            stderr_console.print(f"[yellow]Could not get image dimensions: {str(e)}[/yellow]")

                        # Print the image path to stdout so it can be captured
                        print(f"\n\n[IMAGE_DATA_{i+1}]\nMIME-Type: {mime_type}\nPath: {temp_path}\n[/IMAGE_DATA_{i+1}]")

                    except Exception as e:
                        stderr_console.print(f"[red]Error saving image: {str(e)}[/red]")

            # For Gemini models, try direct approach if no images were detected
            elif self.model.startswith('gemini/') and not image_parts and self.create_image_mode:
                try:
                    stderr_console = Console(file=sys.stderr)
                    stderr_console.print("\n[yellow]No images detected in LiteLLM response. Trying direct Google GenAI SDK approach...[/yellow]")

                    # Extract the prompt from messages
                    prompt = ""
                    if hasattr(self, 'messages') and self.messages:
                        # Find the last user message
                        for msg in reversed(self.messages):
                            if msg.get('role') == 'user':
                                prompt = msg.get('content', '')
                                break

                    # If no prompt found in messages, use the last prompt sent
                    if not prompt and hasattr(self, 'last_prompt'):
                        prompt = self.last_prompt

                    if prompt:
                        # Initialize Google GenAI client
                        google_key = self.config.get('DEFAULT', 'google_api_key', fallback='')
                        if google_key:
                            from google import genai
                            from google.genai import types

                            client = genai.Client(api_key=google_key)
                            model_name = self.model.split('/', 1)[1] if '/' in self.model else self.model

                            stderr_console.print(f"[yellow]Sending prompt to {model_name} using direct API...[/yellow]")

                            # Generate content with image response
                            response = client.models.generate_content(
                                model=model_name,
                                contents=prompt,
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

                                                    stderr_console.print(f"[green]Image found with direct API! MIME type: {mime_type}[/green]")

                                                    # Save the image to a temporary file
                                                    import tempfile
                                                    import os

                                                    # Create a temporary file with the appropriate extension
                                                    ext = mime_type.split('/')[-1]
                                                    fd, temp_path = tempfile.mkstemp(suffix=f'.{ext}')
                                                    os.close(fd)

                                                    # Write the image data to the file
                                                    with open(temp_path, 'wb') as f:
                                                        f.write(image_data)

                                                    stderr_console.print(f"[green]Image saved to: {temp_path}[/green]")

                                                    # Try to get image dimensions
                                                    try:
                                                        from PIL import Image
                                                        image = Image.open(temp_path)
                                                        width, height = image.size
                                                        stderr_console.print(f"[green]Dimensions: {width}x{height}[/green]")
                                                    except ImportError:
                                                        stderr_console.print("[yellow]PIL/Pillow not installed. Cannot get image dimensions.[/yellow]")
                                                    except Exception as e:
                                                        stderr_console.print(f"[yellow]Could not get image dimensions: {str(e)}[/yellow]")

                                                    # Print the image path to stdout so it can be captured
                                                    print(f"\n\n[IMAGE_DATA_1]\nMIME-Type: {mime_type}\nPath: {temp_path}\n[/IMAGE_DATA_1]")
                                                    break
                        else:
                            stderr_console.print("[red]No Google API key found in configuration[/red]")
                    else:
                        stderr_console.print("[red]No prompt found to send to the model[/red]")
                except Exception as e:
                    stderr_console.print(f"[red]Error using direct Google GenAI SDK approach: {str(e)}[/red]")
                    traceback.print_exc(file=sys.stderr)

            # Estimate output tokens by word count
            self.output_tokens = len(response_content.split())

        except Exception as e:
            print(f"Error: {str(e)}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            yield f"Error: {str(e)}"

    def send_prompt_test(self, prompt: str, debug: bool = False) -> Generator[str, None, None]:
        """Test model that returns predefined responses for testing."""
        try:
            test_response = "This is a test response from the test model.\n"
            test_response += "It can be used for testing without hitting real LLMs.\n"
            test_response += f"Your prompt was: {prompt}\n"
            test_response += f"System prompt was: {self.system_prompt}"

            # Set token counts for test model
            self.input_tokens = len(prompt.split()) + len(self.system_prompt.split())
            self.output_tokens = len(test_response.split())

            words = test_response.split()
            for word in words:
                yield word + " "
                if self.stream_mode:
                    time.sleep(0.01)

        except Exception as e:
            yield f"Error in test model: {str(e)}"

    def _chat_completion_test(self, messages: List[Dict[str, str]], stream: bool) -> Generator[str, None, None]:
        """Handle test model chat completion"""
        try:
            test_response = "This is a test chat response.\n"
            test_response += "Chat history:\n"

            # Calculate input tokens from messages
            input_token_count = 0
            for msg in messages:
                test_response += f"{msg['role'].upper()}: {msg['content']}\n"
                input_token_count += len(msg.get('content', '').split())

            # Set token counts for test model
            self.input_tokens = input_token_count
            self.output_tokens = len(test_response.split())

            if stream:
                words = test_response.split()
                for word in words:
                    yield word + " "
                    if self.stream_mode:
                        time.sleep(0.01)
            else:
                yield test_response

        except Exception as e:
            yield f"Error in test model: {str(e)}"

    def _send_prompt_with_files(self, prompt: str, debug: bool = False) -> Generator[str, None, None]:
        """Send prompt using Google GenAI SDK directly when cached content or uploaded files are available."""
        if not self.google_client:
            yield "Error: Google client not available for file content."
            return

        try:
            from google.genai import types
        except Exception:
            yield "Error: google-genai package is required for file content."
            return

        try:
            model_name = self.model.split('/', 1)[1] if '/' in self.model else self.model

            if debug:
                if self.cache_id:
                    print(f"\n[DEBUG] Using Google GenAI SDK directly with cache: {self.cache_id}", file=sys.stderr)
                elif self.uploaded_files:
                    print(f"\n[DEBUG] Using Google GenAI SDK directly with {len(self.uploaded_files)} uploaded files", file=sys.stderr)
                print(f"\n[DEBUG] Model: {model_name}", file=sys.stderr)
                print(f"\n[DEBUG] Prompt: {prompt}", file=sys.stderr)

            # Prepare contents for the API call
            if self.cache_id:
                # Use cached content
                config = types.GenerateContentConfig(
                    cached_content=self.cache_id
                )
                contents = prompt
            elif self.uploaded_files:
                # Use uploaded files directly
                config = types.GenerateContentConfig()

                # Create contents with prompt and uploaded files
                contents = [prompt]
                for file_path, file_obj in self.uploaded_files:
                    contents.append(file_obj)
                    if debug:
                        print(f"\n[DEBUG] Added uploaded file: {file_path} -> {file_obj.uri}", file=sys.stderr)
            else:
                yield "Error: No cached content or uploaded files available."
                return

            # Add thinking config for Gemini 2.5 models
            if '2.' in model_name:
                config.thinking_config = types.ThinkingConfig(
                    thinking_budget=self.thinking_budget
                )

            # Generate content
            response = self.google_client.models.generate_content(
                model=model_name,
                contents=contents,
                config=config
            )

            # Extract and yield the response text
            if hasattr(response, 'text') and response.text:
                response_text = response.text
                self.output_tokens = len(response_text.split())
                yield response_text
            else:
                yield "Error: No response text received from the model."

        except Exception as e:
            if debug:
                import traceback
                traceback.print_exc(file=sys.stderr)
            yield f"Error using file content: {str(e)}"

    def _chat_completion_with_files(self, messages: List[Dict[str, str]], stream: bool = True) -> Generator[str, None, None]:
        """Handle chat completion using Google GenAI SDK directly when cached content or uploaded files are available."""
        if not self.google_client:
            yield "Error: Google client not available for file content."
            return

        try:
            from google.genai import types
        except Exception:
            yield "Error: google-genai package is required for file content."
            return

        try:
            model_name = self.model.split('/', 1)[1] if '/' in self.model else self.model

            if hasattr(self, 'debug') and self.debug:
                if self.cache_id:
                    print(f"\n[DEBUG] Using Google GenAI SDK directly for chat with cache: {self.cache_id}", file=sys.stderr)
                elif self.uploaded_files:
                    print(f"\n[DEBUG] Using Google GenAI SDK directly for chat with {len(self.uploaded_files)} uploaded files", file=sys.stderr)
                print(f"\n[DEBUG] Model: {model_name}", file=sys.stderr)
                print(f"\n[DEBUG] Messages: {messages}", file=sys.stderr)

            # Extract the user message (last message should be from user)
            user_message = ""
            for msg in reversed(messages):
                if msg["role"] == "user":
                    user_message = msg["content"]
                    break

            if not user_message:
                yield "Error: No user message found in chat history."
                return

            # Prepare contents for the API call
            if self.cache_id:
                # Use cached content
                config = types.GenerateContentConfig(
                    cached_content=self.cache_id
                )
                contents = user_message
            elif self.uploaded_files:
                # Use uploaded files directly
                config = types.GenerateContentConfig()

                # Create contents with user message and uploaded files
                contents = [user_message]
                for file_path, file_obj in self.uploaded_files:
                    contents.append(file_obj)
                    if hasattr(self, 'debug') and self.debug:
                        print(f"\n[DEBUG] Added uploaded file to chat: {file_path} -> {file_obj.uri}", file=sys.stderr)
            else:
                yield "Error: No cached content or uploaded files available."
                return

            # Add thinking config for Gemini 2.5 models
            if '2.' in model_name:
                config.thinking_config = types.ThinkingConfig(
                    thinking_budget=self.thinking_budget
                )

            # Generate content
            response = self.google_client.models.generate_content(
                model=model_name,
                contents=contents,
                config=config
            )

            # Extract and yield the response text
            if hasattr(response, 'text') and response.text:
                response_text = response.text
                self.output_tokens = len(response_text.split())
                yield response_text
            else:
                yield "Error: No response text received from the model."

        except Exception as e:
            if hasattr(self, 'debug') and self.debug:
                import traceback
                traceback.print_exc(file=sys.stderr)
            yield f"Error using file content in chat: {str(e)}"

    def upload_and_cache_files(self, file_paths: List[str]) -> Optional[str]:
        """Upload files using Google GenAI and create a cache.

        Args:
            file_paths: list of local file paths to upload

        Returns:
            The cache resource name or None on failure.
        """
        if not self.google_client:
            print("Google client not available. File upload requires a Google API key.", file=sys.stderr)
            return None

        try:
            from google.genai import types
        except Exception:
            print("google-genai package is required for file caching", file=sys.stderr)
            return None

        uploaded = []
        import mimetypes

        # Upload each file
        for path in file_paths:
            try:
                # Get file size for progress indication
                file_size = os.path.getsize(path)
                if file_size > 20 * 1024 * 1024:  # 20MB limit
                    print(f"Warning: File {path} is {file_size / (1024*1024):.1f}MB. Large files may take time to upload.", file=sys.stderr)

                if hasattr(self, 'debug') and self.debug:
                    print(f"Uploading {path} ({file_size} bytes)...", file=sys.stderr)

                file_obj = self.google_client.files.upload(file=path)
                uploaded.append((path, file_obj))

                if hasattr(self, 'debug') and self.debug:
                    print(f"Successfully uploaded {path} -> {file_obj.uri}", file=sys.stderr)

            except Exception as e:
                print(f"Error uploading {path}: {e}", file=sys.stderr)
                # Continue with other files even if one fails

        if not uploaded:
            print("No files were successfully uploaded.", file=sys.stderr)
            return None

        # Update cached files list (replace existing cache if any)
        self.cached_files = [(p, f.uri) for p, f in uploaded]

        # Create parts for cache
        parts = []
        for p, f_uri in self.cached_files:
            mime, _ = mimetypes.guess_type(p)
            mime = mime or 'application/octet-stream'
            parts.append(types.Part.from_uri(file_uri=f_uri, mime_type=mime))

            if hasattr(self, 'debug') and self.debug:
                print(f"Added part for {p} with MIME type {mime}", file=sys.stderr)

        try:
            model_name = self.model.split('/', 1)[1] if '/' in self.model else self.model

            if hasattr(self, 'debug') and self.debug:
                print(f"Creating cache for model {model_name} with {len(parts)} parts", file=sys.stderr)

            cached = self.google_client.caches.create(
                model=model_name,
                config=types.CreateCachedContentConfig(
                    contents=[types.Content(role='user', parts=parts)],
                    display_name='flowai cache',
                    ttl='3600s'  # 1 hour TTL
                )
            )
            self.cache_id = cached.name

            if hasattr(self, 'debug') and self.debug:
                print(f"Cache created successfully: {self.cache_id}", file=sys.stderr)

            return self.cache_id
        except Exception as e:
            error_message = str(e)
            if hasattr(self, 'debug') and self.debug:
                print(f"Error creating cache: {error_message}", file=sys.stderr)
                import traceback
                traceback.print_exc(file=sys.stderr)

            # Check if the error is due to content being too small for caching
            if "too small" in error_message.lower() or "min_total_token_count" in error_message:
                print(f"Files too small for caching (minimum 1024 tokens required). Using direct file upload instead.", file=sys.stderr)

                # Store uploaded file objects for direct use in API calls
                self.uploaded_files = uploaded

                if hasattr(self, 'debug') and self.debug:
                    print(f"Stored {len(uploaded)} uploaded files for direct use", file=sys.stderr)

                # Return a special indicator that files are uploaded but not cached
                return "uploaded_not_cached"
            else:
                print(f"Error creating cache: {error_message}", file=sys.stderr)
                return None

    def supports_web_search(self) -> bool:
        """Check if the current model supports web search"""
        # Currently only Gemini models support web search
        return self.model.startswith('gemini/')
