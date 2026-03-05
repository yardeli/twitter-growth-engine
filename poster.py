"""
Twitter Auto-Poster
Posts generated ideas to Twitter via browser automation
"""

import sqlite3
import time
from datetime import datetime
from config import DB_PATH, YOUR_ACCOUNT

class TwitterPoster:
    def __init__(self, browser_tool=None):
        """
        Initialize poster
        browser_tool: Reference to the OpenClaw browser tool for automation
        """
        self.db_path = DB_PATH
        self.browser = browser_tool
        self.account = YOUR_ACCOUNT
        self.posted_today = 0
    
    def post_idea(self, idea_id, idea_content):
        """Post an idea to Twitter"""
        if not self.browser:
            return {"status": "error", "message": "Browser tool not configured."}
        
        try:
            page = self.browser.get_page()
            
            print(f"🚀 Navigating to compose...")
            page.goto("https://x.com/compose/post")
            
            # 1. Wait for the textbox to actually exist
            page.wait_for_selector('div[role="textbox"]', timeout=15000)
            time.sleep(3) # Extra buffer for React to load
            
            # 2. FORCE FOCUS: Two clicks to ensure focus is captured
            print("🎯 Targeting textbox...")
            page.click('div[role="textbox"]')
            time.sleep(1)
            page.focus('div[role="textbox"]')
            
            # 3. TYPE: Human-like speed
            print("⌨️ Typing content...")
            page.keyboard.type(idea_content, delay=70)
            time.sleep(2)
            
            # 4. CLICK POST
            print("🖱️ Clicking Post...")
            post_btn = page.locator('[data-testid="tweetButton"], [data-testid="tweetButtonInline"]').first
            
            if post_btn.is_visible():
                post_btn.click()
            else:
                print("⚠️ Button not visible, using Ctrl+Enter...")
                page.keyboard.press("Control+Enter")
            
            time.sleep(5)
            self._mark_posted(idea_id)
            
            return {"status": "success", "message": "Post complete!"}
            
        except Exception as e:
            print(f"❌ Error in poster.py: {e}")
            return {"status": "error", "message": str(e)}

    def _mark_posted(self, idea_id):
        """Mark idea as posted in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE post_ideas 
            SET posted = 1 
            WHERE id = ?
        ''', (idea_id,))
        conn.commit()
        conn.close()

    def schedule_post(self, idea_id, scheduled_time):
        """Schedule post for later"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scheduled_posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                idea_id INTEGER NOT NULL,
                scheduled_time TIMESTAMP NOT NULL,
                posted INTEGER DEFAULT 0,
                FOREIGN KEY(idea_id) REFERENCES post_ideas(id)
            )
        ''')
        cursor.execute('''
            INSERT INTO scheduled_posts (idea_id, scheduled_time)
            VALUES (?, ?)
        ''', (idea_id, scheduled_time))
        conn.commit()
        conn.close()
        return f"Post scheduled for {scheduled_time}"

    def auto_reply_to_comments(self, tweet_url, reply_template):
        """Auto-reply to early comments"""
        if not self.browser:
            return {"status": "error", "message": "Browser not configured"}
        try:
            page = self.browser.get_page()
            page.goto(tweet_url)
            time.sleep(2)
            return {"status": "success", "message": "Replies logic placeholder"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_posting_history(self):
        """Get history of posted ideas"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, title, content, score, posted
            FROM post_ideas
            WHERE posted = 1
            ORDER BY id DESC
            LIMIT 20
        ''')
        results = cursor.fetchall()
        conn.close()
        return [
            {"id": r[0], "title": r[1], "content": r[2], "score": r[3]}
            for r in results
        ]