from utils.browser import initialize_browser, prepare_page_for_screenshot

def take_screenshot(url, save_path, mode='desktop'):
    """
    Take a screenshot of the specified URL and save it to the given path.
    
    Args:
        url: URL of the webpage to screenshot
        save_path: Path where the screenshot should be saved
        mode: 'desktop' or 'mobile' to determine viewport size
    
    Returns:
        bool: True if the screenshot was taken successfully, False otherwise
    """
    driver = None
    try:
        # Initialize the browser with appropriate settings
        driver = initialize_browser(mode)
        
        # Prepare the page by handling popups before taking screenshot
        driver = prepare_page_for_screenshot(driver, url)
        
        # Take the screenshot
        driver.save_screenshot(save_path)
        
        return True
        
    except Exception as e:
        print(f"Error taking screenshot: {e}")
        return False
        
    finally:
        if driver:
            driver.quit()