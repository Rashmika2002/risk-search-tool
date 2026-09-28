"""
Auto-Update Module
Checks for updates from GitHub and downloads new version
NO ONEDRIVE - EVERYTHING FROM GITHUB

v2 changes:
- Tracks installed version in installed_version.txt (fixes endless update loop,
  because config.py is never updated by the updater)
- File list can come from version.json ("files"), so future updates don't
  require replacing auto_updater.py on every laptop
- Downloads everything first, then writes (no half-updated installs)
- Backs up replaced files to .update_backup/
"""

import requests
import json
import os
import sys
import shutil
import subprocess
import time
from datetime import datetime
from config import GITHUB_CONFIG, APP_CONFIG

VERSION_FILE = 'installed_version.txt'
BACKUP_DIR = '.update_backup'

# Fallback list, used if version.json has no "files" key.
# Paths must match the GitHub repo exactly (case-sensitive).
DEFAULT_FILES = [
    'app.py',
    'cloud_sync.py',
    'auto_updater.py',
    'requirements.txt',
    'templates/index.html',
    'static/style.css',
    'static/logo.png',
]

# config.py is NEVER updated - it has embedded credentials
PROTECTED_FILES = {'config.py'}


class AutoUpdater:
    """Handles automatic updates from GitHub"""

    def __init__(self):
        self.current_version = self._get_installed_version()
        self.repo_owner = GITHUB_CONFIG['repo_owner']
        self.repo_name = GITHUB_CONFIG['repo_name']
        self.branch = GITHUB_CONFIG['branch']
        self.auto_update = GITHUB_CONFIG['auto_update']
        self.new_version = None
        self.files_to_update = list(DEFAULT_FILES)

    # ------------------------------------------------------------------
    # Version handling
    # ------------------------------------------------------------------
    def _get_installed_version(self):
        """Use the higher of config.py version and installed_version.txt"""
        config_ver = APP_CONFIG['current_version']
        try:
            if os.path.exists(VERSION_FILE):
                with open(VERSION_FILE, 'r') as f:
                    file_ver = f.read().strip()
                if file_ver and self._is_newer_version(file_ver, config_ver):
                    return file_ver
        except Exception:
            pass
        return config_ver

    def _save_installed_version(self, version):
        try:
            with open(VERSION_FILE, 'w') as f:
                f.write(version)
        except Exception as e:
            print(f"⚠️  Could not save installed version: {str(e)}")

    def _is_newer_version(self, new_ver, current_ver):
        """Compare version numbers (e.g., '1.0.1' vs '1.0.0')"""
        try:
            new_parts = [int(x) for x in new_ver.split('.')]
            current_parts = [int(x) for x in current_ver.split('.')]
            return new_parts > current_parts
        except Exception:
            return False

    # ------------------------------------------------------------------
    # Check
    # ------------------------------------------------------------------
    def check_for_updates(self):
        """
        Check if new version is available from GitHub
        Returns: (has_update, new_version, changes)
        """
        try:
            print("🔍 Checking for updates from GitHub...")

            version_url = (
                f"https://raw.githubusercontent.com/"
                f"{self.repo_owner}/{self.repo_name}/{self.branch}/version.json"
            )

            response = requests.get(version_url, timeout=10)

            if response.status_code != 200:
                print("ℹ️  No updates available")
                return False, None, None

            version_data = response.json()
            new_version = version_data.get('version')
            changes = version_data.get('changes', [])
            critical = version_data.get('critical_update', False)

            # Optional: file list defined in version.json
            files = version_data.get('files')
            if isinstance(files, list) and files:
                self.files_to_update = files

            if new_version and self._is_newer_version(new_version, self.current_version):
                print(f"🆕 New version available: {new_version}")
                print(f"📝 Current version: {self.current_version}")

                if critical:
                    print("⚠️  CRITICAL UPDATE - Must install")

                self.new_version = new_version
                return True, new_version, changes
            else:
                print(f"✅ You have the latest version ({self.current_version})")
                return False, None, None

        except Exception as e:
            print(f"ℹ️  Update check skipped: {str(e)}")
            return False, None, None

    # ------------------------------------------------------------------
    # Download
    # ------------------------------------------------------------------
    def download_update(self):
        """Download latest code from GitHub (all-or-nothing)"""
        try:
            print("📥 Downloading update from GitHub...")

            base_url = (
                f"https://raw.githubusercontent.com/"
                f"{self.repo_owner}/{self.repo_name}/{self.branch}"
            )

            downloaded = {}

            # Step 1: download everything into memory first
            for file in self.files_to_update:
                if file in PROTECTED_FILES:
                    print(f"  🔒 Protected, skipped: {file}")
                    continue

                url = f"{base_url}/{file}"
                response = requests.get(url, timeout=15)

                if response.status_code == 200:
                    downloaded[file] = response.content
                elif response.status_code == 404:
                    print(f"  ⚠️  Skipped: {file} (not found in repo)")
                else:
                    # Unexpected error -> abort so we don't end up half-updated
                    print(f"  ❌ Failed: {file} (HTTP {response.status_code}). Update aborted.")
                    return False

            if not downloaded:
                print("ℹ️  No files were updated")
                return False

            # Step 2: back up + write
            os.makedirs(BACKUP_DIR, exist_ok=True)
            updated_files = []

            for file, content in downloaded.items():
                dir_path = os.path.dirname(file)
                if dir_path and not os.path.exists(dir_path):
                    os.makedirs(dir_path)

                if os.path.exists(file):
                    backup_path = os.path.join(BACKUP_DIR, file)
                    backup_dir = os.path.dirname(backup_path)
                    if backup_dir:
                        os.makedirs(backup_dir, exist_ok=True)
                    shutil.copy2(file, backup_path)

                with open(file, 'wb') as f:
                    f.write(content)

                updated_files.append(file)
                print(f"  ✅ Updated: {file}")

            # Step 3: remember the version so we don't loop
            if self.new_version:
                self._save_installed_version(self.new_version)

            print(f"\n✅ Update complete! Updated {len(updated_files)} files")
            return True

        except Exception as e:
            print(f"⚠️  Update download failed: {str(e)}")
            return False

    # ------------------------------------------------------------------
    # Dependencies
    # ------------------------------------------------------------------
    def install_dependencies(self):
        """Install/update Python dependencies"""
        try:
            print("📦 Installing dependencies...")
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', '-r',
                'requirements.txt', '--quiet', '--upgrade'
            ])
            print("✅ Dependencies installed")
            return True
        except Exception as e:
            print(f"⚠️  Dependency installation failed: {str(e)}")
            return False

    # ------------------------------------------------------------------
    # Full flow
    # ------------------------------------------------------------------
    def perform_update(self):
        """Complete update process"""
        has_update, new_version, changes = self.check_for_updates()

        if not has_update:
            return False

        print("\n" + "=" * 70)
        print(f"📦 UPDATE AVAILABLE: v{new_version}")
        print("=" * 70)

        if changes:
            print("\n📝 Changes:")
            for change in changes:
                print(f"  • {change}")

        print("\n" + "=" * 70)

        if self.auto_update:
            print("🔄 Auto-update enabled. Downloading...")

            if self.download_update():
                self.install_dependencies()

                print("\n✅ UPDATE COMPLETE!")
                print("🔄 Restarting application in 3 seconds...")
                time.sleep(3)

                python = sys.executable
                os.execl(python, python, *sys.argv)

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
# VERSION FILE CREATOR (Run this on YOUR laptop when you release an update)
# ============================================================================

