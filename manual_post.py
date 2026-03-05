import os
import time
from playwright.sync_api import sync_playwright
from poster import TwitterPoster

def run_manual():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    automation_user_data = os.path.join(script_dir, "automation_chrome_profile")

    with sync_playwright() as p:
        print(f"🚀 Launching Isolated Chrome...")
        
        context = p.chromium.launch_persistent_context(
            automation_user_data,
            channel="chrome",
            headless=False,
            no_viewport=True,
            args=["--disable-blink-features=AutomationControlled"]
        )
        
        page = context.pages[0] if context.pages else context.new_page()
        
        print("🌐 Checking Twitter State...")
        page.goto("https://x.com/home")
        
        # 1. Wait for the feed to load (This confirms we are logged in)
        try:
            page.wait_for_selector('a[data-testid="SideNav_NewTweet_Button"]', timeout=10000)
            print("✅ Already logged in!")
        except:
            print("🛑 Please log in manually now...")
            page.wait_for_selector('a[data-testid="SideNav_NewTweet_Button"]', timeout=0)

        # 2. Setup the Engine
        class MockBrowser:
            def __init__(self, page): self.page = page
            def get_page(self): return self.page

        browser_tool = MockBrowser(page)
        poster = TwitterPoster(browser_tool)
        
        # 3. THE FIX: Attempt the post and WAIT
        print("✍️ Executing post_idea...")
        try:
            # We give it a unique message so you can see it on your profile
            timestamp = time.strftime("%H:%M:%S")
            message = f"Manual engine test successful at {timestamp}! 🦞"
            
            poster.post_idea(1, message)
            
            print("⏳ Post command sent. Keeping window open for 60 seconds to verify...")
            # This prevents the "Window shut down" issue
            for i in range(60, 0, -1):
                print(f"Closing in {i} seconds... (Check the browser window!)", end="\r")
                time.sleep(1)
                
        except Exception as e:
            print(f"\n❌ Engine Error: {e}")
            time.sleep(30) # Stay open so you can read the error
        
        context.close()

if __name__ == "__main__":
    run_manual()