# codesys SDK

A Python SDK for interacting with the Claude CLI tool.

## Installation

```bash
pip install codesys
```

## Requirements

- Python 3.8+
- Claude CLI tool must be installed, available in your PATH, and set up with your api key.

## Quick Start

```python
from codesys import Agent

# Initialize with a working directory
agent = Agent(working_dir="/Users/seansullivan/lmsys-sdk/")

# This can be a prompt string or claude code command (treat it as your claude code input)
lines = agent.run("""/init""", stream=True)
```


### Practical Use:

the most effective way I've found of using this sdk is by mimicing my actual workflow with claude code which I've found extremely effective.

the workflow is simple: plan the task by exploring the codebase, then implement the plan
```python
#!/usr/bin/env python3

import os
from codesys import Agent


# Configuration - modify these values as needed
WORKING_DIR = os.getcwd()  # Use the current working directory



USER_MESSAGE = """Your super long, complex task here."""



def generate_plan_and_execute():
    """Generate a plan and then execute it using the same conversation session."""
    agent = Agent(working_dir=WORKING_DIR)



    # Step 1: Generate the plan
    print("Generating plan...")
    prompt = f'''
generate a plan into plan.md file given the following task:
<task>
{USER_MESSAGE}
</task>
Given this task, explore the codebase and create a plan for the implementation into plan.md for our developer to accomplish this task step by step. ultrathink
'''
    agent.run(prompt, stream=True)



    # Step 2: Execute the plan continuing the same conversation
    print("\nExecuting plan from plan.md...")
    prompt = '''
Implement the task laid out in plan.md: ultrathink
'''
    agent.run_convo(prompt, stream=True)



if __name__ == "__main__":
    print(f"Working directory: {WORKING_DIR}")
    print(f"Task: {USER_MESSAGE}")
    generate_plan_and_execute()

```


## Features

- Simple interface to the Claude CLI tool
- Support for all Claude CLI options
- Automatic or manual streaming output
- Customizable tool access
- Conversation management with session continuity
- Support for resuming specific conversations by ID

## API Reference

### Agent Class

```python
Agent(working_dir=None, allowed_tools=None)
```

**Parameters:**
- `working_dir` (str, optional): The working directory for Claude to use. Defaults to current directory.
- `allowed_tools` (list, optional): List of tools to allow Claude to use. Defaults to ["Edit", "Bash", "Write"].

### Methods

#### run

```python
run(prompt, stream=False, output_format=None, additional_args=None, auto_print=True, continue_session=False, session_id=None)
```

Run Claude with the specified prompt.

**Parameters:**
- `prompt` (str): The prompt to send to Claude.
- `stream` (bool): If True, handles streaming output. If False, returns the complete output.
- `output_format` (str, optional): Optional output format (e.g., "stream-json").
- `additional_args` (dict, optional): Additional arguments to pass to the Claude CLI.
- `auto_print` (bool): If True and stream=True, automatically prints output. If False, you need to handle streaming manually.
- `continue_session` (bool): If True, continues the most recent Claude session.
- `session_id` (str, optional): If provided, resumes the specific Claude session with this ID.

**Returns:**
- If `stream=False`: Returns the complete output as a string.
- If `stream=True` and `auto_print=False`: Returns a subprocess.Popen object for manual streaming.
- If `stream=True` and `auto_print=True`: Automatically prints output and returns collected lines as a list.

#### run_with_tools

```python
run_with_tools(prompt, tools, stream=False, auto_print=True, continue_session=False, session_id=None)
```

Run Claude with specific allowed tools.

**Parameters:**
- `prompt` (str): The prompt to send to Claude.
- `tools` (list): List of tools to allow Claude to use.
- `stream` (bool): If True, handles streaming output.
- `auto_print` (bool): If True and stream=True, automatically prints output.
- `continue_session` (bool): If True, continues the most recent Claude session.
- `session_id` (str, optional): If provided, resumes the specific Claude session with this ID.

**Returns:**
- If `stream=False`: Returns the complete output as a string.
- If `stream=True` and `auto_print=False`: Returns a subprocess.Popen object.
- If `stream=True` and `auto_print=True`: Automatically prints output and returns collected lines.

#### run_convo

```python
run_convo(prompt, **kwargs)
```

Continue the most recent Claude conversation. This method maintains the same session state as the previous interaction, allowing for context-aware follow-up prompts.

**Parameters:**
- `prompt` (str): The prompt to send to Claude.
- `**kwargs`: Additional arguments to pass to the run method (stream, output_format, etc.)

**Returns:**
- Same return types as the `run` method, depending on parameters used.

#### resume_convo

```python
resume_convo(session_id, prompt, **kwargs)
```

Resume a specific Claude conversation by ID. This allows you to return to a previous conversation even after starting other sessions.

**Parameters:**
- `session_id` (str): The session ID to resume.
- `prompt` (str): The prompt to send to Claude.
- `**kwargs`: Additional arguments to pass to the run method (stream, output_format, etc.)

**Returns:**
- Same return types as the `run` method, depending on parameters used.

#### get_last_session_id

```python
get_last_session_id()
```

Get the session ID from the last Claude run. Useful for saving session IDs to resume conversations later.

**Returns:**
- The session ID if available, otherwise None.

## Example: Automatic Streaming

```python
from codesys import Agent

agent = Agent()
# This will automatically print the output line by line
lines = agent.run("Generate a short story", stream=True)
```

## Example: Manual Streaming with JSON parsing

