"""
Twitter Poster using Playwright (Headless Mode)
Posts to Twitter without visible browser window
"""

import asyncio
import sqlite3
from datetime import datetime
from playwright.async_api import async_playwright
from config import DB_PATH

class PlaywrightTwitterPoster:
    def __init__(self, headless=True):
        """
        Initialize Playwright poster
        headless=True: Browser runs invisibly in background
        headless=False: Shows browser window (for debugging)
        """
        self.db_path = DB_PATH
        self.headless = headless
        self.browser = None
        self.context = None
        self.page = None
    
    async def init(self):
        """Initialize browser connection"""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=self.headless)
        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()
        print("✅ Playwright browser initialized (headless mode)" if self.headless else "✅ Playwright browser opened")
    
    async def close(self):
        """Close browser connection"""
        if self.page:
            await self.page.close()
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        print("✅ Browser closed")
    
    async def post_tweet(self, content, idea_id=None):
        """Post a tweet without showing the browser"""
        try:
            # Navigate to Twitter
            await self.page.goto("https://x.com/compose/post")
            await self.page.wait_for_load_state("networkidle")
            
            # Find and fill the tweet text area
            # Twitter's text input usually has contenteditable div
            await self.page.click('[data-testid="tweetTextarea_0"]')
            await self.page.type('[data-testid="tweetTextarea_0"]', content)
            
            # Click post button
            await self.page.click('[data-testid="tweetButton"]')
            
            # Wait for post to complete
            await self.page.wait_for_timeout(3000)
            
            # Check if posted successfully
            await self.page.wait_for_url("https://x.com/**", timeout=10000)
            
            # Mark as posted in database
            self._mark_posted(idea_id)
            
            print(f"✅ Tweet posted: {content[:50]}...")
            return {"status": "success", "content": content}
            
        except Exception as e:
            print(f"❌ Failed to post: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    async def post_multiple(self, tweets, delay_seconds=300):
        """
        Post multiple tweets with delay between them
        delay_seconds: Time to wait between posts (default 5 min)
        """
        for i, (content, idea_id) in enumerate(tweets):
            print(f"\n📝 Posting {i+1}/{len(tweets)}: {content[:50]}...")
            
            result = await self.post_tweet(content, idea_id)
            
            if result["status"] == "success" and i < len(tweets) - 1:
                print(f"⏳ Waiting {delay_seconds}s before next post...")
                await self.page.wait_for_timeout(delay_seconds * 1000)
        
        print(f"\n✅ All {len(tweets)} tweets posted!")
    
    async def schedule_posts(self, tweets, times):
        """
        Schedule posts for specific times
        tweets: List of (content, idea_id) tuples
        times: List of "HH:MM" times in PT
        
        Example:
            await poster.schedule_posts(
                [("Tweet 1", 1), ("Tweet 2", 2)],
                ["9:00", "12:00", "17:00"]
            )
        """
        import time as time_module
        from datetime import datetime, timedelta
        
        for content, idea_id in tweets:
            target_time = times[tweets.index((content, idea_id))]
            
            # Wait until target time
            while True:
                now = datetime.now().strftime("%H:%M")
                if now >= target_time:
                    break
                await self.page.wait_for_timeout(60000)  # Check every minute
            
            print(f"🕐 Time {target_time} reached. Posting: {content[:50]}...")
            await self.post_tweet(content, idea_id)
    
    async def auto_engage(self, tweet_url, reply_template, max_replies=5):
        """
        Auto-reply to comments for engagement boost
        Best done within first hour of posting
        """
        try:
            await self.page.goto(tweet_url)
            await self.page.wait_for_load_state("networkidle")
            
            # Scroll to see replies
            await self.page.evaluate("window.scrollBy(0, 500)")
            
            # Find reply buttons (simplified - actual implementation would need refinement)
            reply_count = 0
            print(f"💬 Auto-engaging with replies (max {max_replies})...")
            
            # Find reply links/buttons
            reply_buttons = await self.page.query_selector_all('[data-testid="reply"]')
            
            for button in reply_buttons[:max_replies]:
                try:
                    await button.click()
                    await self.page.wait_for_timeout(500)
                    
                    # Type reply
                    await self.page.click('[data-testid="tweetTextarea_0"]')
                    await self.page.type('[data-testid="tweetTextarea_0"]', reply_template)
                    
                    # Post reply
                    await self.page.click('[data-testid="tweetButton"]')
                    await self.page.wait_for_timeout(1000)
                    
                    reply_count += 1
                    print(f"  ✅ Posted reply {reply_count}/{max_replies}")
                    
                except Exception as e:
                    print(f"  ⚠️  Couldn't reply to this comment: {e}")
                    continue
            
            print(f"✅ Engagement complete: {reply_count} replies posted")
            return reply_count
            
        except Exception as e:
            print(f"❌ Auto-engage failed: {str(e)}")
            return 0
    
    def _mark_posted(self, idea_id):
        """Mark idea as posted in database"""
        if not idea_id:
            return
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE post_ideas 
            SET posted = 1 
            WHERE id = ?
        ''', (idea_id,))
        
        conn.commit()
        conn.close()

# CLI Usage Examples
async def main():
    """Example usage"""
    
    # Example 1: Post a single tweet (headless - invisible)
    poster = PlaywrightTwitterPoster(headless=True)
    await poster.init()
    
    result = await poster.post_tweet(
        "This tweet was posted by Playwright in headless mode 🤖",
        idea_id=1
    )
    
    await poster.close()

if __name__ == "__main__":
    # Install playwright first:
    # pip install playwright
    # playwright install chromium
    
    print("📖 PLAYWRIGHT TWITTER POSTER")
    print("=" * 50)
    print("\nUsage Examples:")
    print("\n1. Single tweet:")
    print("""
    async def post_one():
        poster = PlaywrightTwitterPoster(headless=True)
        await poster.init()
        await poster.post_tweet("Your tweet content", idea_id=1)
        await poster.close()
    
    asyncio.run(post_one())
    """)
    
    print("\n2. Multiple tweets with delay:")
    print("""
    async def post_many():
        poster = PlaywrightTwitterPoster(headless=True)
        await poster.init()
        
        tweets = [
            ("Tweet 1", 1),
            ("Tweet 2", 2),
            ("Tweet 3", 3),
        ]
        
        await poster.post_multiple(tweets, delay_seconds=300)  # 5 min between posts
        await poster.close()
    
    asyncio.run(post_many())
    """)
    
    print("\n3. Scheduled posts:")
    print("""
    async def post_scheduled():
        poster = PlaywrightTwitterPoster(headless=True)
        await poster.init()
        
        tweets = [
            ("Morning post", 1),
            ("Noon post", 2),
            ("Evening post", 3),
        ]
        
        times = ["09:00", "12:00", "17:00"]  # PT times
        await poster.schedule_posts(tweets, times)
        await poster.close()
    
    asyncio.run(post_scheduled())
    """)
    
    print("\n4. Auto-engage with replies:")
    print("""
    async def auto_engage():
        poster = PlaywrightTwitterPoster(headless=True)
        await poster.init()
        
        tweet_url = "https://x.com/@eliasyarden/status/123456"
        reply_template = "Thanks for the comment! Check out this..."
        
        count = await poster.auto_engage(tweet_url, reply_template, max_replies=5)
        await poster.close()
    
    asyncio.run(auto_engage())
    """)
    
    print("\n🎯 Key Benefits:")
    print("  ✅ headless=True: Browser invisible, no window shown")
    print("  ✅ Runs in background while you work")
    print("  ✅ Doesn't steal focus from your work")
    print("  ✅ Can be scheduled via cron/scheduler")
    print("  ✅ Fast and efficient")
