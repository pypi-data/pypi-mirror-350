# UI Explorer MCP Server

An MCP server that provides tools for exploring and interacting with UI elements on your screen.

## Features

- Explore UI hierarchies: Scan and analyze all UI elements on your screen
- Screenshot UI with highlights: Visualize UI elements with boundaries and hierarchy
- Control mouse clicks: Click on UI elements based on coordinates
- Explore specific regions: Focus on parts of the screen like top-left, center, etc.

## Installation Options

### Option 1: Using pip (recommended)

Install the package globally or in a virtual environment:

```bash
pip install mcp-ui-explorer
```

### Option 2: Using git clone

1. Clone the repository:
```bash
git clone https://github.com/modularflow/mcp-ui-explorer
cd mcp-ui-explorer
```

2. Install the package:
   - Using pip in development mode:
   ```bash
   pip install -e .
   ```
   
   - OR using uv (recommended for development):
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install -e .
   ```

## MCP Server Configuration

After installing the package, you need to configure your MCP client to use the UI Explorer server.

### For Roo in Cursor

Add this JSON to your MCP Server config at: 
`C:\Users\<user_name>\AppData\Roaming\Cursor\User\globalStorage\rooveterinaryinc.roo-cline\settings\mcp_settings.json`

```json
{
  "mcpServers": {
    "ui-explorer": {
      "command": "uvx",
      "args": [
        "mcp-ui-explorer"
      ]
    }
  }
}
```

### For Claude Desktop App

Add the server configuration to:
`C:\Users\<user_name>\AppData\Roaming\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "ui-explorer": {
      "command": "uvx",
      "args": [
        "mcp-ui-explorer"
      ]
    }
  }
}
```

### For Direct Use with uvx

If you've installed the package (either globally or in a virtual environment), you can directly use `uvx` to run the server without additional configuration:

```bash
uvx mcp-ui-explorer
```

## Command Line Tools

Besides the MCP server functionality, UI Explorer also provides standalone command line tools for exploring UI elements and automating interactions.

### UI Hierarchy Explorer

Explore UI elements on your screen and export them to JSON/XML files with visualization:

```bash
python -m mcp_ui_explorer.hierarchical_ui_explorer [options]
```

Options:
- `--output PREFIX`: Output filename prefix (default: "ui_hierarchy")
- `--region REGION`: Region to analyze ("screen", "top", "bottom", "left", "right", "center", etc. or custom "left,top,right,bottom" coordinates)
- `--depth DEPTH`: Maximum hierarchy depth to analyze (default: 5)
- `--min-size SIZE`: Minimum element size to include (default: 5px)
- `--focus-window`: Only analyze the foreground window
- `--highlight-levels`: Use different colors for hierarchy levels
- `--format {json,xml,both}`: Output format (default: json)
- `--visible-only`: Only include elements visible on screen
- `--control-type TYPE`: Only include elements of this control type (default: Button)
- `--text TEXT`: Only include elements containing this text

Example:
```bash
python -m mcp_ui_explorer.hierarchical_ui_explorer --region "screen" --control-type "Button" --highlight-levels
```

### UI Element Clicker

Click on UI elements from a previously exported JSON hierarchy:

```bash
python -m mcp_ui_explorer.ui_hierarchy_click [options]
```

Options:
- `--json FILE`: Path to JSON hierarchy file
- `--type TYPE`: Control type to search for (default: Button)
- `--text TEXT`: Text content to search for
- `--wait SECONDS`: Seconds to wait before clicking (default: 2)
- `--path PATH`: Path to element (e.g., 0.children.3.children.2)

Example:
```bash
python -m mcp_ui_explorer.ui_hierarchy_click --json "ui_hierarchy_20240501_123456.json" --type "Button" --text "Submit"
```

**Note**: When you run the UI Hierarchy Explorer, it automatically generates a helper script for clicking elements from the exported hierarchy. This script is named `{output_prefix}_click.py` and can be used directly.

## Usage Guide

### 1. Explore UI Structure

Use the `explore_ui` tool to get a complete hierarchy of UI elements:

Parameters:
- `region`: Screen region to analyze ("screen", "top", "bottom", "left", "right", "center", etc.)
- `depth`: Maximum hierarchy depth to analyze (default: 5)
- `min_size`: Minimum element size to include (default: 5px)
- `focus_window`: Only analyze the foreground window (default: False)
- `visible_only`: Only include elements visible on screen (default: True)
- `control_type`: Type of control to search for (default: "Button")
- `text`: Filter elements by text content (optional)

### 2. Take a Screenshot with UI Elements Highlighted

Use the `screenshot_ui` tool to visualize the UI elements:

Parameters:
- `region`: Screen region to analyze
- `highlight_levels`: Use different colors for hierarchy levels (default: True)
- `output_prefix`: Prefix for output files (default: "ui_hierarchy")

### 3. Click at Screen Coordinates

Use the `click_ui_element` tool to click at specific coordinates:

Parameters:
- `x`: X coordinate to click (required)
- `y`: Y coordinate to click (required)
- `wait_time`: Seconds to wait before clicking (default: 2.0)

### 4. Keyboard Input and Shortcuts

The tool also provides options for keyboard input and shortcuts. See the UI Explorer guide in the MCP interface for details.

## Example Workflow

1. First, explore the UI to understand what's on the screen:
   ```
   explore_ui(region="screen", control_type="Button")
   ```

2. Take a screenshot to visualize the elements:
   ```
   screenshot_ui(region="screen")
   ```

3. Note the coordinates of elements you want to click, then click at those coordinates:
   ```
   click_ui_element(x=500, y=300)
   ```

4. Type text or use keyboard shortcuts as needed:
   ```
   keyboard_input(text="Hello world", press_enter=true)
   ```

## Requirements

- Windows operating system
- Python 3.10+
- MCP 1.6.0+
- PyAutoGUI
- PyWinAuto
- Pillow
- Pydantic 2.0+
