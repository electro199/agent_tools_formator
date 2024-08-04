# simple-agents

A simple package for function calling package. Easy to use and straight forward.

# Installation

```bash
pip install git+https://github.com/electro199/simple-agents.git
```

## Usage

Adding tools 
```py
from function_caller import tool_func

@tool_func
def print_to_console(msg: str) -> None:
    "print the given msg(str) to console"

    print(msg)
```

## Retriving Tools
you can you get relevant tools
```py

Tools=get_relevant_tools("Can you print in console ?")

```

With ollama  and tools usage :

```py
import ollama
from simple_agents.tools_generator import get_relevant_tools, tools, tool_func, call_tools

@tool_func
def print_to_console(msg: str) -> None:
    "print the given msg(str) to console"

    print(msg)

client = ollama.Client()
chat = "Can you print in console ?"
response = client.chat(
        model="llama3.1",
        messages=messages,
        tools=get_relevant_tools(chat),
        options=ollama.Options(temperature=0.5),
    )

```

_Work is progress_