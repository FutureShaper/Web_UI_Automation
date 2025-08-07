"""
Web UI Automation - Main automation class for browser control and click automation.
Provides functionality to automate clicks using pixel coordinates with configurable delays.
"""
import time
from typing import Optional
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
        
        # Move to coordinates and click using absolute offset from the top-left of the viewport
        # Move to coordinates and click using offset from the current mouse position
        self.action_chains.move_by_offset(x, y).click().perform()
        
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
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - cleanup browser."""
        self.stop_browser()