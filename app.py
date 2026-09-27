"""
Flask Web Application for Risk Search Tool
Cloud-Enabled Version with Auto-Updates
"""
from flask import Flask, render_template, request, jsonify, send_file
import urllib.parse
from datetime import datetime
import getpass
import sys
import os

# Import cloud modules
from cloud_sync import CloudSync
from auto_updater import AutoUpdater
from config import APP_CONFIG, GOOGLE_SHEETS_CONFIG, LOCAL_FILES

# The updater does not replace config.py because it contains installation credentials.
APP_CONFIG['current_version'] = '2.0.2'

app = Flask(__name__)

# Initialize cloud sync
cloud = CloudSync()
updater = AutoUpdater()


def create_single_search_url(company_name, keywords):
    """Creates ONE comprehensive Google search URL with all keywords"""
    quoted_company = f'"{company_name}"'
    
    keyword_list = []
    for kw in keywords:
        if ' ' in kw:
            keyword_list.append(f'"{kw}"')
        else:
            keyword_list.append(kw)
    
    keywords_or = ' OR '.join(keyword_list)
    query = f'{quoted_company} ({keywords_or})'
    url = f"https://www.google.com/search?{urllib.parse.urlencode({'q': query})}"
    
    return url

@app.route('/')
def index():
    """Main page"""
    import getpass
    
    keywords = cloud.get_keywords()
    recent_searches = cloud.get_recent_searches(10)
    
    # Count user's searches
    username = getpass.getuser()
    all_searches = cloud.get_all_searches()
    my_search_count = len([s for s in all_searches if s.get('username') == username])
    
    return render_template('index.html', 
                         total_keywords=len(keywords),
                         recent_searches=recent_searches,
                         app_version=APP_CONFIG['current_version'],
                         my_search_count=my_search_count,
                         keyword_sheets=cloud.get_keyword_sheets(),
                         default_keyword_sheet=GOOGLE_SHEETS_CONFIG['keywords_worksheet_name'])


@app.route('/search', methods=['POST'])
def search():
    """Process search request"""
    data = request.get_json()
    if not isinstance(data, dict):
        return jsonify({'success': False, 'message': 'Invalid search request'}), 400

    client_names = data.get('clients', '')
    keyword_sheet = data.get(
        'keyword_sheet',
        GOOGLE_SHEETS_CONFIG['keywords_worksheet_name']
    )
    
    if not client_names:
        return jsonify({'success': False, 'message': 'No client names provided'})

    if not isinstance(keyword_sheet, str):
        return jsonify({'success': False, 'message': 'Invalid keyword sheet'}), 400
    
    try:
        keywords = cloud.get_keywords(keyword_sheet)
    except ValueError as e:
        return jsonify({'success': False, 'message': str(e)}), 400
    except RuntimeError as e:
        return jsonify({'success': False, 'message': str(e)}), 503
    
    if not keywords:
        return jsonify({
            'success': False,
            'message': f"No active keywords available in '{keyword_sheet}'"
        })
    
    # Parse client names
    clients = [c.strip() for c in client_names.split(',') if c.strip()]
    
    results = []
    username = getpass.getuser()
    
    for client in clients:
        search_url = create_single_search_url(client, keywords)
        
        # Create record
        record_data = {
            'client_name': client,
            'report_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'username': username,
            'search_url': search_url,
            'status': 'Success',
            'keywords_used': len(keywords),
            'app_version': APP_CONFIG['current_version']
        }
        
        # Save to cloud
        record_id = cloud.append_search_record(record_data)
        
        if record_id:
            record_data['id'] = record_id
        
        results.append(record_data)
    
    # Get total records
    total_records = cloud.get_total_records()
    
    return jsonify({
        'success': True,
        'message': f"Generated {len(results)} search link(s) using '{keyword_sheet}'",
        'results': results,
        'total_records': total_records
    })


@app.route('/download')
def download():
    """Download master Excel file"""
    records_file = LOCAL_FILES['master_records']
    
    if records_file and os.path.exists(records_file):
        return send_file(records_file, as_attachment=True)
    else:
        return "No records found", 404
    
