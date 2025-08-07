# Web UI Automation

A Python-based solution for automating clicks in web browsers using pixel coordinates with configurable delays and looping functionality.

## Features

- 🖱️ **Precise pixel-based clicking** - Click at exact coordinates on web pages
- 📹 **Click recording** - Record actual clicks on the browser to create automation sequences
- ⏱️ **Configurable delays** - Set waiting time between clicks to allow browser response
- 🔄 **Loop sequences** - Repeat click sequences n times
- 🎯 **Multiple interfaces** - Command-line and interactive modes
- 🚀 **Headless support** - Run automation with or without visible browser
- 📁 **Configuration files** - Define click sequences in JSON format

## Installation

1. Clone the repository:
```bash
git clone https://github.com/FutureShaper/Web_UI_Automation.git
cd Web_UI_Automation
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Recording Mode (NEW!)

Record actual clicks on a webpage to create automation sequences:

```bash
python main.py --record
```

This will:
1. Open a browser with your specified URL
2. Show a recording indicator
3. Capture clicks as you perform them (with visual feedback)
4. Allow you to save the recorded sequence as a JSON config file
5. Optionally run the recorded sequence immediately

### Command Line with Configuration File

Create a JSON configuration file (see `example_config.json`) and run:

```bash
python main.py -c example_config.json
```

Run in headless mode:
```bash
python main.py -c example_config.json --headless
```

### Interactive Mode

Run the automation in interactive mode to define clicks on-the-fly:

```bash
python main.py --interactive
```

### Recording Mode

Record clicks directly on a webpage:

```bash
python main.py --record
```

### Configuration File Format

```json
{
  "name": "Example Click Sequence",
  "loops": 3,
  "url": "https://example.com",
  "window_size": {
    "width": 1024,
    "height": 768
  },
  "clicks": [
    {
      "x": 100,
      "y": 200,
      "delay": 1.5
    },
    {
      "x": 300,
      "y": 400,
      "delay": 2.0
    }
  ]
}
```

### Programmatic Usage

```python
from web_automation import WebAutomation
from click_sequence import ClickSequence

# Option 1: Create a click sequence manually
sequence = ClickSequence("My Automation")
sequence.add_click(100, 200, 1.0)  # x, y, delay
sequence.add_click(300, 400, 1.5)

# Option 2: Record clicks and create sequence
with WebAutomation(headless=False) as automation:
    automation.start_browser("https://example.com")
    automation.start_recording_mode()
    # ... user clicks on browser ...
    recorded_clicks = automation.stop_recording_mode()
    sequence = automation.create_sequence_from_recorded_clicks("Recorded Sequence")

# Run automation
with WebAutomation(headless=False) as automation:
    automation.start_browser("https://example.com")
    automation.execute_click_sequence(sequence, loops=3)
```

## Files

- `main.py` - Command-line interface
- `web_automation.py` - Main automation class using Selenium WebDriver
- `click_sequence.py` - Click sequence management
- `example_config.json` - Example configuration file
- `test_automation.py` - Basic test script
- `requirements.txt` - Python dependencies

## Requirements

- Python 3.6+
- Chrome browser (ChromeDriver managed automatically)
- Internet connection for initial ChromeDriver download

## License

This project is open source. Feel free to use and modify as needed.
