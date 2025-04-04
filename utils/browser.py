def handle_cookie_consent_popups(driver):
    """
    Detect and handle common cookie consent and privacy policy popups
    that might interfere with taking screenshots.
    
    Args:
        driver: Selenium WebDriver instance
    
    Returns:
        bool: True if a popup was found and handled, False otherwise
    """
    # Common button texts for accepting cookies/privacy policies
    accept_button_texts = [
        'Accept', 'Akceptuję', 'Akceptuje', 'Zgadzam się', 'Zgoda', 'OK', 'Agree', 
        'I agree', 'Accept all', 'Accept cookies', 'Akceptuję wszystkie',
        'Zaakceptuj', 'Got it', 'Rozumiem', 'Zamknij', 'Tylko niezbędne',
        'W porządku', 'Niezbędne', 'Necessary only', 'Only necessary',
        'Save settings', 'Zapisz ustawienia', 'Dbamy o twoja Prywatnosc',
        'Akceptuję cookies', 'Wyrażam zgodę', 'Zgadzam się na cookies'
    ]
    
    # Common button IDs and class names
    common_selectors = [
        # IDs
        "#cookieConsent .accept", "#gdpr-consent-accept", "#onetrust-accept-btn-handler",
        "#consent_prompt_submit", "#accept-cookies", "#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll",
        "#cookies-accept-all", "#rodo-accept", "#privacy-policy-accept", "#cookiePolicyOK",
        "#cookies-accept", "#cookie-accept-all", "#cookie-consent-accept", "#akceptuje",
        "#akceptuj-cookies", "#cookie-agreement-accept", "#cookies-agree", "#accept-all-cookies",
        
        # Classes
        ".cookie-consent__accept", ".cookie-accept", ".consent-accept", ".cc-accept",
        ".agree-button", ".accept-cookies", ".accept_gdpr", ".privacy-policy-agree",
        ".cookie-law-button", ".cookie-accept-button", ".cookies-agreement-button",
        ".cookie-message__button", ".cookie-notice-accept", ".cookie-info__button",
        ".cookie-btn-accept", ".cookies-btn-accept", ".cookie-notice__agree",
        ".cookie-consent-button", ".cookie-consent__button", ".cookie-notice-button"
    ]

    # Common Polish cookie consent container selectors
    cookie_container_selectors = [
        '.cookie-notice', '.cookies-popup', '.cookies-alert', '.cookie-info',
        '.cookie-message', '.cookie-bar', '.cookie-compliance', '.rodo-popup',
        '#cookieInfo', '#cookieNotice', '#cookiesInfo', '#cookieBanner',
        '#cookieConsent', '#cookies-notice', '#cookies-alert', '#rodo-alert',
        '.rodo-message', '.gdpr-cookie', '.cookie-law'
    ]

    try:
        # First try - check for common Polish cookie banner patterns
        for selector in cookie_container_selectors:
            try:
                container = driver.find_element_by_css_selector(selector)
                if container and container.is_displayed():
                    # Look for buttons with 'Akceptuj' text anywhere inside container
                    buttons = container.find_elements_by_tag_name('button')
                    links = container.find_elements_by_tag_name('a')
                    divs = container.find_elements_by_tag_name('div')
                    
                    # Check all potential clickable elements
                    for el in buttons + links + divs:
                        if el.is_displayed():
                            el_text = el.text.lower()
                            if 'akceptuj' in el_text or 'zgadzam' in el_text or 'wyrażam zgodę' in el_text:
                                try:
                                    el.click()
                                    print(f"Clicked on element with text: {el.text}")
                                    return True
                                except:
                                    pass
            except:
                continue

        # Try direct XPath with more elements (button, a, div, span, input)
        for text in accept_button_texts:
            xpath = (f"//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{text.lower()}')] | "
                     f"//a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{text.lower()}')] | "
                     f"//div[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{text.lower()}')] | "
                     f"//span[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{text.lower()}')] | "
                     f"//input[@value[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{text.lower()}')]]")
            
            elements = driver.find_elements_by_xpath(xpath)
            for element in elements:
                if element.is_displayed():
                    try:
                        element.click()
                        print(f"Clicked on consent element with text: {text}")
                        return True
                    except Exception as e:
                        print(f"Could not click element with text '{text}': {e}")
        
        # Try by aria-label
        aria_labels = ["accept cookies", "akceptuj cookies", "akceptuję", "accept all cookies", 
                       "zaakceptuj wszystkie", "zgadzam się"]
        
        for label in aria_labels:
            xpath = f"//*[@aria-label='{label}']"
            try:
                elements = driver.find_elements_by_xpath(xpath)
                for element in elements:
                    if element.is_displayed():
                        element.click()
                        print(f"Clicked element with aria-label: {label}")
                        return True
            except:
                continue
                
        # Then, try common selectors
        for selector in common_selectors:
            try:
                elements = driver.find_elements_by_css_selector(selector)
                for element in elements:
                    if element.is_displayed():
                        element.click()
                        print(f"Clicked on consent element with selector: {selector}")
                        return True
            except:
                continue

        # Try iframes containing cookie consent
        iframes = driver.find_elements_by_tag_name('iframe')
        for iframe in iframes:
            try:
                iframe_src = iframe.get_attribute('src') or ''
                iframe_id = iframe.get_attribute('id') or ''
                iframe_name = iframe.get_attribute('name') or ''
                
                # Check if iframe is related to cookies or consent
                if ('cookie' in iframe_src.lower() or 'consent' in iframe_src.lower() or 
                    'cookie' in iframe_id.lower() or 'consent' in iframe_id.lower() or
                    'privacy' in iframe_id.lower() or 'rodo' in iframe_id.lower() or
                    'cookie' in iframe_name.lower() or 'consent' in iframe_name.lower()):
                    
                    driver.switch_to.frame(iframe)
                    
                    # Look for buttons inside iframe
                    for text in accept_button_texts:
                        xpath = (f"//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{text.lower()}')] | "
                                 f"//a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{text.lower()}')] | "
                                 f"//div[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{text.lower()}')] | "
                                 f"//span[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{text.lower()}')]")
                        elements = driver.find_elements_by_xpath(xpath)
                        for element in elements:
                            if element.is_displayed():
                                try:
                                    element.click()
                                    driver.switch_to.default_content()
                                    print(f"Clicked on consent element in iframe with text: {text}")
                                    return True
                                except:
                                    pass
                    
                    driver.switch_to.default_content()
            except:
                driver.switch_to.default_content()
                continue
                
    except Exception as e:
        print(f"Error while handling cookie consent popups: {e}")
    
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