@app.route('/download_my_searches')
def download_my_searches():
    """Download only current user's searches as Excel file"""
    import getpass
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from datetime import datetime
    
    # Get current username
    username = getpass.getuser()
    
    # Create new workbook for user's searches
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = f"{username} Searches"
    
    # Style settings
    header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF", size=12)
    border = Border(
        left=Side(style='thin'), right=Side(style='thin'),
        top=Side(style='thin'), bottom=Side(style='thin')
    )
    
    # Add headers
    headers = ['ID', 'Client Name', 'Report Date', 'Search URL', 'Status', 'Keywords Used', 'App Version']
    for col_num, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_num)
        cell.value = header
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal='center', vertical='center')
        cell.border = border
    
    # Get all searches and filter by username
    all_searches = cloud.get_all_searches()  # We'll create this method
    my_searches = [s for s in all_searches if s.get('username') == username]
    
    # Add user's searches
    for row_num, search in enumerate(my_searches, 2):
        ws.cell(row=row_num, column=1).value = search.get('id')
        ws.cell(row=row_num, column=1).border = border
        
        ws.cell(row=row_num, column=2).value = search.get('client_name')
        ws.cell(row=row_num, column=2).border = border
        
        ws.cell(row=row_num, column=3).value = search.get('report_date')
        ws.cell(row=row_num, column=3).border = border
        
        search_url = search.get('search_url')
        ws.cell(row=row_num, column=4).value = search_url
        ws.cell(row=row_num, column=4).hyperlink = search_url
        ws.cell(row=row_num, column=4).font = Font(color="0563C1", underline="single")
        ws.cell(row=row_num, column=4).border = border
        
        ws.cell(row=row_num, column=5).value = search.get('status')
        ws.cell(row=row_num, column=5).border = border
        
        ws.cell(row=row_num, column=6).value = search.get('keywords_used')
        ws.cell(row=row_num, column=6).border = border
        
        ws.cell(row=row_num, column=7).value = search.get('app_version')
        ws.cell(row=row_num, column=7).border = border
    
    # Adjust column widths
    ws.column_dimensions['A'].width = 10
    ws.column_dimensions['B'].width = 35
    ws.column_dimensions['C'].width = 22
    ws.column_dimensions['D'].width = 70
    ws.column_dimensions['E'].width = 15
    ws.column_dimensions['F'].width = 15
    ws.column_dimensions['G'].width = 15
    
    # Create filename with username and date
    today = datetime.now().strftime('%Y-%m-%d')
    filename = f'RiskSearches_{username}_{today}.xlsx'
    filepath = os.path.join(os.path.expanduser('~'), 'Downloads', filename)
    
    # Save file
    wb.save(filepath)
    
    return send_file(filepath, as_attachment=True, download_name=filename)

@app.route('/stats')
def stats():
    """Get statistics"""
    total_records = cloud.get_total_records()
    keywords = cloud.get_keywords()
    
    return jsonify({
        'total_records': total_records,
        'total_keywords': len(keywords),
        'app_version': APP_CONFIG['current_version']
    })


@app.route('/check_update')
def check_update():
    """Check for updates"""
    has_update, new_version, changes = updater.check_for_updates()
    
    return jsonify({
        'has_update': has_update,
        'current_version': APP_CONFIG['current_version'],
        'new_version': new_version,
        'changes': changes
    })


def startup_checks():
    """Perform startup checks and updates"""
    print("\n" + "="*80)
    print(f"🚀 {APP_CONFIG['app_name'].upper()} v{APP_CONFIG['current_version']}")
    print("="*80)
    
    # Check for updates
    if APP_CONFIG.get('auto_update', True):
        print("\n🔍 Checking for updates...")
        updater.perform_update()
    
    # Test cloud connection
    print("\n☁️  Testing cloud connection...")
    keywords = cloud.get_keywords()
    
    if keywords:
        print(f"✅ Cloud connected - {len(keywords)} keywords loaded")
    else:
        print("⚠️  Cloud connection failed - using offline mode")
    
    print("\n" + "="*80)
    print(f"🌐 Server starting on http://{APP_CONFIG['host']}:{APP_CONFIG['port']}")
    print("Press Ctrl+C to stop the server")
    print("="*80 + "\n")


if __name__ == '__main__':
    import os
    
    # Perform startup checks
    startup_checks()
    
    # Run Flask app
    app.run(
        debug=APP_CONFIG['debug_mode'], 
        host=APP_CONFIG['host'], 
        port=APP_CONFIG['port']
    )
