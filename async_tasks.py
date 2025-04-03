import json
import os
import threading
import time
import uuid
from datetime import datetime, timedelta

from screenshot_utils import visit_links_and_take_screenshots, is_valid_url

# Directory for storing task information
TASKS_DIR = 'data/tasks'
os.makedirs(TASKS_DIR, exist_ok=True)

# Task states
PENDING = 'PENDING'
STARTED = 'STARTED'
PROCESSING = 'PROCESSING'
SUCCESS = 'SUCCESS'
FAILURE = 'FAILURE'

# Dictionary to keep track of running threads
active_tasks = {}

def _save_task_status(task_id, state, info=None):
    """Save the current status of a task to a JSON file."""
    if info is None:
        info = {}
        
    task_data = {
        'id': task_id,
        'state': state,
        'updated_at': datetime.now().isoformat(),
        'info': info
    }
    
    task_file = os.path.join(TASKS_DIR, f"{task_id}.json")
    
    with open(task_file, 'w') as f:
        json.dump(task_data, f)

def _get_task_status_from_file(task_id):
    """Read task status from file."""
    task_file = os.path.join(TASKS_DIR, f"{task_id}.json")
    
    if not os.path.exists(task_file):
        return {'id': task_id, 'state': 'UNKNOWN', 'info': {'error': 'Task not found'}}
    
    try:
        with open(task_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        return {'id': task_id, 'state': 'ERROR', 'info': {'error': f"Error reading task status: {str(e)}"}}

def take_screenshots_thread(task_id, url, device_type, max_links=50):
    """Background thread function for taking screenshots."""
    try:
        # Update task status to started
        _save_task_status(task_id, STARTED, {
            'status': 'Starting screenshot process',
            'domain': url,
            'device': device_type
        })
        
        # Start processing screenshots
        _save_task_status(task_id, PROCESSING, {
            'status': 'Processing screenshots',
            'domain': url,
            'device': device_type
        })
        
        # Actually take screenshots
        visit_links_and_take_screenshots(url, device_type, max_links)
        
        # Mark task as successful when done
        _save_task_status(task_id, SUCCESS, {
            'status': 'Completed successfully',
            'domain': url,
            'device': device_type
        })
        
    except Exception as e:
        # Mark task as failed if any error occurs
        _save_task_status(task_id, FAILURE, {
            'status': 'Failed',
            'error': str(e),
            'domain': url,
            'device': device_type
        })
    
    finally:
        # Clean up the thread reference
        if task_id in active_tasks:
            del active_tasks[task_id]

def take_screenshots_async(url, device_type, max_links=50):
    """Start a background task to take screenshots and return task ID."""
    try:
        url = is_valid_url(url)
    except Exception as e:
        raise ValueError(f"Invalid URL: {str(e)}")
    
    # Generate a unique task ID
    task_id = str(uuid.uuid4())
    
    # Create initial task status
    _save_task_status(task_id, PENDING, {
        'status': 'Task created, waiting to start',
        'domain': url,
        'device': device_type
    })
    
    # Start a new thread for the task
    task_thread = threading.Thread(
        target=take_screenshots_thread,
        args=(task_id, url, device_type, max_links),
        daemon=True
    )
    
    # Store the thread reference
    active_tasks[task_id] = task_thread
    
    # Start the thread
    task_thread.start()
    
    return task_id

def get_task_status(task_id):
    """Get the current status of a task."""
    return _get_task_status_from_file(task_id)

def cleanup_old_tasks(max_age_hours=24):
    """Remove task files older than max_age_hours."""
    try:
        now = datetime.now()
        count = 0
        
        for filename in os.listdir(TASKS_DIR):
            if filename.endswith('.json'):
                file_path = os.path.join(TASKS_DIR, filename)
                
                try:
                    # Check file modification time
                    file_modified = datetime.fromtimestamp(os.path.getmtime(file_path))
                    if now - file_modified > timedelta(hours=max_age_hours):
                        os.remove(file_path)
                        count += 1
                except Exception as e:
                    print(f"Error cleaning up task file {filename}: {str(e)}")
                    
        return count
    except Exception as e:
        print(f"Error during task cleanup: {str(e)}")
        return 0

def get_all_active_tasks():
    """Return a list of all currently tracked tasks."""
    tasks = []
    
    for filename in os.listdir(TASKS_DIR):
        if not filename.endswith('.json'):
            continue
            
        task_id = filename[:-5]  # Remove .json extension
        
        try:
            task_data = _get_task_status_from_file(task_id)
            tasks.append(task_data)
        except Exception as e:
            print(f"Error reading task {task_id}: {str(e)}")
            
    return tasks

def cancel_task(task_id):
    """Mark a task as canceled if it's still running."""
    if task_id in active_tasks:
        # Cannot actually stop the thread safely in Python,
        # but we can mark it as canceled in the status file
        _save_task_status(task_id, 'CANCELED', {
            'status': 'Task was manually canceled',
        })
        return True
    else:
        return False
