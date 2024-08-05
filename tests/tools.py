from simple_agents import  tool_func

@tool_func
def print_to_console(msg: str) -> None:
    "print the given msg(str) to console"

    print(msg)

@tool_func
def call_phone_number(number: str) -> bool:
    """
    calls a phone number

    Return :
        bool : whether call started or not
    """
    return True

@tool_func
def get_number(name: str) -> str:
    """
    get number by name from phone book
    search name

    returns : number
    """
    print(name)
    return {"mom": "123", "alison": "111"}.get(name.lower(), "No number found")

@tool_func
def open_youtube() -> bool:
    """
    start youtube in the device

    return :
        bool : app stating or not
    """
    return True

@tool_func
def open_chrome() -> bool:
    """
    start chrome in the device

    return :
        bool : app stating or not
    """
    return True

@tool_func
def open_spotify() -> bool:
    """
    start spotify in the device

    return :
        bool : app stating or not
    """
    return True

@tool_func
def open_nootpad() -> bool:
    """
    start nootpad in the device

    return :
        bool : app stating or not
    """
    return True

@tool_func
def get_time() -> str:
    """Get current time """
    return "1:16 am"

@tool_func
def get_recent_Messages() -> list[str]:
    """
    get recent messages
    """
    return [
        "mom : what are you doing ?",
        "boss : can you join meeting by 2:14 AM  ",
        "232: Ad for 1 dollar get 1 bar",
    ]


# Simulates an API call to get flight times
# In a real application, this would fetch data from a live database or API

# tools: dict[str, Callable] = {
#     "print_to_console": print_to_console,
#     "get_recent_Messages": get_recent_Messages,
#     "get_number": get_number,
#     "call_phone_number": call_phone_number,
#     "open_youtube": open_youtube,
#     "open_spotify": open_spotify,
#     "open_chrome": open_chrome,
#     "open_nootpad": open_nootpad,
#     "get_time": get_time,
# }
