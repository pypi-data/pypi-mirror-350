"""
Call management module for handling calls and call-related utilities.
"""

from datetime import datetime


async def transfer_call():
    """
    Transfer the call to a licensed agent.
    
    Returns:
        str: Confirmation message
    """
    print("Call transfer in progress...")
    return "Transferring the call"


async def end_call():
    """
    End the current call.
    
    Returns:
        str: Confirmation message
    """
    print("Call ended.")
    return "End the call."


async def get_weekday(date: str) -> str:
    """
    Takes a date string in YYYY-MM-DD format and returns a formatted response indicating
    the day of the week that date falls on.
    
    Args:
        date (str): Date in YYYY-MM-DD format
        
    Returns:
        str: Formatted message with weekday
    """
    try:
        dt = datetime.strptime(date, "%Y-%m-%d")
        weekday = dt.strftime("%A")
        return f"User asked to be scheduled to {weekday}"
    except ValueError:
        return "Invalid date format. Please use YYYY-MM-DD."


# Function calling tools definition
FUNCTION_CALLING_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "transfer_call",
            "description": "Use this function to transfer client to the licensed agent when they agreed to.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "end_call",
            "description": "End the phone call when:\n- if the human user and the assistant have clearly finished speaking to each other;\n- if the user said goodbye (e.g., 'bye', 'goodbye', 'farewell', 'see you', 'adios');\n- after assistant has left the voicemail message.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_weekday",
            "description": "Use this to determine what day of the week a given date falls on (e.g., Monday, Tuesday). This helps decide if a requested call can be scheduled.",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {
                        "type": "string",
                        "description": "The date to check, in YYYY-MM-DD format",
                    }
                },
                "required": ["date"],
            },
        },
    },
] 