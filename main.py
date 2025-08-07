#!/usr/bin/env python3
"""
Web UI Automation - Command Line Interface
Automate clicks in web browser using pixel coordinates with configurable delays and loops.
"""
import json
import argparse
import sys
from web_automation import WebAutomation
from click_sequence import ClickSequence


def load_config(config_file: str):
    """Load configuration from JSON file."""
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Configuration file '{config_file}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in configuration file: {e}")
        sys.exit(1)


def run_automation_from_config(config_file: str, headless: bool = False):
    """Run automation from a configuration file."""
    config = load_config(config_file)
    
    # Extract configuration
    sequence_name = config.get('name', 'Automated Sequence')
    loops = config.get('loops', 1)
    url = config.get('url', 'about:blank')
    clicks = config.get('clicks', [])
    window_size = config.get('window_size', {})
    
    # Validate clicks
    if not clicks:
        print("Error: No clicks defined in configuration.")
        sys.exit(1)

    # Validate each click entry
    for idx, click in enumerate(clicks):
        if not isinstance(click, dict):
            print(f"Error: Click #{idx+1} is not a valid object: {click}")
            sys.exit(1)
        if 'x' not in click or 'y' not in click:
            print(f"Error: Click #{idx+1} missing 'x' or 'y' field: {click}")
            sys.exit(1)
        if not (isinstance(click['x'], int) or isinstance(click['x'], float)):
            print(f"Error: Click #{idx+1} 'x' coordinate is not a number: {click['x']}")
            sys.exit(1)
        if not (isinstance(click['y'], int) or isinstance(click['y'], float)):
            print(f"Error: Click #{idx+1} 'y' coordinate is not a number: {click['y']}")
            sys.exit(1)
        if 'delay' in click and not (isinstance(click['delay'], int) or isinstance(click['delay'], float)):
            print(f"Error: Click #{idx+1} 'delay' is not a number: {click['delay']}")
            sys.exit(1)

    # Run automation
    with WebAutomation(headless=headless) as automation:
        # Create click sequence
        sequence = ClickSequence(sequence_name)
        sequence.add_clicks(clicks)
        automation.start_browser(url)
        
        # Set window size if specified
        if window_size.get('width') and window_size.get('height'):
            automation.set_window_size(window_size['width'], window_size['height'])
        
        # Execute the sequence
        automation.execute_click_sequence(sequence, loops)


def run_interactive_mode():
    """Run automation in interactive mode."""
    print("Web UI Automation - Interactive Mode")
    print("=====================================")
    
    # Get basic configuration
    url = input("Enter URL (or press Enter for blank page): ").strip()
    if not url:
        url = "about:blank"
    
    loops = input("Number of loops (default: 1): ").strip()
    try:
        loops = int(loops) if loops else 1
    except ValueError:
        loops = 1
    
    headless = input("Run in headless mode? (y/N): ").strip().lower() == 'y'
    
    # Create sequence
    sequence = ClickSequence("Interactive Sequence")
    
    print("\nEnter click coordinates (press Enter with empty x to finish):")
    while True:
        x_input = input("X coordinate: ").strip()
        if not x_input:
            break
        
        y_input = input("Y coordinate: ").strip()
        delay_input = input("Delay after click (default: 1.0): ").strip()
        
        try:
            x = int(x_input)
            y = int(y_input)
            delay = float(delay_input) if delay_input else 1.0
            sequence.add_click(x, y, delay)
            print(f"Added click at ({x}, {y}) with {delay}s delay")
        except ValueError:
            print("Invalid input. Please enter numeric values.")
    
    if len(sequence) == 0:
        print("No clicks added. Exiting.")
        return
    
    # Run automation
    print(f"\nStarting automation...")
    with WebAutomation(headless=headless) as automation:
        automation.start_browser(url)
        automation.execute_click_sequence(sequence, loops)


def main():
    parser = argparse.ArgumentParser(
        description="Web UI Automation - Automate clicks using pixel coordinates"
    )
    parser.add_argument(
        '-c', '--config',
        help='Configuration file (JSON format)'
    )
    parser.add_argument(
        '--headless',
        action='store_true',
        help='Run browser in headless mode'
    )
    parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help='Run in interactive mode'
    )
    
    args = parser.parse_args()
    
    if args.interactive:
        run_interactive_mode()
    elif args.config:
        run_automation_from_config(args.config, args.headless)
    else:
        # Show help if no arguments provided
        parser.print_help()
        print("\nExample usage:")
        print("  python main.py -c example_config.json")
        print("  python main.py --interactive")
        print("  python main.py -c example_config.json --headless")


if __name__ == "__main__":
    main()