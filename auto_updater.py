"""
Auto-Update Module
Checks for updates from GitHub and downloads new version
"""

import requests
import json
import os
import sys
import subprocess
from datetime import datetime
from config import GITHUB_CONFIG, APP_CONFIG, ONEDRIVE_CONFIG, LOCAL_FILES


class AutoUpdater:
    """Handles automatic updates from GitHub"""
    
    def __init__(self):
        self.current_version = APP_CONFIG['current_version']
        self.repo_owner = GITHUB_CONFIG['repo_owner']
        self.repo_name = GITHUB_CONFIG['repo_name']
        self.branch = GITHUB_CONFIG['branch']
        self.auto_update = GITHUB_CONFIG['auto_update']
    
    def check_for_updates(self):
        """
        Check if new version is available
        Returns: (has_update, new_version, changes)
        """
        try:
            print("🔍 Checking for updates...")
            
            # Download version.json from OneDrive
            version_url = ONEDRIVE_CONFIG['version_url']
            
            if not version_url or version_url == "YOUR_ONEDRIVE_VERSION_JSON_DIRECT_LINK":
                print("⚠️  Version URL not configured")
                return False, None, None
            
            response = requests.get(version_url, timeout=5)
            response.raise_for_status()
            
            version_data = response.json()
            new_version = version_data.get('version')
            changes = version_data.get('changes', [])
            critical = version_data.get('critical_update', False)
            
            if self._is_newer_version(new_version, self.current_version):
                print(f"🆕 New version available: {new_version}")
                print(f"📝 Current version: {self.current_version}")
                
                if critical:
                    print("⚠️  CRITICAL UPDATE - Must install")
                
                return True, new_version, changes
            else:
                print(f"✅ You have the latest version ({self.current_version})")
                return False, None, None
        
        except Exception as e:
            print(f"❌ Update check failed: {str(e)}")
            return False, None, None
    
    def _is_newer_version(self, new_ver, current_ver):
        """Compare version numbers (e.g., '1.0.1' vs '1.0.0')"""
        try:
            new_parts = [int(x) for x in new_ver.split('.')]
            current_parts = [int(x) for x in current_ver.split('.')]
            return new_parts > current_parts
        except:
            return False
    
    def download_update(self):
        """Download latest code from GitHub"""
        try:
            print("📥 Downloading update from GitHub...")
            
            # GitHub raw file URLs
            base_url = f"https://raw.githubusercontent.com/{self.repo_owner}/{self.repo_name}/{self.branch}"
            
            files_to_update = [
                'app.py',
                'cloud_sync.py',
                'auto_updater.py',
                'config.py',
                'requirements.txt',
                'templates/index.html',
            ]
            
            updated_files = []
            
            for file in files_to_update:
                try:
                    url = f"{base_url}/{file}"
                    response = requests.get(url, timeout=10)
                    
                    if response.status_code == 200:
                        # Create directory if needed
                        dir_path = os.path.dirname(file)
                        if dir_path and not os.path.exists(dir_path):
                            os.makedirs(dir_path)
                        
                        # Save file
                        with open(file, 'w', encoding='utf-8') as f:
                            f.write(response.text)
                        
                        updated_files.append(file)
                        print(f"  ✅ Updated: {file}")
                    else:
                        print(f"  ⚠️  Skipped: {file} (not found)")
                
                except Exception as e:
                    print(f"  ❌ Failed: {file} - {str(e)}")
            
            if updated_files:
                print(f"\n✅ Update complete! Updated {len(updated_files)} files")
                print("🔄 Please restart the application")
                return True
            else:
                print("❌ No files were updated")
                return False
        
        except Exception as e:
            print(f"❌ Update download failed: {str(e)}")
            return False
    
    def install_dependencies(self):
        """Install/update Python dependencies"""
        try:
            print("📦 Installing dependencies...")
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', '-r', 
                'requirements.txt', '--quiet'
            ])
            print("✅ Dependencies installed")
            return True
        except Exception as e:
            print(f"❌ Dependency installation failed: {str(e)}")
            return False
    
    def perform_update(self):
        """Complete update process"""
        has_update, new_version, changes = self.check_for_updates()
        
        if not has_update:
            return False
        
        print("\n" + "="*60)
        print(f"📦 UPDATE AVAILABLE: v{new_version}")
        print("="*60)
        
        if changes:
            print("\n📝 Changes:")
            for change in changes:
                print(f"  • {change}")
        
        print("\n" + "="*60)
        
        if self.auto_update:
            print("🔄 Auto-update enabled. Downloading...")
            
            if self.download_update():
                self.install_dependencies()
                
                print("\n✅ UPDATE COMPLETE!")
                print("🔄 Restarting application in 3 seconds...")
                
                import time
                time.sleep(3)
                
                # Restart application
                os.execv(sys.executable, [sys.executable] + sys.argv)
            
            return True
        else:
            response = input("\n❓ Download and install update? (y/n): ")
            
            if response.lower() == 'y':
                if self.download_update():
                    self.install_dependencies()
                    print("\n✅ Update installed! Please restart the application.")
                    sys.exit(0)
            else:
                print("⏭️  Update skipped")
        
        return False


# ============================================================================
# VERSION FILE CREATOR
# ============================================================================

def create_version_file(version="1.0.0", changes=None):
    """Create version.json file for upload to OneDrive"""
    
    if changes is None:
        changes = ["Initial release"]
    
    version_data = {
        "version": version,
        "release_date": datetime.now().strftime("%Y-%m-%d"),
        "changes": changes,
        "critical_update": False,
        "download_url": f"https://github.com/{GITHUB_CONFIG['repo_owner']}/{GITHUB_CONFIG['repo_name']}/archive/refs/heads/{GITHUB_CONFIG['branch']}.zip"
    }
    
    with open('version.json', 'w') as f:
        json.dump(version_data, f, indent=2)
    
    print("✅ Created version.json")
    print(f"📦 Version: {version}")
    print("📝 Upload this file to OneDrive")


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("🧪 Auto-Updater Test\n")
    
    # Create sample version file
    create_version_file(
        version="1.0.1",
        changes=[
            "Added cloud synchronization",
            "Implemented auto-update feature",
            "Fixed search URL encoding"
        ]
    )
    
    print("\n" + "="*60)
    
    # Test update check
    updater = AutoUpdater()
    has_update, new_ver, changes = updater.check_for_updates()
    
    if has_update:
        print(f"\n✅ Update test successful!")
        print(f"New version: {new_ver}")
        print("Changes:", changes)
    else:
        print("\nℹ️  No updates found (expected if version.json not on OneDrive yet)")
