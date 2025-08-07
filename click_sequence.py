"""
Click sequence management for web UI automation.
Handles sequences of clicks with pixel coordinates and timing.
"""
import time
from typing import List, Dict, Any, Union


class ClickAction:
    """Represents a single click action with coordinates and optional delay."""
    
    def __init__(self, x: Union[int, float], y: Union[int, float], delay: float = 1.0):
        self.x = x
        self.y = y
        self.delay = delay
    
    def __repr__(self):
        return f"ClickAction(x={self.x}, y={self.y}, delay={self.delay})"


class ClickSequence:
    """Manages a sequence of click actions that can be executed repeatedly."""
    
    def __init__(self, name: str = "Unnamed Sequence"):
        self.name = name
        self.actions: List[ClickAction] = []
    
    def add_click(self, x: int, y: int, delay: float = 1.0):
        """Add a click action to the sequence."""
        action = ClickAction(x, y, delay)
        self.actions.append(action)
        return self
    
    def add_clicks(self, clicks: List[Dict[str, Any]]):
        """Add multiple clicks from a list of dictionaries."""
        for click in clicks:
            if 'x' not in click or 'y' not in click:
                raise ValueError("Each click dictionary must contain 'x' and 'y' keys.")
            x = click['x']
            y = click['y']
            delay = click.get('delay', 1.0)
            self.add_click(x, y, delay)
        return self
    
    def clear(self):
        """Clear all actions from the sequence."""
        self.actions.clear()
    
    def __len__(self):
        return len(self.actions)
    
    def __repr__(self):
        return f"ClickSequence(name='{self.name}', actions={len(self.actions)})"