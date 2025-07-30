from pathlib import Path
import json
import signal
from typing import Optional, Dict, List, Any
from datetime import datetime

class ChatManager:
    def __init__(self, stream: bool = False, debug: bool = False):
        self.history: List[Dict[str, str]] = []
        self.context: Dict[str, Any] = {}
        self.stream = stream
        self.debug = debug
        self._setup_signal_handlers()

        # Maximum number of messages to keep in history (excluding system message)
        self.max_history = 10

        # Token tracking
        self.total_input_tokens = 0
        self.total_output_tokens = 0

    def _setup_signal_handlers(self):
        """Setup Ctrl-C handler for graceful interruption"""
        signal.signal(signal.SIGINT, self._handle_interrupt)

    def _handle_interrupt(self, signum, frame):
        """Handle Ctrl-C by stopping current operation"""
        print("\n(Interrupted!)")

    def start_session(self, initial_context: Optional[Dict[str, Any]] = None) -> None:
        """Start new chat session with optional context from previous flowai operation"""
        # Only reset token counts if there's no initial context
        if not initial_context:
            self.total_input_tokens = 0
            self.total_output_tokens = 0
        else:
            # If we have initial context, use the token counts from it
            self.context.update(initial_context)
            if 'input_tokens' in initial_context:
                self.total_input_tokens = initial_context['input_tokens']
            if 'output_tokens' in initial_context:
                self.total_output_tokens = initial_context['output_tokens']
            # Format initial context as a system message
            system_msg = self._format_system_message(initial_context)
            if system_msg:
                self.add_message("system", system_msg)

    def _format_system_message(self, context: Dict[str, Any]) -> Optional[str]:
        """Format the initial context as a clear system message"""
        if not context:
            return None

        parts = []
        if context.get('last_command'):
            parts.append(f"Previous command: {context['last_command']}")

        if context.get('prompt'):
            parts.append(f"Original prompt: {context['prompt']}")

        if context.get('full_prompt'):
            parts.append(f"Full prompt with context:\n{context['full_prompt']}")
        elif context.get('context'):
            parts.append(f"Context:\n{context['context']}")

        if context.get('last_response'):
            parts.append(f"Previous response:\n{context['last_response']}")

        if context.get('files'):
            files_list = ', '.join(context['files']) if isinstance(context['files'], list) else str(context['files'])
            parts.append(f"Cached files: {files_list}")

        if parts:
            return "\n\n".join(parts)
        return None

    def add_message(self, role: str, content: str) -> None:
        """Add message to history"""
        # For system messages, replace existing system message if any
        if role == 'system':
            self.history = [msg for msg in self.history if msg['role'] != 'system']

        self.history.append({
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat()
        })

        # Trim history if needed (keeping system message)
        if role != 'system':
            non_system_msgs = [msg for msg in self.history if msg['role'] != 'system']
            if len(non_system_msgs) > self.max_history:
                system_msg = next((msg for msg in self.history if msg['role'] == 'system'), None)
                self.history = ([system_msg] if system_msg else []) + non_system_msgs[-self.max_history:]

    def get_formatted_history(self) -> List[Dict[str, str]]:
        """Get chat history formatted for LLM consumption"""
        formatted = []

        # Always include system message if present
        system_msg = next((msg for msg in self.history if msg['role'] == 'system'), None)
        if system_msg:
            formatted.append({
                'role': 'system',
                'content': system_msg['content']
            })

        # Get recent messages, excluding system message
        recent_messages = [
            msg for msg in self.history
            if msg['role'] != 'system' and msg.get('content', '').strip()
        ][-self.max_history:]

        # Add recent messages
        formatted.extend({
            'role': msg['role'],
            'content': msg['content']
        } for msg in recent_messages)

        return formatted

    def handle_command(self, cmd: str) -> bool:
        """Handle special chat commands"""
        cmd = cmd.strip()
        lower_cmd = cmd.lower()
        if lower_cmd == '/quit':
            return False
        elif lower_cmd.startswith('/stream'):
            parts = cmd.split()
            if len(parts) == 1:  # just /stream
                self.stream = not self.stream
                print(f"Stream mode {'enabled' if self.stream else 'disabled'}")
            elif len(parts) == 2:  # /stream on or /stream off
                if parts[1] == 'on':
                    self.stream = True
                    print("Stream mode enabled")
                elif parts[1] == 'off':
                    self.stream = False
                    print("Stream mode disabled")
                else:
                    print("Invalid stream command. Use: /stream, /stream on, or /stream off")
        elif lower_cmd == '/clear':
            self.history = []
            self.total_input_tokens = 0
            self.total_output_tokens = 0
            print("Chat history cleared!")
        elif lower_cmd.startswith('/save'):
            parts = cmd.split()
            last_only = False
            filename = None
            if len(parts) >= 2:
                if parts[1].lower() == 'last':
                    last_only = True
                    if len(parts) >= 3:
                        filename = parts[2]
                else:
                    filename = parts[1]

            if not filename:
                suffix = 'last' if last_only else 'session'
                filename = f"chat_{suffix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

            filepath = Path.cwd() / filename
            self._save_history(filepath, last_only)
            which = 'last response' if last_only else 'chat session'
            print(f"Saved {which} to {filepath}")
        elif lower_cmd == '/help':
            self._show_help()
        return True

    def _show_help(self) -> None:
        """Show available chat commands"""
        help_text = """
Available Commands:
/quit         - Exit chat mode
/clear        - Clear chat history
/stream       - Toggle stream mode
/stream on    - Enable stream mode
/stream off   - Disable stream mode
/save [last] [filename] - Save chat session or last response
/add-file <path> - Upload and cache a file (Gemini 1.5+ models only)
/list-files   - Show all files cached in this session
/help         - Show this help message
        """
        print(help_text)

    def _save_history(self, path: Path, last_only: bool = False) -> None:
        """Save chat history or last response to a markdown file"""
        if last_only:
            content = next((msg['content'] for msg in reversed(self.history)
                            if msg['role'] == 'assistant'), '')
            markdown = content
        else:
            lines = []
            for msg in self.history:
                role = msg['role'].capitalize()
                ts = msg.get('timestamp', '')
                lines.append(f"### {role} ({ts})\n\n{msg['content']}\n")
            markdown = "\n".join(lines)
        path.write_text(markdown)

    def get_status_display(self) -> str:
        """Get formatted status display with stream mode and token counts"""
        stream_status = "⚡" if self.stream else "⭘"
        token_info = f"{self.total_input_tokens}↑{self.total_output_tokens}↓"

        if self.debug:
            import sys
            print(f"[#555555]ChatManager status - Input tokens: {self.total_input_tokens}, Output tokens: {self.total_output_tokens}[/#555555]", file=sys.stderr)

        return f"[cyan]{stream_status}[/cyan] [blue]{token_info}[/blue] ❯ "
