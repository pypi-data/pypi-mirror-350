"""
Tests for checking the compatibility of the adapter with the original functions.

These tests verify that the adapter correctly redirects calls to the library
and that the function signatures match the originals.
"""

import unittest
import asyncio
import sys
import os
from datetime import datetime
from typing import List, Dict

# Add parent directory path to be able to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import adapter
from voice_agent.agent_zero.MainAgent.tools_adapter import (
    transfer_call, 
    get_available_time_slots, 
    book_appointment, 
    get_weekday, 
    end_call, 
    convert_slot_to_iso_format,
    check_slot_availability,
    FUNCTION_CALLING_TOOLS
)

# Import library functions for comparison
from spacestep_tool_call import (
    transfer_call as lib_transfer_call,
    get_available_time_slots as lib_get_available_time_slots,
    book_appointment as lib_book_appointment,
    get_weekday as lib_get_weekday,
    end_call as lib_end_call,
    FUNCTION_CALLING_TOOLS as LIB_FUNCTION_CALLING_TOOLS
)


class TestAdapter(unittest.TestCase):
    """Tests for checking the compatibility of the adapter with the library."""

    def test_function_calling_tools(self):
        """Check that FUNCTION_CALLING_TOOLS match the originals."""
        self.assertEqual(FUNCTION_CALLING_TOOLS, LIB_FUNCTION_CALLING_TOOLS)

    def test_transfer_call(self):
        """Check that transfer_call redirects to the library."""
        result1 = asyncio.run(transfer_call())
        result2 = asyncio.run(lib_transfer_call())
        self.assertEqual(result1, result2)

    def test_end_call(self):
        """Check that end_call redirects to the library."""
        result1 = asyncio.run(end_call())
        result2 = asyncio.run(lib_end_call())
        self.assertEqual(result1, result2)

    def test_get_weekday(self):
        """Check that get_weekday redirects to the library."""
        date = "2023-06-01"  # Thursday
        result1 = asyncio.run(get_weekday(date))
        result2 = asyncio.run(lib_get_weekday(date))
        self.assertEqual(result1, result2)

    def test_convert_slot_to_iso_format(self):
        """Check that convert_slot_to_iso_format redirects to the library."""
        time_slot = "14:00 - 14:30"
        date_str = "2023-06-01"
        
        # Import library function for comparison
        from spacestep_tool_call.scheduling import convert_slot_to_iso_format as lib_convert
        
        result1 = asyncio.run(convert_slot_to_iso_format(time_slot, date_str))
        result2 = asyncio.run(lib_convert(time_slot, date_str))
        
        self.assertEqual(result1, result2)
        self.assertIn('start_date', result1)
        self.assertIn('end_date', result1)

    def test_get_available_time_slots(self):
        """
        Check that get_available_time_slots redirects to the library.
        
        Note: this test only checks the structure of the response, not the exact data,
        as the function uses random data when webhook_url is not set.
        """
        dates = ["2023-06-01"]  # One date for simplicity
        
        # Get results from both functions
        result1 = asyncio.run(get_available_time_slots(dates))
        result2 = asyncio.run(lib_get_available_time_slots(dates))
        
        # Check that the response structure is the same
        self.assertEqual(len(result1), len(result2))
        self.assertEqual(type(result1), type(result2))
        
        # Check the first element (for each date)
        for i in range(len(result1)):
            self.assertIn('date', result1[i])
            self.assertIn('free_slots', result1[i])


if __name__ == '__main__':
    unittest.main() 