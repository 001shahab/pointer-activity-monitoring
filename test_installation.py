#!/usr/bin/env python3
"""
Installation test script for Pointer Activity Monitoring Service
Created by: Prof. Shahab Anbarjafari from 3S Holding OÜ, Tartu Estonia

This script tests if all dependencies are properly installed and the service can run.
"""

import sys
import importlib

def test_import(module_name, friendly_name=None):
    """Test if a module can be imported"""
    if friendly_name is None:
        friendly_name = module_name
    
    try:
        importlib.import_module(module_name)
        print(f"✅ {friendly_name}: OK")
        return True
    except ImportError as e:
        print(f"❌ {friendly_name}: FAILED ({e})")
        return False

def main():
    """Main test function"""
    print("=" * 60)
    print("Pointer Activity Monitoring Service - Installation Test")
    print("Created by: Prof. Shahab Anbarjafari from 3S Holding OÜ")
    print("=" * 60)
    
    print("\nTesting Python version...")
    python_version = sys.version_info
    if python_version >= (3, 7):
        print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}: OK")
    else:
        print(f"❌ Python {python_version.major}.{python_version.minor}.{python_version.micro}: FAILED (requires 3.7+)")
        return False
    
    print("\nTesting required dependencies...")
    
    all_good = True
    
    # Test core dependencies
    all_good &= test_import("tkinter", "Tkinter (GUI)")
    all_good &= test_import("pynput", "Pynput (Mouse tracking)")
    all_good &= test_import("matplotlib", "Matplotlib (Plotting)")
    all_good &= test_import("matplotlib.pyplot", "Matplotlib pyplot")
    all_good &= test_import("seaborn", "Seaborn (Visualization)")
    all_good &= test_import("numpy", "NumPy (Numerical computing)")
    all_good &= test_import("screeninfo", "Screeninfo (Screen detection)")
    
    # Test optional dependencies
    test_import("PIL", "Pillow (Image processing) - Optional")
    
    print("\nTesting service components...")
    
    try:
        from pointer_monitor import PointerActivityMonitor
        print("✅ Main service class: OK")
    except ImportError as e:
        print(f"❌ Main service class: FAILED ({e})")
        all_good = False
    
    print("\nTesting screen detection...")
    try:
        import screeninfo
        screens = screeninfo.get_monitors()
        print(f"✅ Screen detection: OK ({len(screens)} screen(s) detected)")
        for i, screen in enumerate(screens):
            print(f"   Screen {i+1}: {screen.width}x{screen.height} at ({screen.x}, {screen.y})")
    except Exception as e:
        print(f"❌ Screen detection: FAILED ({e})")
        all_good = False
    
    print("\n" + "=" * 60)
    
    if all_good:
        print("🎉 ALL TESTS PASSED!")
        print("\nYour installation is ready. You can now run:")
        print("   python pointer_monitor.py")
        print("   or")
        print("   python run.py")
    else:
        print("❌ SOME TESTS FAILED!")
        print("\nPlease install missing dependencies:")
        print("   pip install -r requirements.txt")
    
    print("=" * 60)
    return all_good

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
