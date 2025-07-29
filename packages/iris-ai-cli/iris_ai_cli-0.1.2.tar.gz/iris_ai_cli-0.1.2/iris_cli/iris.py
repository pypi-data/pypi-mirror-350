import os
import sys
import argparse
import json
from typing import Optional, Dict, Any, List
import logging
from datetime import datetime
from groq import Groq
import time
import platform
import psutil
import shutil

# Rich imports for beautiful UI
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.progress import track, Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm
from rich.syntax import Syntax
from rich.markdown import Markdown
from rich.tree import Tree
from rich.columns import Columns
from rich import box
from rich.align import Align

# Initialize rich console
console = Console()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# Disable httpx logging
logging.getLogger("httpx").setLevel(logging.WARNING)

class GroqCLI:
    """CLI interface for Groq AI with beautiful UI"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Groq client"""
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            console.print("[bold red]❌ Error: GROQ_API_KEY environment variable is required[/bold red]")
            console.print("[yellow]Please set your Groq API key:[/yellow]")
            console.print("[dim]Windows: set GROQ_API_KEY=your_api_key_here[/dim]")
            console.print("[dim]Linux/Mac: export GROQ_API_KEY=your_api_key_here[/dim]")
            raise ValueError("GROQ_API_KEY environment variable required")
        
        try:
            self.client = Groq(api_key=self.api_key)
        except Exception as e:
            console.print(f"[bold red]❌ Error initializing Groq client: {e}[/bold red]")
            raise
            
        self.conversation_history: List[Dict[str, str]] = []
        
        # Define models for different purposes
        self.routing_model = "llama3-70b-8192"
        self.tool_use_model = "llama-3.3-70b-versatile"
        self.general_model = "llama3-70b-8192"
        
        self.system_prompt = """You are a CLI AI assistant with system monitoring capabilities.
For system commands, respond with:
COMMAND
<command>

For general questions, respond directly and concisely. Be helpful but brief.
If asked about shell commands, suggest the appropriate command.
For Windows, translate Unix commands (e.g., ls → dir, rm → del).

Examples:
Q: How to list files?
COMMAND
dir

Q: What is Python?
Python is a high-level programming language known for its simplicity and readability.
"""
        
        # Define available tools
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_system_info",
                    "description": "Get current system information including memory, disk, and running processes",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "include_memory": {"type": "boolean", "description": "Include memory usage info"},
                            "include_disk": {"type": "boolean", "description": "Include disk usage info"},
                            "include_processes": {"type": "boolean", "description": "Include running processes"}
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_git_status",
                    "description": "Get current git repository information including branch, status, and recent commits",
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_directory_contents",
                    "description": "Get current directory contents and structure",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "max_items": {"type": "integer", "description": "Maximum number of items to return"}
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_environment_variables",
                    "description": "Get environment variables from the system",
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    }
                }
            }
        ]
        
        self.show_welcome()
    
    def show_welcome(self):
        """Display beautiful welcome message"""
        welcome_text = Text()
        welcome_text.append("🤖 ", style="bold blue")
        welcome_text.append("Groq CLI Assistant", style="bold cyan")
        welcome_text.append(" ⚡", style="bold yellow")
        
        panel = Panel(
            Align.center(welcome_text),
            box=box.DOUBLE,
            border_style="bright_blue",
            padding=(1, 2)
        )
        console.print(panel)
    
    def show_help(self):
        """Display beautiful help information"""
        help_table = Table(
            title="🔧 Available Commands",
            title_style="bold magenta",
            box=box.ROUNDED,
            border_style="cyan"
        )
        help_table.add_column("Command", style="bold green", no_wrap=True)
        help_table.add_column("Description", style="white")
        help_table.add_column("Example", style="dim italic")
        
        help_table.add_row(
            "chat", 
            "Start interactive chat mode", 
            "groq_cli.py chat"
        )
        help_table.add_row(
            "prompt", 
            "Send a single prompt", 
            'groq_cli.py prompt "Hello AI"'
        )
        help_table.add_row(
            "file", 
            "Process a file", 
            "groq_cli.py file input.txt"
        )
        help_table.add_row(
            "system", 
            "Get system information", 
            "groq_cli.py system status"
        )
        help_table.add_row(
            "clear", 
            "Clear conversation history", 
            "clear"
        )
        help_table.add_row(
            "exit", 
            "Exit the application", 
            "exit"
        )
        
        console.print(help_table)
        
        # Available tools section
        tools_panel = Panel(
            "[bold cyan]🛠️  Available System Tools:[/bold cyan]\n\n"
            "• [green]System Info[/green] - Memory, disk, and process monitoring\n"
            "• [blue]Git Status[/blue] - Repository information and changes\n"
            "• [yellow]Directory Contents[/yellow] - File and folder listings\n"
            "• [magenta]Environment Variables[/magenta] - System environment data",
            title="Tools Overview",
            border_style="green"
        )
        console.print(tools_panel)

    def configure_model(self, model_name: str = "llama3-70b-8192") -> None:
        """Configure the Groq model to use"""
        self.model_name = model_name
        console.print(f"[bold green]✓[/bold green] Configured Groq model: [cyan]{model_name}[/cyan]")
    
    def add_to_history(self, role: str, content: str) -> None:
        """Add message to conversation history"""
        self.conversation_history.append({
            "role": role,
            "content": content
        })
    
    def clear_history(self) -> None:
        """Clear conversation history"""
        self.conversation_history.clear()
        console.print("[bold yellow]🗑️  Conversation history cleared![/bold yellow]")
    
    def route_query(self, query: str) -> str:
        """Route query to determine if tools are needed"""
        routing_prompt = f"""
Given the following user query, determine if any system tools are needed to answer it.
Available tools:
- get_system_info: For memory, disk, process information
- get_git_status: For git repository information  
- get_directory_contents: For listing directory contents
- get_environment_variables: For environment variables

If system tools are needed, respond with 'TOOL: SYSTEM'.
If no tools are needed, respond with 'NO TOOL'.

User query: {query}

Response:
"""
        
        response = self.client.chat.completions.create(
            model=self.routing_model,
            messages=[
                {"role": "system", "content": "You are a routing assistant. Determine if system tools are needed based on the user query."},
                {"role": "user", "content": routing_prompt}
            ],
            max_completion_tokens=20
        )
        
        routing_decision = response.choices[0].message.content.strip()
        
        if "TOOL: SYSTEM" in routing_decision:
            return "system_tools"
        else:
            return "no_tool"

    def run_with_tools(self, query: str) -> str:
        """Use tools to answer the query"""
        messages = [
            {
                "role": "system",
                "content": "You are a system monitoring assistant. Use the available tools to gather system information and provide helpful responses."
            },
            {
                "role": "user",
                "content": query
            }
        ]
        
        response = self.client.chat.completions.create(
            model=self.tool_use_model,
            messages=messages,
            tools=self.tools,
            tool_choice="auto",
            max_completion_tokens=4096
        )
        
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls
        
        if tool_calls:
            messages.append(response_message)
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                function_response = self.execute_tool(function_name, function_args)
                
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response
                })
            
            second_response = self.client.chat.completions.create(
                model=self.tool_use_model,
                messages=messages
            )
            return second_response.choices[0].message.content
        
        return response_message.content

    def execute_tool(self, function_name: str, args: Dict[str, Any]) -> str:
        """Execute the specified tool function"""
        if function_name == "get_system_info":
            return self.get_system_info(**args)
        elif function_name == "get_git_status":
            return self.get_git_status()
        elif function_name == "get_directory_contents":
            return self.get_directory_contents(args.get("max_items", 20))
        elif function_name == "get_environment_variables":
            return self.get_environment_variables()
        else:
            return json.dumps({"error": f"Unknown function: {function_name}"})

    def get_system_info(self, include_memory=True, include_disk=True, include_processes=False):
        """Get system information with beautiful formatting"""
        info_table = Table(
            title="🖥️  System Information",
            title_style="bold blue",
            box=box.ROUNDED,
            border_style="blue"
        )
        info_table.add_column("Component", style="bold cyan", no_wrap=True)
        info_table.add_column("Details", style="white")
        info_table.add_column("Status", style="bold", no_wrap=True)
        
        if include_memory:
            mem = psutil.virtual_memory()
            memory_status = "🟢 Good" if mem.percent < 80 else "🟡 High" if mem.percent < 90 else "🔴 Critical"
            info_table.add_row(
                "Memory",
                f"Total: {mem.total / (1024**3):.1f}GB | Available: {mem.available / (1024**3):.1f}GB",
                f"{memory_status} ({mem.percent}%)"
            )
        
        if include_disk:
            disk = shutil.disk_usage(os.getcwd())
            disk_percent = (disk.used / disk.total) * 100
            disk_status = "🟢 Good" if disk_percent < 80 else "🟡 High" if disk_percent < 90 else "🔴 Critical"
            info_table.add_row(
                "Disk",
                f"Total: {disk.total / (1024**3):.1f}GB | Free: {disk.free / (1024**3):.1f}GB",
                f"{disk_status} ({disk_percent:.1f}%)"
            )
        
        if include_processes:
            processes = []
            for proc in list(psutil.process_iter(['name', 'pid']))[:5]:
                try:
                    processes.append(f"{proc.info['name']} (PID: {proc.info['pid']})")
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            info_table.add_row(
                "Top Processes",
                "\n".join(processes),
                "🔄 Running"
            )
        
        console.print(info_table)
        return json.dumps({"status": "displayed_in_console"})

    def get_git_status(self):
        """Get git repository status with beautiful formatting and accurate information"""
        try:
            import subprocess
            import os
            
            # Check if we're in a git repository
            result = subprocess.run(['git', 'rev-parse', '--is-inside-work-tree'], 
                                  capture_output=True, text=True, cwd=os.getcwd())
            if result.returncode != 0:
                error_panel = Panel(
                    "[red]❌ Not a git repository[/red]",
                    title="Git Error",
                    border_style="red"
                )
                console.print(error_panel)
                return json.dumps({"error": "Not a git repository"})
            
            # Get repository root
            repo_root = subprocess.run(['git', 'rev-parse', '--show-toplevel'], 
                                     capture_output=True, text=True, cwd=os.getcwd()).stdout.strip()
            
            # Get current branch
            branch_result = subprocess.run(['git', 'branch', '--show-current'], 
                                         capture_output=True, text=True, cwd=os.getcwd())
            current_branch = branch_result.stdout.strip() or "HEAD (detached)"
            
            # Get repository status
            status_result = subprocess.run(['git', 'status', '--porcelain'], 
                                         capture_output=True, text=True, cwd=os.getcwd())
            status_lines = status_result.stdout.strip().split('\n') if status_result.stdout.strip() else []
            
            # Get remote information
            remote_result = subprocess.run(['git', 'remote', '-v'], 
                                         capture_output=True, text=True, cwd=os.getcwd())
            remotes = remote_result.stdout.strip().split('\n') if remote_result.stdout.strip() else []
            
            # Get ahead/behind information
            ahead_behind = subprocess.run(['git', 'rev-list', '--left-right', '--count', f'{current_branch}...origin/{current_branch}'], 
                                        capture_output=True, text=True, cwd=os.getcwd())
            ahead_behind_count = ahead_behind.stdout.strip().split('\t') if ahead_behind.returncode == 0 else ['0', '0']
            
            # Categorize changes
            staged_files = []
            modified_files = []
            untracked_files = []
            deleted_files = []
            
            for line in status_lines:
                if len(line) >= 2:
                    status_code = line[:2]
                    filename = line[3:]
                    
                    if status_code[0] in ['A', 'M', 'D', 'R', 'C']:
                        staged_files.append(f"{status_code[0]} {filename}")
                    if status_code[1] == 'M':
                        modified_files.append(filename)
                    elif status_code[1] == 'D':
                        deleted_files.append(filename)
                    elif status_code == '??':
                        untracked_files.append(filename)
            
            # Create main repository info panel
            repo_name = os.path.basename(repo_root)
            status_text = "Clean working tree" if not status_lines else f"{len(status_lines)} changes"
            
            git_info = f"[bold green]📁 Repository:[/bold green] {repo_name}\n"
            git_info += f"[bold blue]🌿 Branch:[/bold blue] {current_branch}\n"
            git_info += f"[bold yellow]📊 Status:[/bold yellow] {status_text}\n"
            
            if ahead_behind_count[0] != '0' or ahead_behind_count[1] != '0':
                git_info += f"[bold magenta]🔄 Sync:[/bold magenta] {ahead_behind_count[0]} ahead, {ahead_behind_count[1]} behind\n"
            
            if remotes:
                origin_url = next((r.split('\t')[1].split(' ')[0] for r in remotes if 'origin' in r and '(fetch)' in r), 'No origin')
                git_info += f"[bold cyan]🌐 Origin:[/bold cyan] {origin_url}"
            
            git_panel = Panel(
                git_info,
                title="Git Repository Status",
                border_style="green"
            )
            console.print(git_panel)
            
            # Show detailed changes if any
            if status_lines:
                changes_table = Table(
                    title="📝 Working Directory Changes",
                    box=box.ROUNDED,
                    border_style="yellow"
                )
                changes_table.add_column("Type", style="bold", no_wrap=True)
                changes_table.add_column("Files", style="white")
                changes_table.add_column("Count", style="bold cyan", no_wrap=True)
                
                if staged_files:
                    changes_table.add_row("🟢 Staged", "\n".join(staged_files[:5]), str(len(staged_files)))
                if modified_files:
                    changes_table.add_row("🟡 Modified", "\n".join(modified_files[:5]), str(len(modified_files)))
                if untracked_files:
                    changes_table.add_row("❓ Untracked", "\n".join(untracked_files[:5]), str(len(untracked_files)))
                if deleted_files:
                    changes_table.add_row("🔴 Deleted", "\n".join(deleted_files[:5]), str(len(deleted_files)))
                
                console.print(changes_table)
            
            # Get recent commits with detailed information
            commits_result = subprocess.run(['git', 'log', '--oneline', '-10', '--pretty=format:%h|%an|%ar|%s'], 
                                          capture_output=True, text=True, cwd=os.getcwd())
            
            if commits_result.returncode == 0 and commits_result.stdout.strip():
                commits_table = Table(
                    title="📝 Recent Commits",
                    box=box.SIMPLE,
                    border_style="dim"
                )
                commits_table.add_column("Hash", style="dim cyan", no_wrap=True)
                commits_table.add_column("Author", style="bold", no_wrap=True)
                commits_table.add_column("Time", style="dim", no_wrap=True)
                commits_table.add_column("Message", style="white")
                
                for commit_line in commits_result.stdout.strip().split('\n'):
                    parts = commit_line.split('|', 3)
                    if len(parts) == 4:
                        hash_short, author, time_ago, message = parts
                        commits_table.add_row(hash_short, author, time_ago, message[:60] + "..." if len(message) > 60 else message)
                
                console.print(commits_table)
            
            # Get branch information
            branches_result = subprocess.run(['git', 'branch', '-a'], 
                                           capture_output=True, text=True, cwd=os.getcwd())
            if branches_result.returncode == 0:
                branches = [b.strip().replace('* ', '').replace('remotes/', '') 
                           for b in branches_result.stdout.strip().split('\n') if b.strip()]
                local_branches = [b for b in branches if not b.startswith('origin/')]
                remote_branches = [b for b in branches if b.startswith('origin/')]
                
                if len(local_branches) > 1 or remote_branches:
                    branches_info = f"[bold green]Local:[/bold green] {len(local_branches)} branches"
                    if remote_branches:
                        branches_info += f" | [bold blue]Remote:[/bold blue] {len(remote_branches)} branches"
                    
                    branches_panel = Panel(
                        branches_info,
                        title="🌿 Branch Information",
                        border_style="blue"
                    )
                    console.print(branches_panel)
            
            return json.dumps({
                "status": "success",
                "repository": repo_name,
                "branch": current_branch,
                "changes": len(status_lines),
                "ahead": ahead_behind_count[0],
                "behind": ahead_behind_count[1]
            })
            
        except subprocess.CalledProcessError as e:
            error_panel = Panel(
                f"[red]❌ Git command failed: {e}[/red]",
                title="Git Error",
                border_style="red"
            )
            console.print(error_panel)
            return json.dumps({"error": f"Git command failed: {e}"})
        except FileNotFoundError:
            error_panel = Panel(
                "[red]❌ Git is not installed or not in PATH[/red]",
                title="Git Error",
                border_style="red"
            )
            console.print(error_panel)
            return json.dumps({"error": "Git not installed"})
        except Exception as e:
            error_panel = Panel(
                f"[red]❌ Unexpected error: {str(e)}[/red]",
                title="Git Error",
                border_style="red"
            )
            console.print(error_panel)
            return json.dumps({"error": f"Unexpected error: {str(e)}"})

    def get_directory_contents(self, max_items=20):
        """Get current directory contents with beautiful tree view"""
        tree = Tree(
            f"📁 [bold blue]{os.getcwd()}[/bold blue]",
            guide_style="dim"
        )
        
        try:
            dirs = []
            files = []
            
            with os.scandir(os.getcwd()) as entries:
                for entry in list(entries)[:max_items]:
                    if entry.is_dir():
                        dirs.append(entry.name)
                    else:
                        files.append(entry.name)
            
            # Add directories first
            for dir_name in sorted(dirs):
                tree.add(f"📂 [bold cyan]{dir_name}/[/bold cyan]")
            
            # Add files
            for file_name in sorted(files):
                icon = "📄" if file_name.endswith(('.txt', '.md', '.py', '.js')) else "📋"
                tree.add(f"{icon} [white]{file_name}[/white]")
                
        except Exception as e:
            tree.add(f"[red]❌ Error: {str(e)}[/red]")
        
        console.print(tree)
        return json.dumps({"status": "displayed_in_console"})

    def get_environment_variables(self):
        """Get environment variables with formatted display"""
        env_table = Table(
            title="🌍 Environment Variables",
            box=box.ROUNDED,
            border_style="green",
            width=100
        )
        env_table.add_column("Variable", style="bold cyan", no_wrap=True)
        env_table.add_column("Value", style="white", overflow="fold")
        
        # Show only important environment variables
        important_vars = ['PATH', 'HOME', 'USER', 'USERNAME', 'PYTHON_PATH', 'GROQ_API_KEY']
        
        for var in important_vars:
            value = os.environ.get(var, "Not set")
            if var == 'GROQ_API_KEY' and value != "Not set":
                value = f"{value[:8]}..." + "*" * 20  # Hide API key
            env_table.add_row(var, value)
        
        console.print(env_table)
        console.print(f"\n[dim]Showing {len(important_vars)} important variables out of {len(os.environ)} total[/dim]")
        return json.dumps({"status": "displayed_in_console"})

    def run_general(self, query: str) -> str:
        """Use general model for non-tool queries"""
        messages = [
            {"role": "system", "content": self.system_prompt},
            *self.conversation_history,
            {"role": "user", "content": query}
        ]
        
        response = self.client.chat.completions.create(
            model=self.general_model,
            messages=messages
        )
        return response.choices[0].message.content

    def generate_response(self, prompt: str, system_prompt: Optional[str] = None, 
                         max_tokens: int = 4096, temperature: float = 0.7, 
                         show_progress: bool = True) -> str:
        """Generate response using routing and appropriate model"""
        try:
            # Route the query
            if show_progress:
                with console.status("[bold blue]🔍 Analyzing query...", spinner="dots"):
                    route = self.route_query(prompt)
            else:
                route = self.route_query(prompt)
            
            if route == "system_tools":
                if show_progress:
                    with console.status("[bold blue]🛠️ Using system tools...", spinner="dots"):
                        response = self.run_with_tools(prompt)
                else:
                    response = self.run_with_tools(prompt)
            else:
                if show_progress:
                    with console.status("[bold blue]🤔 Generating response...", spinner="dots"):
                        response = self.run_general(prompt)
                else:
                    response = self.run_general(prompt)
            
            # Add to conversation history
            self.add_to_history("user", prompt)
            self.add_to_history("assistant", response)
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise

    def chat_mode(self) -> None:
        """Interactive chat mode with beautiful UI"""
        chat_panel = Panel(
            "[bold green]🎯 Chat Mode Active[/bold green]\n\n"
            "[cyan]Commands:[/cyan]\n"
            "• Type [bold]'exit'[/bold] to quit\n"
            "• Type [bold]'clear'[/bold] to clear history\n"
            "• Type [bold]'help'[/bold] for commands\n"
            "• Type [bold]'save'[/bold] to save conversation",
            title="Interactive Chat",
            border_style="green"
        )
        console.print(chat_panel)
        
        while True:
            try:
                user_input = Prompt.ask("\n[bold blue]You[/bold blue]").strip()
                
                if user_input.lower() == 'exit':
                    console.print("[bold green]👋 Goodbye![/bold green]")
                    break
                elif user_input.lower() == 'clear':
                    self.clear_history()
                    continue
                elif user_input.lower() == 'help':
                    self.show_help()
                    continue
                elif user_input.lower() == 'save':
                    filename = Prompt.ask("Enter filename", default="conversation.json")
                    self.save_conversation(filename)
                    continue
                elif not user_input:
                    continue
                
                response = self.generate_response(user_input, show_progress=True)
                
                # Display response with beautiful formatting
                if response.startswith("COMMAND"):
                    command = response.replace("COMMAND", "").strip()
                    translated_command = translate_command(command)
                    
                    command_panel = Panel(
                        f"[bold yellow]💻 Suggested Command:[/bold yellow]\n[bold green]{translated_command}[/bold green]",
                        border_style="yellow"
                    )
                    console.print(command_panel)
                    
                    if Confirm.ask("Execute this command?"):
                        console.print(f"[dim]Executing: {translated_command}[/dim]")
                        os.system(translated_command)
                else:
                    response_panel = Panel(
                        response,
                        title="🤖 Groq Response",
                        border_style="cyan",
                        padding=(1, 2)
                    )
                    console.print(response_panel)
                
            except KeyboardInterrupt:
                console.print("\n[bold green]👋 Goodbye![/bold green]")
                break
            except Exception as e:
                console.print(f"[bold red]❌ Error: {e}[/bold red]")

    def process_file(self, file_path: str, output_path: Optional[str] = None) -> None:
        """Process a file with Groq AI"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            prompt = f"Please analyze and provide insights on the following content:\n\n{content}"
            response = self.generate_response(prompt)
            
            if output_path:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(response)
                console.print(f"Response saved to: {output_path}")
            else:
                console.print("Groq Response:")
                console.print("=" * 50)
                console.print(response)
                
        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
        except Exception as e:
            logger.error(f"Error processing file: {e}")
    
    def save_conversation(self, file_path: str) -> None:
        """Save conversation history to file with confirmation"""
        try:
            conversation_data = {
                "timestamp": datetime.now().isoformat(),
                "model": self.model_name,
                "conversation": self.conversation_history
            }
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(conversation_data, f, indent=2, ensure_ascii=False)
            
            console.print(f"[bold green]💾 Conversation saved to: {file_path}[/bold green]")
            
        except Exception as e:
            console.print(f"[bold red]❌ Error saving conversation: {e}[/bold red]")
    
    def load_conversation(self, file_path: str) -> None:
        """Load conversation history from file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                conversation_data = json.load(f)
            
            self.conversation_history = conversation_data.get("conversation", [])
            console.print(f"Conversation loaded from: {file_path}")
            console.print(f"Loaded {len(self.conversation_history)} messages")
            
        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
        except Exception as e:
            logger.error(f"Error loading conversation: {e}")

