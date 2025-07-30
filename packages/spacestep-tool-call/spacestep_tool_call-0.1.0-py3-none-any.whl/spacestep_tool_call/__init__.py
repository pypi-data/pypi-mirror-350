"""
SpaceStep Tool Call - AI-powered call center automation and appointment scheduling library
"""

__version__ = "0.1.0"

# Import commonly used functions for easier access
from spacestep_tool_call.scheduling import (
    get_available_time_slots,
    book_appointment,
    convert_slot_to_iso_format
)

from spacestep_tool_call.call_management import (
    transfer_call,
    end_call,
    get_weekday,
    FUNCTION_CALLING_TOOLS
)

__all__ = [
    'get_available_time_slots',
    'book_appointment',
    'convert_slot_to_iso_format',
    'transfer_call',
    'end_call',
    'get_weekday',
    'FUNCTION_CALLING_TOOLS',
] 