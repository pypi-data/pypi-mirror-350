"""
Scheduling module for appointment booking and time slot management.
"""

from datetime import datetime
import asyncio
import os
import random
from typing import List
import aiohttp
import httpx


async def convert_slot_to_iso_format(time_slot: str, date_str: str) -> dict:
    """
    Converts a time slot and date to ISO format for start_date and end_date.
    
    Args:
        time_slot (str): Time slot in format "HH:MM - HH:MM"
        date_str (str): Date in format "YYYY-MM-DD"
        
    Returns:
        dict: Dictionary with start_date and end_date in ISO format
    """
    start_time, end_time = time_slot.split(' - ')
    
    # Parse the date
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    
    # Parse start and end times
    start_hours, start_minutes = map(int, start_time.split(':'))
    end_hours, end_minutes = map(int, end_time.split(':'))
    
    # Create datetime objects for start and end
    start_datetime = date_obj.replace(hour=start_hours, minute=start_minutes, second=0, microsecond=0)
    end_datetime = date_obj.replace(hour=end_hours, minute=end_minutes, second=0, microsecond=0)
    
    # Return ISO format with Z at the end (UTC)
    return {
        'start_date': start_datetime.strftime('%Y-%m-%dT%H:%M:%S.000Z'),
        'end_date': end_datetime.strftime('%Y-%m-%dT%H:%M:%S.000Z')
    }


async def check_slot_availability(session, time_slot: str, date_str: str, webhook_url: str) -> dict:
    """
    Asynchronously checks slot availability via webhook.
    
    Args:
        session: aiohttp session
        time_slot (str): Time slot in format "HH:MM - HH:MM"
        date_str (str): Date in format "YYYY-MM-DD"
        webhook_url (str): URL to check availability
        
    Returns:
        dict: Dictionary with slot information and availability status
    """
    # Convert slot to ISO format
    slot_params = await convert_slot_to_iso_format(time_slot, date_str)
    
    # Send request to webhook
    try:
        async with session.get(webhook_url, params=slot_params) as response:
            # By default, slot is unavailable
            is_available = False
            
            if response.status == 200:
                try:
                    # Try to read response as JSON
                    result = await response.json()
                    
                    # Check response structure: [{"available": true/false}]
                    if isinstance(result, list) and len(result) > 0 and isinstance(result[0], dict):
                        is_available = result[0].get('available', False)
                    # Also check alternative structure: {"is_available": true/false}
                    elif isinstance(result, dict):
                        is_available = result.get('is_available', result.get('available', False))
                except Exception as json_error:
                    print(f"Error parsing JSON for slot {time_slot} on {date_str}: {json_error}")
                    # If JSON parsing fails, use text response
                    try:
                        text_response = await response.text()
                        # Simple check for keywords in response
                        is_available = 'true' in text_response.lower() or 'available' in text_response.lower()
                    except:
                        pass
            
            # Return result
            return {
                'time_slot': time_slot,
                'is_available': is_available,
                'date': date_str
            }
    except Exception as e:
        # Handle connection errors
        print(f"Error checking slot {time_slot} on {date_str}: {e}")
        return {
            'time_slot': time_slot,
            'is_available': False,
            'date': date_str
        }


