# mopad

[![CI](https://github.com/vincentwarmerdam/mopad/actions/workflows/ci.yml/badge.svg)](https://github.com/vincentwarmerdam/mopad/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/mopad.svg)](https://badge.fury.io/py/mopad)

An anywidget that allows gamepad input in Marimo notebooks. Perfect for interactive data exploration, games, or any application that needs real-time gamepad input.

## Features

- 🎮 **Automatic gamepad detection** - No need to press buttons before starting
- 📊 **Real-time visual feedback** - Connection status and button press information  
- ⏱️ **Precise timestamp tracking** - Millisecond-accurate timing for button presses
- 🔗 **Any button support** - Capture input from any gamepad button
- 🔧 **Minimizable interface** - Hide the widget when you don't need the UI
- 🚀 **Zero setup** - Works out of the box in Marimo

## Installation

```bash
pip install mopad
```

## Quick Start

```python
import marimo as mo
from mopad import MopadWidget

# Display it in your notebook
gamepad = mo.ui.anywidget(MopadWidget())
gamepad
```

## Usage

### Basic Example

```python
import marimo as mo
from mopad import MopadWidget

# Create and display the widget
gamepad = mo.ui.anywidget(MopadWidget())
gamepad
```

### Accessing Gamepad Data

The widget provides comprehensive gamepad input tracking:

```python
# Button presses
print(f"Last button: {gamepad.value.last_button_pressed}")
print(f"Current timestamp: {gamepad.value.current_timestamp}")
print(f"Previous timestamp: {gamepad.value.previous_timestamp}")

# D-pad (directional pad)
print(f"D-pad Up: {gamepad.value.dpad_up}")
print(f"D-pad Down: {gamepad.value.dpad_down}")
print(f"D-pad Left: {gamepad.value.dpad_left}")
print(f"D-pad Right: {gamepad.value.dpad_right}")

# Analog sticks (values between -1.0 and 1.0)
axes = gamepad.value.axes
if len(axes) >= 4:
    print(f"Left stick: ({axes[0]:.2f}, {axes[1]:.2f})")
    print(f"Right stick: ({axes[2]:.2f}, {axes[3]:.2f})")

# Calculate time between button presses
if gamepad.value.previous_timestamp > 0:
    time_diff = (gamepad.value.current_timestamp - gamepad.value.previous_timestamp) / 1000
    print(f"Time between presses: {time_diff:.3f} seconds")
```

### Interactive Example

```python
import marimo as mo
from mopad import MopadWidget
import datetime

gamepad = mo.ui.anywidget(MopadWidget())

# React to button presses
if gamepad.value.last_button_pressed >= 0:
    button = gamepad.value.last_button_pressed
    timestamp = datetime.datetime.fromtimestamp(gamepad.value.current_timestamp / 1000)
    
    mo.md(f"""
    ## Last Input
    - **Button:** {button}
    - **Time:** {timestamp.strftime('%H:%M:%S.%f')[:-3]}
    - **Action:** {['Jump', 'Attack', 'Defend', 'Special'][button] if button < 4 else f'Button {button}'}
    """)
else:
    mo.md("Press any button on your gamepad!")
```

## Widget Properties

| Property | Type | Description |
|----------|------|-------------|
| `last_button_pressed` | `int` | Index of the last pressed button (-1 if none) |
| `current_timestamp` | `float` | Timestamp of the most recent button press (ms) |
| `previous_timestamp` | `float` | Timestamp of the previous button press (ms) |
| `axes` | `list[float]` | Analog stick values: [left_x, left_y, right_x, right_y] |
| `dpad_up` | `bool` | True when D-pad up is pressed |
| `dpad_down` | `bool` | True when D-pad down is pressed |
| `dpad_left` | `bool` | True when D-pad left is pressed |
| `dpad_right` | `bool` | True when D-pad right is pressed |
| `button_id` | `int` | Legacy property for backward compatibility |

## Gamepad Setup

1. **Connect your gamepad** to your computer (USB or Bluetooth)
2. **Press any button** on the gamepad to activate it in the browser
3. **Start the widget** - it will automatically detect the connected gamepad

> **Note:** Due to browser security policies, gamepads need user interaction to be detected. The widget will guide you through the connection process with clear visual indicators.

## Widget Interface

The widget provides a clean, informative interface:

- **🟢 Connected status** - Shows when gamepad is detected with device name
- **🔴 Disconnected status** - Provides connection instructions  
- **📝 Button feedback** - Displays which button was pressed
- **🎮 D-pad display** - Shows active directional pad buttons (↑↓←→)
- **🕹️ Analog stick values** - Real-time left/right stick positions
- **⏱️ Timestamp display** - Shows current, previous, and time difference
- **➖/➕ Minimize button** - Hide/show the full interface

## Use Cases

- **Interactive data visualization** - Navigate through datasets with gamepad controls
- **Real-time monitoring** - Use buttons to trigger actions or mark events
- **Game development** - Prototype games directly in notebooks
- **Accessibility** - Alternative input method for users who prefer gamepads
- **Timing experiments** - Precise measurement of reaction times

## Examples

### Rhythm Game Timer
```python
import marimo as mo
from mopad import MopadWidget

gamepad = mo.ui.anywidget(MopadWidget())

# Check timing accuracy
if gamepad.value.previous_timestamp > 0:
    beat_interval = (gamepad.value.current_timestamp - gamepad.value.previous_timestamp) / 1000
    target_bpm = 120  # Target: 120 BPM = 0.5s per beat
    target_interval = 60 / target_bpm
    accuracy = abs(beat_interval - target_interval)
    
    if accuracy < 0.05:  # Within 50ms
        mo.md("🎯 **Perfect timing!**")
    elif accuracy < 0.1:  # Within 100ms  
        mo.md("👍 **Good timing!**")
    else:
        mo.md("⚠️ **Try to keep the beat!**")
```

### Button Mapping
```python
button_actions = {
    0: "🔥 Fire primary weapon",
    1: "🛡️ Activate shield", 
    2: "⚡ Use special ability",
    3: "🏃 Sprint mode"
}

if gamepad.value.last_button_pressed in button_actions:
    action = button_actions[gamepad.value.last_button_pressed]
    mo.md(f"**Action triggered:** {action}")
```

### D-pad Navigation
```python
import marimo as mo
from mopad import MopadWidget

gamepad = mo.ui.anywidget(MopadWidget())

# Create navigation feedback
directions = []
if gamepad.value.dpad_up: directions.append("⬆️ Up")
if gamepad.value.dpad_down: directions.append("⬇️ Down") 
if gamepad.value.dpad_left: directions.append("⬅️ Left")
if gamepad.value.dpad_right: directions.append("➡️ Right")

if directions:
    mo.md(f"**Navigation:** {' + '.join(directions)}")
else:
    mo.md("Use the D-pad to navigate!")
```

### Analog Stick Control
```python
import marimo as mo
from mopad import MopadWidget
import math

gamepad = mo.ui.anywidget(MopadWidget())

# Calculate stick magnitudes and directions
axes = gamepad.value.axes
if len(axes) >= 4:
    left_magnitude = math.sqrt(axes[0]**2 + axes[1]**2)
    right_magnitude = math.sqrt(axes[2]**2 + axes[3]**2)
    
    # Determine if sticks are being used (with deadzone)
    deadzone = 0.1
    left_active = left_magnitude > deadzone
    right_active = right_magnitude > deadzone
    
    if left_active or right_active:
        mo.md(f"""
        **Analog Sticks:**
        - Left: {'🎯 Active' if left_active else '⭕ Idle'} ({left_magnitude:.2f})
        - Right: {'🎯 Active' if right_active else '⭕ Idle'} ({right_magnitude:.2f})
        """)
    else:
        mo.md("Move the analog sticks!")
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.