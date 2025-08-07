#!/usr/bin/env python3
"""
Screenshot demo of recording functionality
"""
import time
from web_automation import WebAutomation


def take_demo_screenshot():
    """Take a screenshot of the demo recording interface."""
    # Create a demo HTML page
    demo_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Click Recording Demo - Screenshot</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                padding: 20px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                margin: 0;
            }
            .container {
                max-width: 600px;
                margin: 0 auto;
                background: rgba(255,255,255,0.1);
                padding: 30px;
                border-radius: 15px;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255,255,255,0.2);
            }
            h1 { 
                text-align: center; 
                margin-bottom: 30px; 
                color: #fff;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
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
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            }
            .demo-button:hover { 
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(0,0,0,0.3);
            }
            .click-area {
                background: rgba(255,255,255,0.2);
                border: 2px dashed #fff;
                border-radius: 10px;
                padding: 20px;
                margin: 20px 0;
                text-align: center;
                min-height: 80px;
                cursor: pointer;
            }
            .instruction {
                background: rgba(255,255,255,0.15);
                padding: 15px;
                border-radius: 8px;
                margin: 15px 0;
                border-left: 4px solid #4caf50;
            }
            .recording-indicator {
                position: fixed;
                top: 20px;
                left: 50%;
                transform: translateX(-50%);
                background: rgba(255, 0, 0, 0.9);
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                font-family: Arial, sans-serif;
                font-size: 14px;
                z-index: 10000;
                font-weight: bold;
                box-shadow: 0 4px 15px rgba(0,0,0,0.3);
                animation: pulse 2s infinite;
            }
            @keyframes pulse {
                0% { opacity: 1; }
                50% { opacity: 0.7; }
                100% { opacity: 1; }
            }
            .click-marker {
                position: fixed;
                width: 10px;
                height: 10px;
                background-color: red;
                border-radius: 50%;
                pointer-events: none;
                z-index: 9999;
                transform: translate(-50%, -50%);
                animation: fadeOut 1s ease-out forwards;
            }
            @keyframes fadeOut {
                0% { opacity: 1; transform: translate(-50%, -50%) scale(1); }
                100% { opacity: 0; transform: translate(-50%, -50%) scale(2); }
            }
            .features {
                background: rgba(255,255,255,0.1);
                padding: 20px;
                border-radius: 10px;
                margin: 20px 0;
            }
            .feature-item {
                margin: 10px 0;
                padding: 5px 0;
            }
        </style>
    </head>
    <body>
        <div class="recording-indicator">
            🔴 RECORDING CLICKS - Press ESC to stop
        </div>
        
        <div class="container">
            <h1>🖱️ Click Recording Demo</h1>
            
            <div class="instruction">
                <strong>Instructions:</strong> This demonstrates the new click recording feature. 
                Click any button or area below to record precise coordinates and timing.
            </div>
            
            <div style="text-align: center; margin: 20px 0;">
                <button class="demo-button">Button 1</button>
                <button class="demo-button">Button 2</button>
                <button class="demo-button">Button 3</button>
            </div>
            
            <div class="click-area">
                <h3>📍 Free Click Area</h3>
                <p>Click anywhere in this area to test coordinate capture</p>
            </div>
            
            <div style="text-align: center; margin: 20px 0;">
                <button class="demo-button">Start Process</button>
                <button class="demo-button">Submit Form</button>
                <button class="demo-button">Finish</button>
            </div>
            
            <div class="features">
                <h3>✨ Features</h3>
                <div class="feature-item">📹 Record actual clicks with pixel-perfect accuracy</div>
                <div class="feature-item">⏱️ Automatic timing detection between clicks</div>
                <div class="feature-item">💾 Save recordings as JSON configuration files</div>
                <div class="feature-item">🔄 Replay recordings with configurable loop counts</div>
                <div class="feature-item">🎯 Visual feedback with red dot indicators</div>
            </div>
            
            <div class="instruction">
                <strong>💡 Usage:</strong> 
                Run <code>python main.py --record</code> to start recording your own click sequences!
            </div>
        </div>
        
        <!-- Add some click markers for visual effect -->
        <div class="click-marker" style="left: 250px; top: 200px;"></div>
        <div class="click-marker" style="left: 400px; top: 150px; animation-delay: 0.5s;"></div>
        <div class="click-marker" style="left: 350px; top: 300px; animation-delay: 1s;"></div>
    </body>
    </html>
    """
    
    import urllib.parse
    data_url = f"data:text/html;charset=utf-8,{urllib.parse.quote(demo_html)}"
    
    with WebAutomation(headless=False) as automation:
        automation.start_browser(data_url)
        automation.set_window_size(900, 800)
        time.sleep(3)  # Let the page fully load and animations start
        
        # Take screenshot
        automation.driver.save_screenshot("/home/runner/work/Web_UI_Automation/Web_UI_Automation/demo_screenshot.png")
        print("Screenshot saved to demo_screenshot.png")


if __name__ == "__main__":
    take_demo_screenshot()