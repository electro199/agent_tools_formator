"""
These are some scripts i use for testing the basic feature manually 

"""

# import json
import ollama
import asyncio
from simple_agents import get_relevant_tools, tools, call_tools
import tools

second_prompt = False  # for less compute


async def run(chat):
    client = ollama.AsyncClient()

    messages = [
        {"role": "user", "content": chat},
    ]

    # First API call: Send the initial user message to the model

    response = await client.chat(
        model="llama3.1",
        messages=messages,
        tools=get_relevant_tools(chat),
        options=ollama.Options(temperature=0.5),
    )

    # Check if the model decided to use a provided function
    if not response["message"].get("tool_calls"):
        print("The model didn't use a function. Its response was:")
        print(response["message"]["content"])
        return

    messages.append(response["message"])

    # Process function calls made by the model
    if response["message"].get("tool_calls"):
        available_functions = tools
        for tool in response["message"]["tool_calls"]:
            function_to_call = available_functions[tool["function"]["name"]]
            function_response = function_to_call(**tool["function"]["arguments"])
            messages.append({"role": "tool", "content": str(function_response)})

    # Provide context to the model for continuing the conversation
    messages.append(
        {
            "role": "system",
            "content": """You just used a tool. Use the tool response to complete the task (without mentioning it tools) see history for user query""",
        }
    )
    messages.append({"role": "user", "content": f"HISTORY:\n{chat}"})

    # Second API call: Get the final response from the model
    final_response = await client.chat(model="llama3.1", messages=messages)
    print(final_response["message"]["content"])


async def chat_with_agent(chat):
    client = ollama.AsyncClient()

    messages = []

    # messages.append(
    #     {
    #         "role": "system",
    #         "content": """ You are powerful Ai assistant you can use functions if required to complete the task """,
    #     }
    # )
    # First API call: Send the initial user message to the model
    # while 1:
    messages.append(
        {"role": "user", "content": chat},
    )

    response = await client.chat(
        model="llama3.1",
        messages=messages,
        tools=get_relevant_tools(chat),
        # options=ollama.Options(temperature=0.8),
    )

    # Check if the model decided to use a provided function
    tools = get_relevant_tools(chat)
    print(tools)    
    if not response["message"].get("tool_calls"):
        print("The model didn't use a function. Its response was:")
        print(response["message"]["content"])
        return

    messages.append(response)
    print(response)

    # Process function calls made by the model
    if response["message"].get("tool_calls"):
        print(call_tools(response["message"]["tool_calls"]))

        if second_prompt :
            messages.append( # need work
                {
                    "role": "system",
                    "content": """You just used a tool. Use the tool response to complete the task (without mentioning it tools) see history for user query""",
                }
            )
            # messages.append({"role": "user", "content": f"HISTORY:\n{chat}"})

            # Second API call: Get the final response from the model
            final_response = await client.chat(model="llama3.1", messages=messages)

            print(final_response["message"]["content"])



# # Run the async function
prompts = [
    "open youtube app",
    "open notepad app",
    "open spotify app",
    "open chrome app",
    "call mom",
    "get mom number",
    "what time is it ?"
    "anything important for me to do ?"
    "see if boss sent me something",
    "use 2 tools",
    "open youtube and get time",
]
for prompt in prompts:
    asyncio.run(chat_with_agent(prompt))
    # print(prompt,get_relevant_tools(prompt=prompt))
# # print(tools.values())

# print(get_relevant_tools("open youtube app"))