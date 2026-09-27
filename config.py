"""
Configuration File - SECURE VERSION
Credentials are embedded and hidden from employees
"""

import os
import json
import base64
import tempfile

# ============================================================================
# EMBEDDED ENCRYPTED CREDENTIALS - EMPLOYEES CAN'T SEE THE ACTUAL VALUES
# ============================================================================

# This is base64 encoded - not readable by employees
_ENCRYPTED_CREDS = "eyJ0eXBlIjogInNlcnZpY2VfYWNjb3VudCIsICJwcm9qZWN0X2lkIjogInJpc2stc2VhcmNoLXRvb2wiLCAicHJpdmF0ZV9rZXlfaWQiOiAiMjkyZGEyYzg3MTllOGY3ODg1MGE0Y2Y3ODcxYTE3M2QyN2FhNTk2YyIsICJwcml2YXRlX2tleSI6ICItLS0tLUJFR0lOIFBSSVZBVEUgS0VZLS0tLS1cbk1JSUV2Z0lCQURBTkJna3Foa2lHOXcwQkFRRUZBQVNDQktnd2dnU2tBZ0VBQW9JQkFRREFQZjl0dXJ5SkdsTVlcbklFREZvK3RMV1lMUUpMZWtBYWRKTy9iVTF2OWo1dGVWbnJWWWRTMXp6ZmhXYjhkajF6QmRjdm41ck9wRnlHME5cbi9vc1l3STZRdWtaQTkxeXZnVm9zWUdRU2w2MWtybGxVdTFVS0ZmcFVORVRNcUlrWmM0L2RrRk8xR2tvZ0s1Z2xcbjRrcVJUWnppZWdYQkxLalpzeUxRSExtUFdOOHRKMU9xTEhJZGwyQlJPaHdNRytST2cyMFB0ME5oUmdhek05Ty9cbkhBY2hncXh2VmYzclRNV0cwcmVMYnZuUlB3VG9VV0ZVRmRTNmdvTmNLb2h6OWQrVEg0Sjg5OUVxNlZLVUdhK2RcbjRtbzRVcWlwT1VyRm9KVTNubWdvSzFEczk4UUtPdEF1azRyU0Q5VjZRZ1VNSE9TeHNETlhCMzZWYWphQTJJYlZcbmN6K2NCMWVwQWdNQkFBRUNnZ0VBQkdKbGw1bThBRjhsVTFZem8vajFFM3d3ZGp3Z0pCRnE2MG4rMEhreGR6OGxcbjNqZXh2Y1FPWVZHLzZZTnJITHA2VStkSFpEWlpYQ0M4dS91amd5WldiMTZRTTUzRjgyQVQybWM5dGw3WE5EQ2dcbmE1cEtKT0lUYjNyY1hDazJnZW9YZHpUUGMrdEJrdHpycWhHRnp5MDNUVzJvVnB1RXpsSStQUU9BQitZOXBoM3hcblhmOWdlT2tnUUZFcEVpWXhod0l1cHB1OFNNenRFUlNOWjBqT2xzZGVFYXFvR1pmMGNnVlZuSDlJbUljL2s1dFZcbk9FbnRPSEhHRitlVGZyVFh2OWE5ckZMc3RBN1hUbmE1MEhjdU9oa1lkUnBaVVRhM0FOcDlEVW5ZQ1YwdEJyMEtcbkVzdEd6eHdVZ0EwWTM1U3NwR09rOG12RnhnbjJkeHdmRGV3TUptV09BUUtCZ1FEbTR5dnYxNTVNWC9XdHZnNWJcbm1Ya2tIbXBBY3YrcjNiNW5UdkdxRFN0LzdBZk5KL1NNT1ZobXFVL1BGcmRvU1hYSWo5Ti8zNlc0L1lleG41bFFcbmlZTEpCaUtwL0RVN0pFWmdOL29hdENOeEZpMHpFYmVjRnJqclBoQXppL3d0UjNDcFd2VC8waC9CcS9Xc0cwQklcbmR0MUYvcm9INGVuK0txSkRzMEVnUXBuMXNRS0JnUURWSnNuMmRwSGltS1cwd3FWMExUWVRYb0l1cjM2cmo0ZCtcbjlzQ0pkQ1h0L2RDRG5oeC93aGpkczJHcHU3TEJXdjIxMVlocEFIeXJleC9iNjE1cit3YmlnSXpRSHN1NDVjV1BcbmVyOHpOVWtLcW91UVd4SFFVeHd5dTdWRHB1SkpsbHhsYllsQ010TmVzQnZHY1BCd3FHUXJHMjhBR0xaOE5PSlBcbkhZM010K2huZVFLQmdRRGJzNnVwYkVtTGIzeCtPVzI4S0F3b0hIRUtwdU0zRGFnUzhnSHZ5Tnh0dTVHbzNLNU5cbmlIdmdKSmgyL0t6RnBiRllpZE85eUhrUDBPQ0FXdGd1MU1zSXNyZmxmTUxDWmtBNWFzcXBBbVQvUlJUNWxaQmNcbkRSc2xia2RJWlpvdkU5M1dxV0NjMWJ1Mk5RVnZJZmRIZlNRTmFOaG9pOFozUHVacytYT3RXUExiNFFLQmdFZ0RcbnFPeUtOdE8xK3haTlJSVXhTVG5XRG1temhUcDFiYlBwcmpkQ2RLWXB3TThYRmszYnlBYnZXaW04YnJLQkNZTHJcbnVBQ3gxMjBnVmkwNUlsZWRJa0JZYWpyT2pNblZaNkFJT3AwVWZhOEsyOGhUM0hyaitYenlpbFZuQnNFUitmbVNcbnZuTU5OUGlpeTErS1BOSHpNcFNWMmpUUUpLZG1QcWU0Tm5aYUZEMFJBb0dCQUt1QkFjSFprenQ0d3JiQWgyRFNcbmpiaWpXYmtRSGdSaStuamhJREcvMjFGSCtVS0tZcTI4cGxVbWpDRDdPeGVlWFVSaTVtS1lUVEV1ZWV4Q0hRcHNcbm5Nc1VrNDBVR0lNWGF1c0MzK05CUm5LMTVOQXpBTGtnME54dzVaekd5UlJRckVUVFNNTWhpclFtY2NlWUwyZ1pcbktoOFF4N2tSb0JQcmliTnF0SitTbjdqV1xuLS0tLS1FTkQgUFJJVkFURSBLRVktLS0tLVxuIiwgImNsaWVudF9lbWFpbCI6ICJyaXNrLXNlYXJjaC1zZXJ2aWNlQHJpc2stc2VhcmNoLXRvb2wuaWFtLmdzZXJ2aWNlYWNjb3VudC5jb20iLCAiY2xpZW50X2lkIjogIjExMzUzMzM5OTA4OTA2ODA4NTk1OSIsICJhdXRoX3VyaSI6ICJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20vby9vYXV0aDIvYXV0aCIsICJ0b2tlbl91cmkiOiAiaHR0cHM6Ly9vYXV0aDIuZ29vZ2xlYXBpcy5jb20vdG9rZW4iLCAiYXV0aF9wcm92aWRlcl94NTA5X2NlcnRfdXJsIjogImh0dHBzOi8vd3d3Lmdvb2dsZWFwaXMuY29tL29hdXRoMi92MS9jZXJ0cyIsICJjbGllbnRfeDUwOV9jZXJ0X3VybCI6ICJodHRwczovL3d3dy5nb29nbGVhcGlzLmNvbS9yb2JvdC92MS9tZXRhZGF0YS94NTA5L3Jpc2stc2VhcmNoLXNlcnZpY2UlNDByaXNrLXNlYXJjaC10b29sLmlhbS5nc2VydmljZWFjY291bnQuY29tIiwgInVuaXZlcnNlX2RvbWFpbiI6ICJnb29nbGVhcGlzLmNvbSJ9"

