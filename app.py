"""
Flask Web Application for Risk Search Tool
Cloud-Enabled Version with Auto-Updates
"""
from flask import Flask, render_template, request, jsonify, send_file
import urllib.parse
from datetime import datetime
import getpass
import sys

# Import cloud modules
from cloud_sync import CloudSync
from auto_updater import AutoUpdater
from config import APP_CONFIG, LOCAL_FILES

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
    # Get keywords from cloud
    keywords = cloud.get_keywords()
    
    # Get recent searches from cloud
    recent_searches = cloud.get_recent_searches(10)
    
    return render_template('index.html', 
                         total_keywords=len(keywords),
                         recent_searches=recent_searches,
                         app_version=APP_CONFIG['current_version'])


@app.route('/search', methods=['POST'])
def search():
    """Process search request"""
    data = request.get_json()
    client_names = data.get('clients', '')
    
    if not client_names:
        return jsonify({'success': False, 'message': 'No client names provided'})
    
    # Get keywords from cloud
    keywords = cloud.get_keywords()
    
    if not keywords:
        return jsonify({'success': False, 'message': 'No keywords available'})
    
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
        'message': f'Generated {len(results)} search link(s)',
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
