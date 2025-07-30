"""
Tests for the scheduling module
"""

import unittest
import asyncio
from datetime import datetime
from spacestep_tool_call.scheduling import convert_slot_to_iso_format, get_available_time_slots


class TestScheduling(unittest.TestCase):
    """Test cases for scheduling module"""
    
    def test_convert_slot_to_iso_format(self):
        """Test converting time slot to ISO format"""
        result = asyncio.run(convert_slot_to_iso_format("10:00 - 10:30", "2023-06-01"))
        
        # Check if start_date and end_date keys exist
        self.assertIn('start_date', result)
        self.assertIn('end_date', result)
        
        # Check format of start_date
        start_date = result['start_date']
        self.assertEqual(start_date, "2023-06-01T10:00:00.000Z")
        
        # Check format of end_date
        end_date = result['end_date']
        self.assertEqual(end_date, "2023-06-01T10:30:00.000Z")
    
    def test_get_available_time_slots_no_webhook(self):
        """Test getting available time slots without webhook"""
        dates = ["2023-06-01", "2023-06-02"]  # Thursday, Friday
        result = asyncio.run(get_available_time_slots(dates))
        
        # Check if we got results for both dates
        self.assertEqual(len(result), 2)
        
        # Check structure of each result
        for date_result in result:
            self.assertIn('date', date_result)
            self.assertIn('free_slots', date_result)
            self.assertIsInstance(date_result['free_slots'], list)
            
            # All slots should be in ascending order
            if len(date_result['free_slots']) > 1:
                for i in range(1, len(date_result['free_slots'])):
                    self.assertLess(
                        date_result['free_slots'][i-1],
                        date_result['free_slots'][i]
                    )


if __name__ == '__main__':
    unittest.main() 