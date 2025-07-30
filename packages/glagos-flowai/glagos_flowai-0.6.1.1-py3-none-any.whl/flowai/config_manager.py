import os
import configparser
from pathlib import Path
import configparser
from typing import Tuple, Optional

class ConfigManager:
    def __init__(self):
        self.config_dir = Path.home() / ".config" / "flowai"
        self.config_file = self.config_dir / "config.ini"
        self.system_prompt_file = self.config_dir / "system_prompt"
        # Update system prompt if it exists
        if self.system_prompt_file.exists():
            self.update_system_prompt()

    def config_exists(self):
        return self.config_file.exists()

    def create_default_config(self):
        self.config_dir.mkdir(parents=True, exist_ok=True)
        config = configparser.ConfigParser()
        config['DEFAULT'] = {
            'default_provider': 'openai',
            'default_model': 'gpt-3.5-turbo',
            'openai_api_key': '',
            'anthropic_api_key': '',
            'groq_api_key': '',
            'google_api_key': '',
            'ollama_base_url': 'http://localhost:11434',
            'quiet_mode': 'true',
            'stream_mode': 'true'
        }
        self.save_config(config)
        self.create_default_system_prompt()

    def create_default_system_prompt(self):
        self.update_system_prompt()

    def update_system_prompt(self):
        default_prompt = """You are a helpful AI assistant that responds to all questions as accurately as possible.
If you don't know the answer to a question, you will be honest and say so.

If any user instructions are provided at the start of the prompt (prefixed with "User Instructions:"), you MUST incorporate those instructions into your response. Common instructions might include:
- Adding specific identifiers (like ticket numbers)
- Using specific formatting or wording
- Focusing on particular aspects
- Outputting in a different language

Always check for and follow any user instructions before proceeding with your main task.
Answer questions concisely - no explanations, no greetings, no unnecessary white space or formatting.
Just the response."""
        with open(self.system_prompt_file, 'w') as f:
            f.write(default_prompt)

    def get_system_prompt(self):
        if not self.system_prompt_file.exists():
            self.create_default_system_prompt()
        with open(self.system_prompt_file, 'r') as f:
            return f.read().strip()

    def load_config(self):
        config = configparser.ConfigParser()
        config.read(self.config_file)
        return config

    def save_config(self, config):
        # Ensure the directory exists
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        

        with open(self.config_file, 'w') as configfile:
            config.write(configfile)

    def validate_config(self):
        """Validate the configuration file."""
        if not self.config_exists():
            return False, "Configuration file not found"
        
        config = self.load_config()
        
        # Check if default model is set and in correct format
        default_model = config.get('DEFAULT', 'default_model', fallback='')
        if not default_model:
            return False, "No default model set"
        
        if '/' not in default_model:  # Changed from ':' to '/'
            return False, f"Invalid model format '{default_model}'. It should be in the format 'provider/model'."
            
        return True, ""
