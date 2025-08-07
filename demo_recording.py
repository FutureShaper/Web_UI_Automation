#!/usr/bin/env python3
"""
Demo script showing the click recording functionality
"""
import time
from web_automation import WebAutomation


def demo_recording():
    """Demonstrate the click recording functionality."""
    print("=" * 60)
    print("DEMO: Click Recording Functionality")
    print("=" * 60)
    
    # Create a test page with clickable elements
    demo_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Click Recording Demo</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                padding: 20px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            .container {
                max-width: 600px;
                margin: 0 auto;
                background: rgba(255,255,255,0.1);
                padding: 30px;
                border-radius: 15px;
                backdrop-filter: blur(10px);
            }
            h1 { text-align: center; margin-bottom: 30px; }
            .demo-button { 
                background: linear-gradient(45deg, #ff6b6b, #ee5a52);
                color: white; 
                padding: 15px 30px; 
                border: none; 
                border-radius: 8px; 
                margin: 10px; 
                cursor: pointer; 
                font-size: 16px;
                font-weight: bold;
                transition: all 0.3s ease;
                display: inline-block;
                min-width: 120px;
            }
            .demo-button:hover { 
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.3);
                background: linear-gradient(45deg, #ff5252, #d32f2f);
            }
            .demo-button:active { transform: translateY(0px); }
            .click-area {
                background: rgba(255,255,255,0.2);
                border: 2px dashed #fff;
                border-radius: 10px;
                padding: 20px;
                margin: 20px 0;
                text-align: center;
                min-height: 100px;
            }
            .instruction {
                background: rgba(255,255,255,0.15);
                padding: 15px;
                border-radius: 8px;
                margin: 15px 0;
                border-left: 4px solid #4caf50;
            }
            .counter {
                font-size: 24px;
                font-weight: bold;
                color: #4caf50;
                text-align: center;
                margin: 10px 0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🖱️ Click Recording Demo</h1>
            
            <div class="instruction">
                <strong>Instructions:</strong> When recording starts, click the buttons below in any order. 
                Each click will be recorded with precise coordinates and timing.
            </div>
            
            <div style="text-align: center; margin: 20px 0;">
                <button class="demo-button" onclick="updateCounter('Button 1')">Button 1</button>
                <button class="demo-button" onclick="updateCounter('Button 2')">Button 2</button>
                <button class="demo-button" onclick="updateCounter('Button 3')">Button 3</button>
            </div>
            
            <div class="click-area" onclick="updateCounter('Click Area')">
                <h3>Free Click Area</h3>
                <p>Click anywhere in this area</p>
                <div class="counter" id="clickCounter">Clicks: 0</div>
            </div>
            
            <div style="text-align: center; margin: 20px 0;">
                <button class="demo-button" onclick="updateCounter('Start')">Start Process</button>
                <button class="demo-button" onclick="updateCounter('Submit')">Submit Form</button>
                <button class="demo-button" onclick="updateCounter('Finish')">Finish</button>
            </div>
            
            <div class="instruction">
                <strong>💡 Tip:</strong> Press ESC when you're done recording. The recorded sequence 
                can then be saved and replayed multiple times automatically!
            </div>
        </div>
        
        <script>
            let clickCount = 0;
            function updateCounter(buttonName) {
                clickCount++;
                document.getElementById('clickCounter').textContent = `Clicks: ${clickCount} (Last: ${buttonName})`;
                
                // Add visual feedback
                const elements = document.querySelectorAll('.demo-button, .click-area');
                elements.forEach(el => {
                    el.style.transform = 'scale(0.98)';
                    setTimeout(() => {
                        el.style.transform = '';
                    }, 100);
                });
            }
        </script>
    </body>
    </html>
    """
    
    # Create data URL
    import urllib.parse
    data_url = f"data:text/html;charset=utf-8,{urllib.parse.quote(demo_html)}"
    
    print("Opening demo page with clickable elements...")
    print("This demo will show the recording capabilities.")
    print()
    
    with WebAutomation(headless=True) as automation:  # Use headless for demo
        # Load the demo page
        automation.start_browser(data_url)
        automation.set_window_size(900, 700)
        
        print("Demo page loaded! Here's how recording works:")
        print()
        print("1. Recording mode will start automatically")
        print("2. Click on various buttons and areas in the browser")
        print("3. Each click will show a red dot indicator")
        print("4. After 10 seconds, recording will stop automatically")
        print("5. We'll show you what was recorded")
        print()
        input("Press Enter to start recording...")
        
        # Start recording
        automation.start_recording_mode()
        
        # Auto-generate some demo clicks for demonstration
        time.sleep(2)
        print("Generating some demo clicks...")
        
        # Simulate clicks at button locations
        demo_clicks = [
            (200, 250),  # Button 1 area
            (350, 250),  # Button 2 area
            (500, 250),  # Button 3 area
            (350, 350),  # Click area center
            (200, 450),  # Start button
            (500, 450),  # Finish button
        ]
        
        for i, (x, y) in enumerate(demo_clicks):
            time.sleep(1)
            print(f"  Demo click {i+1} at ({x}, {y})")
            automation.driver.execute_script(f"""
                var event = new MouseEvent('click', {{
                    'view': window,
                    'bubbles': true,
                    'cancelable': true,
                    'clientX': {x},
                    'clientY': {y}
                }});
                document.dispatchEvent(event);
            """)
        
        print("\nDemo clicks completed! Stopping recording...")
        time.sleep(1)
        
        # Stop recording
        recorded_clicks = automation.stop_recording_mode()
        
        print(f"\n✅ Recording completed! Captured {len(recorded_clicks)} clicks:")
        print("-" * 50)
        for i, click in enumerate(recorded_clicks, 1):
            print(f"  {i:2d}. Position ({click['x']:3d}, {click['y']:3d}) - Delay: {click['delay']:.1f}s")
        
        # Create and save sequence
        sequence = automation.create_sequence_from_recorded_clicks("Demo Recording")
        demo_config_file = "/tmp/demo_recorded_sequence.json"
        automation.save_recorded_clicks_to_config(
            demo_config_file, 
            "Demo Click Sequence", 
            loops=2
        )
        
        print(f"\n💾 Sequence saved to: {demo_config_file}")
        
        # Ask if user wants to see playback
        print("\n🎬 Playback demonstration:")
        print("Would you like to see the recorded sequence played back?")
        playback = input("This will replay all recorded clicks automatically (y/N): ").strip().lower()
        
        if playback == 'y':
            print("\n▶️  Playing back recorded sequence...")
            print("Watch the browser - you'll see the clicks being replayed!")
            time.sleep(2)
            
            automation.execute_click_sequence(sequence, loops=1)
            print("✅ Playback completed!")
        
        print("\n" + "=" * 60)
        print("DEMO COMPLETED")
        print("=" * 60)
        print("The click recording feature allows you to:")
        print("• Record real clicks with precise coordinates and timing")
        print("• Save recorded sequences as JSON configuration files")
        print("• Replay sequences with configurable loop counts")
        print("• Use both interactive recording and programmatic automation")
        print()
        print("Try it yourself with: python main.py --record")
        print("=" * 60)


if __name__ == "__main__":
    demo_recording()