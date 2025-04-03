import os
import shutil

def fix_template_cases():
    """Create lowercase versions of templates to fix case sensitivity issues"""
    templates_dir = 'templates'
    
    # Check if FiltrScreen.html exists and make a lowercase copy
    filtr_screen = os.path.join(templates_dir, 'FiltrScreen.html')
    filtrscreen_lower = os.path.join(templates_dir, 'filtrscreen.html')
    
    if os.path.exists(filtr_screen) and not os.path.exists(filtrscreen_lower):
        shutil.copy2(filtr_screen, filtrscreen_lower)
        print(f"Created lowercase copy: {filtrscreen_lower}")
    
    # Make sure dashboard.html and login.html exist
    for template in ['dashboard.html', 'login.html']:
        template_path = os.path.join(templates_dir, template)
        if not os.path.exists(template_path):
            print(f"WARNING: Template {template} not found!")

if __name__ == "__main__":
    fix_template_cases()
