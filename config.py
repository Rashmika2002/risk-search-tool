"""
Configuration File - OneDrive Links and Settings
Update these links after setting up OneDrive files
"""

# ============================================================================
# ONEDRIVE CONFIGURATION
# ============================================================================

# OneDrive Direct Download Links
# How to get: Share file → Copy link → Convert to direct download link
# Format: https://onedrive.live.com/download?resid=XXXXX&authkey=XXXXX

ONEDRIVE_CONFIG = {
    # Local OneDrive sync folder path (CHANGE THIS to your actual path)
    "sync_folder": "C:/Users/rhettiarachchi2/OneDrive - KPMG/RiskSearchTool",
    
    # Set to True to use local sync folder instead of downloading
    "use_sync_folder": True,
    
    # Fallback URLs (not needed if using sync folder)
    "keywords_url": None,
    "master_records_url": None,
    "version_url": None,
    
    "cache_duration_hours": 1,
    "offline_mode": False,
}

# ============================================================================
# GITHUB CONFIGURATION
# ============================================================================

GITHUB_CONFIG = {
    "repo_owner": "Rashmika2002",  # Your GitHub username/organization
    "repo_name": "risk-search-tool",  # Repository name
    "branch": "main",  # Branch to pull from
    "auto_update": True,  # Auto-download updates on launch
}

# ============================================================================
# APPLICATION CONFIGURATION
# ============================================================================

APP_CONFIG = {
    "app_name": "Risk Search Tool",
    "current_version": "1.0.0",  # Update this with each release
    "debug_mode": False,
    "host": "127.0.0.1",
    "port": 5000,
}

# ============================================================================
# LOCAL CACHE PATHS
# ============================================================================

import os

CACHE_DIR = os.path.join(os.path.expanduser("~"), ".risk_search_tool")
os.makedirs(CACHE_DIR, exist_ok=True)

LOCAL_FILES = {
    "keywords": os.path.join(CACHE_DIR, "keywords_cache.xlsx"),
    "master_records": os.path.join(CACHE_DIR, "master_records_cache.xlsx"),
    "version": os.path.join(CACHE_DIR, "version_cache.json"),
}

# ============================================================================
# EXCEL COLUMN HEADERS
# ============================================================================

EXCEL_HEADERS = {
    "keywords": ['Category', 'Keyword', 'Active'],
    "master_records": [
        'ID',
        'Client Name',
        'Report Date',
        'Username',
        'Search URL',
        'Status',
        'Keywords Used',
        'App Version'
    ]
}

# ============================================================================
# ONEDRIVE LINK CONVERSION HELPER
# ============================================================================

def convert_onedrive_link(share_link):
    """
    Converts OneDrive share link to direct download link
    
    Example:
    Input:  https://1drv.ms/x/s!XXXXX
    Output: https://onedrive.live.com/download?resid=XXXXX&authkey=XXXXX
    
    Instructions:
    1. Share file in OneDrive
    2. Copy link
    3. Use this function or manually replace:
       - Replace '1drv.ms' with 'onedrive.live.com/download'
       - Add '?resid=' and '&authkey=' parameters
    """
    # This is a placeholder - actual conversion requires OneDrive API or manual
    # For now, users should manually get the direct download link
    print("Please manually convert OneDrive share link to direct download link")
    print("Instructions: https://stackoverflow.com/questions/38466846")
    return share_link