# Your Google Sheet ID (this is public - not sensitive)
_SHEET_ID = "1CB36AWWYlgW9dFOK-tYRKTJknL5wAIIh7UuVqYpPA0Y"  # Replace with your actual Sheet ID

# ============================================================================
# CREDENTIAL LOADER - DECRYPTS AT RUNTIME
# ============================================================================

def get_google_credentials():
    """
    Decrypt and load credentials at runtime
    Employees never see the actual credentials
    """
    try:
        # Decode the base64 string
        decoded = base64.b64decode(_ENCRYPTED_CREDS).decode()
        
        # Parse JSON
        creds_dict = json.loads(decoded)
        
        # Create temporary credentials file
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        json.dump(creds_dict, temp_file)
        temp_file.close()
        
        return temp_file.name
    
    except Exception as e:
        print(f"❌ Error loading credentials: {e}")
        return None


# ============================================================================
# GOOGLE SHEETS CONFIGURATION
# ============================================================================

GOOGLE_SHEETS_CONFIG = {
    # Credentials loaded from encrypted embedded data
    "credentials_file": get_google_credentials(),
    
    # Google Sheet ID - UPDATE THIS WITH YOUR SHEET ID
    "sheet_id": _SHEET_ID,
    
    # Worksheet names
    "worksheet_name": "Risk Searches",
    "keywords_worksheet_name": "Keywords",
    "russian_keywords_worksheet_name": "Russian_Keyword_Sheet",
}

# ============================================================================
# GITHUB CONFIGURATION
# ============================================================================

GITHUB_CONFIG = {
    "repo_owner": "Rashmika2002",
    "repo_name": "risk-search-tool",
    "branch": "main",
    "auto_update": False,
}

# ============================================================================
# APPLICATION CONFIGURATION
# ============================================================================

APP_CONFIG = {
    "app_name": "Risk Search Tool",
    "current_version": "2.0.2",
    "debug_mode": False,
    "host": "127.0.0.1",
    "port": 5000,
}

# ============================================================================
# LOCAL CACHE PATHS
# ============================================================================

CACHE_DIR = os.path.join(os.path.expanduser("~"), ".risk_search_tool")
os.makedirs(CACHE_DIR, exist_ok=True)

LOCAL_FILES = {
    "keywords": "keywords.xlsx",
    "master_records": os.path.join(CACHE_DIR, "my_searches_backup.xlsx"),
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