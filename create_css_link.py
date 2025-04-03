import os
from os import path

def create_symlink():
    """Create a symlink from main.css to style.css"""
    styles_dir = path.join('static', 'styles')
    
    # Ensure directory exists
    if not path.exists(styles_dir):
        os.makedirs(styles_dir)
    
    # Path to the existing CSS file
    style_css_path = path.join(styles_dir, 'style.css')
    
    # Path for the symlink
    main_css_path = path.join(styles_dir, 'main.css')
    
    # Create a copy or symlink
    if not path.exists(main_css_path):
        if os.name == 'nt':  # Windows
            try:
                # Try to create a symlink (requires admin privileges)
                os.symlink(style_css_path, main_css_path)
                print(f"Symlink created from {main_css_path} to {style_css_path}")
            except:
                # If that fails, just copy the file
                import shutil
                if path.exists(style_css_path):
                    shutil.copy2(style_css_path, main_css_path)
                    print(f"Copied {style_css_path} to {main_css_path}")
                else:
                    # Create an empty file
                    with open(main_css_path, 'w') as f:
                        f.write('/* CSS styles for Snaply */\n')
                    print(f"Created empty CSS file: {main_css_path}")
        else:  # Unix/Linux/Mac
            if path.exists(style_css_path):
                os.symlink(style_css_path, main_css_path)
                print(f"Symlink created from {main_css_path} to {style_css_path}")
            else:
                # Create empty file
                with open(main_css_path, 'w') as f:
                    f.write('/* CSS styles for Snaply */\n')
                print(f"Created empty CSS file: {main_css_path}")

if __name__ == "__main__":
    create_symlink()
