from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def handle_cookie_consent_popups(driver):
    """
    Enhanced function to detect and handle common cookie consent and privacy policy popups
    that might interfere with taking screenshots.
    
    Args:
        driver: Selenium WebDriver instance
    
    Returns:
        bool: True if a popup was found and handled, False otherwise
    """
    # Common button texts for accepting cookies/privacy policies
    accept_button_texts = [
        # Polish texts
        'Akceptuję', 'Akceptuje', 'Zgadzam się', 'Zgoda', 'OK', 'Agree', 
        'I agree', 'Accept all', 'Accept cookies', 'Akceptuję wszystkie',
        'Zaakceptuj', 'Got it', 'Rozumiem', 'Zamknij', 'Tylko niezbędne',
        'W porządku', 'Niezbędne', 'Necessary only', 'Only necessary',
        'Save settings', 'Zapisz ustawienia', 'Dbamy o twoja Prywatnosc',
        'Akceptuję cookies', 'Wyrażam zgodę', 'Zgadzam się na cookies',
        'Accept', 'Ok', 'Tak', 'Przejdź dalej', 'Kontynuuj', 'Przejdź do serwisu',
        'Dalej', 'Akceptuję i przechodzę do serwisu', 'Rozumiem', 'Zrozumiałem',
        'Acceptuję wszystkie', 'Zgadzam', 'Potwierdź wybór', 'Akceptuj wszystko'
    ]
    
    # Common button IDs and class names
    common_selectors = [
        # IDs
        "#cookieConsent button", "#gdpr-consent-accept", "#onetrust-accept-btn-handler",
        "#consent_prompt_submit", "#accept-cookies", "#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll",
        "#cookies-accept-all", "#rodo-accept", "#privacy-policy-accept", "#cookiePolicyOK",
        "#cookies-accept", "#cookie-accept-all", "#cookie-consent-accept", "#akceptuje",
        "#akceptuj-cookies", "#cookie-agreement-accept", "#cookies-agree", "#accept-all-cookies",
        "#accept-button", "#cookie-accept", "#cookie-notice-accept-button", "#cookie-permission-button",
        "#cookie-law-consent-btn", "#cookies-policy-consent", "#cookieConsentOK", 
        
        # Classes
        ".cookie-consent__accept", ".cookie-accept", ".consent-accept", ".cc-accept",
        ".agree-button", ".accept-cookies", ".accept_gdpr", ".privacy-policy-agree",
        ".cookie-law-button", ".cookie-accept-button", ".cookies-agreement-button",
        ".cookie-message__button", ".cookie-notice-accept", ".cookie-info__button",
        ".cookie-btn-accept", ".cookies-btn-accept", ".cookie-notice__agree",
        ".cookie-consent-button", ".cookie-consent__button", ".cookie-notice-button",
        ".btn-cookies-accept", ".js-cookie-consent-agree", ".js-accept-cookies"
    ]

    # Common Polish cookie consent container selectors
    cookie_container_selectors = [
        '.cookie-notice', '.cookies-popup', '.cookies-alert', '.cookie-info',
        '.cookie-message', '.cookie-bar', '.cookie-compliance', '.rodo-popup',
        '#cookieInfo', '#cookieNotice', '#cookiesInfo', '#cookieBanner',
        '#cookieConsent', '#cookies-notice', '#cookies-alert', '#rodo-alert',
        '.rodo-message', '.gdpr-cookie', '.cookie-law', '.cookie-container',
        '.cookie-banner', '.cookie-policy', '.cookies-container', '.cookie-disclaimer',
        '.cookie-consent', '.cookies-consent', '.cookie-warning', '.cookies-policy',
        '.cookie-message-container', '.cookie-accept-container', '.cookie-popup',
        '#cookies', '#cookies-wrapper', '#cookies-modal', '#cookiesBox', '#cookiePanel'
    ]

    # Import the necessary Selenium modules
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import time

    try:
        # Try JavaScript approach first - often most effective
        try:
            driver.execute_script("""
            // Common cookie banner selectors
            const selectors = [
                '.cookie-banner', '.cookie-consent', '.cookies-popup', '.cookie-notice',
                '.cookie-alert', '#cookieBanner', '#cookieConsent', '.rodo-popup',
                '#rodo-alert', '#cookies-notice', '#cookies-policy', '.cookies-container'
            ];
            
            // Find cookie banner containers
            let cookieContainers = [];
            for (let selector of selectors) {
                const elements = document.querySelectorAll(selector);
                if (elements.length) {
                    cookieContainers.push(...elements);
                }
            }
            
            // Common accept button texts
            const acceptTexts = ['akceptuj', 'accept', 'zgadzam', 'zgoda', 'rozumiem', 'ok', 'zamknij', 'kontynuuj'];
            
            // Try to find and click accept buttons in found containers
            for (let container of cookieContainers) {
                const buttons = container.querySelectorAll('button, a, div.button, span.button, input[type="button"]');
                
                for (let button of buttons) {
                    const buttonText = button.innerText.toLowerCase();
                    if (acceptTexts.some(text => buttonText.includes(text))) {
                        console.log('Clicking cookie button via JS:', buttonText);
                        button.click();
                        return true;
                    }
                }
            }
            
            // Try finding buttons by text content across the whole page
            const allButtons = document.querySelectorAll('button, a.button, div.button, input[type="button"]');
            for (let button of allButtons) {
                const buttonText = button.innerText.toLowerCase();
                if (buttonText.includes('cookie') || buttonText.includes('ciasteczk') || 
                    buttonText.includes('akceptuj') || buttonText.includes('zgadzam') || 
                    buttonText.includes('zaakceptuj') || buttonText.includes('accept')) {
                    console.log('Clicking button by text via JS:', buttonText);
                    button.click();
                    return true;
                }
            }
            
            // If all else fails, try to remove cookie banners entirely
            for (let container of cookieContainers) {
                if (container.style && container.style.display !== 'none') {
                    console.log('Removing cookie banner via JS');
                    container.style.display = 'none';
                    container.style.visibility = 'hidden';
                    container.style.opacity = '0';
                    container.style.zIndex = '-9999';
                    // Also try removing from DOM
                    if (container.parentNode) {
                        container.parentNode.removeChild(container);
                    }
                    return true;
                }
            }
            
            return false;
            """)
            print("Attempted to handle cookie popups via JavaScript")
            # Give a short pause after JavaScript execution
            time.sleep(1)
        except Exception as e:
            print(f"JavaScript cookie handling error: {e}")

        # Try to wait for and click consent using WebDriverWait first
        try:
            # Wait for any of the common cookie banner selectors to be visible 
            combined_selector = ', '.join(cookie_container_selectors)
            
            wait = WebDriverWait(driver, 3)  # Short timeout to not delay too much
            cookie_banner = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, combined_selector)))
            
            if cookie_banner and cookie_banner.is_displayed():
                # Look inside the cookie banner for accept buttons
                all_clickables = cookie_banner.find_elements(By.CSS_SELECTOR, 
                                                          'button, a, div[role="button"], input[type="button"], span.button')
                
                for element in all_clickables:
                    if element.is_displayed():
                        element_text = element.text.lower()
                        
                        # Try matching with our accept button texts
                        for accept_text in accept_button_texts:
                            if accept_text.lower() in element_text:
                                try:
                                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                                    element.click()
                                    print(f"Clicked cookie banner button with text: {element_text}")
                                    time.sleep(0.5)  # Short pause after clicking
                                    return True
                                except Exception as e:
                                    print(f"Error clicking cookie banner button: {e}")
        except Exception as e:
            # Timeout or other error, continue to other methods
            pass

        # Try more aggressive approach with direct searching
        for text in accept_button_texts:
            try:
                # Use contains() to find elements with the text
                xpath = f"//*[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{text.lower()}')]"
                elements = driver.find_elements(By.XPATH, xpath)
                
                # Try clicking each element that matches
                for element in elements:
                    if element.is_displayed():
                        try:
                            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                            element.click()
                            print(f"Clicked element containing text: {text}")
                            time.sleep(0.5)
                            return True
                        except Exception as click_err:
                            print(f"Failed to click element with text '{text}': {click_err}")
            except Exception as e:
                continue
        
        # Try clicking elements with common selector patterns
        for selector in common_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    if element.is_displayed():
                        try:
                            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                            element.click()
                            print(f"Clicked element matching selector: {selector}")
                            time.sleep(0.5)
                            return True
                        except Exception as e:
                            continue
            except:
                continue
        
        # Try iframes that might contain cookie consent dialogs
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        
        for iframe in iframes:
            try:
                # Check if this iframe looks like it contains a cookie consent
                iframe_id = iframe.get_attribute("id") or ""
                iframe_src = iframe.get_attribute("src") or ""
                
                cookie_related = any(keyword in (iframe_id + iframe_src).lower() 
                                    for keyword in ["cookie", "consent", "gdpr", "rodo", "privacy"])
                
                if cookie_related and iframe.is_displayed():
                    print(f"Found potentially cookie-related iframe: {iframe_id or iframe_src}")
                    
                    # Switch to the iframe
                    driver.switch_to.frame(iframe)
                    
                    # Look for buttons inside iframe
                    for text in accept_button_texts:
                        try:
                            xpath = f"//*[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{text.lower()}')]"
                            elements = driver.find_elements(By.XPATH, xpath)
                            
                            for element in elements:
                                if element.is_displayed():
                                    element.click()
                                    print(f"Clicked element in iframe with text: {text}")
                                    driver.switch_to.default_content()
                                    return True
                        except:
                            continue
                    
                    # Switch back to main content
                    driver.switch_to.default_content()
            except:
                # Ensure we always switch back to main content if there's an error
                driver.switch_to.default_content()
        
        # Last resort: try to remove cookie banners via JavaScript
        try:
            removed = driver.execute_script("""
            // List of selectors that might match cookie banners
            const cookieSelectors = [
                '.cookie-banner', '.cookie-consent', '.cookies-modal', '.cookie-notice',
                '.cookie-law', '.cookie-alert', '.cookieNotice', '.cookie-disclaimer',
                '#cookieConsent', '#cookieNotice', '#cookie-policy', '#cookies-alert',
                '#gdpr-banner', '.gdpr-modal', '.gdpr-content', '.gdpr-banner'
            ];
            
            let removed = false;
            
            // Try to remove each potential cookie banner
            for (let selector of cookieSelectors) {
                const elements = document.querySelectorAll(selector);
                for (let el of elements) {
                    if (el.offsetParent !== null) { // Check if visible
                        console.log('Removing cookie element:', selector);
                        el.remove();
                        removed = true;
                    }
                }
            }
            
            // Also remove any fixed position overlays that might be cookie related
            const overlays = document.querySelectorAll('div[style*="position: fixed"]');
            for (let overlay of overlays) {
                // Check if this is likely a cookie overlay
                if (overlay.offsetParent !== null) { // Check if visible
                    const text = overlay.innerText.toLowerCase();
                    if (text.includes('cookie') || text.includes('gdpr') || 
                        text.includes('rodo') || text.includes('privacy') || 
                        text.includes('ciasteczka') || text.includes('prywatn')) {
                        console.log('Removing fixed overlay that appears to be a cookie notice');
                        overlay.remove();
                        removed = true;
                    }
                }
            }

            // Also remove any modal backdrop/overlay
            const backdrops = document.querySelectorAll('.modal-backdrop, .overlay');
            for (let backdrop of backdrops) {
                if (backdrop.offsetParent !== null) { // Check if visible
                    backdrop.remove();
                    removed = true;
                }
            }
            
            // Finally, ensure body scrolling is enabled
            document.body.style.overflow = 'auto';
            document.body.style.position = 'static';
            
            return removed;
            """)
            
            if removed:
                print("Removed cookie banners via JavaScript")
                return True
        except Exception as e:
            print(f"Error removing cookie banners via JavaScript: {e}")

    except Exception as e:
        print(f"Error in cookie consent handling: {e}")

    return False

