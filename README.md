# Iliya's Clipboard Manager

A lightweight desktop application for managing clipboard history and easily accessing previously copied text.

## Features
- 📋 Store up to 50 clipboard items automatically
- 🔍 Search through clipboard history
- 🖱️ Double-click to copy items back to clipboard
- 🗑️ Delete individual items or clear entire history
- 💾 Persistent storage between sessions
- 🎨 Modern UI with ttkbootstrap themes

## Installation

### Prerequisites
- Python 3.7+
- pip package manager

### Steps
1. Clone the repository:
```bash
   git clone https://github.com/yourusername/clipboard-manager.git
   cd clipboard-manager
```
2.Install required packages:
```bash
    pip install ttkbootstrap
```
3.Run the application:
```bash
    python main.py
```
Usage:
    1.Add Clipboard Item:
    Click "Add Clipboard" button or use keyboard shortcut to save current clipboard content. 
    2.Search History:
    Type in the search box to filter clipboard items.
    3.Copy Item Back:
    Double-click any item in the list or select and click "Copy Selected". 
    4.Manage Items:
    Use "Delete" to remove individual items or "Clear All" to reset history.
Configuration:
Customize the following settings at the top of main.py:
     MAX_ITEMS: Maximum number of clipboard items to store (default: 50)
     DATA_FILE: Location of the storage file (default: ~/.clipboard_manager.json)
     APP_NAME: Application name displayed in window title
Contributing:
Contributions are welcome! Feel free to submit issues or pull requests. 

Built with ❤️ using Python, Tkinter, and ttkbootstrap 