def create_version_file(version="2.0.0", changes=None, files=None):
    """Create version.json file for GitHub"""

    if changes is None:
        changes = ["Initial release"]

    if files is None:
        files = DEFAULT_FILES

    version_data = {
        "version": version,
        "release_date": datetime.now().strftime("%Y-%m-%d"),
        "changes": changes,
        "files": files,
        "critical_update": False
    }

    with open('version.json', 'w') as f:
        json.dump(version_data, f, indent=2)

    print("✅ Created version.json")
    print(f"📦 Version: {version}")
    print("📝 Commit this file to GitHub:")
    print("   git add .")
    print(f"   git commit -m 'Update version to {version}'")
    print("   git push origin main")


# ============================================================================
# RELEASE HELPER
# ============================================================================

if __name__ == "__main__":
    print("🧪 Auto-Updater Release Helper\n")

    create_version_file(
        version="2.0.2",
        changes=[
            "Fixed endless update loop",
            "Safer all-or-nothing updates with backups",
        ],
        files=[
            'app.py',
            'cloud_sync.py',
            'auto_updater.py',
            'requirements.txt',
            'templates/index.html',
            'static/style.css',
            'static/logo.png',
        ],
    )

    print("\n" + "=" * 70)
    print("Next: push version.json + changed files to GitHub to release")