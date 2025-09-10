#!/usr/bin/env python3
"""
Simple launcher script for Pointer Activity Monitoring Service
Created by: Prof. Shahab Anbarjafari from 3S Holding OÜ, Tartu Estonia

This script provides an easy way to launch the pointer monitoring service
with error handling and user-friendly messages.
"""

import sys
import os

def check_dependencies():
    """Check if all required dependencies are installed"""
    missing_deps = []
    
    try:
        import pynput
    except ImportError:
        missing_deps.append("pynput")
    
    try:
        import matplotlib
    except ImportError:
        missing_deps.append("matplotlib")
    
    try:
        import seaborn
    except ImportError:
        missing_deps.append("seaborn")
    
    try:
        import numpy
    except ImportError:
        missing_deps.append("numpy")
    
    try:
        import screeninfo
    except ImportError:
        missing_deps.append("screeninfo")
    
    return missing_deps

def main():
    """Main launcher function"""
    print("=" * 60)
    print("Pointer Activity Monitoring Service")
    print("Created by: Prof. Shahab Anbarjafari from 3S Holding OÜ")
    print("=" * 60)
    
    # Check dependencies
    missing = check_dependencies()
    if missing:
        print(f"\n❌ Missing dependencies: {', '.join(missing)}")
        print("\nPlease install dependencies using:")
        print("pip install -r requirements.txt")
        print("\nOr install individual packages:")
        for dep in missing:
            print(f"pip install {dep}")
        return 1
    
    print("✅ All dependencies found")
    print("\nStarting Pointer Activity Monitor...")
    print("A small control panel will appear in the top-right corner of your screen.")
    print("\nControls:")
    print("• Start: Begin monitoring mouse movements")
    print("• Stop: Stop monitoring and save data")
    print("• 👁 Visualize: Show heatmap of pointer activity")
    print("\nPress Ctrl+C to exit\n")
    
    try:
        # Import and run the main application
        from pointer_monitor import main as run_monitor
        run_monitor()
    except ImportError as e:
        print(f"❌ Error: Failed to import pointer_monitor.py - {e}")
        print("Make sure you're running from the correct directory.")
        return 1
    except KeyboardInterrupt:
        print("\n\n👋 Application stopped by user")
        return 0
    except Exception as e:
        print(f"\n❌ Application error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
