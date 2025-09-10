#!/usr/bin/env python3
"""
Simple UI test for Pointer Activity Monitoring Service
This script tests if the UI appears correctly without mouse tracking
"""

import tkinter as tk
from tkinter import ttk
import screeninfo

def test_ui():
    # Get screen dimensions
    screens = screeninfo.get_monitors()
    screen_width = max(screen.x + screen.width for screen in screens)
    
    # Create root window
    root = tk.Tk()
    root.title("Pointer Monitor - UI Test")
    root.geometry("180x120")
    root.resizable(False, False)
    
    # Position window at center of the screen for better visibility  
    screen_height = max(screen.y + screen.height for screen in screens)
    center_x = (screen_width - 180) // 2  # Horizontally centered
    center_y = (screen_height - 120) // 4  # Upper-center vertically
    root.geometry(f"180x120+{center_x}+{center_y}")
    
    # Make window always on top
    root.attributes('-topmost', True)
    
    # Configure style
    style = ttk.Style()
    style.theme_use('clam')
    
    # Create main frame
    main_frame = ttk.Frame(root, padding="10")
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Status label
    status_label = ttk.Label(main_frame, text="UI Test - Ready", foreground="green")
    status_label.pack(pady=(0, 10))
    
    # Test buttons
    start_btn = ttk.Button(main_frame, text="Start", width=15)
    start_btn.pack(pady=2)
    
    stop_btn = ttk.Button(main_frame, text="Stop", width=15, state=tk.DISABLED)
    stop_btn.pack(pady=2)
    
    visualize_btn = ttk.Button(main_frame, text="👁 Visualize", width=15)
    visualize_btn.pack(pady=2)
    
    print("UI should now be visible in the top-right corner!")
    print("Close the window to continue...")
    
    # Run the GUI
    root.mainloop()
    
    print("UI test completed!")

if __name__ == "__main__":
    print("Testing UI components...")
    test_ui()
