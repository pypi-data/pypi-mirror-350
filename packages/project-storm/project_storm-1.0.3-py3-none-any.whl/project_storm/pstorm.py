from playwright.async_api import async_playwright
import asyncio
import time

async def recaptha(token: str | None = None) -> str:
    """
    Generate a reCAPTCHA token using Playwright (async version)
    """
    playwright = None
    browser = None
    context = None
    page = None
    browserless_token = "2SMMUrhKrCo5VH091b02a818a73528085bb3870390754cff8"  # Renamed for clarity
    
    try:
        print("Generating reCAPTCHA token using Browserless...")
        playwright = await async_playwright().start()
        
        # Connect to Browserless.io
        browser = await playwright.chromium.connect(
            f"wss://production-sfo.browserless.io/chromium/playwright?token={browserless_token}"
        )
        context = await browser.new_context()
        page = await context.new_page()
        
        # Set viewport size
        await page.set_viewport_size({"width": 1, "height": 1})
        
        # Navigate to page with networkidle wait
        await page.goto(
            "https://empire.goodgamestudios.com/",
            wait_until="networkidle",
            timeout=60000
        )
        
        # Wait for main iframe
        await page.wait_for_selector('iframe#game', timeout=60000)
        
        # Get iframe handle
        iframe_element = await page.query_selector('iframe#game')
        iframe = await iframe_element.content_frame()
        
        # Wait for reCAPTCHA to load
        print("Waiting for reCAPTCHA to initialize...")
        start_time = time.time()
        recaptcha_loaded = False
        
        while time.time() - start_time < 60:  # 60 second timeout
            try:
                # Check if reCAPTCHA is loaded
                await iframe.wait_for_function(
                    """() => typeof window.grecaptcha !== 'undefined'""",
                    timeout=5000
                )
                recaptcha_loaded = True
                break
            except:
                await asyncio.sleep(0.1)  # Use async sleep
        
        if not recaptcha_loaded:
            raise TimeoutError("reCAPTCHA API failed to load within 60 seconds")
        
        # Execute reCAPTCHA
        token = await iframe.evaluate("""() => {
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
        print(f"Error generating reCAPTCHA token: {str(e)}")
        return None
        
    finally:
        # Clean up resources in reverse order
        try:
            if page:
                await page.close()
        except:
            pass
        
        try:
            if context:
                await context.close()
        except:
            pass
            
        try:
            if browser:
                await browser.close()
        except:
            pass
            
        try:
            if playwright:
                await playwright.stop()
        except:
            pass