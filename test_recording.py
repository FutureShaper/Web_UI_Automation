#!/usr/bin/env python3
"""
Test script for click recording functionality
"""
import time
import json
import os
from web_automation import WebAutomation
from click_sequence import ClickSequence


def test_recording_functionality():
    """Test the click recording functionality."""
    print("Testing Click Recording Functionality...")
    
    try:
        # Test with a simple HTML page that has clickable elements
        test_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test Page for Click Recording</title>
            <style>
                body { font-family: Arial, sans-serif; padding: 20px; }
                .button { 
                    background: #007cba; 
                    color: white; 
                    padding: 10px 20px; 
                    border: none; 
                    border-radius: 5px; 
                    margin: 10px; 
                    cursor: pointer; 
                    display: inline-block;
                }
                .button:hover { background: #005a8b; }
                .test-area {
                    width: 300px;
                    height: 200px;
                    border: 2px solid #ccc;
                    margin: 20px 0;
                    padding: 20px;
                    background: #f9f9f9;
                }
            </style>
        </head>
        <body>
            <h1>Click Recording Test Page</h1>
            <p>This page is used to test click recording functionality.</p>
            
            <div class="button" onclick="alert('Button 1 clicked!')">Button 1</div>
            <div class="button" onclick="alert('Button 2 clicked!')">Button 2</div>
            <div class="button" onclick="alert('Button 3 clicked!')">Button 3</div>
            
            <div class="test-area">
                <h3>Test Area</h3>
                <p>Click anywhere in this area to test coordinate recording.</p>
                <p>Current coordinates will be captured precisely.</p>
            </div>
            
            <div class="button" onclick="alert('Bottom button clicked!')">Bottom Button</div>
        </body>
        </html>
        """
        
        data_url = f"data:text/html;charset=utf-8,{test_html}"
        
        # Test recording mode
        with WebAutomation(headless=True) as automation:  # Use headless to avoid conflicts
            print("Starting browser with test page...")
            automation.start_browser(data_url)
            automation.set_window_size(800, 600)
            
            print("Starting recording mode...")
            automation.start_recording_mode()
            
            # Simulate some clicks programmatically for testing
            print("Simulating clicks for testing...")
            time.sleep(1)
            
            # Simulate clicks at known coordinates
            automation.driver.execute_script("""
                // Simulate clicks for testing
                function simulateClick(x, y) {
                    const event = new MouseEvent('click', {
                        'view': window,
                        'bubbles': true,
                        'cancelable': true,
                        'clientX': x,
                        'clientY': y
                    });
                    document.dispatchEvent(event);
                }
                
                // Simulate a sequence of clicks with delays
                setTimeout(() => simulateClick(100, 150), 500);
                setTimeout(() => simulateClick(200, 250), 1000);
                setTimeout(() => simulateClick(150, 200), 1500);
                
                // Stop recording after simulated clicks
                setTimeout(() => {
                    window.clickRecorder.recording = false;
                    const indicator = document.getElementById('recordingIndicator');
                    if (indicator) {
                        indicator.innerHTML = '⏹️ RECORDING STOPPED (TEST MODE)';
                        indicator.style.backgroundColor = 'rgba(0, 150, 0, 0.8)';
                    }
                }, 2000);
            """)
            
            # Wait for simulated clicks to complete
            time.sleep(3)
            
            # Stop recording and get results
            recorded_clicks = automation.stop_recording_mode()
            
            if recorded_clicks:
                print(f"✓ Recording successful! Captured {len(recorded_clicks)} clicks:")
                for i, click in enumerate(recorded_clicks, 1):
                    print(f"  {i}. Click at ({click['x']}, {click['y']}) with {click['delay']:.1f}s delay")
                
                # Test creating sequence from recorded clicks
                sequence = automation.create_sequence_from_recorded_clicks("Test Recorded Sequence")
                print(f"✓ Created sequence: {sequence}")
                
                # Test saving to config file
                test_config_file = "/tmp/test_recorded_config.json"
                automation.save_recorded_clicks_to_config(
                    test_config_file, 
                    "Test Recording", 
                    loops=2,
                    url=data_url
                )
                
                # Verify the saved file
                if os.path.exists(test_config_file):
                    with open(test_config_file, 'r') as f:
                        saved_config = json.load(f)
                    print(f"✓ Config file saved successfully with {len(saved_config['clicks'])} clicks")
                    print(f"  Config name: {saved_config['name']}")
                    print(f"  Loops: {saved_config['loops']}")
                    
                    # Clean up test file
                    os.remove(test_config_file)
                else:
                    print("✗ Failed to save config file")
                    return False
                
                # Test playback of recorded sequence (brief test)
                print("Testing playback of recorded sequence...")
                automation.execute_click_sequence(sequence, loops=1)
                print("✓ Playback test completed")
                
                return True
            else:
                print("✗ No clicks were recorded")
                return False
                
    except Exception as e:
        print(f"✗ Error during recording test: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_help_and_arguments():
    """Test that the new recording argument is available."""
    print("\nTesting command-line arguments...")
    
    import subprocess
    import sys
    
    try:
        # Test help output includes recording option
        result = subprocess.run([sys.executable, "main.py", "--help"], 
                              capture_output=True, text=True, timeout=10)
        
        if "--record" in result.stdout and "recording mode" in result.stdout:
            print("✓ Recording argument available in help")
            return True
        else:
            print("✗ Recording argument not found in help output")
            print("Help output:", result.stdout)
            return False
            
    except Exception as e:
        print(f"✗ Error testing command-line arguments: {e}")
        return False


if __name__ == "__main__":
    print("=" * 50)
    print("Testing Click Recording Feature")
    print("=" * 50)
    
    # Test 1: Basic recording functionality
    test1_passed = test_recording_functionality()
    
    # Test 2: Command-line arguments
    test2_passed = test_help_and_arguments()
    
    print("\n" + "=" * 50)
    print("Test Results:")
    print(f"Recording functionality: {'PASS' if test1_passed else 'FAIL'}")
    print(f"Command-line arguments: {'PASS' if test2_passed else 'FAIL'}")
    
    all_passed = test1_passed and test2_passed
    print(f"Overall: {'ALL TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}")
    print("=" * 50)
    
    exit(0 if all_passed else 1)