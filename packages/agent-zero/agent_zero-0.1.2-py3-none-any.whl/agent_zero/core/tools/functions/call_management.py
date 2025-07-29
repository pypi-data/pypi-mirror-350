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


async def await_call_transfer():
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