# Function to use before taking screenshots
def prepare_page_for_screenshot(driver, url):
    """
    Prepare a page for taking screenshot by loading it and handling any popups.
    
    Args:
        driver: Selenium WebDriver instance
        url: URL of the page to screenshot
    """
    driver.get(url)
    
    # Wait for page to load
    wait_for_page_load(driver)
    
    # Handle any cookie/privacy popups with retry
    if not handle_cookie_consent_popups(driver):
        # Some popups might appear after a delay, try again
        import time
        time.sleep(2)
        handle_cookie_consent_popups(driver)
    
    # Additional waiting to ensure popups are fully handled
    time.sleep(1)
    
    # Return the driver ready for screenshots
    return driver

def wait_for_page_load(driver, timeout=30):
    """
    Wait for page to completely load.
    
    Args:
        driver: Selenium WebDriver instance
        timeout: Maximum time to wait in seconds
    """
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException
    
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )
    except TimeoutException:
        print("Page load timeout - continuing anyway")

def initialize_browser(mode='desktop'):
    """
    Initialize a browser instance with appropriate settings for screenshots.
    
    Args:
        mode: 'desktop' or 'mobile' to determine viewport size
    
    Returns:
        WebDriver: Configured browser instance
    """
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--ignore-certificate-errors")
    
    # Set viewport size based on mode
    if mode.lower() == 'mobile':
        chrome_options.add_argument("--window-size=375,812")  # iPhone X resolution
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1")
    else:
        chrome_options.add_argument("--window-size=1920,1080")
    
    # Create driver
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    
    return driver