```python
from codesys import Agent
import json

agent = Agent()
process = agent.run("Generate a short story", stream=True, output_format="stream-json", auto_print=False)

for line in process.stdout:
    if line.strip():
        try:
            data = json.loads(line)
            print(data.get("content", ""))
        except json.JSONDecodeError:
            print(f"Error parsing JSON: {line}")
```

# Examples

```python
from codesys import Agent

# Initialize with a working directory
agent = Agent(working_dir="/Users/seansullivan/lmsys-sdk/")

# Run Claude with a prompt and automatically print streaming output
lines = agent.run("create another example of example1_custom_tools.py which shows how to use read only tools. note the source code of the sdk in codesys/agent.py", stream=True)

```

```python
"""
Example 1: Customizing tools during initialization

This example demonstrates how to initialize an Agent with only specific tools.
"""

from codesys import Agent

# Initialize with only specific tools
restricted_agent = Agent(
    working_dir="./",
    allowed_tools=["Edit", "Write", "View"]  # Only allow editing, writing files and viewing
)  # Implementation in agent.py lines 19-39

print(f"Agent initialized with tools: {restricted_agent.allowed_tools}")
```

```python

from codesys import Agent

# Initialize with default tools
agent = Agent(working_dir="./")  # Implementation in agent.py lines 19-39
print(f"Default tools: {agent.allowed_tools}")

# Run with only specific tools for one operation
bash_only_response = agent.run_with_tools(
    prompt="List files in the current directory",
    tools=["Bash"],  # Only allow Bash for this specific run
    stream=False
)  # Implementation in agent.py lines 132-155

print(f"Tools after run_with_tools: {agent.allowed_tools}  # Original tools are restored")
```

```python
"""
Example 3: Manual handling of streaming output

This example demonstrates how to manually handle streaming output from the agent.
"""

from codesys import Agent
import json
import time

# Initialize an agent
agent = Agent(working_dir="./")

# Get a process for streaming manually
process = agent.run(
    prompt="Explain what an LLM Agent is in 3 sentences",
    stream=True,
    auto_print=False  # Don't auto-print, we'll handle the output manually
)  # Implementation in agent.py lines 41-96 (stream=True, auto_print=False path)

print("Streaming output manually, processing each line:")
for i, line in enumerate(process.stdout):
    # Parse the JSON line
    try:
        data = json.loads(line)
        # Do something with each piece of output
        print(f"Line {i+1}: {data.get('content', '')}")
    except json.JSONDecodeError:
        print(f"Raw line: {line}")

    # Simulate processing time
    time.sleep(0.1)
    # Compare with agent.py lines 98-116 (auto-handling of streaming)
```

```python
"""
Example 4: Using output formats and additional arguments

This example demonstrates how to use different output formats and pass additional arguments.
"""

from codesys import Agent

# Initialize an agent
agent = Agent(working_dir="./")

# Run with custom output format and additional arguments
response = agent.run(
    prompt="What can you tell me about this codebase?",
    output_format="json",  # Request JSON output
    additional_args={
        "temperature": 0.7,     # Set temperature
        "max-tokens": 500,      # Limit output tokens
        "silent": True          # Suppress progress output
    }
)  # Implementation in agent.py lines 41-70 (output_format handling), 74-80 (additional_args)

print(f"Response type: {type(response)}")
print("First 100 characters of response:", response[:100] if isinstance(response, str) else "Not a string")
```

```python
"""
Example 5: Using run_convo and resume_convo for multi-turn conversations

This example demonstrates how to continue conversations with Claude and maintain context.
"""

from codesys import Agent
import time

# Initialize an agent
agent = Agent(working_dir="./")

# Start a new conversation
print("Starting a new conversation...")
response1 = agent.run(
    prompt="Analyze the structure of this project. What are the main components?",
    stream=True
)

# Continue the same conversation with follow-up
print("\nContinuing the conversation with a follow-up question...")
response2 = agent.run_convo(
    prompt="What improvements would you suggest for this codebase?",
    stream=True
)  # Implementation in agent.py lines 184-197

# Get the session ID for later use
session_id = agent.get_last_session_id()
print(f"\nSession ID: {session_id}")

# Start a different conversation
print("\nStarting a new, unrelated conversation...")
agent.run(
    prompt="Tell me about Python's type hinting system.",
    stream=True
)

# Later, resume the original conversation by ID
print("\nResuming our original conversation about codebase improvements...")
agent.resume_convo(
    session_id=session_id,
    prompt="Could you elaborate on the first improvement you suggested?",
    stream=True
)  # Implementation in agent.py lines 199-211
```



## License

MIT
#### CodeSYS




Summarise the component diagram into a **C4 model container diagram**
(Mermaid syntax) showing services, databases and queues relevant to
"{query}". Output ONLY Mermaid code.


Create a **C4 system context diagram** (Mermaid graph TD)
highlighting external actors, third-party systems and their interactions
with "{query}". Output ONLY Mermaid code.


Combine the four Mermaid diagrams provided below into a single Markdown
document named ARCH_DIAGRAM_{query}.md.


Requirements:
• H2 headings for each level (Detailed Flow, Component View,
    Container View, System Context).
• A legend explaining colours / shapes.
• Colour-code nodes by architectural tier.
• Hyperlink every node to its source file using a relative GitHub link
    (e.g. `src/auth/login.py#L12`).
• Place each diagram inside a fenced ```mermaid block.

Here are the diagrams:

```mermaid
%% DETAILED FLOW
{diag1.strip()}
```

```mermaid
%% COMPONENTS
{diag2.strip()}
```

```mermaid
%% CONTAINERS
{diag3.strip()}
```

```mermaid
%% SYSTEM CONTEXT
{diag4.strip()}
```

Now produce the combined Markdown document ONLY.
