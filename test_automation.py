#!/usr/bin/env python3
"""
Test script for Web UI Automation
"""
import sys
from web_automation import WebAutomation
from click_sequence import ClickSequence


def test_basic_automation():
    """Test basic automation functionality."""
    print("Testing Web UI Automation...")
    
    # Create a simple test sequence
    sequence = ClickSequence("Test Sequence")
    sequence.add_click(100, 100, 0.5)
    sequence.add_click(200, 200, 0.5)
    sequence.add_click(300, 300, 0.5)
    
    print(f"Created sequence: {sequence}")
    print(f"Number of actions: {len(sequence)}")
    
    try:
        # Test with headless browser
        with WebAutomation(headless=True) as automation:
            print("Starting browser...")
            automation.start_browser("data:text/html,<html><body><h1>Test Page</h1></body></html>")
            
            print("Setting window size...")
            automation.set_window_size(800, 600)
            
            print("Getting window size...")
            size = automation.get_window_size()
            print(f"Window size: {size}")
            
            print("Executing click sequence...")
            automation.execute_click_sequence(sequence, loops=2)
            
            print("Test completed successfully!")
            return True
            
    except Exception as e:
        print(f"Error during automation test: {e}")
        return False


if __name__ == "__main__":
    success = test_basic_automation()
    sys.exit(0 if success else 1)