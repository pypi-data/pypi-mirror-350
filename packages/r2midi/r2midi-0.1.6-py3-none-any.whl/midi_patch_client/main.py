#!/usr/bin/env python3
import sys
import argparse
from PyQt6.QtWidgets import QApplication

from midi_patch_client.ui.main_window import MainWindow

def parse_args():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(description="MIDI Patch Selection Client")
    parser.add_argument(
        "--server-url", 
        default="http://localhost:7777",
        help="URL of the MIDI Patch Selection server (default: http://localhost:7777)"
    )
    return parser.parse_args()

def main():
    """Main entry point for the application"""
    # Parse command-line arguments
    args = parse_args()

    # Create the Qt application
    app = QApplication(sys.argv)
    app.setApplicationName("MIDI Patch Selection")

    # Create and show the main window
    window = MainWindow(server_url=args.server_url)
    window.show()

    # Start the application event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
