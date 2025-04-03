import json
import os
import time
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# File paths for data storage
DATA_DIR = 'data'
DOMAINS_FILE = os.path.join(DATA_DIR, 'domains.json')
USERS_FILE = os.path.join(DATA_DIR, 'users.json')
SCREENSHOTS_FILE = os.path.join(DATA_DIR, 'screenshots.json')

# Ensure the data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Initialize data files if they don't exist
def init_data_files():
    """Initialize the JSON data files if they don't exist."""
    # Domains file
    if not os.path.exists(DOMAINS_FILE):
        with open(DOMAINS_FILE, 'w') as f:
            json.dump({"domains": []}, f)
    
    # Users file - create with default admin user
    if not os.path.exists(USERS_FILE):
        default_admin = {
            "admin": {
                "password_hash": generate_password_hash("Snaply2025!"),
                "role": "admin",
                "created_at": datetime.now().isoformat()
            }
        }
        with open(USERS_FILE, 'w') as f:
            json.dump({"users": default_admin}, f)
    
    # Screenshots file
    if not os.path.exists(SCREENSHOTS_FILE):
        with open(SCREENSHOTS_FILE, 'w') as f:
            json.dump({"screenshots": []}, f)

# Domain functions
def get_domains():
    """Get all domains from the domains file."""
    if not os.path.exists(DOMAINS_FILE):
        return []
    
    with open(DOMAINS_FILE, 'r') as f:
        data = json.load(f)
    
    return data.get("domains", [])

def save_domains(domains):
    """Save domains to the domains file."""
    # Remove duplicates
    unique_domains = list(set(domains))
    
    # Create data structure
    data = {"domains": unique_domains}
    
    # Save to file
    with open(DOMAINS_FILE, 'w') as f:
        json.dump(data, f)

def add_domain(domain_name):
    """Add a new domain if it doesn't already exist."""
    domains = get_domains()
    if domain_name not in domains:
        domains.append(domain_name)
        save_domains(domains)
        return True
    return False

def remove_domain(domain_name):
    """Remove a domain if it exists."""
    domains = get_domains()
    if domain_name in domains:
        domains.remove(domain_name)
        save_domains(domains)
        return True
    return False

def update_domain(old_name, new_name):
    """Update a domain name."""
    domains = get_domains()
    if old_name in domains and new_name not in domains:
        domains[domains.index(old_name)] = new_name
        save_domains(domains)
        return True
    return False

# User functions
def get_users():
    """Get all users from the users file."""
    if not os.path.exists(USERS_FILE):
        return {}
    
    with open(USERS_FILE, 'r') as f:
        data = json.load(f)
    
    return data.get("users", {})

def save_users(users_dict):
    """Save users to the users file."""
    data = {"users": users_dict}
    
    with open(USERS_FILE, 'w') as f:
        json.dump(data, f)

def add_user(username, password, role="user"):
    """Add a new user."""
    users = get_users()
    if username not in users:
        users[username] = {
            "password_hash": generate_password_hash(password),
            "role": role,
            "created_at": datetime.now().isoformat()
        }
        save_users(users)
        return True
    return False

def check_password(username, password):
    """Check if the password for a user is correct."""
    users = get_users()
    if username in users:
        return check_password_hash(users[username]['password_hash'], password)
    return False

def get_user_role(username):
    """Get the role of a user."""
    users = get_users()
    if username in users:
        return users[username].get('role', 'user')
    return None

# Screenshot tracking functions
def get_screenshots():
    """Get all screenshot records."""
    if not os.path.exists(SCREENSHOTS_FILE):
        return []
    
    with open(SCREENSHOTS_FILE, 'r') as f:
        data = json.load(f)
    
    return data.get("screenshots", [])

def save_screenshot_record(domain, device_type, path):
    """Save a record of a screenshot that was taken."""
    screenshots = get_screenshots()
    
    # Create new record
    new_record = {
        "id": int(time.time() * 1000),  # Use timestamp as ID
        "domain": domain,
        "device_type": device_type,
        "path": path,
        "created_at": datetime.now().isoformat()
    }
    
    # Add to list
    screenshots.append(new_record)
    
    # Save to file
    with open(SCREENSHOTS_FILE, 'w') as f:
        json.dump({"screenshots": screenshots}, f)
    
    return new_record

# Initialize data files on import
init_data_files()
