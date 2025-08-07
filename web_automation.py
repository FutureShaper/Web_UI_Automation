"""
Web UI Automation - Main automation class for browser control and click automation.
Provides functionality to automate clicks using pixel coordinates with configurable delays.
"""
import time
import json
from typing import Optional, List, Dict, Union
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from click_sequence import ClickSequence, ClickAction


class WebAutomation:
    """Main automation class for web browser control and click automation."""
    
    _driver_path = None  # Class attribute to cache ChromeDriver path
    
    def __init__(self, headless: bool = False):
        self.driver: Optional[webdriver.Chrome] = None
        self.headless = headless
        self.action_chains: Optional[ActionChains] = None
        self.recorded_clicks: List[Dict[str, Union[int, float]]] = []
        self.recording_mode: bool = False
    
    def start_browser(self, url: str = "about:blank"):
        """Initialize and start the web browser."""
        if self.driver:
            self.stop_browser()
        
        # Setup Chrome options
        options = Options()
        if self.headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument(f'--user-data-dir=/tmp/chrome_user_data_{int(time.time() * 1000000)}_{id(self)}')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Setup Chrome driver
        if WebAutomation._driver_path is None:
            try:
                # Try to use system ChromeDriver first
                import shutil
                system_chromedriver = shutil.which('chromedriver')
                if system_chromedriver:
                    WebAutomation._driver_path = system_chromedriver
                else:
                    WebAutomation._driver_path = ChromeDriverManager().install()
            except ImportError:
                # Fallback to ChromeDriverManager if system driver not available
                WebAutomation._driver_path = ChromeDriverManager().install()
        service = Service(WebAutomation._driver_path)
        self.driver = webdriver.Chrome(service=service, options=options)
        self.action_chains = ActionChains(self.driver)
        
        # Navigate to URL
        if url != "about:blank":
            self.driver.get(url)
        
        return self
    
    def stop_browser(self):
        """Close the web browser and cleanup resources."""
        if self.driver:
            self.driver.quit()
            self.driver = None
            self.action_chains = None
    
    def navigate_to(self, url: str):
        """Navigate to a specific URL."""
        if not self.driver:
            raise RuntimeError("Browser not started. Call start_browser() first.")
        self.driver.get(url)
        return self
    
    def click_at_coordinates(self, x: int, y: int, delay: float = 1.0):
        """Click at specific pixel coordinates (relative to top-left of the viewport)."""
        if not self.driver or not self.action_chains:
            raise RuntimeError("Browser not started. Call start_browser() first.")
        
        # Execute JavaScript to click at absolute coordinates
        # This is more reliable than ActionChains for absolute positioning
        self.driver.execute_script(f"""
            var event = new MouseEvent('click', {{
                'view': window,
                'bubbles': true,
                'cancelable': true,
                'clientX': {x},
                'clientY': {y}
            }});
            var element = document.elementFromPoint({x}, {y});
            if (element) element.dispatchEvent(event);
        """)
        
        # Wait for the specified delay
        if delay > 0:
            time.sleep(delay)
        
        return self
    
    def execute_click_sequence(self, sequence: ClickSequence, loops: int = 1):
        """Execute a click sequence for the specified number of loops."""
        if not self.driver:
            raise RuntimeError("Browser not started. Call start_browser() first.")
        
        if not sequence.actions:
            print("Warning: No actions in sequence to execute")
            return self
        
        print(f"Executing sequence '{sequence.name}' {loops} time(s)")
        print(f"Sequence contains {len(sequence.actions)} actions")
        
        for loop in range(loops):
            print(f"Loop {loop + 1}/{loops}")
            
            for i, action in enumerate(sequence.actions):
                print(f"  Action {i + 1}: Click at ({action.x}, {action.y})")
                self.click_at_coordinates(action.x, action.y, action.delay)
        
        print("Sequence execution completed")
        return self
    
    def wait(self, seconds: float):
        """Wait for a specified number of seconds."""
        time.sleep(seconds)
        return self
    
    def get_window_size(self):
        """Get the current window size."""
        if not self.driver:
            raise RuntimeError("Browser not started. Call start_browser() first.")
        return self.driver.get_window_size()
    
    def set_window_size(self, width: int, height: int):
        """Set the browser window size."""
        if not self.driver:
            raise RuntimeError("Browser not started. Call start_browser() first.")
        self.driver.set_window_size(width, height)
        return self
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def start_recording_mode(self):
        """Start recording mode to capture clicks."""
        if not self.driver:
            raise RuntimeError("Browser not started. Call start_browser() first.")
        
        self.recording_mode = True
        self.recorded_clicks.clear()
        
        # Inject JavaScript to capture click events
        self.driver.execute_script("""
            // Store reference to automation object for access from click handler
            window.clickRecorder = {
                recordedClicks: [],
                recording: true
            };
            
            // Function to handle click events
            function recordClick(event) {
                if (window.clickRecorder.recording) {
                    const click = {
                        x: event.clientX,
                        y: event.clientY,
                        timestamp: Date.now()
                    };
                    window.clickRecorder.recordedClicks.push(click);
                    
                    // Visual feedback for recorded click
                    const marker = document.createElement('div');
                    marker.style.position = 'fixed';
                    marker.style.left = event.clientX + 'px';
                    marker.style.top = event.clientY + 'px';
                    marker.style.width = '10px';
                    marker.style.height = '10px';
                    marker.style.backgroundColor = 'red';
                    marker.style.borderRadius = '50%';
                    marker.style.pointerEvents = 'none';
                    marker.style.zIndex = '9999';
                    marker.style.transform = 'translate(-50%, -50%)';
                    document.body.appendChild(marker);
                    
                    // Remove marker after 1 second
                    setTimeout(() => {
                        if (marker.parentNode) {
                            marker.parentNode.removeChild(marker);
                        }
                    }, 1000);
                    
                    console.log('Recorded click at:', event.clientX, event.clientY);
                }
            }
            
            // Add click event listener
            document.addEventListener('click', recordClick, true);
            
            // Show recording indicator
            const indicator = document.createElement('div');
            indicator.id = 'recordingIndicator';
            indicator.innerHTML = '🔴 RECORDING CLICKS - Press ESC to stop';
            indicator.style.position = 'fixed';
            indicator.style.top = '10px';
            indicator.style.left = '50%';
            indicator.style.transform = 'translateX(-50%)';
            indicator.style.backgroundColor = 'rgba(255, 0, 0, 0.8)';
            indicator.style.color = 'white';
            indicator.style.padding = '10px 20px';
            indicator.style.borderRadius = '5px';
            indicator.style.fontFamily = 'Arial, sans-serif';
            indicator.style.fontSize = '14px';
            indicator.style.zIndex = '10000';
            indicator.style.fontWeight = 'bold';
            document.body.appendChild(indicator);
            
            // Add ESC key listener to stop recording
            function stopRecordingOnEsc(event) {
                if (event.key === 'Escape') {
                    window.clickRecorder.recording = false;
                    const indicator = document.getElementById('recordingIndicator');
                    if (indicator) {
                        indicator.innerHTML = '⏹️ RECORDING STOPPED - Close this tab to continue';
                        indicator.style.backgroundColor = 'rgba(0, 150, 0, 0.8)';
                    }
                    document.removeEventListener('keydown', stopRecordingOnEsc);
                    document.removeEventListener('click', recordClick, true);
                }
            }
            document.addEventListener('keydown', stopRecordingOnEsc);
        """)
        
        print("Recording mode started! Click anywhere on the page to record clicks.")
        print("Press ESC key to stop recording.")
        return self
    
    def stop_recording_mode(self):
        """Stop recording mode and retrieve recorded clicks."""
        if not self.driver:
            raise RuntimeError("Browser not started.")
        
        # Stop recording and get recorded clicks
        recorded_data = self.driver.execute_script("""
            if (window.clickRecorder) {
                window.clickRecorder.recording = false;
                return window.clickRecorder.recordedClicks;
            }
            return [];
        """)
        
        self.recording_mode = False
        
        # Convert recorded clicks and calculate delays
        if recorded_data:
            for i, click in enumerate(recorded_data):
                # Calculate delay as time since previous click (default 1.0s for first click)
                if i == 0:
                    delay = 1.0
                else:
                    time_diff = (click['timestamp'] - recorded_data[i-1]['timestamp']) / 1000.0
                    delay = max(0.1, min(time_diff, 10.0))  # Clamp between 0.1s and 10s
                
                self.recorded_clicks.append({
                    'x': click['x'],
                    'y': click['y'],
                    'delay': delay
                })
        
        print(f"Recording stopped. Captured {len(self.recorded_clicks)} clicks.")
        return self.recorded_clicks
    
    def get_recorded_clicks(self):
        """Get the list of recorded clicks."""
        return self.recorded_clicks.copy()
    
    def create_sequence_from_recorded_clicks(self, name: str = "Recorded Sequence"):
        """Create a ClickSequence from recorded clicks."""
        sequence = ClickSequence(name)
        sequence.add_clicks(self.recorded_clicks)
        return sequence
    
    def save_recorded_clicks_to_config(self, filename: str, name: str = "Recorded Sequence", 
                                      loops: int = 1, url: str = None):
        """Save recorded clicks to a JSON configuration file."""
        if not self.recorded_clicks:
            raise ValueError("No clicks recorded. Use start_recording_mode() first.")
        
        current_url = url or (self.driver.current_url if self.driver else "about:blank")
        window_size = self.get_window_size() if self.driver else {"width": 1024, "height": 768}
        
        config = {
            "name": name,
            "loops": loops,
            "url": current_url,
            "window_size": window_size,
            "clicks": self.recorded_clicks
        }
        
        with open(filename, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"Recorded clicks saved to {filename}")
        return filename
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - cleanup browser."""
        self.stop_browser()