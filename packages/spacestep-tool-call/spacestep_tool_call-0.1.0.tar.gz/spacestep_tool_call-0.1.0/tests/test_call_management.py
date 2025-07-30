"""
Tests for the call management module
"""

import unittest
import asyncio
from datetime import datetime
from spacestep_tool_call.call_management import get_weekday, FUNCTION_CALLING_TOOLS


class TestCallManagement(unittest.TestCase):
    """Test cases for call management module"""
    
    def test_get_weekday(self):
        """Test getting weekday from date"""
        # Test valid date format
        result = asyncio.run(get_weekday("2023-06-01"))  # This is a Thursday
        self.assertEqual(result, "User asked to be scheduled to Thursday")
        
        # Test invalid date format
        result = asyncio.run(get_weekday("01-06-2023"))
        self.assertEqual(result, "Invalid date format. Please use YYYY-MM-DD.")
    
    def test_function_calling_tools(self):
        """Test that function calling tools are properly defined"""
        # Check that tools list is not empty
        self.assertTrue(len(FUNCTION_CALLING_TOOLS) > 0)
        
        # Check that each tool has correct structure
        for tool in FUNCTION_CALLING_TOOLS:
            self.assertIn('type', tool)
            self.assertEqual(tool['type'], 'function')
            self.assertIn('function', tool)
            self.assertIn('name', tool['function'])
            self.assertIn('description', tool['function'])
            self.assertIn('parameters', tool['function'])


if __name__ == '__main__':
    unittest.main() 