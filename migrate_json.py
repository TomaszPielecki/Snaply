#!/usr/bin/env python3
import json
import os
import sys
from dotenv import load_dotenv

# Import data storage functions
from data_storage import (
    DOMAINS_FILE, USERS_FILE, SCREENSHOTS_FILE,
    get_domains, save_domains, add_domain,
    get_users, add_user
)

def migrate_from_json_file():
    """Migrate domains from data.json to the new JSON storage."""
    print("Starting migration from data.json to new storage...")
    
    # Check if data.json exists
    old_domains_file = 'data.json'
    if not os.path.exists(old_domains_file):
        print(f"Error: {old_domains_file} not found.")
        return False
    
    # Read domains from the JSON file
    try:
        with open(old_domains_file, 'r') as f:
            data = json.load(f)
            domains = data.get('domains', [])
        
        if not domains:
            print("No domains found in data.json")
            return False
            
        print(f"Found {len(domains)} domains in data.json")
    except json.JSONDecodeError:
        print(f"Error: {old_domains_file} contains invalid JSON.")
        return False
    except Exception as e:
        print(f"Error reading {old_domains_file}: {str(e)}")
        return False
    
    # Now migrate to new storage
    added_domains = []
    
    for domain_name in domains:
        if domain_name not in get_domains():
            if add_domain(domain_name):
                added_domains.append(domain_name)
            else:
                print(f"Error adding domain: {domain_name}")
    
    print(f"Successfully migrated {len(added_domains)} domains to the new storage")
    if added_domains:
        print("Migrated domains:")
        for domain in added_domains:
            print(f"  - {domain}")
    
    return True

def migrate_users_file():
    """Migrate users from old users.json if it exists."""
    old_users_file = 'users.json'
    if not os.path.exists(old_users_file):
        print(f"No old users file found at {old_users_file}")
        return False
    
    try:
        with open(old_users_file, 'r') as f:
            users = json.load(f)
        
        migrated_count = 0
        
        # Assuming the structure is just a dictionary of users
        for username, user_data in users.items():
            # The new structure requires storing the password hash
            # For simplicity, we'll just assume the password in old file 
            # is already a hash and use it directly
            password_hash = user_data.get('password', 'default_password_hash')
            role = user_data.get('role', 'user')
            
            # Get current users
            current_users = get_users()
            
            # Only add if not already exists
            if username not in current_users:
                # We can't add with hash directly, so we'll modify the users data
                current_users[username] = {
                    "password_hash": password_hash,
                    "role": role
                }
                migrated_count += 1
        
        # Now save the users data back
        with open(USERS_FILE, 'w') as f:
            json.dump({"users": current_users}, f)
        
        print(f"Migrated {migrated_count} users from old users file")
        return True
    
    except Exception as e:
        print(f"Error migrating users: {str(e)}")
        return False

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    
    # Check the operation mode
    if len(sys.argv) > 1 and sys.argv[1] == '--users':
        migrate_users_file()
    else:
        # Perform domain migration by default
        success = migrate_from_json_file()
        
        if success:
            print("\nMigration completed successfully.")
        else:
            print("\nMigration completed with errors.")
            sys.exit(1)