def translate_command(command: str) -> str:
    """Translate Unix commands to Windows if needed"""
    command_map = {
        "ls": "dir",
        "rm": "del",
        "cp": "copy",
        "mv": "move",
        "cat": "type",
        "pwd": "cd",
        "clear": "cls"
    }
    
    parts = command.split()
    if parts and parts[0] in command_map:
        parts[0] = command_map[parts[0]]
    return " ".join(parts)

def create_parser() -> argparse.ArgumentParser:
    """Create command line argument parser"""
    parser = argparse.ArgumentParser(
        description="Groq CLI - AI Assistant powered by Groq",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  groq_cli.py chat                           # Start interactive chat
  groq_cli.py prompt "Hello, how are you?"   # Single prompt
  groq_cli.py file input.txt                 # Process file
  groq_cli.py file input.txt -o output.txt   # Process file with output
        """
    )
    
    parser.add_argument('--api-key', help='Groq API key (or set GROQ_API_KEY env var)')
    parser.add_argument('--model', default='llama3-70b-8192', 
                       help='Groq model to use (default: llama3-70b-8192)')
    parser.add_argument('--temperature', type=float, default=0.7,
                       help='Temperature for response generation (default: 0.7)')
    parser.add_argument('--max-tokens', type=int, default=4096,
                       help='Maximum tokens in response (default: 4096)')
    parser.add_argument('--system-prompt', help='System prompt to use')
    parser.add_argument('--save-conversation', help='Save conversation to file')
    parser.add_argument('--load-conversation', help='Load conversation from file')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Chat command
    chat_parser = subparsers.add_parser('chat', help='Start interactive chat mode')
    
    # Prompt command
    prompt_parser = subparsers.add_parser('prompt', help='Send a single prompt')
    prompt_parser.add_argument('text', help='Prompt text to send')
    
    # File command
    file_parser = subparsers.add_parser('file', help='Process a file')
    file_parser.add_argument('input_file', help='Input file path')
    file_parser.add_argument('-o', '--output', help='Output file path')
    
    return parser

def validate_api_key():
    """Validate if GROQ_API_KEY is set"""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        console.print("[bold red]❌ Error: GROQ_API_KEY environment variable is required[/bold red]")
        console.print("\n[yellow]Please set your Groq API key:[/yellow]")
        console.print("[dim]Windows: set GROQ_API_KEY=your_api_key_here[/dim]")
        console.print("[dim]Linux/Mac: export GROQ_API_KEY=your_api_key_here[/dim]")
        return False
    return True

def main():
    """Main CLI entry point with beautiful interface"""
    try:
        # Validate API key first
        if not validate_api_key():
            sys.exit(1)
            
        # Handle direct query if arguments are provided
        if len(sys.argv) > 1:
            query = " ".join(sys.argv[1:])
            
            if query.lower() == "chat":
                groq_cli = GroqCLI()
                groq_cli.chat_mode()
                return
            elif query.lower() == "help":
                groq_cli = GroqCLI()
                groq_cli.show_help()
                return
                
            # Initialize for direct query
            groq_cli = GroqCLI()
            groq_cli.configure_model("llama3-70b-8192")
            
            response = groq_cli.generate_response(query, show_progress=True)
            
            # Handle command responses
            if response.startswith("COMMAND"):
                command = response.replace("COMMAND", "").strip()
                translated_command = translate_command(command)
                
                command_panel = Panel(
                    f"[bold yellow]💻 Suggested Command:[/bold yellow]\n[bold green]{translated_command}[/bold green]",
                    border_style="yellow"
                )
                console.print(command_panel)
                
                if Confirm.ask("Execute this command?"):
                    console.print(f"[dim]Executing: {translated_command}[/dim]")
                    os.system(translated_command)
            else:
                response_panel = Panel(
                    response,
                    title="🤖 Groq Response",
                    border_style="cyan",
                    padding=(1, 2)
                )
                console.print(response_panel)
            return
        
        # If no arguments, show help and start chat
        groq_cli = GroqCLI()
        groq_cli.show_help()
        console.print("\n[dim]No command specified. Starting chat mode...[/dim]")
        time.sleep(1)
        groq_cli.chat_mode()
            
    except Exception as e:
        console.print(f"[bold red]❌ Error: {e}[/bold red]")
        sys.exit(1)

if __name__ == "__main__":
    main()
