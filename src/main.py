import sys
import argparse
import ctypes
import os
from pathlib import Path

# Add src to path so we can import core
sys.path.append(str(Path(__file__).parent))

from core.blocker import AIBlocker

def run_as_admin():
    """Relaunch the current script as administrator."""
    if ctypes.windll.shell32.IsUserAnAdmin():
        return True
    
    # Re-run the program with admin rights
    try:
        if sys.argv[0].endswith('.exe'):
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.argv[0], " ".join(sys.argv[1:]), None, 1)
        else:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        return False # The new process started, so we exit this one
    except Exception as e:
        print(f"Failed to elevate privileges: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="IfNoAI - The AI Blackout Experiment")
    parser.add_argument("action", choices=["on", "off", "status", "gui"], nargs="?", default="gui", help="Action to perform (default: gui)")
    parser.add_argument("--force", action="store_true", help="Force action without confirmation")
    
    args = parser.parse_args()
    
    # If GUI requested (default)
    if args.action == "gui":
        # Check admin rights immediately for GUI
        if not ctypes.windll.shell32.IsUserAnAdmin():
            if not run_as_admin():
                return # Exit if elevation failed or new process started
            return # Exit the non-admin process

        try:
            from PySide6.QtWidgets import QApplication
            from gui.main_window import MainWindow
            
            app = QApplication(sys.argv)
            window = MainWindow()
            window.show()
            sys.exit(app.exec())
        except ImportError:
            print("Error: PySide6 not found. Please install requirements: pip install -r requirements.txt")
            sys.exit(1)
        return

    blocker = AIBlocker()

    if args.action == "status":
        is_active = blocker.status()
        print(f"\n[IfNoAI] Status: {'🔴 DISCONNECTED (AI Blocked)' if is_active else '🟢 CONNECTED (AI Available)'}")
        return

    # For modifying actions, check admin
    if not blocker.is_admin():
        print("Requesting administrator privileges...")
        if not run_as_admin():
            return # Exit, the new process will handle it or it failed
        return # Exit the non-admin process

    if args.action == "on":
        print("\n=== INITIATING AI BLACKOUT ===")
        if not args.force:
            confirm = input("Are you sure you want to block all AI services? (y/N): ")
            if confirm.lower() != 'y':
                print("Aborted.")
                return
        
        if blocker.enable_block():
            print("\n[SUCCESS] The cloud is silent. Welcome to the quiet zone.")
            print("Try accessing ChatGPT or Copilot to verify.")

    elif args.action == "off":
        print("\n=== RESTORING CONNECTIVITY ===")
        if blocker.disable_block():
            print("\n[SUCCESS] Connection re-established. The noise returns.")

if __name__ == "__main__":
    main()
