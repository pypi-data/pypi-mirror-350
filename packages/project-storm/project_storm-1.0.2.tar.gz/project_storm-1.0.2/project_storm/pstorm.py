from playwright.sync_api import sync_playwright
import time
def recaptha(token: str | None = None) -> str:
    """
    Generate a reCAPTCHA token using Playwright"""
    playwright = None
    browser = None
    context = None
    page = None
    
    try:
        print("Generating reCAPTCHA token using Browserless...")
        playwright = sync_playwright().start()
        
        # Connect to Browserless.io
        browser = playwright.chromium.connect(
            f"wss://production-sfo.browserless.io/chromium/playwright?token={token}"
        )
        context = browser.new_context()
        page = context.new_page()
        
        # Set viewport size
        page.set_viewport_size({"width": 1, "height": 1})
        
        # Add debugging
        
        # Navigate to page with networkidle wait
        page.goto(
            "https://empire.goodgamestudios.com/",
            wait_until="networkidle",
            timeout=60000
        )
        
        # Wait for main iframe
        page.wait_for_selector('iframe#game', timeout=60000)
        # Get iframe handle
        iframe_element = page.query_selector('iframe#game')
        iframe = iframe_element.content_frame()
        
        # Wait for reCAPTCHA to load
        print("Waiting for reCAPTCHA to initialize...")
        start_time = time.time()
        recaptcha_loaded = False
        
        while time.time() - start_time < 60:  # 60 second timeout
            try:
                # Check if reCAPTCHA is loaded
                iframe.wait_for_function(
                    """() => typeof window.grecaptcha !== 'undefined'""",
                    timeout=5000
                )
                recaptcha_loaded = True
                break
            except:
                time.sleep(0.1)  # Use Python sleep instead of Playwright timeout
        
        if not recaptcha_loaded:
            raise TimeoutError("reCAPTCHA API failed to load within 60 seconds")
        
        # Execute reCAPTCHA
        token = iframe.evaluate("""() => {
            return new Promise((resolve, reject) => {
                window.grecaptcha.ready(() => {
                    window.grecaptcha.execute(
                        '6Lc7w34oAAAAAFKhfmln41m96VQm4MNqEdpCYm-k', 
                        { action: 'submit' }
                    )
                    .then(resolve)
                    .catch(reject);
                });
            });
        }""")
        
        if not token:
            raise ValueError("Failed to generate reCAPTCHA token")
        
        return token
        
    except Exception as e:
        return None
        
    finally:
        # Clean up resources in reverse order
        try:
            if page:
                page.close()
        except:
            pass
        
        try:
            if context:
                context.close()
        except:
            pass
            
        try:
            if browser:
                browser.close()
        except:
            pass
            
        try:
            if playwright:
                playwright.stop()
        except:
            pass
