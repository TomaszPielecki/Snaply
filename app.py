import json
import logging
import os
from datetime import datetime, timedelta
from functools import wraps
from urllib.parse import urlparse

from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, session
from flask import send_file
from flask import send_from_directory
from flask_socketio import SocketIO
from werkzeug.security import check_password_hash
from dotenv import load_dotenv

# Import new data storage functions instead of database models
from data_storage import (
    get_domains, save_domains, add_domain, remove_domain, update_domain,
    get_users, add_user, check_password, get_user_role
)

from filterScreen import find_screenshots_by_date
from forms import AddDomainForm, LoginForm, RegisterForm
from screenshot_utils import is_valid_url, visit_links_and_take_screenshots, create_directory_for_domain, get_screenshots
from async_tasks import take_screenshots_async, get_task_status, cleanup_old_tasks

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'fallback_secret_key_only_for_development')
socketio = SocketIO(app)

# Paths to files
LOG_FILE = 'logs/logfile.log'
MAX_LOG_LINES = 1000
SCREENSHOT_DIR = 'static/screenshots'
BASE_SCREENSHOT_FOLDER = 'static/screenshots'

# Configure logging
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Helper functions
def get_logs():
    """Get application logs with proper formatting."""
    ensure_log_directory()
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r', encoding='utf-8', errors='replace') as file:
            logs = file.readlines()
        
        # Clean log entries (remove extra whitespace, newlines)
        logs = [log.strip() for log in logs if log.strip()]
        logs.reverse()  # Most recent first
        
        # Format any entries missing timestamps (some Flask log entries have different format)
        formatted_logs = []
        for log in logs:
            # If it's an entry without timestamp, prefix with current date
            if not (log.startswith('20') and ' - ' in log):
                if log.startswith('INFO') or log.startswith('WARNING') or log.startswith('ERROR'):
                    # It's already a basic log entry without timestamp
                    formatted_logs.append(log)
                else:
                    # It's some other content, prefix with INFO
                    formatted_logs.append(f"INFO - {log}")
            else:
                formatted_logs.append(log)
                
        return formatted_logs
    else:
        return []

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Zaloguj się, aby uzyskać dostęp do tej strony.', 'danger')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Zaloguj się, aby uzyskać dostęp do tej strony.', 'danger')
            return redirect(url_for('login', next=request.url))
        
        role = get_user_role(session['user'])
        if role != 'admin':
            flash('Nie masz uprawnień do tej strony.', 'danger')
            return redirect(url_for('dashboard'))
        
        return f(*args, **kwargs)
    return decorated_function

# Authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        users = get_users()
        
        if username in users and check_password(username, password):
            session['user'] = username
            session['role'] = users[username].get('role', 'user')
            flash(f'Witaj, {username}!', 'success')
            
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('dashboard'))
        else:
            flash('Nieprawidłowa nazwa użytkownika lub hasło.', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
@admin_required
def register():
    form = RegisterForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        role = form.role.data
        
        if add_user(username, password, role):
            flash(f'Użytkownik {username} został zarejestrowany.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash(f'Użytkownik {username} już istnieje.', 'danger')
    
    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    if 'user' in session:
        flash(f'Wylogowano użytkownika {session["user"]}.', 'success')
        session.pop('user', None)
        session.pop('role', None)
    return redirect(url_for('login'))

# Application routes
@app.route('/')
@login_required
def dashboard():
    write_log("Accessed dashboard")
    logs = get_logs()
    domains = get_domains()
    screenshots = get_screenshots(SCREENSHOT_DIR)
    screenshot_files = [f for f in os.listdir(SCREENSHOT_DIR) if os.path.isfile(os.path.join(SCREENSHOT_DIR, f))]
    screenshot_count = len(screenshot_files)
    log_count = len(logs)
    domain_count = len(domains)

    return render_template(
        'dashboard.html',  # Make sure this matches the actual filename (case-sensitive)
        log_count=log_count,
        domain_count=domain_count,
        screenshot_count=screenshot_count,
        logs=logs,
        screenshots=screenshots,
        domains=domains,
        user=session.get('user'),
        role=session.get('role')
    )

@app.route('/manage_pages', methods=['GET', 'POST'])
@login_required
def manage_domains():
    form = AddDomainForm()
    domains = get_domains()

    if form.validate_on_submit():
        domain = form.new_domain.data
        if domain:
            if add_domain(domain):
                flash('Domain added successfully!', 'success')
            else:
                flash('Domain already exists.', 'warning')
        else:
            flash('Please provide all required information.', 'danger')

    return render_template('manage_pages.html', domains=domains, add_domain_form=form)

@app.route('/domains/delete/<domain>', methods=['POST'])
@admin_required
def delete_domain(domain):
    if remove_domain(domain):
        flash('Domain deleted successfully!', 'success')
    else:
        flash('Domain does not exist.', 'danger')

    return redirect(url_for('manage_domains'))

@app.route('/domains/edit/<old_domain>', methods=['GET', 'POST'])
def edit_domain(old_domain):
    form = AddDomainForm()
    domains = get_domains()

    if request.method == 'POST' and form.validate_on_submit():
        new_domain = form.new_domain.data
        if update_domain(old_domain, new_domain):
            flash('Domain updated successfully!', 'success')
        else:
            flash('Domain update failed. Either the original domain does not exist or the new domain already exists.', 'danger')
        return redirect(url_for('manage_domains'))

    form.new_domain.data = old_domain
    return render_template('edit_domain.html', form=form, old_domain=old_domain)

@app.route('/copy_domain/<domain>', methods=['POST'])
def copy_domain(domain):
    try:
        domains = get_domains()
        if domain not in domains:
            flash("Domain not found!", 'danger')
            return redirect(url_for('manage_domains'))

        new_domain = f"{domain}_copy"
        if new_domain in domains:
            flash(f"Domain '{new_domain}' already exists!", 'danger')
            return redirect(url_for('manage_domains'))

        domains.append(new_domain)
        save_domains(domains)
        flash(f"Domain '{domain}' copied as '{new_domain}'.", 'success')
    except Exception as e:
        flash(f"Error copying domain: {str(e)}", 'danger')

    return redirect(url_for('manage_domains'))

@app.route('/filtrScreen')
def gallery():
    screenshots_dir = os.path.join(app.static_folder, 'screenshots')
    domains = get_domains()
    today_date = datetime.now().strftime('%Y-%m-%d')
    return render_template('filtrScreen.html', domains=domains, today_date=today_date)

@app.route('/screenshots/delete/<folder>/<screenshot>', methods=['POST'])
def delete_screenshot_from_folder(folder, screenshot):
    screenshot_path = os.path.join(SCREENSHOT_DIR, folder, screenshot)
    if os.path.exists(screenshot_path):
        os.remove(screenshot_path)
        flash('Screenshot deleted successfully!', 'success')
    else:
        flash('Screenshot does not exist.', 'danger')
    return redirect(url_for('many_screen', folder=folder))

@app.route('/logs/delete', methods=['POST'])
def delete_logs_route():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as file:
            lines = file.readlines()
        if len(lines) >= 500:
            lines = lines[500:]
            with open(LOG_FILE, 'w') as file:
                file.writelines(lines)
            return jsonify({"success": True})
        else:
            return jsonify({"success": False, "error": "Log count is less than 500."}), 400
    else:
        return jsonify({"success": False, "error": "Log file does not exist."}), 404

def setup_logging():
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def write_log(message, level=logging.INFO):
    ensure_log_directory()
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as file:
            lines = file.readlines()
        lines.reverse()
        if len(lines) >= MAX_LOG_LINES:
            lines = lines[:MAX_LOG_LINES - 1]
    else:
        lines = []

    lines.insert(0, f"{logging.getLevelName(level)} - {message}\n")

    with open(LOG_FILE, 'w') as file:
        file.writelines(lines)

def ensure_log_directory():
    log_dir = os.path.dirname(LOG_FILE)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

@app.route('/manyScreen')
@app.route('/manyScreen/<folder>')
def many_screen(folder=None):
    if folder:
        folder_path = os.path.join(SCREENSHOT_DIR, folder)
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            screenshots = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        else:
            screenshots = []
        return render_template('manyScreen.html', folder=folder, screenshots=screenshots)
    else:
        screenshot_dirs = [d for d in os.listdir(SCREENSHOT_DIR) if os.path.isdir(os.path.join(SCREENSHOT_DIR, d))]
        domains = get_domains()
        screenshots = get_screenshots(SCREENSHOT_DIR)
        return render_template('manyScreen.html', screenshot_dirs=screenshot_dirs, domains=domains,
                               screenshots=screenshots)

@app.route('/screenshots/delete/<screenshot>', methods=['POST'])
def delete_screenshots(screenshot):
    screenshot_path = os.path.join(SCREENSHOT_DIR, screenshot)
    if os.path.exists(screenshot_path):
        os.remove(screenshot_path)
        flash('Screenshot deleted successfully!', 'success')
    else:
        flash('Screenshot does not exist.', 'danger')
    return redirect(url_for('screenshots_route'))

@app.route('/create_domain_folder', methods=['POST'])
def create_domain_folder():
    url = request.form.get('url')
    if url:
        domain_name = urlparse(url).netloc.replace('www.', '').replace(':', '_')
        create_directory_for_domain(domain_name)
        flash('Folder created successfully!', 'success')
    else:
        flash('Please provide a valid URL.', 'danger')
    return redirect(url_for('dashboard'))

@app.route('/search_screenshots', methods=['GET', 'POST'])
def search_screenshots():
    if request.method == 'POST':
        start_date_str = request.form.get('start_date')
        end_date_str = request.form.get('end_date')
        domain = request.form.get('domain')
        device_type = request.form.get('device_type')

        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        except ValueError:
            flash('Invalid date format. Please use YYYY-MM-DD.', 'danger')
            return redirect(url_for('search_screenshots'))

        screenshots_dir = os.path.join(app.static_folder, 'screenshots')
        filtered_screenshots = []

        for folder in os.listdir(screenshots_dir):
            folder_path = os.path.join(screenshots_dir, folder)
            if os.path.isdir(folder_path):
                subfolders = ['desktop', 'mobile'] if not device_type else [device_type]
                for subfolder in subfolders:
                    subfolder_path = os.path.join(folder_path, subfolder)
                    if os.path.exists(subfolder_path) and os.path.isdir(subfolder_path):
                        screenshots = find_screenshots_by_date(subfolder_path, start_date, end_date, domain,
                                                               device_type)
                        filtered_screenshots.extend(screenshots)

        return render_template('filtrScreen.html', screenshots=filtered_screenshots,
                               start_date=start_date_str, end_date=end_date_str, domain=domain, device_type=device_type)

    domains = get_domains()
    return render_template('filtrScreen.html', domains=domains)

@app.route('/get_screenshots', methods=['GET'])
def get_screenshots_route():
    screenshots_dir = os.path.join(app.static_folder, 'screenshots')
    screenshots = get_screenshots(screenshots_dir)
    return jsonify(screenshots)

@app.route('/download/<path:filename>')
def download_file(filename):
    screenshots_dir = os.path.join(app.static_folder, 'screenshots')
    return send_from_directory(screenshots_dir, filename, as_attachment=True)

@app.route('/api/search_screenshots', methods=['POST'])
def api_search_screenshots():
    try:
        start_date_str = request.form.get('start_date')
        end_date_str = request.form.get('end_date')
        domain_filter = request.form.get('domain')
        device_type = request.form.get('device_type')

        logging.info(f"Screenshot search - Parameters: start_date={start_date_str}, end_date={end_date_str}, domain={domain_filter}, device_type={device_type}")

        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
            # Add one day to end_date to include the end date in results
            end_date = datetime.combine(end_date.date() + timedelta(days=1), datetime.min.time())
        except ValueError as e:
            logging.error(f"Date parsing error: {str(e)}")
            return jsonify({"error": f"Invalid date format: {str(e)}. Please use YYYY-MM-DD."}), 400

        screenshots_dir = os.path.join(app.static_folder, 'screenshots')
        filtered_screenshots = []

        # Check if screenshots directory exists
        if not os.path.exists(screenshots_dir):
            logging.warning(f"Screenshots directory not found: {screenshots_dir}")
            return jsonify({"screenshots": []})

        # Iterate through domain directories
        for domain_dir in os.listdir(screenshots_dir):
            domain_path = os.path.join(screenshots_dir, domain_dir)
            
            # Skip if not directory or doesn't match domain filter
            if not os.path.isdir(domain_path):
                continue
                
            if domain_filter and domain_filter.lower() not in domain_dir.lower():
                continue

            # Filter by device type
            device_dirs = []
            if device_type:
                if os.path.isdir(os.path.join(domain_path, device_type.lower())):
                    device_dirs.append(device_type.lower())
            else:
                # Check both device types if no filter is applied
                if os.path.isdir(os.path.join(domain_path, 'desktop')):
                    device_dirs.append('desktop')
                if os.path.isdir(os.path.join(domain_path, 'mobile')):
                    device_dirs.append('mobile')

            # Check each device directory
            for device_dir in device_dirs:
                device_path = os.path.join(domain_path, device_dir)
                
                # List all files in the device directory
                for screenshot in os.listdir(device_path):
                    file_path = os.path.join(device_path, screenshot)
                    
                    # Skip directories
                    if not os.path.isfile(file_path):
                        continue
                        
                    # Check if file extension is an image
                    if not screenshot.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                        continue
                        
                    # Check file date
                    file_date = datetime.fromtimestamp(os.path.getmtime(file_path))
                    
                    if start_date <= file_date <= end_date:
                        relative_path = os.path.join(domain_dir, device_dir, screenshot)
                        filtered_screenshots.append(relative_path.replace('\\', '/'))

        logging.info(f"Screenshot search - Found {len(filtered_screenshots)} results")
        return jsonify({"screenshots": filtered_screenshots})
        
    except Exception as e:
        logging.exception("Error in screenshot search API")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route('/screenshots/delete', methods=['POST'])
def delete_screenshot():
    screenshot = request.args.get('screenshot')
    screenshot_path = os.path.join(SCREENSHOT_DIR, screenshot)
    if os.path.exists(screenshot_path):
        os.remove(screenshot_path)
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": "Screenshot does not exist."}), 404

@app.route('/zrobscreen', methods=['POST'])
@login_required
def zrobscreen():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400
    if 'domain' not in data:
        return jsonify({"error": "Missing 'domain' field"}), 400
    if 'deviceType' not in data:
        return jsonify({"error": "Missing 'deviceType' field"}), 400
    if data['deviceType'] not in ['mobile', 'desktop']:
        return jsonify({"error": "Invalid device type. Must be 'mobile' or 'desktop'"}), 400

    domain = data['domain']
    device_type = data['deviceType']
    try:
        # Ensure URL has proper format
        if not domain.startswith('http://') and not domain.startswith('https://'):
            domain = f"http://{domain}"
        
        write_log(f"Starting screenshot task for {domain} on {device_type}")
        
        # Run task in a separate thread
        task_id = take_screenshots_async(domain, device_type, max_links=50)
        write_log(f"User {session.get('user')} initiated screenshots task {task_id} for {domain} on {device_type}")
        
        return jsonify({
            "success": True,
            "task_id": task_id,
            "message": f"Screenshot task started for {domain} ({device_type})"
        }), 202
    except Exception as e:
        write_log(f"Error scheduling screenshot task: {str(e)}", level=logging.ERROR)
        return jsonify({"error": str(e)}), 500

@app.route('/task_status/<task_id>')
@login_required
def task_status(task_id):
    status = get_task_status(task_id)
    return jsonify(status)

# Simplified API endpoints
@app.route('/api/domains', methods=['GET'])
@login_required
def api_get_domains():
    """API endpoint to get all domains"""
    domains = get_domains()
    return jsonify({'domains': domains})

@app.route('/api/domains', methods=['POST'])
@login_required
def api_add_domain():
    """API endpoint to add a new domain"""
    data = request.json
    if not data or 'domain' not in data:
        return jsonify({'success': False, 'error': 'Missing domain name'}), 400
    
    domain_name = data['domain']
    # Validate domain format
    import re
    if not re.match(r'^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$', domain_name):
        return jsonify({'success': False, 'error': 'Invalid domain format'}), 400
    
    # Check if domain already exists
    if domain_name in get_domains():
        return jsonify({'success': False, 'error': 'Domain already exists'}), 400
    
    # Add the new domain
    if add_domain(domain_name):
        return jsonify({'success': True, 'domain': domain_name})
    else:
        return jsonify({'success': False, 'error': 'Failed to add domain'}), 500

@app.route('/api/domains/<domain_name>', methods=['PUT'])
@login_required
def api_update_domain(domain_name):
    """API endpoint to update a domain"""
    data = request.json
    if not data or 'domain' not in data:
        return jsonify({'success': False, 'error': 'Missing new domain name'}), 400
    
    new_domain_name = data['domain']
    # Validate domain format
    import re
    if not re.match(r'^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$', new_domain_name):
        return jsonify({'success': False, 'error': 'Invalid domain format'}), 400
    
    # Check if domain exists
    if domain_name not in get_domains():
        return jsonify({'success': False, 'error': 'Domain not found'}), 404
    
    # Update the domain
    if update_domain(domain_name, new_domain_name):
        return jsonify({'success': True, 'domain': new_domain_name})
    else:
        return jsonify({'success': False, 'error': 'Failed to update domain'}), 500

@app.route('/api/domains/<domain_name>', methods=['DELETE'])
@admin_required
def api_delete_domain(domain_name):
    """API endpoint to delete a domain"""
    # Check if domain exists
    if domain_name not in get_domains():
        return jsonify({'success': False, 'error': 'Domain not found'}), 404
    
    # Delete the domain
    if remove_domain(domain_name):
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Failed to delete domain'}), 500

# Before the if __name__ == '__main__' block, add this initialization code
def ensure_css_files():
    """Make sure all necessary CSS files exist"""
    styles_dir = os.path.join('static', 'styles')
    css_dir = os.path.join('static', 'css')
    
    # Ensure directories exist
    os.makedirs(styles_dir, exist_ok=True)
    os.makedirs(css_dir, exist_ok=True)
    
    # Check for main.css
    main_css_path = os.path.join(styles_dir, 'main.css')
    style_css_path = os.path.join(styles_dir, 'style.css')
    
    # If main.css doesn't exist but style.css does, copy it
    if not os.path.exists(main_css_path) and os.path.exists(style_css_path):
        import shutil
        shutil.copy2(style_css_path, main_css_path)
        print(f"Created main.css from existing style.css")
    
    # Ensure animations.css exists
    animations_css_path = os.path.join(css_dir, 'animations.css')
    if not os.path.exists(animations_css_path):
        with open(animations_css_path, 'w') as f:
            f.write('/* Animations for Snaply */\n')
            print(f"Created empty animations.css file")

def ensure_directories():
    """Make sure all necessary directories exist for the application."""
    directories = [
        'static/images',
        'static/screenshots',
        'static/styles',
        'static/css',
        'logs',
        'data',
        'data/tasks',
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    # Create placeholder image if needed
    placeholder_image = os.path.join('static', 'images', 'placeholder.png')
    if not os.path.exists(placeholder_image):
        try:
            from PIL import Image, ImageDraw
            img = Image.new('RGB', (400, 300), color=(240, 240, 240))
            d = ImageDraw.Draw(img)
            d.text((150, 150), "No Image", fill=(100, 100, 100))
            img.save(placeholder_image)
            print(f"Created placeholder image: {placeholder_image}")
        except ImportError:
            print("PIL not available to create placeholder image")
            with open(placeholder_image, 'wb') as f:
                # Create a very simple 1x1 transparent pixel PNG
                f.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\rIDAT\x08\xd7c\xf8\xff\xff?\x03\x00\x08\xfc\x02\xfe\xa7\x9a\xa0\xa0\x00\x00\x00\x00IEND\xaeB`\x82')

if __name__ == '__main__':
    setup_logging()
    write_log("Application started")
    
    # Initialize CSS files and directories
    ensure_css_files()
    ensure_directories()
    
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    
    import socket
    def get_local_ip():
        try:
            # Create a socket connection to an external server to determine local IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception:
            return "unknown"
    
    host = '0.0.0.0'  # Listen on all network interfaces
    port = 5000
    
    print("\nSnaply is running!")
    print(f" * Local URL: http://127.0.0.1:{port}")
    print(f" * Network URL: http://{get_local_ip()}:{port}")
    print(f" * Access the application from any device on your network using your computer's IP address\n")
    
    socketio.run(app, debug=True, host=host, port=port)