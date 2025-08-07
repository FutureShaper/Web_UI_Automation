#!/usr/bin/env python3
"""
Web UI Automation - Command Line Interface
Automate clicks in web browser using pixel coordinates with configurable delays and loops.
"""
import json
import argparse
import sys
import time
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


def run_recording_mode():
    """Run automation in recording mode to capture clicks."""
    print("Web UI Automation - Recording Mode")
    print("==================================")
    
    # Get basic configuration
    url = input("Enter URL to load for recording (or press Enter for blank page): ").strip()
    if not url:
        url = "about:blank"
    
    headless = input("Run in headless mode? (y/N): ").strip().lower() == 'y'
    if headless:
        print("Warning: Recording mode works best in non-headless mode for visual feedback.")
        proceed = input("Continue with headless mode? (y/N): ").strip().lower() == 'y'
        if not proceed:
            headless = False
    
    print(f"\nStarting recording session on: {url}")
    print("Instructions:")
    print("1. Browser will open with the specified URL")
    print("2. Click anywhere on the page to record clicks")
    print("3. Red dots will appear where you click")
    print("4. Press ESC key when done recording")
    print("5. You'll be prompted to save the recorded sequence")
    
    input("Press Enter to start recording...")
    
    # Start recording
    with WebAutomation(headless=headless) as automation:
        automation.start_browser(url)
        automation.start_recording_mode()
        
        # Wait for user to finish recording
        print("\nRecording started! Click on the webpage and press ESC when done.")
        print("Waiting for recording to complete...")
        
        # Poll for recording completion
        while automation.recording_mode:
            time.sleep(0.5)
            try:
                # Check if recording has stopped
                is_recording = automation.driver.execute_script("""
                    return window.clickRecorder ? window.clickRecorder.recording : false;
                """)
                if not is_recording:
                    break
            except:
                # Browser might be closed or error occurred
                break
        
        # Stop recording and get clicks
        recorded_clicks = automation.stop_recording_mode()
        
        if not recorded_clicks:
            print("No clicks were recorded.")
            return
        
        print(f"\nRecorded {len(recorded_clicks)} clicks:")
        for i, click in enumerate(recorded_clicks, 1):
            print(f"  {i}. Click at ({click['x']}, {click['y']}) with {click['delay']:.1f}s delay")
        
        # Ask if user wants to save the recording
        save_recording = input("\nSave this recording? (Y/n): ").strip().lower()
        if save_recording != 'n':
            # Get save options
            name = input("Enter sequence name (default: 'Recorded Sequence'): ").strip()
            if not name:
                name = "Recorded Sequence"
            
            while True:
                loops_input = input("Number of loops for automation (default: 1): ").strip()
                if not loops_input:
                    loops = 1
                    break
                try:
                    loops = int(loops_input)
                    if loops < 1:
                        print("Please enter a positive integer for loops.")
                        continue
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid integer for loops.")
            
            filename = input("Save to filename (default: 'recorded_config.json'): ").strip()
            if not filename:
                filename = "recorded_config.json"
            if not filename.endswith('.json'):
                filename += '.json'
            
            # Save the configuration
            automation.save_recorded_clicks_to_config(filename, name, loops, url)
            
            # Ask if user wants to run the recorded sequence
            run_now = input(f"\nRun the recorded sequence now? (y/N): ").strip().lower() == 'y'
            if run_now:
                print(f"Running recorded sequence '{name}' {loops} time(s)...")
                sequence = automation.create_sequence_from_recorded_clicks(name)
                automation.execute_click_sequence(sequence, loops)
                print("Playback completed!")


def run_interactive_mode():
    """Run automation in interactive mode."""
    print("Web UI Automation - Interactive Mode")
    print("=====================================")
    
    # Get basic configuration
    url = input("Enter URL (or press Enter for blank page): ").strip()
    if not url:
        url = "about:blank"
    
    while True:
        loops_input = input("Number of loops (default: 1): ").strip()
        if not loops_input:
            loops = 1
            break
        try:
            loops = int(loops_input)
            if loops < 1:
                print("Please enter a positive integer for loops.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer for loops.")
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
    parser.add_argument(
        '-r', '--record',
        action='store_true',
        help='Run in recording mode to capture clicks'
    )
    
    args = parser.parse_args()
    
    if args.record:
        run_recording_mode()
    elif args.interactive:
        run_interactive_mode()
    elif args.config:
        run_automation_from_config(args.config, args.headless)
    else:
        # Show help if no arguments provided
        parser.print_help()
        print("\nExample usage:")
        print("  python main.py -c example_config.json")
        print("  python main.py --interactive")
        print("  python main.py --record")
        print("  python main.py -c example_config.json --headless")


if __name__ == "__main__":
    main()