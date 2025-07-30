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
def detect_os(self) -> str:
        """Detect the operating system and return appropriate name"""
        system = platform.system().lower()
        if system == "windows":
            return "Windows"
        elif system == "darwin":
            return "macOS"
        elif system == "linux":
            return "Linux"
        else:
            return "Unknown"
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
        self.routing_model = "llama-3.1-8b-instant"
        self.tool_use_model = "llama-3.3-70b-versatile"
        self.general_model = "llama-3.3-70b-versatile"
        
        self.system_prompt = """You are a CLI AI assistant running on {detect_os}. Handle queries that don’t require system tools in three ways:

1. For general knowledge questions, respond directly and concisely.
2. For queries requesting to perform a CLI action (e.g., "create a file," "list files," "build a docker image"), respond with:
   COMMAND
   <windows_command>
   - Use Windows commands (e.g., "dir" instead of "ls").
3. For queries asking how to perform a CLI task (e.g., "how do I list files," "how do I build a docker image"), explain briefly in simple English, using Windows commands unless Unix is specified.

**Examples:**

- "What is Python?" → **"Python is a high-level programming language known for its simplicity."**

- "List files" → **"COMMAND"**  
  **"dir"**

- "Create a file" → **"COMMAND"**  
  **"echo. > filename.txt"**

- "Build a docker image" → **"COMMAND"**  
  **"docker build -t image_name ."**

- "How do I list files?" → **"Use the 'dir' command in the terminal to list files."**

- "How do I build a docker image?" → **"Run 'docker build -t image_name .' in the terminal."**

- "How do I list files in Unix?" → **"Use the 'ls' command in the terminal."**

- "What is the capital of France?" → **"The capital of France is Paris."**

Be helpful, brief, and precise. Analyze the query and respond appropriately.
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
            },
            {
                "type": "function",
                "function": {
                    "name": "create_python_script",
                    "description": "Save a Python script to a file. You should generate the complete Python code and pass it to this tool along with the filename.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "python_code": {"type": "string", "description": "Complete Python code to save to file"},
                            "filename": {"type": "string", "description": "Name of the file to save the script (without .py extension)"},
                            "use_case": {"type": "string", "description": "Brief description of what the script does"}
                        },
                        "required": ["python_code", "filename"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "execute_python_script",
                    "description": "Execute a Python script file and return the output",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "filename": {"type": "string", "description": "Name of the Python file to execute (with or without .py extension)"}
                        },
                        "required": ["filename"]
                    }
                }
            }
        ]
        
        self.show_welcome()
    
    def show_welcome(self):
        """Display beautiful welcome message"""
        welcome_text = Text()
        welcome_text.append("🤖 ", style="bold blue")
        welcome_text.append("Iris CLI Assistant", style="bold cyan")
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
            "iris chat"
        )
        help_table.add_row(
            "prompt", 
            "Send a single prompt", 
            'iris  "Hello AI"'
        )
        help_table.add_row(
            "system", 
            "Get system information", 
            "iris system status"
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
            "• [magenta]Environment Variables[/magenta] - System environment data\n"
            "• [red]Create Python Script[/red] - Generate and save Python scripts\n"
            "• [bright_green]Execute Python Script[/bright_green] - Run Python scripts and show output",
            title="Tools Overview",
            border_style="green"
        )
        console.print(tools_panel)

    def configure_model(self, model_name: str = "llama-3.3-70b-versatile") -> None:
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
You are an assistant running on {detect_os} that determines whether a system tool is required to answer a user's query. The available tools include functions for retrieving system information (e.g., memory, disk, processes), git status, directory contents, environment variables, executing Python scripts, and creating Python scripts.

**Rules:**

1. Respond with **"TOOL: SYSTEM"** if the query requires:
   - Performing an action to access system information (e.g., memory usage, disk space), git status, directory contents, or environment variables.
   - Executing a Python script.
   - Creating a Python script.

2. Respond with **"NO TOOL"** if the query can be answered with:
   - General knowledge (no system interaction).
   - A single CLI command that does not require the specified tools to execute (e.g., "node -v", "dir").

**Key Distinction:**
- If the query asks to *perform* an action (e.g., "list files," "check node version"), but it can be resolved with a simple CLI command, use "NO TOOL."
- If the query explicitly requires a tool (e.g., script creation or complex system access), use "TOOL: SYSTEM."

**Examples:**

- "What is the current memory usage?" → **"TOOL: SYSTEM"**  
  *(Requires system information access)*

- "List the files in the current directory." → **"NO TOOL"**  
  *(Can be done with "COMMAND dir")*

- "Show me the git status of this repository." → **"NO TOOL"**  
  *(Can be done with "COMMAND git status")*

- "Execute this C:\script.py" → **"TOOL: SYSTEM"**  
  *(Requires script execution)*

- "Create a Python script to print numbers" → **"TOOL: SYSTEM"**  
  *(Requires script creation)*

- "Check the node version" → **"NO TOOL"**  
  *(Can be done with "COMMAND node -v")*

- "What is the capital of France?" → **"NO TOOL"**  
  *(General knowledge)*

- "Is there an llm key in the environment variables?" → **"TOOL: SYSTEM"**  
  *(Requires environment variable access)*

- "How to list files?" → **"NO TOOL"**  
  *(Asks for a command, not action execution)*

Please analyze the user's query and respond with either **"TOOL: SYSTEM"** or **"NO TOOL"**.
"""
        # print("Routing prompt", routing_prompt)
        
        response = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": f"{routing_prompt}"},
                {"role": "user", "content": f"User query: {query}"}
            ],
            max_completion_tokens=20
        )
        
        routing_decision = response.choices[0].message.content.strip()
        
        if "TOOL: SYSTEM" in routing_decision:
            # print("[bold green]✓[/bold green] Routing decision: Using system tools")
            return "system_tools"
        else:
            return "no_tool"

    def run_with_tools(self, query: str) -> str:
        """Use tools to answer the query with multi-turn execution"""
        messages = [
            {
                "role": "system",
                "content": "You are an AI assistant with access to system tools. Use the available tools to gather information and help users. When users request Python scripts, generate the complete code and use the create_python_script tool to save it. The create_python_script tool expects you to provide the complete Python code. You can use multiple tools in sequence to complete complex tasks."
            },
            {
                "role": "user",
                "content": query
            }
        ]
        
        final_response = []
        turn_count = 1
        max_turns = 10  # Prevent infinite loops
        
        console.print("🚀 Starting multi-turn task execution...")
        
        while turn_count <= max_turns:
            console.print(f"[dim]Turn {turn_count}: Analyzing and executing...[/dim]")
            
            try:
                response = self.client.chat.completions.create(
                    model=self.tool_use_model,
                    messages=messages,
                    tools=self.tools,
                    tool_choice="auto",
                    max_completion_tokens=4096
                )
            except Exception as e:
                console.print(f"[bold red]❌ Error during turn {turn_count}: {e}[/bold red]")
                break
            
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls
            
            # Handle text content
            if response_message.content:
                console.print(f"[bold cyan]🤖 Iris (Turn {turn_count}):[/bold cyan]")
                response_panel = Panel(
                    response_message.content,
                    border_style="cyan",
                    padding=(1, 2)
                )
                console.print(response_panel)
                final_response.append(response_message.content)
            
            # If no tool calls, task is complete
            if not tool_calls:
                console.print("✅ Task completed - no more tools needed.")
                break
            
            console.print(f"[yellow]🛠️  Executing {len(tool_calls)} tool(s) in turn {turn_count}...[/yellow]")
            
            # Add the assistant's response (with tool calls) to messages
            messages.append({
                "role": "assistant",
                "content": response_message.content,
                "tool_calls": tool_calls
            })
            
            # Execute each tool call and add results
            for i, tool_call in enumerate(tool_calls):
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                console.print(f"[dim]Tool {i+1}/{len(tool_calls)}: {function_name}[/dim]")
                
                # Execute the tool
                function_response = self.execute_tool(function_name, function_args)
                
                # Add tool result to messages
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": function_response
                })
                
                # Check if tool execution failed - only fail if there's an actual error
                try:
                    result_data = json.loads(function_response)
                    # Only treat it as an error if status is "error" or if there's a non-null error field
                    if (result_data.get("status") == "error" or 
                        (result_data.get("error") is not None and result_data.get("error") != "")):
                        error_msg = result_data.get("error", "Unknown error")
                        console.print(f"[bold red]❌ Tool {function_name} failed: {error_msg}[/bold red]")
                        return "\n".join(final_response) if final_response else "Task failed due to tool error."
                except json.JSONDecodeError:
                    # If response is not JSON, assume it's successful unless it contains explicit error indicators
                    if "error" in function_response.lower() and "failed" in function_response.lower():
                        console.print(f"[bold red]❌ Tool {function_name} failed: {function_response}[/bold red]")
                        return "\n".join(final_response) if final_response else "Task failed due to tool error."
            
            turn_count += 1
            
            # Add a small delay to prevent overwhelming the API
            time.sleep(0.5)
        
        if turn_count > max_turns:
            console.print(f"[bold yellow]⚠️  Reached maximum turns ({max_turns}). Task may be incomplete.[/bold yellow]")
        
        console.print("🎯 Multi-turn execution completed!")
        return "\n".join(final_response) if final_response else "Task completed successfully."
    
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
        elif function_name == "create_python_script":
            return self.create_python_script(args.get("python_code"), args.get("filename"), args.get("use_case", "Python script"))
        elif function_name == "execute_python_script":
            return self.execute_python_script(args.get("filename"))
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
        mem_stat = None
        disk_stat = None
        if include_memory:
            mem = psutil.virtual_memory()
            memory_status = "🟢 Good" if mem.percent < 80 else "🟡 High" if mem.percent < 90 else "🔴 Critical"
            mem_stat = "Memory percent:"+ f" {mem.percent}%" + "Memory status:" + f" {memory_status}"

            info_table.add_row(
                "Memory",
                f"Total: {mem.total / (1024**3):.1f}GB | Available: {mem.available / (1024**3):.1f}GB",
                f"{memory_status} ({mem.percent}%)"
            )
        
        if include_disk:
            disk = shutil.disk_usage(os.getcwd())
            disk_percent = (disk.used / disk.total) * 100
            disk_status = "🟢 Good" if disk_percent < 80 else "🟡 High" if disk_percent < 90 else "🔴 Critical"
            disk_stat = "Disk percent:" + f" {disk_percent:.1f}%" + "Disk status:" + f" {disk_status}"
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
        return json.dumps({"status": "displayed_in_console","info": {
            "memory": mem_stat if mem_stat else None,
            "disk": disk_stat if disk_stat else None
        }})

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
        
        all_env_vars = dict(os.environ)
        
        # Sort variables for consistent display
        for var in sorted(all_env_vars.keys()):
            value = all_env_vars[var]
            
            # Hide sensitive information
            if any(sensitive in var.upper() for sensitive in ['API_KEY', 'SECRET', 'PASSWORD', 'TOKEN']):
                if len(value) > 8:
                    value = f"{value[:8]}..." + "*" * 20
            
            # Truncate very long values (like PATH)
            if len(value) > 200:
                value = value[:200] + "..."
        
        # Return all environment variables as key-value pairs
        return json.dumps({
            "status": "displayed_in_console",
            "total_variables": len(all_env_vars),
            "variables": all_env_vars
        })

    def create_python_script(self, python_code: str, filename: str, use_case: str = "Python script") -> str:
        """Save Python code to a file (code is provided by Groq)"""
        try:
            if not python_code:
                error_panel = Panel(
                    "[red]❌ No Python code provided[/red]",
                    title="Script Creation Error",
                    border_style="red"
                )
                console.print(error_panel)
                return json.dumps({"error": "No Python code provided"})
            
            # Clean up the code (remove markdown formatting if present)
            generated_code = python_code.strip()
            if "```python" in generated_code:
                generated_code = generated_code.split("```python")[1].split("```")[0].strip()
            elif "```" in generated_code:
                generated_code = generated_code.split("```")[1].split("```")[0].strip()
            
            # Ensure filename has .py extension
            if not filename.endswith('.py'):
                filename = f"{filename}.py"
            
            # Save to file
            script_path = os.path.join(os.getcwd(), filename)
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(generated_code)
            
            # Display success message
            success_panel = Panel(
                f"[bold green]✅ Python script created successfully![/bold green]\n\n"
                f"[cyan]File:[/cyan] {script_path}\n"
                f"[cyan]Use case:[/cyan] {use_case}\n"
                f"[cyan]Lines of code:[/cyan] {len(generated_code.splitlines())}",
                title="🐍 Script Generation Complete",
                border_style="green"
            )
            console.print(success_panel)
            
            # Show code preview
            code_preview = Syntax(generated_code[:500] + "..." if len(generated_code) > 500 else generated_code, 
                                 "python", theme="monokai", line_numbers=True)
            preview_panel = Panel(
                code_preview,
                title="📝 Code Preview",
                border_style="blue"
            )
            console.print(preview_panel)
            
            return json.dumps({
                "status": "success",
                "filename": filename,
                "filepath": script_path,
                "lines_of_code": len(generated_code.splitlines()),
                "code_preview": generated_code[:200] + "..." if len(generated_code) > 200 else generated_code
            })
            
        except Exception as e:
            error_panel = Panel(
                f"[red]❌ Error creating Python script: {str(e)}[/red]",
                title="Script Generation Error",
                border_style="red"
            )
            console.print(error_panel)
            return json.dumps({"error": f"Failed to create script: {str(e)}"})

    def execute_python_script(self, filename: str) -> str:
        """Execute a Python script and return the output"""
        try:
            import subprocess
            
            # Ensure filename has .py extension
            if not filename.endswith('.py'):
                filename = f"{filename}.py"
            
            # Check if file exists
            script_path = os.path.join(os.getcwd(), filename)
            if not os.path.exists(script_path):
                error_panel = Panel(
                    f"[red]❌ File not found: {script_path}[/red]",
                    title="Execution Error",
                    border_style="red"
                )
                console.print(error_panel)
                return json.dumps({"error": f"File not found: {script_path}"})
            
            # Show execution start
            exec_panel = Panel(
                f"[bold yellow]🚀 Executing Python script...[/bold yellow]\n"
                f"[cyan]File:[/cyan] {script_path}",
                title="Script Execution",
                border_style="yellow"
            )
            console.print(exec_panel)
            
            # Execute the script
            result = subprocess.run(
                [sys.executable, script_path],
                capture_output=True,
                text=True,
                timeout=30,  # 30 second timeout
                cwd=os.getcwd()
            )
            
            # Prepare output
            stdout = result.stdout.strip()
            stderr = result.stderr.strip()
            return_code = result.returncode
            
            # Display results
            if return_code == 0:
                # Successful execution
                if stdout:
                    output_panel = Panel(
                        stdout,
                        title="✅ Script Output",
                        border_style="green"
                    )
                    console.print(output_panel)
                else:
                    console.print("[green]✅ Script executed successfully with no output[/green]")
                
                return json.dumps({
                    "status": "success",
                    "return_code": return_code,
                    "output": stdout,
                    "error": stderr if stderr else None
                })
            else:
                # Execution failed
                error_panel = Panel(
                    f"[red]Return code: {return_code}[/red]\n\n{stderr}",
                    title="❌ Script Execution Failed",
                    border_style="red"
                )
                console.print(error_panel)
                
                return json.dumps({
                    "status": "error",
                    "return_code": return_code,
                    "output": stdout if stdout else None,
                    "error": stderr
                })
                
        except subprocess.TimeoutExpired:
            error_panel = Panel(
                "[red]❌ Script execution timed out (30 seconds)[/red]",
                title="Execution Timeout",
                border_style="red"
            )
            console.print(error_panel)
            return json.dumps({"error": "Script execution timed out"})
        except Exception as e:
            error_panel = Panel(
                f"[red]❌ Error executing script: {str(e)}[/red]",
                title="Execution Error",
                border_style="red"
            )
            console.print(error_panel)
            return json.dumps({"error": f"Failed to execute script: {str(e)}"})

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
        response = ""
        try:
            # Route the query
            if show_progress:
                with console.status("[bold blue]🔍 Analyzing query...", spinner="dots"):
                    route = self.route_query(prompt)
            else:
                route = self.route_query(prompt)
            print(f"Routing decision: {route}")
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
                        title="🤖 Iris Response",
                        border_style="cyan",
                        padding=(1, 2)
                    )
                    console.print(response_panel)
                
            except KeyboardInterrupt:
                console.print("\n[bold green]👋 Goodbye![/bold green]")
                break
            except Exception as e:
                console.print(f"[bold red]❌ Error: {e}[/bold red]")

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

    def read_and_edit_file(self, file_path: str) -> None:
        """Read and edit file with beautiful formatting"""
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                error_panel = Panel(
                    f"[red]❌ File not found: {file_path}[/red]",
                    title="File Error",
                    border_style="red"
                )
                console.print(error_panel)
                return

            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Detect file type for syntax highlighting
            file_extension = os.path.splitext(file_path)[1].lower()
            lexer = "python" if file_extension == ".py" else \
                    "javascript" if file_extension in [".js", ".jsx", ".ts", ".tsx"] else \
                    "html" if file_extension in [".html", ".htm"] else \
                    "css" if file_extension == ".css" else \
                    "json" if file_extension == ".json" else \
                    "markdown" if file_extension in [".md", ".markdown"] else \
                    "yaml" if file_extension in [".yml", ".yaml"] else \
                    "text"

            # Display file info
            file_info = Table(show_header=False, box=box.ROUNDED, border_style="cyan")
            file_info.add_row("[bold cyan]File Path:[/bold cyan]", file_path)
            file_info.add_row("[bold cyan]Size:[/bold cyan]", f"{os.path.getsize(file_path):,} bytes")
            file_info.add_row("[bold cyan]Last Modified:[/bold cyan]", 
                            datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S'))
            console.print(file_info)

            # Display file content with syntax highlighting
            content_panel = Panel(
                Syntax(content, lexer, theme="monokai", line_numbers=True),
                title=f"📄 {os.path.basename(file_path)}",
                border_style="blue",
                padding=(1, 2)
            )
            console.print(content_panel)

            # Ask if user wants to edit the file
            if Confirm.ask("Would you like to edit this file?"):
                # Create temporary file with line numbers for reference
                temp_content = "\n".join(f"{i+1}: {line}" for i, line in enumerate(content.splitlines()))
                temp_panel = Panel(
                    temp_content,
                    title="File Content with Line Numbers",
                    border_style="yellow"
                )
                console.print(temp_panel)

                while True:
                    edit_type = Prompt.ask(
                        "Choose edit type",
                        choices=["line", "append", "prepend", "replace", "cancel"],
                        default="cancel"
                    )

                    if edit_type == "cancel":
                        break

                    try:
                        if edit_type == "line":
                            line_num = int(Prompt.ask("Enter line number to edit")) - 1
                            lines = content.splitlines()
                            if 0 <= line_num < len(lines):
                                console.print(f"Current line: {lines[line_num]}")
                                new_line = Prompt.ask("Enter new content")
                                lines[line_num] = new_line
                                content = "\n".join(lines)
                            else:
                                console.print("[red]Invalid line number[/red]")

                        elif edit_type == "append":
                            new_content = Prompt.ask("Enter content to append")
                            content = content.rstrip() + "\n" + new_content

                        elif edit_type == "prepend":
                            new_content = Prompt.ask("Enter content to prepend")
                            content = new_content + "\n" + content.lstrip()

                        elif edit_type == "replace":
                            old_text = Prompt.ask("Enter text to replace")
                            new_text = Prompt.ask("Enter replacement text")
                            content = content.replace(old_text, new_text)

                        # Show preview of changes
                        preview_panel = Panel(
                            Syntax(content, lexer, theme="monokai", line_numbers=True),
                            title="Preview of Changes",
                            border_style="green"
                        )
                        console.print(preview_panel)

                        if Confirm.ask("Save changes?"):
                            with open(file_path, 'w', encoding='utf-8') as f:
                                f.write(content)
                            console.print("[bold green]✅ Changes saved successfully![/bold green]")
                            break
                        else:
                            # Reload original content if changes are discarded
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                            console.print("[yellow]Changes discarded[/yellow]")

                    except ValueError as e:
                        console.print(f"[red]Invalid input: {e}[/red]")
                    except Exception as e:
                        console.print(f"[red]Error during edit: {e}[/red]")

        except Exception as e:
            error_panel = Panel(
                f"[red]❌ Error reading/editing file: {str(e)}[/red]",
                title="File Error",
                border_style="red"
            )
            console.print(error_panel)

def translate_command(command: str) -> str:
    """Translate Unix commands to Windows if needed"""
    # Only translate commands on Windows
    if platform.system().lower() != "windows":
        return command
        
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
        description="Iris CLI - AI Assistant ",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  iris chat                           # Start interactive chat
  iris hello there                    # Direct query (just type naturally)
  iris read path/to/file.txt          # Read and edit file
        """
    )
    
    # Add optional arguments
    parser.add_argument('--api-key', help='Groq API key (or set GROQ_API_KEY env var)')
    parser.add_argument('--model', default='llama-3.3-70b-versatile', 
                       help='Groq model to use (default: llama-3.3-70b-versatile)')
    parser.add_argument('--temperature', type=float, default=0.7,
                       help='Temperature for response generation (default: 0.7)')
    parser.add_argument('--max-tokens', type=int, default=4096,
                       help='Maximum tokens in response (default: 4096)')
    parser.add_argument('--system-prompt', help='System prompt to use')
    parser.add_argument('--save-conversation', help='Save conversation to file')
    parser.add_argument('--load-conversation', help='Load conversation from file')
    
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
            elif query.lower().startswith("read "):
                # Handle read command
                groq_cli = GroqCLI()
                groq_cli.read_and_edit_file(query.split(" ", 1)[1])
                return
                
            # Initialize for direct query
            groq_cli = GroqCLI()
            groq_cli.configure_model("llama-3.3-70b-versatile")
            
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
                    title="🤖 Iris Response",
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
