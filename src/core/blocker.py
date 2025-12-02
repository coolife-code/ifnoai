import os
import sys
import shutil
import json
import ctypes
import subprocess
from datetime import datetime
from pathlib import Path

class AIBlocker:
    def __init__(self):
        self.hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
        self.backup_path = r"C:\Windows\System32\drivers\etc\hosts.backup.ifnoai"
        self.domains_file = Path(__file__).parents[2] / "data" / "ai_domains.json"
        self.marker_start = "# === IfNoAI START ==="
        self.marker_end = "# === IfNoAI END ==="

    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def load_domains(self):
        if not self.domains_file.exists():
            print(f"Error: Domain list not found at {self.domains_file}")
            return []
        
        try:
            with open(self.domains_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                domains = set() # Use set to avoid duplicates
                for category in data.get("categories", {}).values():
                    # Handle new structure where category is an object with "domains" list
                    if isinstance(category, dict) and "domains" in category:
                        domains.update(category["domains"])
                    # Handle old structure where category was just a list
                    elif isinstance(category, list):
                        domains.update(category)
                return list(domains)
        except Exception as e:
            print(f"Error loading domains: {e}")
            return []

    def backup_hosts(self):
        """Creates a backup of the hosts file if it doesn't exist."""
        if not os.path.exists(self.hosts_path):
            print("Error: Hosts file not found!")
            return False
            
        if not os.path.exists(self.backup_path):
            try:
                shutil.copy2(self.hosts_path, self.backup_path)
                print(f"Backup created at {self.backup_path}")
                return True
            except Exception as e:
                print(f"Failed to create backup: {e}")
                return False
        return True

    def enable_block(self):
        """Adds AI domains to the hosts file."""
        if not self.is_admin():
            print("Error: Administrator privileges required to modify hosts file.")
            return False

        if not self.backup_hosts():
            return False

        domains = self.load_domains()
        if not domains:
            print("No domains to block.")
            return False

        try:
            # Read current content
            with open(self.hosts_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check if already blocked
            if self.marker_start in content:
                print("IfNoAI is already active.")
                return True

            # Prepare block block
            block_lines = [f"\n{self.marker_start}\n"]
            block_lines.append(f"# Active since: {datetime.now().isoformat()}\n")
            for domain in domains:
                # Redirect to localhost to capture stats via Sinkhole
                # IPv4
                block_lines.append(f"127.0.0.1 {domain}\n")
                # IPv6
                block_lines.append(f"::1 {domain}\n")
            block_lines.append(f"{self.marker_end}\n")

            # Write new content
            with open(self.hosts_path, 'a', encoding='utf-8') as f:
                f.writelines(block_lines)
            
            print(f"Blocked {len(domains)} AI domains.")
            self.flush_dns()
            return True

        except Exception as e:
            print(f"Failed to modify hosts file: {e}")
            return False

    def disable_block(self):
        """Removes AI domains from the hosts file."""
        if not self.is_admin():
            print("Error: Administrator privileges required to modify hosts file.")
            return False

        if not os.path.exists(self.hosts_path):
            return False

        try:
            with open(self.hosts_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            new_lines = []
            in_block = False
            for line in lines:
                if self.marker_start in line:
                    in_block = True
                    continue
                if self.marker_end in line:
                    in_block = False
                    continue
                
                if not in_block:
                    new_lines.append(line)

            with open(self.hosts_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)

            print("AI block removed.")
            self.flush_dns()
            return True

        except Exception as e:
            print(f"Failed to restore hosts file: {e}")
            return False

    def flush_dns(self):
        """Flushes the Windows DNS cache."""
        try:
            subprocess.run(["ipconfig", "/flushdns"], check=True, stdout=subprocess.PIPE)
            print("DNS cache flushed.")
        except Exception as e:
            print(f"Failed to flush DNS: {e}")

    def status(self):
        """Checks if blocking is currently active."""
        try:
            with open(self.hosts_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return self.marker_start in content
        except:
            return False

if __name__ == "__main__":
    # Simple test
    blocker = AIBlocker()
    if not blocker.is_admin():
        print("Please run as administrator to test.")
    else:
        print("Current Status:", "Active" if blocker.status() else "Inactive")
