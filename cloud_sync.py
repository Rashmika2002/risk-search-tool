"""
Cloud Synchronization Module
Handles OneDrive Excel file downloads and uploads
"""

import requests
import openpyxl
import json
import os
from datetime import datetime, timedelta
from config import ONEDRIVE_CONFIG, LOCAL_FILES, EXCEL_HEADERS


class CloudSync:
    """Manages synchronization with OneDrive files"""
    
    def __init__(self):
        self.cache_duration = timedelta(hours=ONEDRIVE_CONFIG['cache_duration_hours'])
        self.offline_mode = ONEDRIVE_CONFIG['offline_mode']
    
    def _is_cache_valid(self, filepath):
        """Check if cached file is still valid"""
        if not os.path.exists(filepath):
            return False
        
        file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
        return datetime.now() - file_time < self.cache_duration
    
    def _download_file(self, url, destination):
        """Download file from OneDrive"""
        try:
            print(f"📥 Downloading from cloud: {os.path.basename(destination)}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            with open(destination, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ Downloaded successfully")
            return True
        
        except Exception as e:
            print(f"❌ Download failed: {str(e)}")
            return False
    
    def _upload_file(self, filepath, url):
        """Upload file to OneDrive (requires Microsoft Graph API)"""
        # Note: Direct upload to OneDrive requires Graph API authentication
        # For now, we'll append records locally and periodically sync
        # Alternative: Use OneDrive sync folder
        print("⚠️  Upload requires OneDrive sync folder or Graph API")
        print("📝 Records saved locally. Sync via OneDrive desktop app.")
        return False
    
    def get_keywords(self):
        """
        Get keywords from OneDrive Excel
        Returns list of active keywords
        """
        keywords_file = LOCAL_FILES['keywords']
        
        # Try to download fresh copy
        if not self._is_cache_valid(keywords_file):
            url = ONEDRIVE_CONFIG['keywords_url']
            if url and url != "YOUR_ONEDRIVE_KEYWORDS_DIRECT_LINK":
                self._download_file(url, keywords_file)
        
        # Read keywords from cache
        if os.path.exists(keywords_file):
            try:
                wb = openpyxl.load_workbook(keywords_file)
                ws = wb.active
                
                keywords = []
                for row in ws.iter_rows(min_row=2, values_only=True):
                    if row[2]:  # Active column = TRUE
                        keywords.append(row[1])  # Keyword column
                
                print(f"📋 Loaded {len(keywords)} keywords from cloud")
                return keywords
            
            except Exception as e:
                print(f"❌ Error reading keywords: {str(e)}")
        
        # Fallback to default keywords if offline
        if self.offline_mode:
            print("⚠️  Using default keywords (offline mode)")
            return self._get_default_keywords()
        
        return []
    
    def _get_default_keywords(self):
        """Fallback keywords if cloud is unavailable"""
        return [
            "fraud", "corruption", "bribery", "money laundering",
            "terrorist financing", "sanctions violation", "embezzlement", 
            "tax evasion", "lawsuit", "litigation", "court case",
            "regulatory action", "enforcement action", "compliance breach",
            "human rights violation", "forced labour", "child labour",
            "discrimination at work", "labour law violation", "union suppression",
            "collective bargaining restriction", "unsafe working conditions",
            "environmental damage", "pollution incident", 
            "environmental negligence", "toxic waste",
            "management misconduct", "governance failure",
            "ethics violation", "whistleblower allegation",
            "data breach", "leaked documents"
        ]
    
    def append_search_record(self, record_data):
        """
        Append search record to master records file
        
        Args:
            record_data: dict with keys: client_name, report_date, username, 
                        search_url, status, keywords_used, app_version
        """
        records_file = LOCAL_FILES['master_records']
        
        # Download latest version first
        url = ONEDRIVE_CONFIG['master_records_url']
        if url and url != "YOUR_ONEDRIVE_MASTER_RECORDS_DIRECT_LINK":
            self._download_file(url, records_file)
        
        # Create file if doesn't exist
        if not os.path.exists(records_file):
            self._create_master_records_file(records_file)
        
        # Append record
        try:
            wb = openpyxl.load_workbook(records_file)
            ws = wb.active
            
            next_row = ws.max_row + 1
            next_id = next_row - 1
            
            ws.cell(row=next_row, column=1).value = next_id
            ws.cell(row=next_row, column=2).value = record_data['client_name']
            ws.cell(row=next_row, column=3).value = record_data['report_date']
            ws.cell(row=next_row, column=4).value = record_data['username']
            ws.cell(row=next_row, column=5).value = record_data['search_url']
            ws.cell(row=next_row, column=6).value = record_data['status']
            ws.cell(row=next_row, column=7).value = record_data['keywords_used']
            ws.cell(row=next_row, column=8).value = record_data['app_version']
            
            wb.save(records_file)
            print(f"✅ Record saved (ID: {next_id})")
            
            # Note: Manual sync to OneDrive via desktop app or Graph API
            return next_id
        
        except Exception as e:
            print(f"❌ Error saving record: {str(e)}")
            return None
    
    def _create_master_records_file(self, filepath):
        """Create new master records Excel file"""
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Risk Search Records"
        
        # Add headers
        for col_num, header in enumerate(EXCEL_HEADERS['master_records'], 1):
            ws.cell(row=1, column=col_num).value = header
        
        wb.save(filepath)
        print(f"📄 Created new master records file")
    
    def get_recent_searches(self, limit=10):
        """Get recent searches from master records"""
        records_file = LOCAL_FILES['master_records']
        
        # Try to download fresh copy
        url = ONEDRIVE_CONFIG['master_records_url']
        if url and url != "YOUR_ONEDRIVE_MASTER_RECORDS_DIRECT_LINK":
            self._download_file(url, records_file)
        
        if not os.path.exists(records_file):
            return []
        
        try:
            wb = openpyxl.load_workbook(records_file)
            ws = wb.active
            
            searches = []
            max_row = ws.max_row
            start_row = max(2, max_row - limit + 1)
            
            for row in range(max_row, start_row - 1, -1):
                if row > 1:
                    searches.append({
                        'id': ws.cell(row=row, column=1).value,
                        'client_name': ws.cell(row=row, column=2).value,
                        'report_date': ws.cell(row=row, column=3).value,
                        'username': ws.cell(row=row, column=4).value,
                        'search_url': ws.cell(row=row, column=5).value,
                        'status': ws.cell(row=row, column=6).value,
                        'keywords_used': ws.cell(row=row, column=7).value,
                        'app_version': ws.cell(row=row, column=8).value
                    })
            
            return searches
        
        except Exception as e:
            print(f"❌ Error reading recent searches: {str(e)}")
            return []
    
    def get_total_records(self):
        """Get total number of records"""
        records_file = LOCAL_FILES['master_records']
        
        if not os.path.exists(records_file):
            return 0
        
        try:
            wb = openpyxl.load_workbook(records_file)
            ws = wb.active
            return ws.max_row - 1  # Exclude header
        except:
            return 0


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def create_keywords_template():
    """Create template keywords Excel file for OneDrive upload"""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Risk Keywords"
    
    # Headers
    ws['A1'] = 'Category'
    ws['B1'] = 'Keyword'
    ws['C1'] = 'Active'
    
    # Sample data
    keywords_data = [
        ('Financial Crime', 'fraud', True),
        ('Financial Crime', 'corruption', True),
        ('Financial Crime', 'bribery', True),
        ('Financial Crime', 'money laundering', True),
        ('Financial Crime', 'terrorist financing', True),
        ('Financial Crime', 'sanctions violation', True),
        ('Financial Crime', 'embezzlement', True),
        ('Financial Crime', 'tax evasion', True),
        ('Legal & Regulatory', 'lawsuit', True),
        ('Legal & Regulatory', 'litigation', True),
        ('Legal & Regulatory', 'court case', True),
        ('Legal & Regulatory', 'regulatory action', True),
        ('Legal & Regulatory', 'enforcement action', True),
        ('Legal & Regulatory', 'compliance breach', True),
        ('Human Rights & Labour', 'human rights violation', True),
        ('Human Rights & Labour', 'forced labour', True),
        ('Human Rights & Labour', 'child labour', True),
        ('Human Rights & Labour', 'discrimination at work', True),
        ('Human Rights & Labour', 'labour law violation', True),
        ('Human Rights & Labour', 'union suppression', True),
        ('Human Rights & Labour', 'collective bargaining restriction', True),
        ('Human Rights & Labour', 'unsafe working conditions', True),
        ('Environmental & ESG', 'environmental damage', True),
        ('Environmental & ESG', 'pollution incident', True),
        ('Environmental & ESG', 'environmental negligence', True),
        ('Environmental & ESG', 'toxic waste', True),
        ('Governance & Ethics', 'management misconduct', True),
        ('Governance & Ethics', 'governance failure', True),
        ('Governance & Ethics', 'ethics violation', True),
        ('Governance & Ethics', 'whistleblower allegation', True),
        ('Cyber & Data', 'data breach', True),
        ('Cyber & Data', 'leaked documents', True),
    ]
    
    for row_num, (category, keyword, active) in enumerate(keywords_data, 2):
        ws.cell(row=row_num, column=1).value = category
        ws.cell(row=row_num, column=2).value = keyword
        ws.cell(row=row_num, column=3).value = active
    
    wb.save('keywords_template.xlsx')
    print("✅ Created keywords_template.xlsx - Upload this to OneDrive")


if __name__ == "__main__":
    # Create template for developers
    create_keywords_template()
    print("\n📋 Template created successfully!")
    print("Next steps:")
    print("1. Upload keywords_template.xlsx to OneDrive")
    print("2. Get shareable link with 'edit' permissions")
    print("3. Convert to direct download link")
    print("4. Update config.py with the link")