async def get_available_time_slots(dates: List[str], webhook_url: str = None):
    """
    Asynchronously gets all available time slots for a list of dates.
    
    Args:
        dates (List[str]): List of dates in format "YYYY-MM-DD"
        webhook_url (str, optional): URL to check availability. If None, uses environment variable 
                                     TOOL_CHECK_SLOT_AVAILABILITY_WEBHOOK_URL.
        
    Returns:
        List[dict]: List of dictionaries with dates and available slots
    """
    time_slots = [
        "09:00 - 09:30", "09:30 - 10:00", "10:00 - 10:30", "10:30 - 11:00",
        "11:00 - 11:30", "11:30 - 12:00", "13:00 - 13:30", "13:30 - 14:00",
        "14:00 - 14:30", "14:30 - 15:00", "15:00 - 15:30", "15:30 - 16:00",
        "16:00 - 16:30", "16:30 - 17:00"
    ]
    
    result = []
    
    # Use provided webhook_url or get from environment
    webhook_url = webhook_url or os.getenv("TOOL_CHECK_SLOT_AVAILABILITY_WEBHOOK_URL")
    
    # Create a single session for all requests
    async with aiohttp.ClientSession() as session:
        for date_str in dates:
            dt_obj = datetime.strptime(date_str, "%Y-%m-%d")
            formatted_date = f"{date_str}, {dt_obj.strftime('%A')}"
            
            # Skip weekends
            if dt_obj.weekday() in [5, 6]:  # 5 = Saturday, 6 = Sunday
                result.append({
                    "date": formatted_date,
                    "free_slots": []
                })
                continue
            
            # If webhook is not set, use pseudo-random slot selection
            if not webhook_url:
                random.seed(int(dt_obj.timestamp()))
                free_slots_count = random.randint(0, 7)
                free_slots = random.sample(time_slots, free_slots_count) if free_slots_count > 0 else []
                result.append({
                    "date": formatted_date,
                    "free_slots": sorted(free_slots)
                })
                continue
            
            # Create a list of tasks to check all slots for the current date
            tasks = [
                check_slot_availability(session, slot, date_str, webhook_url)
                for slot in time_slots
            ]
            
            # Run all tasks concurrently
            slot_results = await asyncio.gather(*tasks)
            
            # Filter only available slots
            available_slots = [
                item['time_slot'] for item in slot_results 
                if item['is_available']
            ]
            
            result.append({
                "date": formatted_date,
                "free_slots": sorted(available_slots)
            })
    
    return result


async def book_appointment(name: str, email: str, phone_number: str, selected_time_slot: str, webhook_url: str = None) -> dict:

    
    """
    Book an appointment for a client.

    Args:
        name (str): Client's full name.
        email (str): Client's email address.
        phone_number (str): Client's phone number.
        selected_time_slot (str): Appointment slot in the format "YYYY-MM-DD, HH:MM - HH:MM".
        webhook_url (str, optional): URL to submit booking. If None, uses environment variable
                                    TOOL_BOOKING_WEBHOOK_URL.

    Returns:
        dict: { status: "success"|"error", message: str }
    """
    # Use provided webhook_url or get from environment
    url = webhook_url or os.getenv("TOOL_BOOKING_WEBHOOK_URL")
    if not url:
        return {"status": "error", "message": "Webhook URL is not configured."}

    payload = {
        "name": name,
        "email": email,
        "phone_number": phone_number,
        "selected_time_slot": selected_time_slot
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            return {"status": "success", "message": "Appointment booked successfully."}
        else:
            return {"status": "error", "message": "Sorry, I can't book an appointment right now."}
    except Exception as e:
        return {"status": "error", "message": f"error: {e}"} 

FUNCTION_CALLING_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_available_time_slots",
            "description": "Get the available time slots in a calendar for specified dates.",
            "parameters": {
                "type": "object",
                "properties": {
                    "dates": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "format": "date",
                            "description": "A date in the format yyyy-mm-dd."
                        },
                        "description": "A list of dates to check for available slots. Each date must have the format yyyy-mm-dd."
                    }
                },
                "required": ["dates"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "book_appointment",
            "description": "Book an appointment for a client.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Client's full name."
                    },
                    "email": {
                        "type": "string",
                        "description": "Client's email address."
                    },
                    "phone_number": {
                        "type": "string",
                        "description": "Client's phone number."
                    },
                    "selected_time_slot": {
                        "type": "string",
                        "description": "Appointment slot in the format \"YYYY-MM-DD, HH:MM - HH:MM\"."
                    }
                },
                "required": ["name", "email", "phone_number", "selected_time_slot"]
            }
        }
    }
]
